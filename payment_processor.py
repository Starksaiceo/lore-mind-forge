import requests
import os
from typing import Dict, List, Optional
from config import STRIPE_SECRET_KEY, SHOPIFY_PRODUCTS_URL, SHOPIFY_ACCESS_TOKEN
import stripe
from datetime import datetime, timedelta
from config import get_stripe_config

def log_business_event(event_type, data):
    """Log business events"""
    print(f"📊 {event_type}: {data}")

# Original calculate_ad_budget removed and replaced by new implementation below.

class StripeProcessor:
    def __init__(self):
        self.config = get_stripe_config()
        stripe.api_key = self.config.get("secret_key")

    def is_configured(self):
        """Check if Stripe is properly configured"""
        return bool(self.config.get("secret_key"))

    def create_product(self, product_data):
        """Create a Stripe product"""
        try:
            product = stripe.Product.create(
                name=product_data["title"],
                description=product_data["description"],
                type="service"
            )

            price = stripe.Price.create(
                product=product.id,
                unit_amount=int(product_data["price"] * 100),
                currency="usd"
            )

            return {
                "success": True,
                "product_id": product.id,
                "price_id": price.id,
                "url": f"https://dashboard.stripe.com/products/{product.id}"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_recent_charges(self, limit=100):
        """Get recent Stripe charges for revenue calculation"""
        try:
            charges = stripe.Charge.list(limit=limit)
            return {
                "success": True,
                "charges": charges.data,
                "total_revenue": sum(charge.amount / 100 for charge in charges.data if charge.paid)
            }
        except Exception as e:
            print(f"❌ Stripe API error: {e}")
            return {"success": False, "error": str(e), "charges": [], "total_revenue": 0}

def calculate_ad_budget():
    """Calculate available ad budget based on real Stripe revenue"""
    try:
        processor = StripeProcessor()
        charges_result = processor.get_recent_charges()

        if charges_result["success"]:
            total_revenue = charges_result["total_revenue"]
            # Use 25% of revenue for ads
            ad_budget = total_revenue * 0.25
            return max(ad_budget, 0.0)
        else:
            return 0.0
    except Exception as e:
        print(f"❌ Ad budget calculation error: {e}")
        return 0.0

def get_real_stripe_revenue():
    """Get real revenue from Stripe API"""
    try:
        processor = StripeProcessor()
        charges_result = processor.get_recent_charges()

        if charges_result["success"]:
            return charges_result["total_revenue"]
        else:
            return 0.0
    except Exception as e:
        print(f"❌ Stripe revenue fetch error: {e}")
        return 0.0


class ShopifyProcessor:
    """Handle Shopify products and sales - REPLACES GumroadProcessor"""

    @staticmethod
    def create_product(name: str, price: float, description: str = "") -> Dict:
        """Create a Shopify product"""
        try:
            headers = {
                "Content-Type": "application/json",
                "X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN
            }

            data = {
                "product": {
                    "title": name,
                    "body_html": f"<p>{description}</p>",
                    "vendor": "AI CEO",
                    "product_type": "Digital Product",
                    "variants": [
                        {
                            "price": str(price)
                        }
                    ]
                }
            }

            response = requests.post(SHOPIFY_PRODUCTS_URL, headers=headers, json=data, timeout=15)

            if response.status_code == 201:
                result = response.json()
                product_data = result["product"]

                log_business_event("shopify_product_created", {
                    "product_id": product_data["id"],
                    "title": product_data["title"],
                    "price": price
                })

                return {
                    "success": True,
                    "product_id": product_data["id"],
                    "url": f"https://ai-ceo-store-agent.myshopify.com/products/{product_data['handle']}",
                    "admin_url": f"https://ai-ceo-store-agent.myshopify.com/admin/products/{product_data['id']}"
                }
            else:
                return {"success": False, "error": response.text}

        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def get_sales(limit: int = 10) -> List[Dict]:
        """Get recent Shopify orders"""
        try:
            from config import SHOPIFY_BASE_URL

            headers = {
                "Content-Type": "application/json",
                "X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN
            }

            response = requests.get(
                f"{SHOPIFY_BASE_URL}/orders.json",
                headers=headers,
                params={"limit": limit, "status": "any"},
                timeout=15
            )

            if response.status_code == 200:
                data = response.json()
                orders = data.get("orders", [])
                return [{"amount": float(order.get("total_price", 0)), "id": order.get("id")} for order in orders]

            return []

        except Exception as e:
            print(f"Shopify sales error: {e}")
            return []

def create_stripe_payment(product_data):
    """Create Stripe payment - wrapper function for compatibility"""
    try:
        processor = StripeProcessor()
        return processor.create_product(product_data)
    except Exception as e:
        return {"success": False, "error": str(e)}

# All marketplace operations now use Shopify only