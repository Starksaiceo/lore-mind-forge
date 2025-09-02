
#!/usr/bin/env python3
"""
Setup script to verify and guide Replit Secrets configuration
"""

import os
from config import validate_api_keys

def check_secrets_setup():
    """Check current secrets configuration and provide guidance"""
    
    print("🔐 REPLIT SECRETS SETUP GUIDE")
    print("=" * 60)
    
    # Required secrets with their values (for reference)
    required_secrets = {
        "OPENROUTER_API_KEY": "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",
        "STRIPE_PUBLISHABLE_KEY": "pk_live_51RrfM5G0HoeSSRcXeBHOLDJUazsHVUyCZoNSDz9LK5ozLioIFdS5WdmlUtrugEAwFS1hOKbqSXs3apD8l7oQu2Qt00QUYJrhqv",
        "STRIPE_SECRET_KEY": "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",
        "META_APP_ID": "678014266826429",
        "META_APP_SECRET": "396cf1b06652dfbc58b3597373f96",
        "THREADS_APP_ID": "738198879208049",
        "GUMROAD_APP_ID": "dzHaaTPkij_5SrHuTWy0zGlsEraxC4NLYXJ9LOTmTos",
        "GUMROAD_APP_SECRET": "ZM8ho_sCw3PA6imjeyL6aMiXep9EHBjcJUPyWNxZ-xc",
        "GUMROAD_ACCESS_TOKEN": "tMYPg6y1nZPo1weCwd7Ohj4_Myv54oRFMRxCBDxFlhE",
        "XANO_BASE_URL": "https://x8ki-letl-twmt.n7.xano.io/api:8fyoFbLh",
        "XANO_PROFIT_ENDPOINT": "https://x8ki-letl-twmt.n7.xano.io/api:8fyoFbLh/profit"
    }
    
    # Check current environment
    configured_secrets = []
    missing_secrets = []
    
    for key, expected_value in required_secrets.items():
        current_value = os.getenv(key)
        if current_value:
            configured_secrets.append(key)
            # Mask the value for security
            masked_value = current_value[:8] + "..." + current_value[-8:] if len(current_value) > 16 else "***"
            print(f"✅ {key}: {masked_value}")
        else:
            missing_secrets.append(key)
            print(f"❌ {key}: NOT SET")
    
    print("\n" + "=" * 60)
    print(f"SUMMARY: {len(configured_secrets)} configured, {len(missing_secrets)} missing")
    
    if missing_secrets:
        print("\n🔧 TO FIX MISSING SECRETS:")
        print("1. Go to the 'Secrets' tab in your Replit (🔒 icon in sidebar)")
        print("2. Add each missing secret with these values:")
        print()
        
        for key in missing_secrets:
            value = required_secrets[key]
            print(f"   Key: {key}")
            print(f"   Value: {value}")
            print()
    
    # Validate API keys using config
    print("🧪 TESTING API KEY LOADING...")
    validation = validate_api_keys()
    
    if validation["all_required_present"]:
        print("✅ All required API keys loaded successfully!")
    else:
        print("❌ Some required keys failed to load:", validation["missing_required"])
    
    print("\n🚀 NEXT STEPS:")
    print("1. Set missing secrets in Replit Secrets tab")
    print("2. Restart your Repl (stop and run again)")
    print("3. Run: python api_validation.py")
    print("4. Test the AI CEO app!")
    
    return len(missing_secrets) == 0

if __name__ == "__main__":
    success = check_secrets_setup()
    if success:
        print("\n🎉 All secrets configured! Your AI CEO is ready!")
    else:
        print("\n⚠️  Please configure missing secrets and restart.")
