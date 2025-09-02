
import os
import requests
import shopify
from langchain.agents import Tool

# ——— AMAZON PRODUCTS TOOL ———
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_HOST = "amazon-product-reviews.p.rapidapi.com"

def fetch_amazon_products(keyword: str, max_results: int = 5) -> list:
    """Search Amazon products via RapidAPI"""
    if not RAPIDAPI_KEY:
        return [{"error": "RAPIDAPI_KEY not set"}]
    
    url = f"https://{RAPIDAPI_HOST}/product/amazon/search"
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": RAPIDAPI_HOST
    }
    params = {"keywords": keyword}
    
    try:
        res = requests.get(url, headers=headers, params=params, timeout=10)
        res.raise_for_status()
        items = res.json().get("results", [])[:max_results]
        return [
            {
                "title": p.get("title"),
                "price": p.get("price", {}).get("value"),
                "currency": p.get("price", {}).get("currency"),
                "url": p.get("link")
            }
            for p in items
        ]
    except Exception as e:
        return [{"error": f"Amazon search failed: {str(e)}"}]

# ——— SHOPIFY STORE TOOLS ———
def init_shopify():
    """Initialize Shopify session"""
    shop_url = os.getenv("SHOPIFY_DOMAIN", "ai-ceo-store-agent.myshopify.com")
    api_version = os.getenv("SHOPIFY_API_VERSION", "2023-10")
    access_token = os.getenv("SHOPIFY_API_ACCESS_TOKEN")
    
    if not access_token:
        raise ValueError("SHOPIFY_API_ACCESS_TOKEN not set")
    
    session = shopify.Session(shop_url, api_version, access_token)
    shopify.ShopifyResource.activate_session(session)

def list_store_products(limit: int = 10) -> list:
    """List products from the Shopify store"""
    try:
        init_shopify()
        products = shopify.Product.find(limit=limit)
        return [p.to_dict() for p in products]
    except Exception as e:
        return [{"error": f"Failed to list products: {str(e)}"}]

def create_shopify_product(title: str, body_html: str, vendor: str, product_type: str, price: float) -> dict:
    """Create a new Shopify product"""
    try:
        init_shopify()
        product = shopify.Product()
        product.title = title
        product.body_html = body_html
        product.vendor = vendor
        product.product_type = product_type
        product.variants = [shopify.Variant({"price": price})]
        
        if product.save():
            return product.to_dict()
        else:
            return {"error": "Failed to save product", "errors": product.errors.full_messages()}
    except Exception as e:
        return {"error": f"Failed to create product: {str(e)}"}

# ——— LANGCHAIN TOOLS ———
amazon_products_tool = Tool(
    name="fetch_amazon_products",
    func=fetch_amazon_products,
    description="Search Amazon via RapidAPI. Returns top products for a keyword."
)

list_products_tool = Tool(
    name="list_store_products",
    func=list_store_products,
    description="List products from the Shopify store."
)

create_product_tool = Tool(
    name="create_shopify_product",
    func=create_shopify_product,
    description="Create a new Shopify product with title, HTML description, vendor, type, and price."
)
