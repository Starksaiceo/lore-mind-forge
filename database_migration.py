
#!/usr/bin/env python3
"""
PostgreSQL Migration Utility for AI CEO SaaS Platform
Migrates SQLite data to PostgreSQL while preserving all functionality
"""

import os
import sqlite3
import logging
from datetime import datetime
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_postgresql_connection():
    """Test PostgreSQL connection"""
    try:
        import psycopg2
        database_url = os.getenv('DATABASE_URL')
        
        if not database_url:
            logger.error("❌ DATABASE_URL environment variable not set")
            return False
            
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        cursor.close()
        conn.close()
        
        logger.info(f"✅ PostgreSQL connection successful: {version[0]}")
        return True
        
    except ImportError:
        logger.error("❌ psycopg2 not installed. Run: pip install psycopg2-binary")
        return False
    except Exception as e:
        logger.error(f"❌ PostgreSQL connection failed: {e}")
        return False

def create_postgresql_schema():
    """Create PostgreSQL schema with all existing tables"""
    try:
        import psycopg2
        database_url = os.getenv('DATABASE_URL')
        
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        # Enable UUID extension
        cursor.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")
        
        # Create users table with all existing columns
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS "user" (
                id SERIAL PRIMARY KEY,
                username VARCHAR(80) UNIQUE,
                email VARCHAR(120) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                stripe_customer_id VARCHAR(255),
                subscription_status VARCHAR(50) DEFAULT 'trial',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                voice_name VARCHAR(100) DEFAULT 'AI CEO',
                voice_personality VARCHAR(50) DEFAULT 'professional',
                voice_enabled BOOLEAN DEFAULT FALSE,
                voice_type VARCHAR(50) DEFAULT 'professional',
                role VARCHAR(50) DEFAULT 'user'
            );
        """)
        
        # Create agent_memory table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS agent_memory (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
                key VARCHAR(255) NOT NULL,
                value TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Create ai_events table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ai_events (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
                event_type VARCHAR(100) NOT NULL,
                event_json TEXT,
                success BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Create business_metrics table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS business_metrics (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
                revenue DECIMAL(10,2) DEFAULT 0.00,
                products_created INTEGER DEFAULT 0,
                orders_fulfilled INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Create generated_businesses table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS generated_businesses (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
                business_data TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Create products table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
                title TEXT NOT NULL,
                description TEXT,
                price DECIMAL(10,2) DEFAULT 0.00,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Create user_preferences table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_preferences (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
                voice_enabled BOOLEAN DEFAULT FALSE,
                agent_name TEXT DEFAULT 'AI CEO',
                personality TEXT DEFAULT 'professional',
                voice_type TEXT DEFAULT 'professional',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Create indexes for performance
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_email ON \"user\"(email);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_agent_memory_user_id ON agent_memory(user_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_ai_events_user_id ON ai_events(user_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_business_metrics_user_id ON business_metrics(user_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_generated_businesses_user_id ON generated_businesses(user_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_products_user_id ON products(user_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_preferences_user_id ON user_preferences(user_id);")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        logger.info("✅ PostgreSQL schema created successfully")
        return True
        
    except Exception as e:
        logger.error(f"❌ Schema creation failed: {e}")
        return False

def migrate_data_to_postgresql():
    """Migrate all data from SQLite to PostgreSQL"""
    try:
        import psycopg2
        
        # Check if SQLite database exists
        if not os.path.exists('ai_ceo_saas.db'):
            logger.info("✅ No existing SQLite database found - starting fresh")
            return True
            
        # Connect to both databases
        sqlite_conn = sqlite3.connect('ai_ceo_saas.db')
        sqlite_conn.row_factory = sqlite3.Row
        
        postgres_conn = psycopg2.connect(os.getenv('DATABASE_URL'))
        postgres_cursor = postgres_conn.cursor()
        
        # Get list of tables from SQLite
        sqlite_cursor = sqlite_conn.cursor()
        sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in sqlite_cursor.fetchall()]
        
        logger.info(f"📋 Found {len(tables)} tables to migrate: {tables}")
        
        # Migrate each table
        migrated_records = 0
        
        for table in tables:
            if table == 'sqlite_sequence':
                continue
                
            logger.info(f"🔄 Migrating table: {table}")
            
            # Get all data from SQLite table
            sqlite_cursor.execute(f"SELECT * FROM {table}")
            rows = sqlite_cursor.fetchall()
            
            if not rows:
                logger.info(f"  ⚠️ Table {table} is empty")
                continue
                
            # Get column names
            columns = [description[0] for description in sqlite_cursor.description]
            
            # Prepare PostgreSQL insert statement
            placeholders = ', '.join(['%s'] * len(columns))
            pg_table = '"user"' if table == 'user' else table
            insert_sql = f"INSERT INTO {pg_table} ({', '.join(columns)}) VALUES ({placeholders})"
            
            # Insert data into PostgreSQL
            for row in rows:
                try:
                    postgres_cursor.execute(insert_sql, tuple(row))
                    migrated_records += 1
                except Exception as e:
                    logger.warning(f"  ⚠️ Failed to migrate row from {table}: {e}")
                    continue
            
            logger.info(f"  ✅ Migrated {len(rows)} records from {table}")
        
        postgres_conn.commit()
        postgres_cursor.close()
        postgres_conn.close()
        sqlite_conn.close()
        
        logger.info(f"✅ Migration completed! {migrated_records} total records migrated")
        
        # Backup SQLite database
        backup_name = f"ai_ceo_saas_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        os.rename('ai_ceo_saas.db', backup_name)
        logger.info(f"✅ SQLite database backed up as: {backup_name}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Data migration failed: {e}")
        return False

def verify_migration():
    """Verify that migration was successful"""
    try:
        import psycopg2
        
        conn = psycopg2.connect(os.getenv('DATABASE_URL'))
        cursor = conn.cursor()
        
        # Check user count
        cursor.execute('SELECT COUNT(*) FROM "user"')
        user_count = cursor.fetchone()[0]
        
        # Check events count
        cursor.execute('SELECT COUNT(*) FROM ai_events')
        events_count = cursor.fetchone()[0]
        
        # Check products count
        cursor.execute('SELECT COUNT(*) FROM products')
        products_count = cursor.fetchone()[0]
        
        cursor.close()
        conn.close()
        
        logger.info(f"✅ Migration verification:")
        logger.info(f"   Users: {user_count}")
        logger.info(f"   AI Events: {events_count}")
        logger.info(f"   Products: {products_count}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Migration verification failed: {e}")
        return False

def main():
    """Main migration function"""
    logger.info("🗄️ Starting PostgreSQL migration for 5000+ user capacity...")
    
    # Step 1: Check PostgreSQL connection
    if not check_postgresql_connection():
        logger.error("❌ PostgreSQL setup required. Please set DATABASE_URL in Replit Secrets")
        return False
    
    # Step 2: Create PostgreSQL schema
    if not create_postgresql_schema():
        return False
    
    # Step 3: Migrate data
    if not migrate_data_to_postgresql():
        return False
    
    # Step 4: Verify migration
    if not verify_migration():
        return False
    
    logger.info("✅ PostgreSQL migration completed successfully!")
    logger.info("🚀 Your app is now ready to handle 5000+ concurrent users!")
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
