
#!/usr/bin/env python3

import os
from agent_logic import generate_product, upload_to_shopify

def test_shopify_integration():
    """Test the complete Shopify integration"""
    print("🧪 Testing Shopify Integration")
    print("=" * 40)
    
    # Check credentials
    required_vars = [
        "SHOPIFY_DOMAIN", 
        "SHOPIFY_API_ACCESS_TOKEN",
        "SHOPIFY_API_KEY"
    ]
    
    missing = []
    for var in required_vars:
        if not os.getenv(var):
            missing.append(var)
    
    if missing:
        print(f"❌ Missing environment variables: {missing}")
        print("Please add these to your Replit Secrets first")
        return False
    
    # Test product generation
    print("\n1. Testing product generation...")
    test_product = {
        "title": "AI CEO Test Product",
        "description": "This is a test product created by the AI CEO system to verify Shopify integration.",
        "price": 19.99,
        "category": "digital_guide"
    }
    print(f"✅ Generated test product: {test_product['title']}")
    
    # Test Shopify upload
    print("\n2. Testing Shopify upload...")
    result = upload_to_shopify(test_product)
    
    if result.get("success"):
        print(f"✅ Successfully uploaded to Shopify!")
        print(f"   Product ID: {result.get('product_id')}")
        print(f"   Admin URL: {result.get('admin_url')}")
        print(f"   Store URL: {result.get('storefront_url')}")
        return True
    else:
        print(f"❌ Shopify upload failed: {result.get('error')}")
        return False

if __name__ == "__main__":
    test_shopify_integration()
