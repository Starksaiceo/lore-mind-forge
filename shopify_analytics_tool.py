import os
import shopify
from typing import Dict, List
from datetime import datetime, timedelta
from langchain.agents import Tool

# Load credentials from environment
API_KEY = os.getenv("SHOPIFY_API_KEY")
PASSWORD = os.getenv("SHOPIFY_API_ACCESS_TOKEN")  # Using existing token
SHOP_NAME = os.getenv("SHOPIFY_DOMAIN", "ai-ceo-store-agent.myshopify.com").replace('.myshopify.com', '')

def init_shopify_session():
    """Initialize Shopify session with existing credentials"""
    try:
        if not PASSWORD:
            raise ValueError("SHOPIFY_API_ACCESS_TOKEN not set")

        # Use the session approach for private apps
        session = shopify.Session(
            f"{SHOP_NAME}.myshopify.com", 
            "2023-10", 
            PASSWORD
        )
        shopify.ShopifyResource.activate_session(session)
        return True
    except Exception as e:
        print(f"Shopify session error: {e}")
        return False

def fetch_shopify_analytics(days: int = 7) -> Dict:
    """
    Returns comprehensive Shopify analytics for the last `days` days:
    orders, revenue, products, customers, and performance metrics.
    """
    try:
        if not init_shopify_session():
            return {"error": "Failed to connect to Shopify"}

        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        # Format dates for Shopify API
        start_str = start_date.strftime('%Y-%m-%dT%H:%M:%S-00:00')

        # Fetch orders
        orders = shopify.Order.find(
            status='any',
            created_at_min=start_str,
            limit=250
        )

        # Calculate metrics
        total_orders = len(orders)
        total_revenue = sum(float(order.total_price) for order in orders if order.total_price)
        avg_order_value = (total_revenue / total_orders) if total_orders > 0 else 0.0

        # Get top products from orders
        product_sales = {}
        for order in orders:
            for item in order.line_items:
                product_name = item.title
                quantity = int(item.quantity)
                product_sales[product_name] = product_sales.get(product_name, 0) + quantity

        top_products = sorted(product_sales.items(), key=lambda x: x[1], reverse=True)[:5]

        # Get store info
        shop = shopify.Shop.current()

        return {
            "success": True,
            "period_days": days,
            "store_name": shop.name,
            "store_url": f"https://{shop.domain}",
            "total_orders": total_orders,
            "total_revenue": round(total_revenue, 2),
            "avg_order_value": round(avg_order_value, 2),
            "currency": shop.currency,
            "top_products": [{"name": name, "units_sold": qty} for name, qty in top_products],
            "daily_average_revenue": round(total_revenue / days, 2) if days > 0 else 0,
            "conversion_insights": {
                "orders_per_day": round(total_orders / days, 1) if days > 0 else 0,
                "revenue_trend": "positive" if total_revenue > 0 else "neutral"
            }
        }

    except Exception as e:
        return {"success": False, "error": f"Shopify analytics failed: {str(e)}"}

def fetch_shopify_products(limit: int = 10) -> Dict:
    """Fetch current product catalog"""
    try:
        if not init_shopify_session():
            return {"error": "Failed to connect to Shopify"}

        products = shopify.Product.find(limit=limit)

        product_list = []
        for product in products:
            variants = product.variants
            prices = [float(v.price) for v in variants if v.price]

            product_list.append({
                "id": product.id,
                "title": product.title,
                "handle": product.handle,
                "product_type": product.product_type,
                "vendor": product.vendor,
                "status": product.status,
                "price_range": {
                    "min": min(prices) if prices else 0,
                    "max": max(prices) if prices else 0
                },
                "variant_count": len(variants),
                "created_at": str(product.created_at)
            })

        return {
            "success": True,
            "products_found": len(product_list),
            "products": product_list
        }

    except Exception as e:
        return {"success": False, "error": f"Product fetch failed: {str(e)}"}

def get_shopify_store_health() -> Dict:
    """Get overall store health metrics"""
    try:
        if not init_shopify_session():
            return {"error": "Failed to connect to Shopify"}

        shop = shopify.Shop.current()

        # Get basic store info
        store_health = {
            "success": True,
            "store_name": shop.name,
            "domain": shop.domain,
            "currency": shop.currency,
            "timezone": shop.timezone,
            "plan_name": shop.plan_name,
            "created_at": str(shop.created_at),
            "updated_at": str(shop.updated_at)
        }

        # Get recent metrics
        recent_analytics = fetch_shopify_analytics(30)  # Last 30 days
        if recent_analytics.get("success"):
            store_health.update({
                "monthly_revenue": recent_analytics["total_revenue"],
                "monthly_orders": recent_analytics["total_orders"],
                "avg_order_value": recent_analytics["avg_order_value"]
            })

        return store_health

    except Exception as e:
        return {"success": False, "error": f"Store health check failed: {str(e)}"}

def shopify_analytics_tool(query: str) -> str:
    """
    Shopify Analytics Tool - Get real store performance data
    Input: 'store_id' or 'summary' for overview
    """
    try:
        if not query:
            return "Please specify 'store_id' or 'summary' to get Shopify analytics"

        # Try to get real Shopify data
        try:
            import shopify
            import os

            shopify_api_key = os.getenv("SHOPIFY_API_KEY")
            shopify_api_secret = os.getenv("SHOPIFY_API_SECRET") 
            shopify_access_token = os.getenv("SHOPIFY_API_ACCESS_TOKEN")
            shopify_shop_url = os.getenv("SHOPIFY_SHOP_URL")

            if not all([shopify_api_key, shopify_api_secret, shopify_access_token, shopify_shop_url]):
                return "❌ Shopify credentials not configured. Please set SHOPIFY_API_KEY, SHOPIFY_API_SECRET, SHOPIFY_API_ACCESS_TOKEN, and SHOPIFY_SHOP_URL"

            # Initialize Shopify session
            api_version = os.getenv("SHOPIFY_API_VERSION", "2024-01")
            shopify.Session.setup(api_key=shopify_api_key, secret=shopify_api_secret)
            session = shopify.Session(shopify_shop_url, api_version, shopify_access_token)
            shopify.ShopifyResource.activate_session(session)

            # Get real shop data
            shop = shopify.Shop.current()
            orders = shopify.Order.find(limit=250, status='any')
            products = shopify.Product.find(limit=10)

            # Calculate real metrics
            total_sales = sum(float(order.total_price) for order in orders if order.total_price)
            orders_count = len(orders)
            avg_order_value = total_sales / orders_count if orders_count > 0 else 0

            print(f"💰 Real Shopify Data - Sales: ${total_sales:.2f}, Orders: {orders_count}")

            if total_sales == 0 and orders_count == 0:
                return f"""
📊 Shopify Store Analytics:

🏪 Store: {shop.name}
💰 Total Sales: $0.00
📦 Orders: 0
💵 AOV: $0.00
📊 Status: Store connected but no sales yet

🔧 Recommendation: Start creating products and driving traffic to generate sales data.
"""

            return f"""
📊 Shopify Store Analytics:

🏪 Store: {shop.name}
💰 Total Sales: ${total_sales:,.2f}
📦 Orders: {orders_count}
💵 AOV: ${avg_order_value:.2f}
🏪 Domain: {shop.domain}
💱 Currency: {shop.currency}

📦 Products: {len(products)} active
📊 All data above is REAL from your Shopify store
"""

        except ImportError:
            return "❌ Shopify Python SDK not installed. Run: pip install ShopifyAPI"
        except Exception as shopify_error:
            print(f"❌ Shopify API Error: {shopify_error}")
            return f"❌ Shopify connection failed: {str(shopify_error)}. Please check your credentials."

    except Exception as e:
        return f"❌ Error fetching Shopify analytics: {str(e)}"

# LangChain Tools
shopify_analytics_tool = Tool(
    name="ShopifyAnalytics",
    func=fetch_shopify_analytics,
    description="Get Shopify sales analytics (orders, revenue, AOV, top products) for the past N days. Usage: ShopifyAnalytics(7)"
)

shopify_products_tool = Tool(
    name="ShopifyProducts",
    func=fetch_shopify_products,
    description="Fetch current Shopify product catalog with prices and details. Usage: ShopifyProducts(10)"
)

shopify_health_tool = Tool(
    name="ShopifyStoreHealth",
    func=get_shopify_store_health,
    description="Get overall Shopify store health metrics and basic info"
)