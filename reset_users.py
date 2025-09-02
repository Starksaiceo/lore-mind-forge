
import os
import sqlite3
from werkzeug.security import generate_password_hash

def reset_users():
    """Reset and recreate users in database"""
    db_path = 'ai_ceo_saas.db'
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Delete existing users
        cursor.execute('DELETE FROM user')
        
        # Create admin user
        admin_password_hash = generate_password_hash('test123')
        cursor.execute('''
            INSERT INTO user (
                email, password_hash, role, username, 
                voice_name, voice_personality, voice_enabled, voice_type,
                stripe_customer_id, subscription_status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            'admin@example.com',
            admin_password_hash,
            'admin',
            'admin',
            'AI CEO',
            'professional',
            1,
            'professional',
            None,
            'trial'
        ))
        
        # Create Tyler user
        tyler_password_hash = generate_password_hash('test123')
        cursor.execute('''
            INSERT INTO user (
                email, password_hash, role, username,
                voice_name, voice_personality, voice_enabled, voice_type,
                stripe_customer_id, subscription_status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            'tylerstarks45@gmail.com',
            tyler_password_hash,
            'user',
            'tyler',
            'AI CEO',
            'professional',
            1,
            'professional',
            None,
            'trial'
        ))
        
        conn.commit()
        
        # Verify users were created
        cursor.execute('SELECT id, email, role FROM user')
        users = cursor.fetchall()
        
        print("✅ Users reset successfully!")
        for user in users:
            print(f"   ID: {user[0]}, Email: {user[1]}, Role: {user[2]}")
            
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error resetting users: {e}")
        return False

if __name__ == "__main__":
    reset_users()
