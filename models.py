from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
from flask_login import UserMixin
import os
from cryptography.fernet import Fernet

db = SQLAlchemy()

# Configure database for production scaling
def configure_database_for_production():
    """Configure database settings for 5000+ user capacity"""
    database_url = os.getenv('DATABASE_URL')
    if database_url and 'postgresql' in database_url:
        # PostgreSQL optimizations for high concurrency
        return {
            'pool_size': 30,
            'max_overflow': 50,
            'pool_recycle': 3600,
            'pool_pre_ping': True,
            'pool_timeout': 30,
            'echo': False
        }
    return {}

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=True)  # Match database schema
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)  # Match database column name
    stripe_customer_id = db.Column(db.String(255), nullable=True)
    subscription_status = db.Column(db.String(50), default='trial')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Voice system columns - matching database schema
    voice_name = db.Column(db.String(100), default='AI CEO')
    voice_personality = db.Column(db.String(50), default='professional')
    voice_enabled = db.Column(db.Boolean, default=False)
    voice_type = db.Column(db.String(50), default='professional')

    # Role column to match database schema
    role = db.Column(db.String(50), default='user')

    # Property to maintain compatibility with existing code
    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, value):
        self.password_hash = value

    # Flask-Login required methods
    @property 
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class TeamMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    role = db.Column(db.String(32), default="member")  # owner|marketer|assistant
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    stripe_customer_id = db.Column(db.String(120))
    stripe_subscription_id = db.Column(db.String(120))
    plan_id = db.Column(db.String(64))  # starter|pro|enterprise
    status = db.Column(db.String(64), default="inactive")  # trialing|active|past_due|canceled|pending
    current_period_end = db.Column(db.Integer, default=0)  # epoch
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class AgentMemory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    key = db.Column(db.String(120))
    value = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class AIEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_type = db.Column(db.String(80))
    event_json = db.Column(db.Text)  # JSON string
    success = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class UserSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
    logo_path = db.Column(db.String(256))
    primary_color = db.Column(db.String(16))
    secondary_color = db.Column(db.String(16))
    subdomain = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Plugin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    code_blob = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class UserPlugin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    plugin_id = db.Column(db.Integer, db.ForeignKey('plugin.id'), nullable=False)
    installed_at = db.Column(db.DateTime, default=datetime.utcnow)

class ShopifyOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    shopify_order_id = db.Column(db.String(120), unique=True)
    total_price = db.Column(db.Float, default=0.0)
    currency = db.Column(db.String(8), default="USD")
    status = db.Column(db.String(32))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ProductStore(db.Model):
    """Store generated products and their metadata"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, default=0.0)
    category = db.Column(db.String(100))
    file_path = db.Column(db.String(500))  # Local file location
    shopify_product_id = db.Column(db.String(120))  # Shopify integration
    status = db.Column(db.String(50), default='draft')  # draft|published|sold
    revenue = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class APIEndpoint(db.Model):
    """Track API usage and performance"""
    __tablename__ = 'api_endpoints'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    endpoint_name = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    method = db.Column(db.String(10), nullable=False, default='GET')
    headers = db.Column(db.Text)  # JSON string
    payload = db.Column(db.Text)  # JSON string
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_used = db.Column(db.DateTime)
    usage_count = db.Column(db.Integer, default=0)

class SocialPost(db.Model):
    """Social media posts tracking"""
    __tablename__ = 'social_posts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    platform = db.Column(db.String(50), nullable=False)  # x, instagram, tiktok, etc.
    post_id = db.Column(db.String(100), nullable=False)  # Platform-specific post ID
    status = db.Column(db.String(20), default='published')  # published, scheduled, failed
    caption = db.Column(db.Text)
    media_url = db.Column(db.String(500))
    link_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Index for efficient queries
    __table_args__ = (
        db.Index('idx_social_posts_user_platform', 'user_id', 'platform'),
    )

class AdEntity(db.Model):
    """Advertising entities tracking"""
    __tablename__ = 'ad_entities'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    platform = db.Column(db.String(50), nullable=False)  # meta, google, tiktok
    campaign_id = db.Column(db.String(100))
    adset_id = db.Column(db.String(100))
    ad_id = db.Column(db.String(100))
    objective = db.Column(db.String(50))  # traffic, sales, leads
    budget_daily = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(20), default='active')  # active, paused, completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Index for efficient queries
    __table_args__ = (
        db.Index('idx_ad_entities_user_platform', 'user_id', 'platform'),
    )

class ProfitLog(db.Model):
    """Track daily profit/loss for AI memory system"""
    __tablename__ = 'profit_log'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    source = db.Column(db.String(100), nullable=False)  # shopify, subscription, products
    amount = db.Column(db.Float, nullable=False)
    profit_type = db.Column(db.String(50), default='revenue')  # revenue, cost, profit
    date = db.Column(db.Date, default=datetime.utcnow)
    additional_metadata = db.Column(db.Text)  # JSON for additional data
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Index for efficient queries
    __table_args__ = (
        db.Index('idx_profit_log_user_date', 'user_id', 'date'),
        db.Index('idx_profit_log_source', 'source'),
    )

class StrategyCache(db.Model):
    """Cache strategy performance for AI learning"""
    __tablename__ = 'strategy_cache'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    strategy = db.Column(db.String(200), nullable=False)
    average_profit = db.Column(db.Float, default=0.0)
    usage_count = db.Column(db.Integer, default=0)
    success_rate = db.Column(db.Float, default=0.0)
    last_used = db.Column(db.DateTime, default=datetime.utcnow)
    performance_data = db.Column(db.Text)  # JSON for detailed metrics
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Index for efficient queries
    __table_args__ = (
        db.Index('idx_strategy_cache_user_strategy', 'user_id', 'strategy'),
        db.Index('idx_strategy_cache_performance', 'average_profit', 'success_rate'),
    )

class TrendData(db.Model):
    """Store real-time trend data for strategist"""
    __tablename__ = 'trend_data'
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(100), nullable=False)  # google, amazon, producthunt, tiktok
    keyword = db.Column(db.String(200), nullable=False)
    rank = db.Column(db.Integer, default=0)
    trend_score = db.Column(db.Float, default=0.0)
    category = db.Column(db.String(100))
    additional_data = db.Column(db.Text)  # JSON for source-specific data
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    # Index for efficient queries
    __table_args__ = (
        db.Index('idx_trend_data_source_timestamp', 'source', 'timestamp'),
        db.Index('idx_trend_data_keyword', 'keyword'),
        db.Index('idx_trend_data_rank', 'rank'),
    )

# ===== MULTI-TENANT OAUTH SYSTEM =====

class Tenant(db.Model):
    """Multi-tenant organization model for OAuth and billing"""
    __tablename__ = 'tenants'
    id = db.Column(db.Integer, primary_key=True)
    owner_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    stripe_customer_id = db.Column(db.String(120))
    stripe_subscription_id = db.Column(db.String(120))
    stripe_connect_account_id = db.Column(db.String(120))  # For user payouts
    plan = db.Column(db.String(50), default='starter')  # starter|pro|enterprise
    status = db.Column(db.String(50), default='active')  # active|past_due|suspended|cancelled
    autopilot_enabled = db.Column(db.Boolean, default=False)  # Autopilot automation status
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    connections = db.relationship('TenantConnection', backref='tenant', lazy=True, cascade='all, delete-orphan')
    
    # Index for efficient queries
    __table_args__ = (
        db.Index('idx_tenants_owner', 'owner_user_id'),
        db.Index('idx_tenants_stripe_customer', 'stripe_customer_id'),
    )

class Integration(db.Model):
    """Available OAuth integrations and their settings"""
    __tablename__ = 'integrations'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False)  # shopify, google, meta, linkedin, x, openrouter
    display_name = db.Column(db.String(100), nullable=False)  # Shopify, Google, Meta, LinkedIn, X, OpenRouter
    auth_type = db.Column(db.String(20), nullable=False)  # oauth, apikey
    description = db.Column(db.Text)
    icon_class = db.Column(db.String(100))  # CSS icon class
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class TenantConnection(db.Model):
    """User connections to external platforms via OAuth"""
    __tablename__ = 'tenant_connections'
    id = db.Column(db.Integer, primary_key=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenants.id'), nullable=False)
    integration_code = db.Column(db.String(50), db.ForeignKey('integrations.code'), nullable=False)
    status = db.Column(db.String(50), default='connected')  # connected|disconnected|error|expired
    meta_json = db.Column(db.Text)  # Store account IDs, domain names, etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    secrets = db.relationship('TenantSecret', backref='connection', lazy=True, cascade='all, delete-orphan')
    
    # Index for efficient queries
    __table_args__ = (
        db.Index('idx_tenant_connections_tenant_integration', 'tenant_id', 'integration_code'),
        db.Index('idx_tenant_connections_status', 'status'),
    )

class TenantSecret(db.Model):
    """Encrypted storage for OAuth tokens and API keys"""
    __tablename__ = 'tenant_secrets'
    id = db.Column(db.Integer, primary_key=True)
    connection_id = db.Column(db.Integer, db.ForeignKey('tenant_connections.id'), nullable=False)
    key = db.Column(db.String(100), nullable=False)  # access_token, refresh_token, api_key, etc.
    value_encrypted = db.Column(db.Text, nullable=False)  # Fernet encrypted value
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    @staticmethod
    def get_fernet_key():
        """Get or generate Fernet encryption key"""
        fernet_key = os.getenv('FERNET_KEY')
        if not fernet_key:
            # Generate new key for development
            fernet_key = Fernet.generate_key().decode()
            print(f"⚠️ Generated new FERNET_KEY: {fernet_key}")
            print("⚠️ Add this to your Replit Secrets for production!")
        return fernet_key.encode() if isinstance(fernet_key, str) else fernet_key
    
    def encrypt_value(self, value):
        """Encrypt and store a secret value"""
        fernet = Fernet(self.get_fernet_key())
        self.value_encrypted = fernet.encrypt(value.encode()).decode()
    
    def decrypt_value(self):
        """Decrypt and return the secret value"""
        fernet = Fernet(self.get_fernet_key())
        return fernet.decrypt(self.value_encrypted.encode()).decode()
    
    # Index for efficient queries
    __table_args__ = (
        db.Index('idx_tenant_secrets_connection_key', 'connection_id', 'key'),
    )

class AuditLog(db.Model):
    """Track all tenant actions for compliance and debugging"""
    __tablename__ = 'audit_logs'
    id = db.Column(db.Integer, primary_key=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenants.id'), nullable=False)
    actor = db.Column(db.String(100), nullable=False)  # user|system|ai_agent
    action = db.Column(db.String(100), nullable=False)  # connect_shopify, post_content, create_ad, etc.
    payload_json = db.Column(db.Text)  # Action details in JSON
    ip_address = db.Column(db.String(45))  # IPv4/IPv6 support
    user_agent = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Index for efficient queries
    __table_args__ = (
        db.Index('idx_audit_logs_tenant_created', 'tenant_id', 'created_at'),
        db.Index('idx_audit_logs_action', 'action'),
    )

class ConnectedStore(db.Model):
    """Model for tracking connected external stores"""
    __tablename__ = 'connected_stores'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    platform = db.Column(db.String(50), nullable=False)  # shopify, woocommerce, etc.
    store_url = db.Column(db.String(500), nullable=False)
    current_revenue = db.Column(db.Integer, default=0)  # Monthly revenue
    status = db.Column(db.String(50), default='analyzing')  # analyzing, connected, optimizing, error
    api_credentials = db.Column(db.Text)  # Encrypted API keys/tokens
    last_sync = db.Column(db.DateTime)
    connected_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Index for efficient queries
    __table_args__ = (
        db.Index('idx_connected_stores_user', 'user_id'),
        db.Index('idx_connected_stores_platform', 'platform'),
    )

class InviteCode(db.Model):
    """Model for invite-only registration system"""
    __tablename__ = 'invite_codes'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(32), unique=True, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    used_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    uses_remaining = db.Column(db.Integer, default=1)  # How many times this code can be used
    expires_at = db.Column(db.DateTime, nullable=True)  # Optional expiration
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    used_at = db.Column(db.DateTime, nullable=True)
    
    # Index for efficient queries
    __table_args__ = (
        db.Index('idx_invite_codes_code', 'code'),
        db.Index('idx_invite_codes_active', 'is_active'),
    )

class AccessControl(db.Model):
    """Model for IP whitelist and access controls"""
    __tablename__ = 'access_controls'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    control_type = db.Column(db.String(50), nullable=False)  # ip_whitelist, session_timeout, etc.
    control_value = db.Column(db.String(500), nullable=False)  # IP address, timeout value, etc.
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Index for efficient queries
    __table_args__ = (
        db.Index('idx_access_controls_user_type', 'user_id', 'control_type'),
        db.Index('idx_access_controls_active', 'is_active'),
    )


def create_all():
    """Initialize all database tables"""
    try:
        db.create_all()
        print("✅ Database tables created successfully")
        return True
    except Exception as e:
        print(f"❌ Database creation failed: {e}")
        return False

# Export for backward compatibility
__all__ = ['db', 'User', 'Team', 'TeamMember', 'Subscription', 'AgentMemory', 'AIEvent', 'UserSettings', 'Plugin', 'UserPlugin', 'ShopifyOrder', 'ProductStore', 'APIEndpoint', 'SocialPost', 'AdEntity', 'ProfitLog', 'StrategyCache', 'TrendData', 'Tenant', 'Integration', 'TenantConnection', 'TenantSecret', 'AuditLog', 'ConnectedStore', 'InviteCode', 'AccessControl', 'create_all']