
import os
from typing import Dict, Any

class ScalingConfig:
    """Production scaling configuration for 5000+ users"""
    
    # Database scaling
    POSTGRESQL_POOL_SIZE = 20
    POSTGRESQL_MAX_OVERFLOW = 30
    POSTGRESQL_POOL_RECYCLE = 3600
    
    # Redis for session/cache scaling
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    SESSION_TYPE = 'redis'
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_KEY_PREFIX = 'ai_ceo_session:'
    
    # File storage scaling
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Rate limiting for API endpoints
    RATELIMIT_STORAGE_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/1')
    RATELIMIT_DEFAULT = "100 per hour, 20 per minute"
    
    # Celery for background tasks
    CELERY_BROKER_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/2')
    CELERY_RESULT_BACKEND = os.getenv('REDIS_URL', 'redis://localhost:6379/3')
    
    @staticmethod
    def get_production_config() -> Dict[str, Any]:
        """Get production configuration for high-traffic deployment"""
        return {
            'SQLALCHEMY_ENGINE_OPTIONS': {
                'pool_size': ScalingConfig.POSTGRESQL_POOL_SIZE,
                'max_overflow': ScalingConfig.POSTGRESQL_MAX_OVERFLOW,
                'pool_recycle': ScalingConfig.POSTGRESQL_POOL_RECYCLE,
                'pool_pre_ping': True
            },
            'SESSION_TYPE': ScalingConfig.SESSION_TYPE,
            'SESSION_REDIS': ScalingConfig.REDIS_URL,
            'RATELIMIT_STORAGE_URL': ScalingConfig.RATELIMIT_STORAGE_URL,
            'CELERY_BROKER_URL': ScalingConfig.CELERY_BROKER_URL,
            'CELERY_RESULT_BACKEND': ScalingConfig.CELERY_RESULT_BACKEND
        }

# Replit Autoscale Deployment Configuration
REPLIT_AUTOSCALE_CONFIG = {
    'machine_power': 'medium',      # 2 vCPU, 4GB RAM per instance
    'max_instances': 10,            # Scale up to 10 instances
    'min_instances': 2,             # Always keep 2 instances running
    'target_cpu_utilization': 70,  # Scale when CPU > 70%
    'health_check_path': '/health',
    'environment_variables': {
        'FLASK_ENV': 'production',
        'SQLALCHEMY_POOL_SIZE': '20',
        'REDIS_URL': '${REDIS_URL}',
        'DATABASE_URL': '${DATABASE_URL}'
    }
}
