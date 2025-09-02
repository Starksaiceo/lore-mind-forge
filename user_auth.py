
import streamlit as st
import sqlite3
import hashlib
import os
from datetime import datetime

class UserAuth:
    def __init__(self):
        self.db_path = "users.db"
        self.init_db()
    
    def init_db(self):
        """Initialize user database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                subscription_tier TEXT DEFAULT 'free',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                api_calls_used INTEGER DEFAULT 0,
                monthly_limit INTEGER DEFAULT 10
            )
        ''')
        conn.commit()
        conn.close()
    
    def hash_password(self, password: str) -> str:
        """Hash password with salt"""
        salt = os.urandom(32)
        pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        return salt + pwd_hash
    
    def verify_password(self, stored_password: bytes, provided_password: str) -> bool:
        """Verify password"""
        salt = stored_password[:32]
        stored_hash = stored_password[32:]
        pwd_hash = hashlib.pbkdf2_hmac('sha256', provided_password.encode('utf-8'), salt, 100000)
        return pwd_hash == stored_hash
    
    def register_user(self, email: str, password: str) -> bool:
        """Register new user"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            password_hash = self.hash_password(password)
            cursor.execute(
                "INSERT INTO users (email, password_hash) VALUES (?, ?)",
                (email, password_hash)
            )
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def login_user(self, email: str, password: str) -> dict:
        """Login user and return user data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        conn.close()
        
        if user and self.verify_password(user[2], password):
            return {
                "id": user[0],
                "email": user[1],
                "subscription_tier": user[3],
                "api_calls_used": user[5],
                "monthly_limit": user[6]
            }
        return None
    
    def check_api_limit(self, user_id: int) -> bool:
        """Check if user has API calls remaining"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT api_calls_used, monthly_limit FROM users WHERE id = ?", (user_id,))
        user_data = cursor.fetchone()
        conn.close()
        
        if user_data:
            return user_data[0] < user_data[1]
        return False
    
    def increment_api_usage(self, user_id: int):
        """Increment user's API usage"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET api_calls_used = api_calls_used + 1 WHERE id = ?",
            (user_id,)
        )
        conn.commit()
        conn.close()

# Streamlit authentication functions
def show_login_page():
    """Show login/signup page"""
    st.title("🤖 AI CEO - Login")
    
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    auth = UserAuth()
    
    with tab1:
        st.subheader("Login to AI CEO")
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login"):
            user = auth.login_user(email, password)
            if user:
                st.session_state.user = user
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid email or password")
    
    with tab2:
        st.subheader("Sign Up for AI CEO")
        email = st.text_input("Email", key="signup_email")
        password = st.text_input("Password", type="password", key="signup_password")
        confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password")
        
        if st.button("Sign Up"):
            if password != confirm_password:
                st.error("Passwords don't match")
            elif len(password) < 6:
                st.error("Password must be at least 6 characters")
            elif auth.register_user(email, password):
                st.success("Registration successful! Please login.")
            else:
                st.error("Email already exists")

def require_auth():
    """Require user authentication"""
    if 'user' not in st.session_state:
        show_login_page()
        return False
    return True

def show_subscription_info():
    """Show user subscription information"""
    if 'user' in st.session_state:
        user = st.session_state.user
        
        with st.sidebar:
            st.write(f"👤 **{user['email']}**")
            st.write(f"📊 **Plan:** {user['subscription_tier'].title()}")
            st.write(f"🔧 **API Calls:** {user['api_calls_used']}/{user['monthly_limit']}")
            
            progress = user['api_calls_used'] / user['monthly_limit']
            st.progress(progress)
            
            if user['subscription_tier'] == 'free':
                st.info("🚀 Upgrade to Pro for unlimited API calls!")
                if st.button("Upgrade to Pro ($29/mo)"):
                    st.info("Stripe integration coming soon!")
            
            if st.button("Logout"):
                del st.session_state.user
                st.rerun()
