
#!/usr/bin/env python3
"""
Simple database setup utility
"""

import os
import sys
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_database():
    """Initialize database with required tables"""
    try:
        # Run the database upgrade
        from database_upgrade import upgrade_database
        success = upgrade_database()
        
        if success:
            logger.info("✅ Database setup completed!")
            return True
        else:
            logger.error("❌ Database setup failed!")
            return False
            
    except Exception as e:
        logger.error(f"❌ Setup error: {e}")
        return False

if __name__ == "__main__":
    success = setup_database()
    sys.exit(0 if success else 1)
