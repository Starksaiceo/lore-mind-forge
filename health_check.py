
#!/usr/bin/env python3
"""Health check for AI CEO app"""

import sys
import importlib

required_modules = [
    'streamlit',
    'requests', 
    'pandas',
    'numpy',
    'matplotlib'
]

def check_module(module_name):
    try:
        importlib.import_module(module_name)
        print(f"✅ {module_name}")
        return True
    except ImportError:
        print(f"❌ {module_name} - MISSING")
        return False

def main():
    print("🔧 AI CEO App Health Check")
    print("=" * 40)
    
    all_good = True
    for module in required_modules:
        if not check_module(module):
            all_good = False
    
    print("=" * 40)
    if all_good:
        print("✅ All dependencies OK")
        print("🚀 App should load successfully")
    else:
        print("❌ Missing dependencies detected")
        print("💡 Run: pip install -r requirements.txt")
    
    return all_good

if __name__ == "__main__":
    main()
