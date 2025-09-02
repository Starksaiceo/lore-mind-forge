
#!/usr/bin/env python3
"""Test API connections for Stripe and Gumroad"""

import os
import stripe
import requests
from config import STRIPE_SECRET_KEY, GUMROAD_ACCESS_TOKEN

def test_stripe():
    """Test Stripe connection"""
    try:
        stripe.api_key = STRIPE_SECRET_KEY
        account = stripe.Account.retrieve()
        print(f"✅ Stripe connected - Account ID: {account.id}")
        return True
    except Exception as e:
        print(f"❌ Stripe error: {e}")
        return False

def test_shopify():
    """Test Shopify connection"""
    try:
        from marketplace_uploader import check_shopify_connection
        result = check_shopify_connection()
        if result.get("connected"):
            print(f"✅ Shopify connected - Store: {result.get('store_name', 'Unknown')}")
            return True
        else:
            print(f"❌ Shopify error: {result.get('error', 'Connection failed')}")
            return False
    except Exception as e:
        print(f"❌ Shopify error: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Testing API connections...")
    stripe_ok = test_stripe()
    shopify_ok = test_shopify()
    
    if stripe_ok and shopify_ok:
        print("🎯 All APIs connected successfully!")
    else:
        print("⚠️ Some API connections failed. Check your credentials")r keys in Secrets.")
