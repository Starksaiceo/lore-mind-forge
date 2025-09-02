"""
Webhook Router System for AI CEO Platform
Handles webhooks from all connected platforms with security verification
"""

import os
import json
import hmac
import hashlib
import logging
from datetime import datetime
from flask import Blueprint, request, jsonify
from models import db, TenantConnection, TenantSecret, AuditLog, Tenant
import stripe

logger = logging.getLogger(__name__)

webhook_bp = Blueprint('webhooks', __name__)

class WebhookRouter:
    """Routes and processes webhooks from all platforms"""
    
    def __init__(self):
        self.platform_handlers = {
            'shopify': self.handle_shopify_webhook,
            'stripe': self.handle_stripe_webhook,
            'meta': self.handle_meta_webhook,
            'google': self.handle_google_webhook,
            'linkedin': self.handle_linkedin_webhook,
            'x': self.handle_x_webhook
        }
    
    def verify_shopify_webhook(self, payload, signature, webhook_secret):
        """Verify Shopify webhook signature"""
        try:
            expected_signature = base64.b64encode(
                hmac.new(
                    webhook_secret.encode('utf-8'),
                    payload,
                    hashlib.sha256
                ).digest()
            ).decode('utf-8')
            
            return hmac.compare_digest(signature, expected_signature)
        except Exception as e:
            logger.error(f"Shopify webhook verification failed: {e}")
            return False
    
    def verify_stripe_webhook(self, payload, signature):
        """Verify Stripe webhook signature"""
        try:
            webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET')
            if not webhook_secret:
                return False
            
            stripe.Webhook.construct_event(payload, signature, webhook_secret)
            return True
        except Exception as e:
            logger.error(f"Stripe webhook verification failed: {e}")
            return False
    
    def verify_meta_webhook(self, payload, signature, webhook_secret):
        """Verify Meta webhook signature"""
        try:
            expected_signature = hmac.new(
                webhook_secret.encode('utf-8'),
                payload,
                hashlib.sha256
            ).hexdigest()
            
            return hmac.compare_digest(signature, f'sha256={expected_signature}')
        except Exception as e:
            logger.error(f"Meta webhook verification failed: {e}")
            return False
    
    def handle_shopify_webhook(self, payload, tenant_id):
        """Process Shopify webhook"""
        try:
            data = json.loads(payload)
            event_type = request.headers.get('X-Shopify-Topic', 'unknown')
            
            if event_type == 'orders/create':
                # New order created
                order = data
                logger.info(f"📦 New Shopify order: {order.get('name')} for ${order.get('total_price')}")
                
                # Log revenue to tenant
                self._log_revenue(tenant_id, 'shopify', float(order.get('total_price', 0)))
                
            elif event_type == 'app/uninstalled':
                # App was uninstalled
                self._disconnect_platform(tenant_id, 'shopify')
                logger.info(f"❌ Shopify app uninstalled for tenant {tenant_id}")
                
            elif event_type == 'products/create':
                # New product created
                product = data
                logger.info(f"✅ New Shopify product: {product.get('title')}")
            
            return True
            
        except Exception as e:
            logger.error(f"Shopify webhook processing failed: {e}")
            return False
    
    def handle_stripe_webhook(self, payload, tenant_id=None):
        """Process Stripe webhook"""
        try:
            event = stripe.Webhook.construct_event(
                payload, 
                request.headers.get('Stripe-Signature'),
                os.getenv('STRIPE_WEBHOOK_SECRET')
            )
            
            if event['type'] == 'payment_intent.succeeded':
                payment_intent = event['data']['object']
                amount = payment_intent['amount'] / 100  # Convert from cents
                
                # Check if this is for our headless store
                if payment_intent['metadata'].get('store_type') == 'headless':
                    tenant_id = payment_intent.get('transfer_data', {}).get('destination')
                    if tenant_id:
                        tenant = Tenant.query.filter_by(stripe_connect_account_id=tenant_id).first()
                        if tenant:
                            self._log_revenue(tenant.id, 'headless_store', amount)
                            logger.info(f"💰 Headless store sale: ${amount}")
                
            elif event['type'] == 'account.updated':
                # Stripe Connect account updated
                account = event['data']['object']
                account_id = account['id']
                
                tenant = Tenant.query.filter_by(stripe_connect_account_id=account_id).first()
                if tenant:
                    logger.info(f"🔄 Stripe Connect account updated for tenant {tenant.id}")
            
            return True
            
        except Exception as e:
            logger.error(f"Stripe webhook processing failed: {e}")
            return False
    
    def handle_meta_webhook(self, payload, tenant_id):
        """Process Meta (Facebook/Instagram) webhook"""
        try:
            data = json.loads(payload)
            
            for entry in data.get('entry', []):
                for change in entry.get('changes', []):
                    field = change.get('field')
                    
                    if field == 'ad_campaign':
                        # Ad campaign status change
                        logger.info(f"📊 Meta ad campaign update for tenant {tenant_id}")
                        
                    elif field == 'page':
                        # Page activity (comments, messages)
                        logger.info(f"💬 Meta page activity for tenant {tenant_id}")
            
            return True
            
        except Exception as e:
            logger.error(f"Meta webhook processing failed: {e}")
            return False
    
    def handle_google_webhook(self, payload, tenant_id):
        """Process Google Ads webhook"""
        try:
            data = json.loads(payload)
            
            # Google uses Cloud Pub/Sub for webhooks
            if 'message' in data:
                message_data = data['message'].get('data', '')
                if message_data:
                    # Decode base64 message
                    import base64
                    decoded_data = json.loads(base64.b64decode(message_data))
                    
                    logger.info(f"📊 Google Ads update for tenant {tenant_id}: {decoded_data}")
            
            return True
            
        except Exception as e:
            logger.error(f"Google webhook processing failed: {e}")
            return False
    
    def handle_linkedin_webhook(self, payload, tenant_id):
        """Process LinkedIn webhook"""
        try:
            data = json.loads(payload)
            
            # LinkedIn webhook for post engagement
            if 'activity' in data:
                activity = data['activity']
                logger.info(f"👔 LinkedIn activity for tenant {tenant_id}: {activity}")
            
            return True
            
        except Exception as e:
            logger.error(f"LinkedIn webhook processing failed: {e}")
            return False
    
    def handle_x_webhook(self, payload, tenant_id):
        """Process X (Twitter) webhook"""
        try:
            data = json.loads(payload)
            
            # X webhook for tweets, mentions
            if 'tweet_create_events' in data:
                tweets = data['tweet_create_events']
                logger.info(f"🐦 X tweet events for tenant {tenant_id}: {len(tweets)} tweets")
                
            elif 'favorite_events' in data:
                favorites = data['favorite_events']
                logger.info(f"❤️ X favorite events for tenant {tenant_id}: {len(favorites)} favorites")
            
            return True
            
        except Exception as e:
            logger.error(f"X webhook processing failed: {e}")
            return False
    
    def _log_revenue(self, tenant_id, source, amount):
        """Log revenue to audit trail"""
        try:
            audit_log = AuditLog(
                tenant_id=tenant_id,
                actor='system',
                action='revenue_recorded',
                payload_json=json.dumps({
                    'source': source,
                    'amount': amount,
                    'timestamp': datetime.utcnow().isoformat()
                }),
                ip_address=request.environ.get('REMOTE_ADDR'),
                user_agent='webhook'
            )
            db.session.add(audit_log)
            db.session.commit()
        except Exception as e:
            logger.error(f"Revenue logging failed: {e}")
            db.session.rollback()
    
    def _disconnect_platform(self, tenant_id, platform):
        """Mark platform as disconnected"""
        try:
            connection = TenantConnection.query.filter_by(
                tenant_id=tenant_id,
                integration_code=platform
            ).first()
            
            if connection:
                connection.status = 'disconnected'
                db.session.commit()
                
                self._log_audit(tenant_id, 'system', f'auto_disconnect_{platform}', {
                    'reason': 'webhook_uninstall',
                    'platform': platform
                })
        except Exception as e:
            logger.error(f"Auto disconnect failed: {e}")
            db.session.rollback()
    
    def _log_audit(self, tenant_id, actor, action, payload):
        """Log audit trail"""
        try:
            audit_log = AuditLog(
                tenant_id=tenant_id,
                actor=actor,
                action=action,
                payload_json=json.dumps(payload),
                ip_address=request.environ.get('REMOTE_ADDR'),
                user_agent=request.environ.get('HTTP_USER_AGENT')
            )
            db.session.add(audit_log)
            db.session.commit()
        except Exception as e:
            logger.error(f"Audit log failed: {e}")
            db.session.rollback()

# Initialize router
webhook_router = WebhookRouter()

# Routes
@webhook_bp.route('/webhook/<platform>', methods=['POST'])
def handle_webhook(platform):
    """Generic webhook handler for all platforms"""
    try:
        payload = request.get_data()
        
        if platform not in webhook_router.platform_handlers:
            logger.warning(f"Unknown platform webhook: {platform}")
            return jsonify({'error': 'Unsupported platform'}), 400
        
        # Platform-specific verification
        verified = False
        tenant_id = None
        
        if platform == 'shopify':
            # Shopify sends shop domain in headers
            shop_domain = request.headers.get('X-Shopify-Shop-Domain')
            if shop_domain:
                # Find tenant by shop domain
                connection = TenantConnection.query.filter(
                    TenantConnection.integration_code == 'shopify',
                    TenantConnection.meta_json.like(f'%{shop_domain}%')
                ).first()
                
                if connection:
                    tenant_id = connection.tenant_id
                    # Get webhook secret for verification
                    secret_record = TenantSecret.query.filter_by(
                        connection_id=connection.id,
                        key='webhook_secret'
                    ).first()
                    
                    if secret_record:
                        webhook_secret = secret_record.decrypt_value()
                        signature = request.headers.get('X-Shopify-Hmac-Sha256')
                        verified = webhook_router.verify_shopify_webhook(payload, signature, webhook_secret)
        
        elif platform == 'stripe':
            # Stripe webhooks are global but we filter by account
            signature = request.headers.get('Stripe-Signature')
            verified = webhook_router.verify_stripe_webhook(payload, signature)
            # For Stripe, tenant_id is extracted from event data
        
        elif platform == 'meta':
            # Meta webhook verification
            signature = request.headers.get('X-Hub-Signature-256')
            if signature:
                # Get webhook secret from environment (global for all Meta connections)
                webhook_secret = os.getenv('META_WEBHOOK_SECRET')
                if webhook_secret:
                    verified = webhook_router.verify_meta_webhook(payload, signature.replace('sha256=', ''), webhook_secret)
        
        # For other platforms, implement similar verification patterns
        
        if not verified:
            logger.warning(f"Webhook verification failed for {platform}")
            return jsonify({'error': 'Verification failed'}), 401
        
        # Process webhook
        handler = webhook_router.platform_handlers[platform]
        success = handler(payload, tenant_id)
        
        if success:
            return jsonify({'status': 'success'}), 200
        else:
            return jsonify({'error': 'Processing failed'}), 500
            
    except Exception as e:
        logger.error(f"Webhook routing failed for {platform}: {e}")
        return jsonify({'error': 'Webhook processing failed'}), 500

@webhook_bp.route('/webhook/test/<platform>', methods=['POST'])
def test_webhook(platform):
    """Test webhook endpoint for development"""
    try:
        if os.getenv('FLASK_ENV') != 'development':
            return jsonify({'error': 'Test endpoints only available in development'}), 403
        
        payload = request.get_data()
        logger.info(f"🧪 Test webhook for {platform}: {len(payload)} bytes")
        
        # Log the test webhook
        audit_log = AuditLog(
            tenant_id=None,
            actor='system',
            action=f'test_webhook_{platform}',
            payload_json=json.dumps({
                'platform': platform,
                'payload_size': len(payload),
                'headers': dict(request.headers),
                'timestamp': datetime.utcnow().isoformat()
            }),
            ip_address=request.environ.get('REMOTE_ADDR'),
            user_agent=request.environ.get('HTTP_USER_AGENT')
        )
        db.session.add(audit_log)
        db.session.commit()
        
        return jsonify({'status': 'test webhook received'}), 200
        
    except Exception as e:
        logger.error(f"Test webhook failed: {e}")
        return jsonify({'error': str(e)}), 500

@webhook_bp.route('/webhook/status')
def webhook_status():
    """Get webhook system status"""
    try:
        # Count recent webhooks by platform
        from sqlalchemy import func, and_
        from datetime import timedelta
        
        recent_date = datetime.utcnow() - timedelta(hours=24)
        
        webhook_stats = db.session.query(
            AuditLog.action,
            func.count(AuditLog.id).label('count')
        ).filter(
            and_(
                AuditLog.created_at >= recent_date,
                AuditLog.action.like('webhook_%')
            )
        ).group_by(AuditLog.action).all()
        
        stats = {stat.action: stat.count for stat in webhook_stats}
        
        return jsonify({
            'status': 'operational',
            'last_24_hours': stats,
            'supported_platforms': list(webhook_router.platform_handlers.keys()),
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Webhook status failed: {e}")
        return jsonify({'error': str(e)}), 500

# Initialize router
webhook_router = WebhookRouter()