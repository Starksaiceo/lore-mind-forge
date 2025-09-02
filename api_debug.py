
import os
import requests
import stripe
from config import get_shopify_config, get_stripe_config

def test_shopify_connection():
    """Test Shopify API connection"""
    try:
        config = get_shopify_config()
        access_token = config.get("admin_api_token") or config.get("access_token")
        
        if not access_token:
            return {"status": "❌", "error": "No access token configured"}
        
        headers = {"X-Shopify-Access-Token": access_token}
        url = f"https://{config['store_url']}/admin/api/{config['api_version']}/shop.json"
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            shop_data = response.json()["shop"]
            return {
                "status": "✅", 
                "message": f"Connected to {shop_data['name']}",
                "store": shop_data["name"]
            }
        else:
            return {
                "status": "❌", 
                "error": f"HTTP {response.status_code}: {response.text[:100]}"
            }
            
    except Exception as e:
        return {"status": "❌", "error": str(e)}

def test_stripe_connection():
    """Test Stripe API connection"""
    try:
        config = get_stripe_config()
        secret_key = config.get("secret_key")
        
        if not secret_key:
            return {"status": "❌", "error": "No secret key configured"}
        
        stripe.api_key = secret_key
        
        # Test with a simple API call
        account = stripe.Account.retrieve()
        
        return {
            "status": "✅",
            "message": f"Connected to Stripe account",
            "account_id": account.id
        }
        
    except Exception as e:
        return {"status": "❌", "error": str(e)}

if __name__ == "__main__":
    print("🔍 Testing API Connections...")
    
    print("\n🛒 Shopify Test:")
    shopify_result = test_shopify_connection()
    print(f"{shopify_result['status']} {shopify_result.get('message', shopify_result.get('error'))}")
    
    print("\n💳 Stripe Test:")
    stripe_result = test_stripe_connection()
    print(f"{stripe_result['status']} {stripe_result.get('message', stripe_result.get('error'))}")
