import os
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from models import db, AIEvent, ShopifyOrder, Subscription, User
import requests
from config import SHOPIFY_DOMAIN, SHOPIFY_ACCESS_TOKEN, STRIPE_SECRET_KEY
import stripe

# Configure Stripe
stripe.api_key = STRIPE_SECRET_KEY

# Shopify configuration
SHOPIFY_STORE_URL = f"https://{SHOPIFY_DOMAIN}"

def get_products_created(user_id: int, days: int = 30) -> Dict[str, Any]:
    """Get products created by user in the last N days"""
    try:
        cutoff_date = datetime.utcnow() - timedelta(days=days)

        # Get product creation events
        product_events = AIEvent.query.filter(
            AIEvent.user_id == user_id,
            AIEvent.event_type.in_(['product_created', 'product_generated', 'shopify_upload']),
            AIEvent.created_at >= cutoff_date,
            AIEvent.success == True
        ).all()

        products = []
        total_value = 0

        for event in product_events:
            try:
                event_data = json.loads(event.event_json) if event.event_json else {}
                product_name = event_data.get('product_name', event_data.get('title', 'Unnamed Product'))
                price = float(event_data.get('price', 0))

                products.append({
                    "name": product_name,
                    "price": price,
                    "created_at": event.created_at.isoformat(),
                    "type": event_data.get('type', 'digital'),
                    "status": "active"
                })

                total_value += price

            except (json.JSONDecodeError, ValueError):
                continue

        return {
            "total_products": len(products),
            "products": products,
            "total_value": round(total_value, 2),
            "average_price": round(total_value / len(products), 2) if products else 0,
            "period_days": days
        }

    except Exception as e:
        print(f"❌ Get products created failed: {e}")
        return {"total_products": 0, "products": [], "total_value": 0, "average_price": 0}

def get_store_revenue(user_id: int, days: int = 30) -> Dict[str, Any]:
    """Get store revenue from Shopify orders and Stripe payments"""
    try:
        cutoff_date = datetime.utcnow() - timedelta(days=days)

        # Get Shopify orders
        shopify_revenue = 0
        shopify_orders = ShopifyOrder.query.filter(
            ShopifyOrder.user_id == user_id,
            ShopifyOrder.created_at >= cutoff_date
        ).all()

        for order in shopify_orders:
            shopify_revenue += order.total_price

        # Get Stripe payments (fallback/additional)
        stripe_revenue = 0
        try:
            # Get customer for this user
            subscription = Subscription.query.filter_by(user_id=user_id).first()
            if subscription and subscription.stripe_customer_id:
                # Get payment intents for this customer
                payments = stripe.PaymentIntent.list(
                    customer=subscription.stripe_customer_id,
                    created={"gte": int(cutoff_date.timestamp())},
                    limit=100
                )

                for payment in payments.data:
                    if payment.status == "succeeded":
                        stripe_revenue += payment.amount / 100  # Convert from cents

        except Exception as stripe_error:
            print(f"⚠️ Stripe revenue fetch failed: {stripe_error}")

        total_revenue = shopify_revenue + stripe_revenue

        return {
            "total_revenue": round(total_revenue, 2),
            "shopify_revenue": round(shopify_revenue, 2),
            "stripe_revenue": round(stripe_revenue, 2),
            "orders_count": len(shopify_orders),
            "average_order_value": round(total_revenue / len(shopify_orders), 2) if shopify_orders else 0,
            "period_days": days,
            "currency": "USD"
        }

    except Exception as e:
        print(f"❌ Get store revenue failed: {e}")
        return {"total_revenue": 0, "shopify_revenue": 0, "stripe_revenue": 0, "orders_count": 0}

def get_orders_fulfilled(user_id: int, days: int = 30) -> Dict[str, Any]:
    """Get fulfilled orders statistics"""
    try:
        cutoff_date = datetime.utcnow() - timedelta(days=days)

        orders = ShopifyOrder.query.filter(
            ShopifyOrder.user_id == user_id,
            ShopifyOrder.created_at >= cutoff_date
        ).all()

        fulfilled_orders = [order for order in orders if order.status in ["fulfilled", "completed"]]
        pending_orders = [order for order in orders if order.status in ["pending", "processing"]]

        return {
            "total_orders": len(orders),
            "fulfilled_orders": len(fulfilled_orders),
            "pending_orders": len(pending_orders),
            "fulfillment_rate": round(len(fulfilled_orders) / len(orders) * 100, 1) if orders else 0,
            "orders": [
                {
                    "id": order.shopify_order_id,
                    "total": order.total_price,
                    "status": order.status,
                    "created_at": order.created_at.isoformat()
                }
                for order in orders[:10]  # Latest 10 orders
            ],
            "period_days": days
        }

    except Exception as e:
        print(f"❌ Get orders fulfilled failed: {e}")
        return {"total_orders": 0, "fulfilled_orders": 0, "pending_orders": 0, "fulfillment_rate": 0}

def get_ai_activity_summary(user_id: int, days: int = 7) -> Dict[str, Any]:
    """Get AI activity summary for dashboard"""
    try:
        cutoff_date = datetime.utcnow() - timedelta(days=days)

        events = AIEvent.query.filter(
            AIEvent.user_id == user_id,
            AIEvent.created_at >= cutoff_date
        ).all()

        success_events = [e for e in events if e.success]
        failed_events = [e for e in events if not e.success]

        event_types = {}
        for event in events:
            event_types[event.event_type] = event_types.get(event.event_type, 0) + 1

        return {
            "total_events": len(events),
            "successful_events": len(success_events),
            "failed_events": len(failed_events),
            "success_rate": round(len(success_events) / len(events) * 100, 1) if events else 0,
            "event_types": event_types,
            "most_active_day": get_most_active_day(events),
            "period_days": days
        }

    except Exception as e:
        print(f"❌ Get AI activity failed: {e}")
        return {"total_events": 0, "successful_events": 0, "failed_events": 0, "success_rate": 0}

def get_most_active_day(events: List) -> str:
    """Find the most active day from events"""
    try:
        day_counts = {}
        for event in events:
            day = event.created_at.strftime("%A")
            day_counts[day] = day_counts.get(day, 0) + 1

        if day_counts:
            return max(day_counts.items(), key=lambda x: x[1])[0]
        return "No data"

    except Exception:
        return "Unknown"

def get_marketing_performance(user_id: int, days: int = 30) -> Dict[str, Any]:
    """Get marketing campaign performance"""
    try:
        cutoff_date = datetime.utcnow() - timedelta(days=days)

        marketing_events = AIEvent.query.filter(
            AIEvent.user_id == user_id,
            AIEvent.event_type.in_(['email_generated', 'ad_created', 'social_post_scheduled']),
            AIEvent.created_at >= cutoff_date
        ).all()

        emails_generated = len([e for e in marketing_events if e.event_type == 'email_generated'])
        ads_created = len([e for e in marketing_events if e.event_type == 'ad_created'])
        posts_scheduled = len([e for e in marketing_events if e.event_type == 'social_post_scheduled'])

        return {
            "emails_generated": emails_generated,
            "ads_created": ads_created,
            "posts_scheduled": posts_scheduled,
            "total_campaigns": emails_generated + ads_created + posts_scheduled,
            "period_days": days
        }

    except Exception as e:
        print(f"❌ Get marketing performance failed: {e}")
        return {"emails_generated": 0, "ads_created": 0, "posts_scheduled": 0, "total_campaigns": 0}

def get_success_metrics(user_id: int, days: int = 30) -> Dict[str, Any]:
    """Get success metrics for user - simplified dashboard data"""
    try:
        products_data = get_products_created(user_id, days)
        revenue_data = get_store_revenue(user_id, days)
        orders_data = get_orders_fulfilled(user_id, days)

        return {
            "total_revenue": revenue_data.get("total_revenue", 0),
            "products_created": products_data.get("total_products", 0),
            "orders_fulfilled": orders_data.get("fulfilled_orders", 0),
            "average_order_value": revenue_data.get("average_order_value", 0),
            "success_rate": orders_data.get("fulfillment_rate", 0),
            "period_days": days
        }

    except Exception as e:
        print(f"❌ Get success metrics failed: {e}")
        return {
            "total_revenue": 0,
            "products_created": 0,
            "orders_fulfilled": 0,
            "average_order_value": 0,
            "success_rate": 0,
            "period_days": days
        }

def get_success_metrics_safe(user_id: int):
    """Get success metrics without Flask context requirement"""
    try:
        # Use direct SQLite connection for Streamlit compatibility
        import sqlite3
        import os

        db_path = 'ai_ceo_saas.db'
        if not os.path.exists(db_path):
            print(f"Database not found at {db_path}, returning default metrics")
            return get_default_metrics()

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Get basic metrics safely
        try:
            cursor.execute("SELECT COUNT(*) FROM agent_memory WHERE user_id = ? AND key LIKE '%product%'", (user_id,))
            result = cursor.fetchone()
            products_created = result[0] if result else 0
        except:
            products_created = 0

        # Mock revenue for now - replace with actual revenue table query
        total_revenue = 0.0
        orders_fulfilled = 0

        conn.close()

        return {
            'total_revenue': total_revenue,
            'products_created': products_created,
            'orders_fulfilled': orders_fulfilled,
            'conversion_rate': 0.0,
            'avg_order_value': 0.0
        }
    except Exception as e:
        print(f"Warning: Could not load success metrics: {e}")
        return get_default_metrics()

def get_default_metrics():
    """Return default metrics when database is unavailable"""
    return {
        'total_revenue': 0.0,
        'products_created': 0,
        'orders_fulfilled': 0,
        'conversion_rate': 0.0,
        'avg_order_value': 0.0
    }

def get_comprehensive_dashboard(user_id: int):
    """Get comprehensive dashboard data"""
    try:
        return {
            "user_id": user_id,
            "generated_at": datetime.utcnow().isoformat(),
            "products": get_products_created(user_id, 30),
            "revenue": get_store_revenue(user_id, 30),
            "orders": get_orders_fulfilled(user_id, 30),
            "ai_activity": get_ai_activity_summary(user_id, 7),
            "marketing": get_marketing_performance(user_id, 30),
            "quick_stats": {
                "total_products_created": get_products_created(user_id, 30)["total_products"],
                "monthly_revenue": get_store_revenue(user_id, 30)["total_revenue"],
                "success_rate": get_ai_activity_summary(user_id, 7)["success_rate"],
                "campaigns_active": get_marketing_performance(user_id, 30)["total_campaigns"]
            }
        }

    except Exception as e:
        print(f"❌ Get comprehensive dashboard failed: {e}")
        return {"error": str(e), "user_id": user_id}

def get_comprehensive_dashboard_safe(user_id: int):
    """Safe version that works without Flask context"""
    import pandas as pd
    from datetime import datetime, timedelta

    # Generate sample data
    dates = pd.date_range(start=datetime.now() - timedelta(days=7), periods=7, freq='D')
    data = {
        'Date': dates.strftime('%Y-%m-%d'),
        'Revenue': [25.99, 45.00, 0, 89.99, 15.50, 0, 67.00],
        'Products': [1, 2, 0, 3, 1, 0, 2],
        'Status': ['Active', 'Active', 'Maintenance', 'Active', 'Active', 'Maintenance', 'Active']
    }
    return pd.DataFrame(data)

def save_dashboard_report(user_id: int, report_data: Dict[str, Any]) -> str:
    """Save dashboard report to file"""
    try:
        os.makedirs("reports", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        filename = f"reports/dashboard_report_{user_id}_{timestamp}.json"

        with open(filename, 'w') as f:
            json.dump(report_data, f, indent=2, default=str)

        print(f"📊 Dashboard report saved: {filename}")
        return filename

    except Exception as e:
        print(f"❌ Save dashboard report failed: {e}")
        return ""

# Flask route functions (to be registered in main app)
def create_success_dashboard_routes():
    """Create Flask routes for success dashboard"""
    from flask import Blueprint, jsonify, request

    dashboard_bp = Blueprint("dashboard", __name__)

    @dashboard_bp.route("/reports/success/<int:user_id>", methods=["GET"])
    def get_success_report(user_id):
        """Get success dashboard report"""
        days = request.args.get('days', 30, type=int)

        report = {
            "products": get_products_created(user_id, days),
            "revenue": get_store_revenue(user_id, days),
            "orders": get_orders_fulfilled(user_id, days)
        }

        return jsonify(report)

    @dashboard_bp.route("/reports/comprehensive/<int:user_id>", methods=["GET"])
    def get_comprehensive_report(user_id):
        """Get comprehensive dashboard report"""
        report = get_comprehensive_dashboard(user_id)
        return jsonify(report)

    return dashboard_bp

# Export functions
__all__ = [
    'get_products_created', 'get_store_revenue', 'get_orders_fulfilled',
    'get_ai_activity_summary', 'get_marketing_performance', 'get_success_metrics',
    'get_comprehensive_dashboard', 'save_dashboard_report', 'create_success_dashboard_routes',
    'get_success_metrics_safe', 'get_comprehensive_dashboard_safe'
]