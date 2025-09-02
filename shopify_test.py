
#!/usr/bin/env python3
"""
Shopify Integration Test Suite
Tests connection, product creation, theme editing, and order management
"""

import os
import sys
from store_designer import ShopifyStoreDesigner
from marketplace_uploader import ShopifyUploader

def test_shopify_integration():
    """Complete test of Shopify integration"""
    print("🧪 Shopify Integration Test Suite")
    print("=" * 50)
    
    # Initialize components
    uploader = ShopifyUploader()
    designer = ShopifyStoreDesigner()
    
    # Test 1: Connection Check
    print("\n🔍 Test 1: Connection Check")
    connection = uploader.check_connection()
    if connection.get('success'):
        print(f"✅ Connected to: {connection.get('shop_name')}")
        print(f"🌐 Domain: {connection.get('domain')}")
    else:
        print(f"❌ Connection failed: {connection.get('error')}")
        return False
    
    # Test 2: Create Test Product
    print("\n🔍 Test 2: Product Creation")
    test_product = {
        "name": "AI CEO Test Product",
        "description": "<h2>Test Product by AI CEO</h2><p>This is a test product created by the AI CEO system to verify Shopify integration.</p><ul><li>Instant download</li><li>AI-generated content</li><li>Premium quality</li></ul>",
        "price": 9.99,
        "category": "Digital Product",
        "tags": "test,ai-ceo,digital,instant-download"
    }
    
    product_result = uploader.create_product(test_product)
    if product_result.get('success'):
        print(f"✅ Product created: {product_result.get('title')}")
        print(f"🔗 URL: {product_result.get('url')}")
        product_id = product_result.get('product_id')
    else:
        print(f"❌ Product creation failed: {product_result.get('error')}")
        product_id = None
    
    # Test 3: Theme Customization
    print("\n🔍 Test 3: Theme Customization")
    theme_result = designer.customize_store_colors("#ff6b35", "#ff8c42")
    if theme_result.get('success'):
        print("✅ Theme colors customized")
    else:
        print(f"❌ Theme customization failed: {theme_result.get('error')}")
    
    # Test 4: Get Products
    print("\n🔍 Test 4: Product Listing")
    products_result = uploader.get_products(10)
    if products_result.get('success'):
        count = products_result.get('count', 0)
        print(f"✅ Retrieved {count} products")
    else:
        print(f"❌ Failed to get products: {products_result.get('error')}")
    
    # Test 5: Get Orders
    print("\n🔍 Test 5: Order Listing")
    orders_result = uploader.get_orders(10)
    if orders_result.get('success'):
        count = orders_result.get('count', 0)
        print(f"✅ Retrieved {count} orders")
    else:
        print(f"❌ Failed to get orders: {orders_result.get('error')}")
    
    # Test 6: Complete Store Design
    print("\n🔍 Test 6: Complete Store Design")
    design_result = designer.design_complete_store("AI Digital Products")
    if design_result.get('success'):
        print("✅ Store design completed")
        for result in design_result.get('results', []):
            print(f"  {result}")
        print(f"🛍️ Store URL: {design_result.get('store_url')}")
    else:
        print(f"❌ Store design failed: {design_result.get('error')}")
    
    print("\n" + "=" * 50)
    print("🎯 Test Summary:")
    print(f"✅ Connection: {'OK' if connection.get('success') else 'FAILED'}")
    print(f"✅ Product Creation: {'OK' if product_result.get('success') else 'FAILED'}")
    print(f"✅ Theme Customization: {'OK' if theme_result.get('success') else 'FAILED'}")
    print(f"✅ Product Listing: {'OK' if products_result.get('success') else 'FAILED'}")
    print(f"✅ Order Management: {'OK' if orders_result.get('success') else 'FAILED'}")
    print(f"✅ Store Design: {'OK' if design_result.get('success') else 'FAILED'}")
    
    return True

if __name__ == "__main__":
    test_shopify_integration()
