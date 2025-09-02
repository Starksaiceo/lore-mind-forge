"""
OAuth Connection System for AI CEO Platform
Handles "one-click" connections to Shopify, Google, Meta, LinkedIn, X, and API keys
"""

import os
import secrets
import requests
import base64
from urllib.parse import urlencode, parse_qs
from flask import Blueprint, request, jsonify, redirect, url_for, session, current_app
from flask_login import login_required, current_user
from models import db, Integration, Tenant, TenantConnection, TenantSecret, AuditLog
from sqlalchemy import select
import json
import logging

logger = logging.getLogger(__name__)

oauth_bp = Blueprint('oauth', __name__)

class OAuthManager:
    """Manages OAuth connections for all supported platforms"""
    
    def __init__(self):
        # Platform configurations
        self.platforms = {
            'shopify': {
                'client_id': os.getenv('SHOPIFY_CLIENT_ID'),
                'client_secret': os.getenv('SHOPIFY_CLIENT_SECRET'),
                'scopes': 'write_products,write_themes,write_pages,write_orders,read_orders,read_customers',
                'auth_url': 'https://{shop}.myshopify.com/admin/oauth/authorize',
                'token_url': 'https://{shop}.myshopify.com/admin/oauth/access_token'
            },
            'google': {
                'client_id': os.getenv('GOOGLE_CLIENT_ID'),
                'client_secret': os.getenv('GOOGLE_CLIENT_SECRET'),
                'scopes': 'https://www.googleapis.com/auth/youtube https://www.googleapis.com/auth/adwords',
                'auth_url': 'https://accounts.google.com/o/oauth2/v2/auth',
                'token_url': 'https://oauth2.googleapis.com/token'
            },
            'meta': {
                'client_id': os.getenv('META_CLIENT_ID'),
                'client_secret': os.getenv('META_CLIENT_SECRET'),
                'scopes': 'ads_management,ads_read,pages_manage_posts,instagram_content_publish',
                'auth_url': 'https://www.facebook.com/v18.0/dialog/oauth',
                'token_url': 'https://graph.facebook.com/v18.0/oauth/access_token'
            },
            'linkedin': {
                'client_id': os.getenv('LINKEDIN_CLIENT_ID'),
                'client_secret': os.getenv('LINKEDIN_CLIENT_SECRET'),
                'scopes': 'w_member_social,r_basicprofile,r_organization_social',
                'auth_url': 'https://www.linkedin.com/oauth/v2/authorization',
                'token_url': 'https://www.linkedin.com/oauth/v2/accessToken'
            },
            'x': {
                'client_id': os.getenv('X_CLIENT_ID'),
                'client_secret': os.getenv('X_CLIENT_SECRET'),
                'scopes': 'tweet.read,tweet.write,users.read,offline.access',
                'auth_url': 'https://twitter.com/i/oauth2/authorize',
                'token_url': 'https://api.twitter.com/2/oauth2/token'
            }
        }
    
    def get_tenant_or_create(self, user_id):
        """Get existing tenant or create new one"""
        tenant = db.session.execute(select(Tenant).where(Tenant.owner_user_id == user_id)).scalar_one_or_none()
        if not tenant:
            from models import User
            user = db.session.get(User, user_id)
            tenant = Tenant(
                owner_user_id=user_id,
                stripe_customer_id=user.stripe_customer_id if user else None,
                plan='starter',
                status='active'
            )
            db.session.add(tenant)
            db.session.flush()
        return tenant
    
    def start_oauth_flow(self, platform, user_id, shop_domain=None):
        """Initiate OAuth flow for a platform"""
        try:
            if platform not in self.platforms:
                raise ValueError(f"Unsupported platform: {platform}")
            
            tenant = self.get_tenant_or_create(user_id)
            config = self.platforms[platform]
            
            if not config['client_id'] or not config['client_secret']:
                raise ValueError(f"Missing OAuth credentials for {platform}")
            
            # Generate state token for security
            state = secrets.token_urlsafe(32)
            session[f'oauth_state_{platform}'] = state
            session[f'oauth_tenant_id_{platform}'] = tenant.id
            
            # Store shop domain for Shopify
            if platform == 'shopify' and shop_domain:
                session[f'oauth_shop_{platform}'] = shop_domain
            
            # Build authorization URL
            redirect_uri = request.host_url.rstrip('/') + url_for('oauth.oauth_callback', platform=platform)
            
            auth_params = {
                'client_id': config['client_id'],
                'redirect_uri': redirect_uri,
                'scope': config['scopes'],
                'state': state,
                'response_type': 'code'
            }
            
            # Platform-specific parameters
            if platform == 'shopify':
                auth_url = config['auth_url'].format(shop=shop_domain)
            elif platform == 'google':
                auth_params['access_type'] = 'offline'
                auth_params['prompt'] = 'consent'
                auth_url = config['auth_url']
            elif platform == 'meta':
                auth_url = config['auth_url']
            elif platform == 'linkedin':
                auth_url = config['auth_url']
            elif platform == 'x':
                auth_params['code_challenge_method'] = 'plain'
                auth_params['code_challenge'] = secrets.token_urlsafe(32)
                session[f'oauth_challenge_{platform}'] = auth_params['code_challenge']
                auth_url = config['auth_url']
            
            full_auth_url = f"{auth_url}?{urlencode(auth_params)}"
            
            self._log_audit(tenant.id, 'user', f'start_oauth_{platform}', {
                'platform': platform,
                'redirect_uri': redirect_uri
            })
            
            return full_auth_url
            
        except Exception as e:
            logger.error(f"OAuth flow start failed for {platform}: {e}")
            raise
    
    def handle_oauth_callback(self, platform, code, state):
        """Handle OAuth callback and exchange code for tokens"""
        try:
            # Verify state token
            expected_state = session.pop(f'oauth_state_{platform}', None)
            if not expected_state or state != expected_state:
                raise ValueError("Invalid state token - possible CSRF attack")
            
            tenant_id = session.pop(f'oauth_tenant_id_{platform}', None)
            if not tenant_id:
                raise ValueError("No tenant ID in session")
            
            tenant = Tenant.query.get(tenant_id)
            if not tenant:
                raise ValueError("Tenant not found")
            
            config = self.platforms[platform]
            redirect_uri = request.host_url.rstrip('/') + url_for('oauth.oauth_callback', platform=platform)
            
            # Prepare token request
            token_data = {
                'client_id': config['client_id'],
                'client_secret': config['client_secret'],
                'code': code,
                'redirect_uri': redirect_uri,
                'grant_type': 'authorization_code'
            }
            
            # Platform-specific token exchange
            if platform == 'shopify':
                shop_domain = session.pop(f'oauth_shop_{platform}')
                token_url = config['token_url'].format(shop=shop_domain)
                response = requests.post(token_url, json=token_data)
                token_info = response.json()
                
                if 'access_token' in token_info:
                    self._save_connection(tenant.id, platform, {
                        'access_token': token_info['access_token'],
                        'shop_domain': shop_domain,
                        'scope': token_info.get('scope', config['scopes'])
                    })
                    return True
                    
            elif platform == 'google':
                response = requests.post(config['token_url'], data=token_data)
                token_info = response.json()
                
                if 'access_token' in token_info:
                    self._save_connection(tenant.id, platform, {
                        'access_token': token_info['access_token'],
                        'refresh_token': token_info.get('refresh_token'),
                        'expires_in': token_info.get('expires_in', 3600),
                        'scope': token_info.get('scope', config['scopes'])
                    })
                    return True
                    
            elif platform == 'meta':
                response = requests.post(config['token_url'], data=token_data)
                token_info = response.json()
                
                if 'access_token' in token_info:
                    # Exchange for long-lived token
                    long_lived_params = {
                        'grant_type': 'fb_exchange_token',
                        'client_id': config['client_id'],
                        'client_secret': config['client_secret'],
                        'fb_exchange_token': token_info['access_token']
                    }
                    long_lived_response = requests.get(config['token_url'], params=long_lived_params)
                    long_lived_token = long_lived_response.json()
                    
                    self._save_connection(tenant.id, platform, {
                        'access_token': long_lived_token.get('access_token', token_info['access_token']),
                        'expires_in': long_lived_token.get('expires_in', token_info.get('expires_in', 3600)),
                        'token_type': token_info.get('token_type', 'bearer')
                    })
                    return True
                    
            elif platform == 'linkedin':
                headers = {'Content-Type': 'application/x-www-form-urlencoded'}
                response = requests.post(config['token_url'], data=token_data, headers=headers)
                token_info = response.json()
                
                if 'access_token' in token_info:
                    self._save_connection(tenant.id, platform, {
                        'access_token': token_info['access_token'],
                        'expires_in': token_info.get('expires_in', 3600),
                        'scope': token_info.get('scope', config['scopes'])
                    })
                    return True
                    
            elif platform == 'x':
                # Add PKCE challenge
                code_verifier = session.pop(f'oauth_challenge_{platform}', None)
                if code_verifier:
                    token_data['code_verifier'] = code_verifier
                
                # X uses Basic Auth
                auth_header = base64.b64encode(
                    f"{config['client_id']}:{config['client_secret']}".encode()
                ).decode()
                headers = {
                    'Authorization': f'Basic {auth_header}',
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
                
                response = requests.post(config['token_url'], data=token_data, headers=headers)
                token_info = response.json()
                
                if 'access_token' in token_info:
                    self._save_connection(tenant.id, platform, {
                        'access_token': token_info['access_token'],
                        'refresh_token': token_info.get('refresh_token'),
                        'expires_in': token_info.get('expires_in', 7200),
                        'scope': token_info.get('scope', config['scopes'])
                    })
                    return True
            
            # If we get here, token exchange failed
            logger.error(f"Token exchange failed for {platform}: {token_info}")
            return False
            
        except Exception as e:
            logger.error(f"OAuth callback handling failed for {platform}: {e}")
            raise
    
    def save_api_key(self, platform, user_id, api_key, additional_data=None):
        """Save API key for platforms that don't use OAuth"""
        try:
            tenant = self.get_tenant_or_create(user_id)
            
            connection_data = {'api_key': api_key}
            if additional_data:
                connection_data.update(additional_data)
            
            self._save_connection(tenant.id, platform, connection_data)
            
            self._log_audit(tenant.id, 'user', f'save_api_key_{platform}', {
                'platform': platform
            })
            
            return True
            
        except Exception as e:
            logger.error(f"API key save failed for {platform}: {e}")
            raise
    
    def get_connection_status(self, user_id):
        """Get status of all connections for a user"""
        try:
            tenant = Tenant.query.filter_by(owner_user_id=user_id).first()
            if not tenant:
                return {}
            
            connections = TenantConnection.query.filter_by(tenant_id=tenant.id).all()
            integrations = {i.code: i for i in Integration.query.all()}
            
            status = {}
            for integration_code, integration in integrations.items():
                connection = next((c for c in connections if c.integration_code == integration_code), None)
                
                status[integration_code] = {
                    'connected': connection is not None and connection.status == 'connected',
                    'status': connection.status if connection else 'not_connected',
                    'display_name': integration.display_name,
                    'auth_type': integration.auth_type,
                    'description': integration.description,
                    'icon_class': integration.icon_class,
                    'last_updated': connection.updated_at.isoformat() if connection else None
                }
            
            return status
            
        except Exception as e:
            logger.error(f"Status check failed for user {user_id}: {e}")
            return {}
    
    def disconnect_platform(self, user_id, platform):
        """Disconnect a platform integration"""
        try:
            tenant = Tenant.query.filter_by(owner_user_id=user_id).first()
            if not tenant:
                return False
            
            connection = TenantConnection.query.filter_by(
                tenant_id=tenant.id,
                integration_code=platform
            ).first()
            
            if connection:
                connection.status = 'disconnected'
                db.session.commit()
                
                self._log_audit(tenant.id, 'user', f'disconnect_{platform}', {
                    'platform': platform
                })
                
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Disconnect failed for {platform}: {e}")
            db.session.rollback()
            raise
    
    def _save_connection(self, tenant_id, platform, token_data):
        """Save connection and encrypted tokens"""
        try:
            # Get or create connection record
            connection = TenantConnection.query.filter_by(
                tenant_id=tenant_id,
                integration_code=platform
            ).first()
            
            if not connection:
                connection = TenantConnection(
                    tenant_id=tenant_id,
                    integration_code=platform,
                    status='connected'
                )
                db.session.add(connection)
                db.session.flush()
            else:
                connection.status = 'connected'
            
            # Store metadata (non-sensitive info)
            meta_data = {}
            if 'shop_domain' in token_data:
                meta_data['shop_domain'] = token_data['shop_domain']
            if 'scope' in token_data:
                meta_data['scope'] = token_data['scope']
            if 'expires_in' in token_data:
                meta_data['expires_in'] = token_data['expires_in']
            
            connection.meta_json = json.dumps(meta_data)
            
            # Save encrypted secrets
            sensitive_keys = ['access_token', 'refresh_token', 'api_key']
            for key in sensitive_keys:
                if key in token_data:
                    # Remove existing secret with same key
                    existing_secret = TenantSecret.query.filter_by(
                        connection_id=connection.id,
                        key=key
                    ).first()
                    if existing_secret:
                        db.session.delete(existing_secret)
                    
                    # Create new encrypted secret
                    secret = TenantSecret(
                        connection_id=connection.id,
                        key=key
                    )
                    secret.encrypt_value(token_data[key])
                    db.session.add(secret)
            
            db.session.commit()
            
            self._log_audit(tenant_id, 'system', f'save_connection_{platform}', {
                'platform': platform,
                'connection_id': connection.id,
                'keys_saved': list(set(token_data.keys()) & set(sensitive_keys))
            })
            
        except Exception as e:
            logger.error(f"Failed to save connection for {platform}: {e}")
            db.session.rollback()
            raise
    
    def _log_audit(self, tenant_id, actor, action, payload):
        """Log audit trail"""
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
            logger.error(f"Audit log failed: {e}")
            db.session.rollback()

# Initialize manager
oauth_manager = OAuthManager()

# Routes
@oauth_bp.route('/connect/<platform>')
@login_required
def connect_platform(platform):
    """Start OAuth connection for a platform"""
    try:
        if platform not in ['shopify', 'google', 'meta', 'linkedin', 'x']:
            return jsonify({'error': 'Unsupported platform'}), 400
        
        # For Shopify, get shop domain from query params
        shop_domain = request.args.get('shop') if platform == 'shopify' else None
        
        if platform == 'shopify' and not shop_domain:
            return jsonify({'error': 'Shop domain required for Shopify'}), 400
        
        auth_url = oauth_manager.start_oauth_flow(platform, current_user.id, shop_domain)
        return redirect(auth_url)
        
    except Exception as e:
        logger.error(f"Connect failed for {platform}: {e}")
        return redirect(url_for('getting_started') + f'?error=connect_{platform}_failed')

@oauth_bp.route('/callback/<platform>')
def oauth_callback(platform):
    """Handle OAuth callback"""
    try:
        code = request.args.get('code')
        state = request.args.get('state')
        error = request.args.get('error')
        
        if error:
            logger.error(f"OAuth error for {platform}: {error}")
            return redirect(url_for('getting_started') + f'?error=oauth_{platform}_{error}')
        
        if not code or not state:
            return redirect(url_for('getting_started') + f'?error=missing_oauth_params')
        
        success = oauth_manager.handle_oauth_callback(platform, code, state)
        
        if success:
            return redirect(url_for('getting_started') + f'?success=connected_{platform}')
        else:
            return redirect(url_for('getting_started') + f'?error=token_exchange_failed')
            
    except Exception as e:
        logger.error(f"OAuth callback failed for {platform}: {e}")
        return redirect(url_for('getting_started') + f'?error=callback_failed')

@oauth_bp.route('/api_key/<platform>', methods=['POST'])
@login_required
def save_api_key(platform):
    """Save API key for platforms that use key-based auth"""
    try:
        data = request.get_json() or {}
        api_key = data.get('api_key')
        
        if not api_key:
            return jsonify({'error': 'API key is required'}), 400
        
        success = oauth_manager.save_api_key(
            platform, 
            current_user.id, 
            api_key,
            data.get('additional_data')
        )
        
        if success:
            return jsonify({'success': True, 'message': f'{platform.title()} API key saved successfully'})
        else:
            return jsonify({'error': 'Failed to save API key'}), 500
            
    except Exception as e:
        logger.error(f"API key save failed for {platform}: {e}")
        return jsonify({'error': str(e)}), 500

@oauth_bp.route('/status')
@login_required
def connection_status():
    """Get connection status for all platforms"""
    try:
        status = oauth_manager.get_connection_status(current_user.id)
        return jsonify(status)
    except Exception as e:
        logger.error(f"Status check failed: {e}")
        return jsonify({'error': str(e)}), 500

@oauth_bp.route('/disconnect/<platform>', methods=['POST'])
@login_required
def disconnect_platform(platform):
    """Disconnect a platform integration"""
    try:
        success = oauth_manager.disconnect_platform(current_user.id, platform)
        
        if success:
            return jsonify({'success': True, 'message': f'{platform.title()} disconnected successfully'})
        else:
            return jsonify({'error': 'Platform not connected or disconnect failed'}), 400
            
    except Exception as e:
        logger.error(f"Disconnect failed for {platform}: {e}")
        return jsonify({'error': str(e)}), 500