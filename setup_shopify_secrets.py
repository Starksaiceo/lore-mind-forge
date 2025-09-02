
import os

def setup_shopify_secrets():
    """
    Script to help set up Shopify secrets in Replit
    Run this after adding the secrets to your Replit environment
    """
    
    # The secrets you need to add to Replit Secrets:
    required_secrets = {
        "SHOPIFY_DOMAIN": "ai-ceo-store-agent.myshopify.com",
        "SHOPIFY_API_KEY": "26c2f02e41c3f8782d6894914dbc9a8d", 
        "SHOPIFY_API_SECRET": "addda1735767ac406939bcc51530fb6f",
        "SHOPIFY_API_ACCESS_TOKEN": "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",
        "SHOPIFY_STOREFRONT_TOKEN": "af239833381ffb1732ddf7b859602073"
    }
    
    print("🔧 Shopify Secrets Setup")
    print("=" * 50)
    
    # Check which secrets are already set
    missing_secrets = []
    configured_secrets = []
    
    for key, value in required_secrets.items():
        if os.getenv(key):
            configured_secrets.append(key)
            print(f"✅ {key}: Configured")
        else:
            missing_secrets.append(key)
            print(f"❌ {key}: Missing")
    
    if missing_secrets:
        print("\n🚨 MISSING SECRETS:")
        print("Please add these to your Replit Secrets:")
        for key in missing_secrets:
            print(f"Key: {key}")
            print(f"Value: {required_secrets[key]}")
            print()
    
    if len(configured_secrets) == len(required_secrets):
        print("\n✅ All Shopify secrets are configured!")
        return test_shopify_connection()
    else:
        print(f"\n⚠️  {len(missing_secrets)} secrets still need to be added")
        return False

def test_shopify_connection():
    """Test if Shopify connection works with current secrets"""
    try:
        import shopify
        
        shop_url = os.getenv("SHOPIFY_DOMAIN")
        api_version = "2024-01"
        access_token = os.getenv("SHOPIFY_API_ACCESS_TOKEN")
        
        if not access_token or not shop_url:
            print("❌ Missing required credentials")
            return False
        
        session = shopify.Session(shop_url, api_version, access_token)
        shopify.ShopifyResource.activate_session(session)
        
        # Test connection by fetching shop info
        shop = shopify.Shop.current()
        
        print(f"🎉 SUCCESS! Connected to Shopify store:")
        print(f"   Store Name: {shop.name}")
        print(f"   Domain: {shop.domain}")
        print(f"   Currency: {shop.currency}")
        print(f"   Plan: {shop.plan_name}")
        
        return True
        
    except Exception as e:
        print(f"❌ Shopify connection failed: {e}")
        return False

if __name__ == "__main__":
    setup_shopify_secrets()
