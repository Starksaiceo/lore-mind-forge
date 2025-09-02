
import requests
import json
from config import SHOPIFY_DOMAIN, SHOPIFY_ACCESS_TOKEN

def upload_product_to_shopify(product_data):
    """Upload a product to Shopify store"""
    url = f"https://{SHOPIFY_DOMAIN}/admin/api/2024-04/products.json"
    
    headers = {
        "Content-Type": "application/json",
        "X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN
    }

    payload = {
        "product": {
            "title": product_data["title"],
            "body_html": product_data["description"],
            "vendor": "AI CEO",
            "product_type": product_data.get("type", "Digital"),
            "tags": product_data.get("tags", ["AI", "Digital", "Auto"]),
            "status": "active",
            "variants": [
                {
                    "price": product_data["price"],
                    "sku": product_data.get("sku", "ai-ceo-product"),
                    "inventory_policy": "continue",
                    "fulfillment_service": "manual"
                }
            ]
        }
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=15)

        if response.status_code == 201:
            product = response.json()["product"]
            print(f"✅ Uploaded to Shopify: {product['title']} → Product ID: {product['id']}")
            return {
                "success": True,
                "product_id": product['id'],
                "admin_url": f"https://{SHOPIFY_DOMAIN}/admin/products/{product['id']}",
                "storefront_url": f"https://{SHOPIFY_DOMAIN}/products/{product['handle']}"
            }
        else:
            print(f"❌ Shopify upload failed: {response.status_code}")
            print(response.text)
            return {
                "success": False,
                "error": f"HTTP {response.status_code}: {response.text}"
            }
    
    except Exception as e:
        print(f"❌ Shopify upload exception: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

def check_shopify_connection():
    """Test Shopify connection"""
    try:
        url = f"https://{SHOPIFY_DOMAIN}/admin/api/2024-04/shop.json"
        headers = {
            "Content-Type": "application/json",
            "X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            shop_data = response.json()["shop"]
            print(f"✅ Connected to Shopify: {shop_data['name']}")
            return True
        else:
            print(f"❌ Shopify connection failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Shopify connection error: {e}")
        return False
