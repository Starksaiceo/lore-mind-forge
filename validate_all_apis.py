
#!/usr/bin/env python3
"""Validate all API connections"""

import os
import stripe
import requests
from dotenv import load_dotenv

load_dotenv()

def test_openrouter():
    """Test OpenRouter API"""
    try:
        from langchain_openai import ChatOpenAI
        
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            return {"status": "❌", "message": "OpenRouter API key not found"}
            
        llm = ChatOpenAI(
            model="anthropic/claude-3-opus",
            temperature=0,
            openai_api_key=api_key,
            openai_api_base="https://openrouter.ai/api/v1"
        )
        
        response = llm.invoke("Say 'OpenRouter working with Claude 3 Opus'")
        return {"status": "✅", "message": f"OpenRouter/Claude working: {response.content[:50]}..."}
        
    except Exception as e:
        return {"status": "❌", "message": f"OpenRouter error: {str(e)}"}

def test_stripe():
    """Test Stripe API"""
    try:
        api_key = os.getenv("STRIPE_SECRET_KEY")
        if not api_key:
            return {"status": "❌", "message": "Stripe secret key not found"}
            
        stripe.api_key = api_key
        account = stripe.Account.retrieve()
        return {"status": "✅", "message": f"Stripe connected: {account.id}"}
        
    except Exception as e:
        return {"status": "❌", "message": f"Stripe error: {str(e)}"}

def test_shopify_only():
    """Test Shopify API only - Gumroad removed"""
    try:
        from marketplace_uploader import check_shopify_connection
        result = check_shopify_connection()
        
        if result.get("connected"):
            return {"status": "✅", "message": f"Shopify connected: {result.get('store_name', 'Store')}"}
        else:
            return {"status": "❌", "message": f"Shopify error: {result.get('error', 'Connection failed')}"}
            
    except Exception as e:
        return {"status": "❌", "message": f"Shopify test failed: {str(e)}"}ad error: {str(e)}"}

def test_meta():
    """Test Meta/Facebook API"""
    try:
        app_id = os.getenv("META_APP_ID")
        app_secret = os.getenv("META_APP_SECRET")
        
        if not app_id or not app_secret:
            return {"status": "❌", "message": "Meta credentials not complete"}
            
        # Test app token generation
        url = f"https://graph.facebook.com/oauth/access_token"
        params = {
            "client_id": app_id,
            "client_secret": app_secret,
            "grant_type": "client_credentials"
        }
        
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            return {"status": "✅", "message": "Meta app credentials valid"}
        else:
            return {"status": "❌", "message": f"Meta error: {response.status_code}"}
            
    except Exception as e:
        return {"status": "❌", "message": f"Meta error: {str(e)}"}

def test_shopify():
    """Test Shopify API"""
    try:
        access_token = os.getenv("SHOPIFY_API_ACCESS_TOKEN")
        domain = os.getenv("SHOPIFY_STORE_DOMAIN")
        
        if not access_token or not domain:
            return {"status": "❌", "message": "Shopify credentials not found"}
            
        url = f"https://{domain}/admin/api/2024-01/shop.json"
        headers = {"X-Shopify-Access-Token": access_token}
        
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            shop_data = response.json()
            shop_name = shop_data.get('shop', {}).get('name', 'Unknown')
            return {"status": "✅", "message": f"Shopify connected: {shop_name}"}
        else:
            return {"status": "❌", "message": f"Shopify error: {response.status_code}"}
            
    except Exception as e:
        return {"status": "❌", "message": f"Shopify error: {str(e)}"}

def main():
    """Run all API tests"""
    print("🔧 COMPREHENSIVE API VALIDATION")
    print("=" * 50)
    
    tests = [
        ("OpenRouter (Claude 3 Opus)", test_openrouter),
        ("Stripe", test_stripe),
        ("Gumroad", test_gumroad),
        ("Meta/Facebook", test_meta),
        ("Shopify", test_shopify)
    ]
    
    results = []
    working_count = 0
    
    for name, test_func in tests:
        print(f"\nTesting {name}...")
        result = test_func()
        results.append((name, result))
        print(f"{result['status']} {name}: {result['message']}")
        if result['status'] == "✅":
            working_count += 1
    
    print("\n" + "=" * 50)
    print("📊 SUMMARY:")
    for name, result in results:
        print(f"{result['status']} {name}")
    
    print(f"\n✅ {working_count}/{len(tests)} APIs working")
    if working_count < len(tests):
        print("⚠️  Some APIs need attention. Check the errors above.")
    else:
        print("🎉 All APIs are working perfectly!")

if __name__ == "__main__":
    main()
