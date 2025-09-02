
import os
from flask import Flask
from models import db, User, AgentSession, BusinessMetrics
import sqlite3

def init_streamlit_db():
    """Initialize database for Streamlit context"""
    try:
        # Create SQLite database directly for Streamlit
        db_path = 'ai_ceo_saas.db'
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username VARCHAR(80) UNIQUE NOT NULL,
                email VARCHAR(120) UNIQUE NOT NULL,
                password_hash VARCHAR(255),
                stripe_customer_id VARCHAR(255),
                subscription_status VARCHAR(50) DEFAULT 'trial',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create agent_memory table
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
        
        # Create ai_events table
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
        
        # Create business_metrics table
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
        
        # Insert demo users if they don't exist
        cursor.execute('SELECT COUNT(*) FROM user')
        user_count = cursor.fetchone()[0]
        
        if user_count == 0:
            demo_users = [
                (1, 'demo_user_1', 'user1@example.com', 'hashed_password', 'cus_demo1', 'active'),
                (2, 'demo_user_2', 'user2@example.com', 'hashed_password', 'cus_demo2', 'trial'),
                (3, 'demo_user_3', 'user3@example.com', 'hashed_password', 'cus_demo3', 'active'),
                (4, 'demo_user_4', 'user4@example.com', 'hashed_password', 'cus_demo4', 'trial'),
                (5, 'demo_user_5', 'user5@example.com', 'hashed_password', 'cus_demo5', 'active')
            ]
            
            cursor.executemany(
                'INSERT OR IGNORE INTO user (id, username, email, password_hash, stripe_customer_id, subscription_status) VALUES (?, ?, ?, ?, ?, ?)',
                demo_users
            )
        
        conn.commit()
        conn.close()
        
        print("✅ Streamlit database initialized successfully")
        return True
        
    except Exception as e:
        print(f"❌ Database initialization error: {e}")
        return False

def create_all():
    """Flask database initialization - for compatibility"""
    try:
        # Create Flask app context for models
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ai_ceo_saas.db'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
        with app.app_context():
            db.init_app(app)
            db.create_all()
            print("✅ Flask database tables created")
            
    except Exception as e:
        print(f"❌ Flask database error: {e}")
        # Fall back to direct SQLite
        init_streamlit_db()

if __name__ == "__main__":
    init_streamlit_db()
