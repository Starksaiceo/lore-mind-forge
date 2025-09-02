"""
Stripe Connect Express implementation for AI CEO platform
Handles individual user money accounts with automatic platform fees
"""

import os
import stripe
from flask import Blueprint, request, jsonify, redirect, url_for, session, current_app
from flask_login import login_required, current_user
from models import db, User, Tenant, AuditLog
from sqlalchemy import select
import json
import logging

logger = logging.getLogger(__name__)

# Initialize Stripe
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
stripe_connect_bp = Blueprint('stripe_connect', __name__)

class StripeConnectManager:
    """Manages Stripe Connect Express accounts for users"""
    
    def __init__(self):
        self.platform_fee_percent = float(os.getenv('PLATFORM_FEE_PERCENT', '10'))  # Default 10%
        self.stripe_webhook_secret = os.getenv('STRIPE_CONNECT_WEBHOOK_SECRET')
    
    def create_express_account(self, user_id, email, business_info=None):
        """Create a Stripe Connect Express account for a user"""
        try:
            # Get or create tenant record
            user = db.session.get(User, user_id)
            tenant = db.session.execute(select(Tenant).where(Tenant.owner_user_id == user_id)).scalar_one_or_none()
            
            if not tenant:
                tenant = Tenant(
                    owner_user_id=user_id,
                    stripe_customer_id=user.stripe_customer_id,
                    plan='starter',
                    status='active'
                )
                db.session.add(tenant)
                db.session.flush()  # Get tenant ID
            
            # Create Express account
            account_data = {
                'type': 'express',
                'country': 'US',  # Can be made configurable
                'email': email,
                'capabilities': {
                    'card_payments': {'requested': True},
                    'transfers': {'requested': True},
                },
                'business_type': 'individual',  # Default to individual
                'settings': {
                    'payouts': {
                        'schedule': {
                            'interval': 'daily'  # Fast payouts for users
                        }
                    }
                }
            }
            
            # Add business information if provided
            if business_info:
                if business_info.get('business_name'):
                    account_data['business_type'] = 'company'
                    account_data['company'] = {'name': business_info['business_name']}
                
                if business_info.get('first_name') and business_info.get('last_name'):
                    account_data['individual'] = {
                        'first_name': business_info['first_name'],
                        'last_name': business_info['last_name']
                    }
            
            # Create the account
            account = stripe.Account.create(**account_data)
            
            # Update tenant with Connect account ID
            tenant.stripe_connect_account_id = account.id
            db.session.commit()
            
            # Log the action
            self._log_audit(tenant.id, 'system', 'create_connect_account', {
                'account_id': account.id,
                'email': email
            })
            
            logger.info(f"✅ Created Stripe Connect account {account.id} for user {user_id}")
            return account
            
        except Exception as e:
            logger.error(f"❌ Failed to create Connect account for user {user_id}: {e}")
            db.session.rollback()
            raise
    
    def create_onboarding_link(self, user_id, return_url, refresh_url):
        """Create an onboarding link for Express account setup"""
        try:
            tenant = Tenant.query.filter_by(owner_user_id=user_id).first()
            if not tenant or not tenant.stripe_connect_account_id:
                raise ValueError("No Connect account found for user")
            
            # Create account link for onboarding
            account_link = stripe.AccountLink.create(
                account=tenant.stripe_connect_account_id,
                refresh_url=refresh_url,
                return_url=return_url,
                type='account_onboarding',
                collect='eventually_due'
            )
            
            self._log_audit(tenant.id, 'user', 'start_onboarding', {
                'account_id': tenant.stripe_connect_account_id
            })
            
            return account_link.url
            
        except Exception as e:
            logger.error(f"❌ Failed to create onboarding link for user {user_id}: {e}")
            raise
    
    def check_account_status(self, user_id):
        """Check the onboarding and verification status of a Connect account"""
        try:
            tenant = Tenant.query.filter_by(owner_user_id=user_id).first()
            if not tenant or not tenant.stripe_connect_account_id:
                return {'status': 'not_created'}
            
            account = stripe.Account.retrieve(tenant.stripe_connect_account_id)
            
            return {
                'status': 'created',
                'account_id': account.id,
                'charges_enabled': account.charges_enabled,
                'payouts_enabled': account.payouts_enabled,
                'details_submitted': account.details_submitted,
                'requirements': account.requirements.to_dict() if account.requirements else None
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to check account status for user {user_id}: {e}")
            return {'status': 'error', 'error': str(e)}
    
    def create_payment_with_fee(self, user_id, amount_cents, currency='usd', description=None):
        """Create a payment that automatically deducts platform fee"""
        try:
            tenant = Tenant.query.filter_by(owner_user_id=user_id).first()
            if not tenant or not tenant.stripe_connect_account_id:
                raise ValueError("No Connect account found for user")
            
            # Calculate platform fee
            platform_fee = int(amount_cents * (self.platform_fee_percent / 100))
            
            # Create PaymentIntent with automatic transfer and fee
            payment_intent = stripe.PaymentIntent.create(
                amount=amount_cents,
                currency=currency,
                description=description or f"AI CEO Platform - User {user_id} sale",
                application_fee_amount=platform_fee,
                transfer_data={
                    'destination': tenant.stripe_connect_account_id,
                },
                metadata={
                    'user_id': str(user_id),
                    'tenant_id': str(tenant.id),
                    'platform_fee': str(platform_fee)
                }
            )
            
            self._log_audit(tenant.id, 'system', 'create_payment', {
                'amount': amount_cents,
                'platform_fee': platform_fee,
                'payment_intent_id': payment_intent.id
            })
            
            return payment_intent
            
        except Exception as e:
            logger.error(f"❌ Failed to create payment for user {user_id}: {e}")
            raise
    
    def handle_webhook(self, payload, sig_header):
        """Handle Stripe Connect webhooks"""
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, self.stripe_webhook_secret
            )
            
            logger.info(f"📥 Received Stripe Connect webhook: {event['type']}")
            
            # Handle different webhook events
            if event['type'] == 'account.updated':
                self._handle_account_updated(event['data']['object'])
            elif event['type'] == 'payment_intent.succeeded':
                self._handle_payment_succeeded(event['data']['object'])
            elif event['type'] == 'transfer.created':
                self._handle_transfer_created(event['data']['object'])
            
            return {'status': 'success'}
            
        except ValueError as e:
            logger.error(f"❌ Invalid webhook signature: {e}")
            return {'error': 'Invalid signature'}, 400
        except Exception as e:
            logger.error(f"❌ Webhook processing error: {e}")
            return {'error': 'Processing failed'}, 500
    
    def _handle_account_updated(self, account):
        """Handle account.updated webhook"""
        tenant = Tenant.query.filter_by(stripe_connect_account_id=account['id']).first()
        if tenant:
            self._log_audit(tenant.id, 'stripe', 'account_updated', {
                'account_id': account['id'],
                'charges_enabled': account.get('charges_enabled'),
                'payouts_enabled': account.get('payouts_enabled')
            })
    
    def _handle_payment_succeeded(self, payment_intent):
        """Handle successful payment with platform fee"""
        if 'user_id' in payment_intent.get('metadata', {}):
            user_id = payment_intent['metadata']['user_id']
            tenant = Tenant.query.filter_by(owner_user_id=user_id).first()
            
            if tenant:
                self._log_audit(tenant.id, 'stripe', 'payment_succeeded', {
                    'payment_intent_id': payment_intent['id'],
                    'amount': payment_intent['amount'],
                    'platform_fee': payment_intent['metadata'].get('platform_fee', 0)
                })
    
    def _handle_transfer_created(self, transfer):
        """Handle transfer to user account"""
        if 'destination' in transfer:
            tenant = Tenant.query.filter_by(stripe_connect_account_id=transfer['destination']).first()
            if tenant:
                self._log_audit(tenant.id, 'stripe', 'transfer_created', {
                    'transfer_id': transfer['id'],
                    'amount': transfer['amount']
                })
    
    def _log_audit(self, tenant_id, actor, action, payload):
        """Log audit trail for Connect operations"""
        try:
            audit_log = AuditLog(
                tenant_id=tenant_id,
                actor=actor,
                action=action,
                payload_json=json.dumps(payload),
                ip_address=request.environ.get('REMOTE_ADDR') if request else None,
                user_agent=request.environ.get('HTTP_USER_AGENT') if request else None
            )
            db.session.add(audit_log)
            db.session.commit()
        except Exception as e:
            logger.error(f"Failed to log audit: {e}")
            db.session.rollback()

# Initialize manager
stripe_connect_manager = StripeConnectManager()

# Routes
@stripe_connect_bp.route('/connect/start', methods=['POST'])
@login_required
def start_connect():
    """Start Stripe Connect onboarding process"""
    try:
        data = request.get_json() or {}
        business_info = data.get('business_info', {})
        
        # Create Express account
        account = stripe_connect_manager.create_express_account(
            current_user.id,
            current_user.email,
            business_info
        )
        
        # Create onboarding link
        return_url = request.host_url + 'connect/success'
        refresh_url = request.host_url + 'connect/refresh'
        
        onboarding_url = stripe_connect_manager.create_onboarding_link(
            current_user.id,
            return_url,
            refresh_url
        )
        
        return jsonify({
            'success': True,
            'onboarding_url': onboarding_url,
            'account_id': account.id
        })
        
    except Exception as e:
        logger.error(f"Connect start failed: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@stripe_connect_bp.route('/connect/status', methods=['GET'])
@login_required
def connect_status():
    """Check Connect account status"""
    try:
        status = stripe_connect_manager.check_account_status(current_user.id)
        return jsonify(status)
    except Exception as e:
        logger.error(f"Status check failed: {e}")
        return jsonify({'status': 'error', 'error': str(e)}), 500

@stripe_connect_bp.route('/connect/success')
@login_required
def connect_success():
    """Handle successful Connect onboarding"""
    return redirect(url_for('dashboard') + '?connect=success')

@stripe_connect_bp.route('/connect/refresh')
@login_required
def connect_refresh():
    """Handle Connect onboarding refresh"""
    return redirect(url_for('getting_started') + '?connect=refresh')

@stripe_connect_bp.route('/webhooks/connect', methods=['POST'])
def connect_webhook():
    """Handle Stripe Connect webhooks"""
    payload = request.get_data()
    sig_header = request.headers.get('Stripe-Signature')
    
    return jsonify(stripe_connect_manager.handle_webhook(payload, sig_header))