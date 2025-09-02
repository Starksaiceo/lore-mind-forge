import os
import stripe
from flask import Blueprint, request, jsonify, session, redirect, url_for, flash, render_template
from flask_login import login_required, current_user
from functools import wraps
import os
from models import db, User, Subscription
from datetime import datetime, timedelta
from replit_db import replit_db_manager
import json
import logging

logger = logging.getLogger(__name__)

billing_bp = Blueprint("billing", __name__)

# Configure Stripe
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")

# Plan configuration
PLANS = {
    "starter": {
        "price_id": os.getenv("STRIPE_PRICE_STARTER", "price_starter_placeholder"),
        "usd": 29,
        "name": "Starter",
        "features": ["Basic AI automation", "5 products/month", "Basic support"]
    },
    "pro": {
        "price_id": os.getenv("STRIPE_PRICE_PRO", "price_pro_placeholder"),
        "usd": 99,
        "name": "Pro",
        "features": ["Advanced AI automation", "Unlimited products", "Priority support", "Team collaboration"]
    },
    "enterprise": {
        "price_id": os.getenv("STRIPE_PRICE_ENTERPRISE", "price_enterprise_placeholder"),
        "usd": 299,
        "name": "Enterprise",
        "features": ["Custom AI models", "White-label solution", "Dedicated support", "API access"]
    }
}

def require_active_subscription(f):
    """Decorator to require active subscription - temporarily allow free usage"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            if request.is_json:
                return jsonify({'error': 'Authentication required'}), 401
            return redirect(url_for('login'))

        # Temporarily allow free usage for testing - comment out subscription check
        # if not is_subscription_active(current_user.id):
        #     if request.is_json:
        #         return jsonify({'error': 'Active subscription required'}), 403
        #     flash('This feature requires an active subscription')
        #     return redirect(url_for('pricing'))

        return f(*args, **kwargs)
    return decorated_function

@billing_bp.route("/plans", methods=["GET"])
def get_plans():
    """Get available subscription plans"""
    return jsonify({"plans": PLANS})

@billing_bp.route("/create-checkout-session", methods=["POST"])
def create_checkout_session():
    """Create Stripe checkout session"""
    try:
        data = request.get_json()
        user_id = data.get("user_id")
        plan = data.get("plan")
        success_url = data.get("success_url", "http://localhost:5000/success")
        cancel_url = data.get("cancel_url", "http://localhost:5000/pricing")

        if plan not in PLANS:
            return jsonify({"error": "invalid_plan"}), 400

        price_id = PLANS[plan]["price_id"]

        # Get or create customer
        existing = Subscription.query.filter_by(user_id=user_id).first()
        customer_id = existing.stripe_customer_id if existing and existing.stripe_customer_id else None

        # Create checkout session
        session_params = {
            "mode": "subscription",
            "line_items": [{"price": price_id, "quantity": 1}],
            "success_url": success_url + "?session_id={CHECKOUT_SESSION_ID}",
            "cancel_url": cancel_url,
            "automatic_tax": {"enabled": True},
            "allow_promotion_codes": True,
            "metadata": {"user_id": str(user_id)}
        }

        if customer_id:
            session_params["customer"] = customer_id

        session = stripe.checkout.Session.create(**session_params)

        # Update or create subscription record
        if not existing:
            existing = Subscription(user_id=user_id, plan_id=plan, status="pending")
            db.session.add(existing)
        else:
            existing.plan_id = plan
            existing.status = "pending"

        db.session.commit()

        return jsonify({"checkout_url": session.url, "session_id": session.id})

    except Exception as e:
        logging.error(f"Checkout creation failed: {e}")
        return jsonify({"error": "checkout_failed"}), 500

@billing_bp.route("/stripe/webhook", methods=["POST"])
def stripe_webhook():
    """Handle Stripe webhooks"""
    try:
        payload = request.data
        sig = request.headers.get("Stripe-Signature")

        if not WEBHOOK_SECRET:
            logging.warning("No webhook secret configured")
            return "", 200

        event = stripe.Webhook.construct_event(payload, sig, WEBHOOK_SECRET)
        event_type = event["type"]
        obj = event["data"]["object"]

        logging.info(f"Processing Stripe webhook: {event_type}")

        if event_type == "checkout.session.completed":
            handle_checkout_completed(obj)
        elif event_type in ("customer.subscription.created", "customer.subscription.updated"):
            handle_subscription_updated(obj)
        elif event_type == "customer.subscription.deleted":
            handle_subscription_deleted(obj)
        elif event_type == "invoice.payment_failed":
            handle_payment_failed(obj)

        return "", 200

    except Exception as e:
        logging.error(f"Webhook processing failed: {e}")
        return "", 400

def handle_checkout_completed(session):
    """Handle successful checkout"""
    user_id = session.get("metadata", {}).get("user_id")
    subscription_id = session.get("subscription")
    customer_id = session.get("customer")

    if user_id and subscription_id:
        sub = Subscription.query.filter_by(user_id=int(user_id)).first()
        if sub:
            sub.stripe_subscription_id = subscription_id
            sub.stripe_customer_id = customer_id
            sub.status = "active"
            db.session.commit()
            logging.info(f"Subscription activated for user {user_id}")

def handle_subscription_updated(subscription):
    """Handle subscription updates"""
    sub = Subscription.query.filter_by(stripe_subscription_id=subscription["id"]).first()
    if sub:
        sub.status = subscription["status"]
        sub.current_period_end = subscription["current_period_end"]
        db.session.commit()
        logging.info(f"Subscription updated: {subscription['id']} -> {subscription['status']}")

def handle_subscription_deleted(subscription):
    """Handle subscription cancellation"""
    sub = Subscription.query.filter_by(stripe_subscription_id=subscription["id"]).first()
    if sub:
        sub.status = "canceled"
        db.session.commit()
        logging.info(f"Subscription canceled: {subscription['id']}")

def handle_payment_failed(invoice):
    """Handle failed payments"""
    subscription_id = invoice.get("subscription")
    if subscription_id:
        sub = Subscription.query.filter_by(stripe_subscription_id=subscription_id).first()
        if sub:
            sub.status = "past_due"
            db.session.commit()
            logging.warning(f"Payment failed for subscription: {subscription_id}")

@billing_bp.route("/subscription-status/<int:user_id>", methods=["GET"])
def get_subscription_status(user_id):
    """Get user's subscription status"""
    sub = Subscription.query.filter_by(user_id=user_id).first()
    if not sub:
        return jsonify({"status": "none", "plan": None})

    return jsonify({
        "status": sub.status,
        "plan": sub.plan_id,
        "current_period_end": sub.current_period_end,
        "features": PLANS.get(sub.plan_id, {}).get("features", [])
    })

@billing_bp.route("/mrr-report", methods=["GET"])
def mrr_report():
    """Get Monthly Recurring Revenue report"""
    try:
        active_subs = Subscription.query.filter(
            Subscription.status.in_(["active", "trialing"])
        ).all()

        mrr = 0
        plan_breakdown = {}

        for sub in active_subs:
            plan_price = PLANS.get(sub.plan_id, {}).get("usd", 0)
            mrr += plan_price
            plan_breakdown[sub.plan_id] = plan_breakdown.get(sub.plan_id, 0) + 1

        return jsonify({
            "mrr": mrr,
            "active_count": len(active_subs),
            "plan_breakdown": plan_breakdown,
            "arr": mrr * 12
        })

    except Exception as e:
        logging.error(f"MRR report failed: {e}")
        return jsonify({"error": "report_failed"}), 500

@billing_bp.route("/cancel-subscription", methods=["POST"])
def cancel_subscription():
    """Cancel user subscription"""
    try:
        data = request.get_json()
        user_id = data.get("user_id")

        sub = Subscription.query.filter_by(user_id=user_id).first()
        if not sub or not sub.stripe_subscription_id:
            return jsonify({"error": "subscription_not_found"}), 404

        # Cancel at period end
        stripe.Subscription.modify(
            sub.stripe_subscription_id,
            cancel_at_period_end=True
        )

        return jsonify({"status": "cancellation_scheduled"})

    except Exception as e:
        logging.error(f"Cancellation failed: {e}")
        return jsonify({"error": "cancellation_failed"}), 500

def get_user_subscription(user_id):
    """Helper to get user's current subscription"""
    return Subscription.query.filter_by(user_id=user_id).first()

def is_subscription_active(user_id):
    """Helper to check if user has active subscription"""
    sub = get_user_subscription(user_id)
    return sub and sub.status in ("active", "trialing")

# Export for use in other modules
__all__ = ['billing_bp', 'require_active_subscription', 'is_subscription_active', 'get_user_subscription', 'PLANS']