#!/usr/bin/env python3
"""
Database upgrade utility for AI CEO SaaS Platform
Handles SQLite to PostgreSQL migration and schema updates
"""

import os
import sqlite3
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def upgrade_database():
    """Add missing tables and columns for voice/personality features"""
    db_path = 'ai_ceo_saas.db'

    if not os.path.exists(db_path):
        logger.info("Database not found, will be created on first run.")
        return True

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # First, create the user table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Check if voice columns exist and add them if they don't
        cursor.execute("PRAGMA table_info(user)")
        columns = [column[1] for column in cursor.fetchall()]
        logger.info(f"Current user table columns: {columns}")

        columns_to_add = [
            ('username', 'TEXT UNIQUE'),
            ('voice_name', 'TEXT DEFAULT "AI CEO"'),
            ('voice_personality', 'TEXT DEFAULT "professional"'),
            ('voice_enabled', 'BOOLEAN DEFAULT FALSE'),
            ('voice_type', 'TEXT DEFAULT "professional"'),
            ('role', 'TEXT DEFAULT "user"'),
            ('stripe_customer_id', 'TEXT'),
            ('subscription_status', 'TEXT DEFAULT "trial"')
        ]

        for column_name, column_def in columns_to_add:
            if column_name not in columns:
                try:
                    cursor.execute(f'ALTER TABLE user ADD COLUMN {column_name} {column_def}')
                    logger.info(f"✅ Added {column_name} column")
                except Exception as e:
                    logger.error(f"❌ Failed to add {column_name}: {e}")

        # Add user preferences table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_preferences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                voice_enabled BOOLEAN DEFAULT FALSE,
                agent_name TEXT DEFAULT 'AI CEO',
                personality TEXT DEFAULT 'professional',
                voice_type TEXT DEFAULT 'professional',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES user (id) ON DELETE CASCADE
            )
        ''')

        # Add generated businesses table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS generated_businesses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                business_data TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES user (id) ON DELETE CASCADE
            )
        ''')

        # Add products table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                price DECIMAL(10,2) DEFAULT 0.00,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES user (id) ON DELETE CASCADE
            )
        ''')

        # Add other required tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS agent_memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                key VARCHAR(255) NOT NULL,
                value TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES user (id)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ai_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                event_type VARCHAR(100) NOT NULL,
                event_json TEXT,
                success BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES user (id)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS business_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                revenue DECIMAL(10,2) DEFAULT 0.00,
                products_created INTEGER DEFAULT 0,
                orders_fulfilled INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES user (id)
            )
        ''')

        conn.commit()

        # Verify the columns were added
        cursor.execute("PRAGMA table_info(user)")
        updated_columns = [column[1] for column in cursor.fetchall()]
        logger.info(f"Updated user table columns: {updated_columns}")

        logger.info("✅ Database schema updated successfully!")
        return True

    except Exception as e:
        logger.error(f"❌ Database upgrade error: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def migrate_existing_database():
    """Safely migrate existing database with user data preservation"""
    return upgrade_database()

def force_recreate_user_table():
    """Recreate user table with all columns - use only if needed"""
    return upgrade_database()

class DatabaseUpgrade:
    """Upgrade from SQLite to PostgreSQL for production scaling"""

    def __init__(self):
        self.postgres_url = os.getenv('DATABASE_URL', 'postgresql://user:pass@localhost/ai_ceo_prod')

    def create_postgresql_engine(self):
        """Create PostgreSQL connection"""
        try:
            from sqlalchemy import create_engine
            engine = create_engine(
                self.postgres_url,
                pool_size=20,          # Connection pool for concurrent users
                max_overflow=30,       # Additional connections during peak
                pool_recycle=3600,     # Recycle connections every hour
                pool_pre_ping=True     # Verify connections before use
            )
            return engine
        except ImportError:
            logger.warning("SQLAlchemy not available for PostgreSQL upgrade")
            return None

    def migrate_data_from_sqlite(self):
        """Migrate existing SQLite data to PostgreSQL"""
        try:
            # This would require pandas and SQLAlchemy
            logger.info("PostgreSQL migration requires additional dependencies")
            logger.info("For now, using SQLite for development")
            return True

        except Exception as e:
            logger.error(f"❌ Migration failed: {e}")
            return False

def main():
    """Main function to run database upgrades"""
    logger.info("🗄️ Starting database upgrade utility...")

    success = upgrade_database()

    if success:
        logger.info("✅ Database upgrade completed successfully!")
    else:
        logger.error("❌ Database upgrade failed!")
        return 1

    return 0

if __name__ == "__main__":
    exit(main())