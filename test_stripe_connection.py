
#!/usr/bin/env python3
"""Test Stripe connection using Replit Secrets"""

import os
import stripe

def test_stripe_connection():
    """Test Stripe API connection"""
    # Get API key from Replit Secrets
    api_key = os.getenv("STRIPE_SECRET_KEY")
    
    if not api_key:
        print("❌ STRIPE_SECRET_KEY not found in Replit Secrets")
        print("💡 Please add your Stripe secret key to Replit Secrets:")
        print("   1. Click Tools > Secrets")
        print("   2. Add key: STRIPE_SECRET_KEY")
        print("   3. Add your sk_live_... or sk_test_... key as value")
        return False
    
    # Test the connection
    stripe.api_key = api_key
    
    try:
        # Try to retrieve account info
        account = stripe.Account.retrieve()
        print(f"✅ Stripe connected successfully!")
        print(f"   Account ID: {account.id}")
        print(f"   Business Name: {account.business_profile.name if account.business_profile else 'Not set'}")
        print(f"   Country: {account.country}")
        return True
        
    except stripe.error.AuthenticationError as e:
        print(f"❌ Stripe authentication failed: {e}")
        print("💡 Check that your STRIPE_SECRET_KEY is correct")
        return False
        
    except Exception as e:
        print(f"❌ Stripe connection failed: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Testing Stripe connection...")
    test_stripe_connection()
