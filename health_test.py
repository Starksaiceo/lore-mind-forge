
#!/usr/bin/env python3
import sys
import os

def test_imports():
    """Test critical imports"""
    print("🔍 Testing imports...")
    
    critical_modules = [
        'flask', 'streamlit', 'sqlalchemy', 'werkzeug'
    ]
    
    for module in critical_modules:
        try:
            __import__(module)
            print(f"  ✅ {module}")
        except ImportError as e:
            print(f"  ❌ {module}: {e}")
            return False
    
    return True

def test_config():
    """Test configuration"""
    print("\n🔧 Testing configuration...")
    
    try:
        from config import CONFIG
        print("  ✅ Config loaded")
        
        # Check key sections
        if 'shopify' in CONFIG:
            print("  ✅ Shopify config found")
        if 'stripe' in CONFIG:
            print("  ✅ Stripe config found")
            
        return True
    except Exception as e:
        print(f"  ❌ Config error: {e}")
        return False

def test_database():
    """Test database connection"""
    print("\n💾 Testing database...")
    
    try:
        import sqlite3
        conn = sqlite3.connect('ai_ceo_saas.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        conn.close()
        
        print(f"  ✅ Database connected ({len(tables)} tables)")
        return True
    except Exception as e:
        print(f"  ❌ Database error: {e}")
        return False

def main():
    """Run health checks"""
    print("🏥 AI CEO Health Check")
    print("=" * 30)
    
    tests = [
        test_imports,
        test_config, 
        test_database
    ]
    
    all_passed = True
    for test in tests:
        if not test():
            all_passed = False
    
    print("\n" + "=" * 30)
    if all_passed:
        print("✅ All health checks passed!")
        print("🚀 Ready to run the application")
    else:
        print("❌ Some health checks failed")
        print("🔧 Check the errors above")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
