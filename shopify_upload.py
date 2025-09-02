
import requests
import os
from config import SHOPIFY_PRODUCTS_URL, SHOPIFY_ACCESS_TOKEN, SHOPIFY_DOMAIN

def upload_to_shopify(product):
    """Upload product to Shopify store - main upload function"""
    print(f"🛒 Uploading to Shopify: {product.get('title', product.get('name', 'Unknown Product'))}")
    
    try:
        headers = {
            "Content-Type": "application/json",
            "X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN
        }

        # Format product data for Shopify
        shopify_data = {
            "product": {
                "title": product.get('title', product.get('name', 'AI Generated Product')),
                "body_html": f"<p>{product.get('description', 'Digital product created by AI CEO')}</p>",
                "vendor": "AI CEO",
                "product_type": "Digital Product",
                "status": "active",
                "variants": [
                    {
                        "price": str(product.get("price", 19.99)),
                        "inventory_policy": "continue",
                        "fulfillment_service": "manual",
                        "requires_shipping": False
                    }
                ],
                "tags": ["AI", "Digital", "Auto-Generated"]
            }
        }

        response = requests.post(SHOPIFY_PRODUCTS_URL, headers=headers, json=shopify_data, timeout=15)

        if response.status_code == 201:
            result = response.json()
            product_data = result["product"]

            print(f"✅ Shopify upload SUCCESS: {product_data['title']}")
            return {
                "success": True,
                "platform": "shopify",
                "url": f"https://{SHOPIFY_DOMAIN}/products/{product_data['handle']}",
                "product_id": product_data["id"],
                "admin_url": f"https://{SHOPIFY_DOMAIN}/admin/products/{product_data['id']}"
            }
        else:
            print(f"❌ Shopify upload failed: {response.status_code}")
            return {
                "success": False,
                "platform": "shopify",
                "error": f"Shopify API error: {response.status_code} - {response.text[:200]}"
            }

    except Exception as e:
        print(f"❌ Shopify upload exception: {str(e)}")
        return {
            "success": False,
            "platform": "shopify",
            "error": f"Shopify upload error: {str(e)}"
        }
