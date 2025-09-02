
import requests

# 🔑 Your Shopify Store Info (already filled in)
SHOPIFY_STORE_URL = "ai-ceo-store-agent.myshopify.com"
SHOPIFY_ADMIN_ACCESS_TOKEN = "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"

# Headers for authentication
headers = {
    "Content-Type": "application/json",
    "X-Shopify-Access-Token": SHOPIFY_ADMIN_ACCESS_TOKEN
}

# 1. Test connection - fetch products
print("🔍 Testing Shopify connection...")
products_url = f"https://{SHOPIFY_STORE_URL}/admin/api/2025-01/products.json"
response = requests.get(products_url, headers=headers)

if response.status_code == 200:
    print("✅ Connection successful!")
    products = response.json()
    print(f"📦 Found {len(products.get('products', []))} existing products")
else:
    print("❌ Connection failed:", response.status_code, response.text)

# 2. Create a test product
print("\n🛒 Creating a test product...")
new_product = {
    "product": {
        "title": "AI CEO Test Product",
        "body_html": "<strong>Created automatically by the AI CEO Agent</strong>",
        "vendor": "AI CEO",
        "product_type": "Digital",
        "variants": [
            {"price": "19.99"}
        ]
    }
}

response = requests.post(products_url, headers=headers, json=new_product)

if response.status_code == 201:
    product_data = response.json()
    print("✅ Test product created successfully!")
    print("🆔 Product ID:", product_data["product"]["id"])
    print("📦 Title:", product_data["product"]["title"])
    print("💲 Price:", product_data["product"]["variants"][0]["price"])
    print("🌐 Store URL:", f"https://{SHOPIFY_STORE_URL}/products/{product_data['product']['handle']}")
else:
    print("❌ Failed to create product:", response.status_code, response.text)

# 3. Test store design functionality
print("\n🎨 Testing store design capabilities...")
themes_url = f"https://{SHOPIFY_STORE_URL}/admin/api/2025-01/themes.json"
response = requests.get(themes_url, headers=headers)

if response.status_code == 200:
    themes = response.json()
    print(f"✅ Found {len(themes.get('themes', []))} themes")
    for theme in themes.get('themes', []):
        if theme.get('role') == 'main':
            print(f"🎨 Main theme: {theme.get('name')} (ID: {theme.get('id')})")
else:
    print("❌ Failed to fetch themes:", response.status_code, response.text)

print("\n🎯 Shopify integration test complete!")
