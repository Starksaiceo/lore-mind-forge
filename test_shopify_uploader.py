
#!/usr/bin/env python3

from shopify_uploader import upload_product_to_shopify, check_shopify_connection

def test_shopify_uploader():
    """Test the Shopify uploader with a sample product"""
    print("🧪 Testing Shopify Uploader")
    print("=" * 40)
    
    # First check connection
    print("\n1. Testing Shopify connection...")
    if not check_shopify_connection():
        print("❌ Cannot connect to Shopify. Please check your credentials.")
        return False
    
    # Test product data
    product_data = {
        "title": "AI CEO Test Product - Instagram Marketing Masterclass",
        "description": "<p>Learn how to grow and monetize an Instagram brand with proven AI-powered strategies.</p><p>✅ Step-by-step video training<br>✅ Downloadable templates and tools<br>✅ 30-day money-back guarantee</p>",
        "price": "29.00",
        "type": "Course",
        "tags": ["Instagram", "Marketing", "Masterclass", "AI CEO"],
        "sku": "ai-ceo-insta-master"
    }
    
    print(f"\n2. Uploading test product: {product_data['title']}")
    result = upload_product_to_shopify(product_data)
    
    if result.get("success"):
        print(f"✅ Upload successful!")
        print(f"   Product ID: {result['product_id']}")
        print(f"   Admin URL: {result['admin_url']}")
        print(f"   Store URL: {result['storefront_url']}")
        return True
    else:
        print(f"❌ Upload failed: {result.get('error')}")
        return False

if __name__ == "__main__":
    test_shopify_uploader()
