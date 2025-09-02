import requests
import os
import json
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class ShopifyUploader:
    """Shopify product uploader using Admin API"""

    def __init__(self):
        # Use credentials from config system
        from config import SHOPIFY_STORE_URL, SHOPIFY_ACCESS_TOKEN
        self.store_url = SHOPIFY_STORE_URL
        self.admin_token = SHOPIFY_ACCESS_TOKEN
        self.base_url = f"https://{self.store_url}/admin/api/2025-01"
        self.headers = {
            "X-Shopify-Access-Token": self.admin_token,
            "Content-Type": "application/json"
        }

    def create_product(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a product using Shopify Admin API"""
        try:
            # Format product data for Shopify
            shopify_product = {
                "product": {
                    "title": product_data.get('name', product_data.get('title', 'Untitled Product')),
                    "body_html": product_data.get('description', 'AI-generated digital product'),
                    "vendor": "AI CEO Store",
                    "product_type": product_data.get('category', 'Digital Product'),
                    "status": "active",
                    "published": True,
                    "tags": product_data.get('tags', 'ai-generated,digital,instant-download'),
                    "variants": [{
                        "price": str(product_data.get('price', 29.99)),
                        "inventory_management": None,
                        "inventory_tracking": False,
                        "requires_shipping": False,
                        "weight": 0,
                        "weight_unit": "kg"
                    }]
                }
            }

            # Add image if provided
            if product_data.get('image_url'):
                shopify_product["product"]["images"] = [{
                    "src": product_data['image_url'],
                    "alt": product_data.get('name', 'Product Image')
                }]

            response = requests.post(
                f"{self.base_url}/products.json",
                headers=self.headers,
                json=shopify_product
            )

            if response.status_code == 201:
                product = response.json().get('product', {})
                logger.info(f"✅ Product created: {product.get('title')} (ID: {product.get('id')})")
                return {
                    "success": True,
                    "product_id": product.get('id'),
                    "title": product.get('title'),
                    "handle": product.get('handle'),
                    "url": f"https://{self.store_url}/products/{product.get('handle')}",
                    "admin_url": f"https://{self.store_url}/admin/products/{product.get('id')}"
                }
            else:
                error_msg = f"Failed to create product: {response.status_code}"
                logger.error(f"{error_msg} - {response.text}")
                return {"success": False, "error": error_msg, "details": response.text}

        except Exception as e:
            error_msg = f"Error creating product: {str(e)}"
            logger.error(error_msg)
            return {"success": False, "error": error_msg}

    def update_product(self, product_id: int, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing product"""
        try:
            shopify_updates = {"product": updates}

            response = requests.put(
                f"{self.base_url}/products/{product_id}.json",
                headers=self.headers,
                json=shopify_updates
            )

            if response.status_code == 200:
                return {"success": True, "message": "Product updated successfully"}
            else:
                return {"success": False, "error": f"Update failed: {response.status_code}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_products(self, limit: int = 50) -> Dict[str, Any]:
        """Get products from the store"""
        try:
            response = requests.get(
                f"{self.base_url}/products.json?limit={limit}",
                headers=self.headers
            )

            if response.status_code == 200:
                products = response.json().get('products', [])
                return {"success": True, "products": products, "count": len(products)}
            else:
                return {"success": False, "error": f"Failed to get products: {response.status_code}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_orders(self, limit: int = 50) -> Dict[str, Any]:
        """Get orders from the store"""
        try:
            response = requests.get(
                f"{self.base_url}/orders.json?limit={limit}&status=any",
                headers=self.headers
            )

            if response.status_code == 200:
                orders = response.json().get('orders', [])
                return {"success": True, "orders": orders, "count": len(orders)}
            else:
                return {"success": False, "error": f"Failed to get orders: {response.status_code}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def check_connection(self) -> Dict[str, Any]:
        """Test connection to Shopify Admin API"""
        try:
            response = requests.get(f"{self.base_url}/shop.json", headers=self.headers)
            if response.status_code == 200:
                shop = response.json().get('shop', {})
                return {
                    "success": True,
                    "status": "connected",
                    "shop_name": shop.get('name'),
                    "domain": shop.get('domain'),
                    "message": "Shopify Admin API connected successfully"
                }
            else:
                return {
                    "success": False,
                    "status": "failed",
                    "error": f"Connection failed: {response.status_code}"
                }
        except Exception as e:
            return {
                "success": False,
                "status": "failed", 
                "error": f"Connection error: {str(e)}"
            }

# Global uploader instance
uploader = ShopifyUploader()

def upload_to_shopify(product):
    """Upload product to Shopify using Admin API"""
    return uploader.create_product(product)

def check_shopify_connection():
    """Check Shopify connection"""
    return uploader.check_connection()

def get_shopify_products(limit=50):
    """Get products from Shopify"""
    return uploader.get_products(limit)

def get_shopify_orders(limit=50):
    """Get orders from Shopify"""
    return uploader.get_orders(limit)

def upload_product_to_shopify(product_data):
    """Legacy function name - redirect to new implementation"""
    return upload_to_shopify(product_data)

# Keep Gumroad placeholder for backward compatibility
def upload_to_gumroad(product):
    """Gumroad upload placeholder (disabled)"""
    logger.info(f"Gumroad upload skipped for: {product.get('name', 'Unknown')}")
    return {"status": "disabled", "platform": "gumroad", "message": "Gumroad integration disabled"}