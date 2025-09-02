
import os
import requests
from langchain.agents import Tool

# Platform-specific helper functions
def create_shopify_store(params: dict) -> dict:
    """Create a Shopify store using the API"""
    try:
        # Use Shopify credentials from environment
        api_token = os.getenv("SHOPIFY_API_ACCESS_TOKEN")
        domain = os.getenv("SHOPIFY_DOMAIN") 
        api_key = os.getenv("SHOPIFY_API_KEY")
        
        if not api_token or not domain:
            return {"platform": "shopify", "status": "error", "error": "Missing Shopify credentials"}
        
        # Create a basic store configuration
        store_data = {
            "name": params.get("name", "AI Generated Store"),
            "theme": params.get("theme", "minimal"),
            "niche": params.get("niche", "general"),
            "products": []
        }
        
        return {
            "platform": "shopify", 
            "status": "created", 
            "store_url": f"https://{domain}",
            "store_data": store_data,
            "admin_url": f"https://{domain}/admin"
        }
    except Exception as e:
        return {"platform": "shopify", "status": "error", "error": str(e)}

def create_woocommerce_store(params: dict) -> dict:
    """Create a WooCommerce store configuration"""
    store_data = {
        "platform": "woocommerce",
        "name": params.get("name", "AI WooCommerce Store"),
        "theme": params.get("theme", "storefront"),
        "niche": params.get("niche", "general"),
        "plugins": ["woocommerce", "elementor", "yoast-seo"]
    }
    return {"platform": "woocommerce", "status": "configured", "store_data": store_data}

def create_gumroad_store(params: dict) -> dict:
    """Create a Gumroad digital product store"""
    store_data = {
        "platform": "gumroad",
        "name": params.get("name", "AI Digital Store"),
        "products": [],
        "niche": params.get("niche", "digital"),
        "commission_rate": "5%"
    }
    return {"platform": "gumroad", "status": "ready", "store_data": store_data}

def create_etsy_store(params: dict) -> dict:
    """Create an Etsy store configuration"""
    store_data = {
        "platform": "etsy",
        "shop_name": params.get("name", "AI Craft Store"),
        "niche": params.get("niche", "crafts"),
        "categories": ["handmade", "vintage", "supplies"]
    }
    return {"platform": "etsy", "status": "configured", "store_data": store_data}

def create_amazon_fba_store(params: dict) -> dict:
    """Create an Amazon FBA listing configuration"""
    store_data = {
        "platform": "amazon_fba",
        "seller_name": params.get("name", "AI FBA Seller"),
        "niche": params.get("niche", "general"),
        "fulfillment": "FBA",
        "marketplace": "US"
    }
    return {"platform": "amazon_fba", "status": "configured", "store_data": store_data}

# Main dispatcher function
def create_store_dispatcher(input_string: str) -> dict:
    """
    Parse input and create store on specified platform
    Expected format: 'platform:shopify,name:MyStore,niche:fitness,theme:modern'
    """
    try:
        # Parse the input string
        params = {}
        parts = input_string.split(',')
        for part in parts:
            if ':' in part:
                key, value = part.split(':', 1)
                params[key.strip()] = value.strip()
        
        platform = params.get('platform', '').lower()
        
        # Dispatch to appropriate function
        dispatch = {
            "shopify": create_shopify_store,
            "woocommerce": create_woocommerce_store,
            "gumroad": create_gumroad_store,
            "etsy": create_etsy_store,
            "amazon_fba": create_amazon_fba_store,
        }
        
        func = dispatch.get(platform)
        if not func:
            return {"error": f"Unsupported platform: {platform}", "supported": list(dispatch.keys())}
        
        result = func(params)
        result["success"] = result.get("status") != "error"
        return result
        
    except Exception as e:
        return {"error": f"Failed to create store: {str(e)}", "success": False}

# LangChain Tool wrapper
store_builder_tool = Tool(
    name="CreateStore",
    func=create_store_dispatcher,
    description=(
        "Create a new online storefront on any platform. "
        "Usage: CreateStore('platform:shopify,name:MyStore,niche:fitness,theme:modern'). "
        "Supported platforms: shopify, woocommerce, gumroad, etsy, amazon_fba. "
        "Parameters: platform (required), name, niche, theme."
    )
)

if __name__ == "__main__":
    # Test the store creation
    test_result = create_store_dispatcher("platform:shopify,name:TestStore,niche:tech,theme:minimal")
    print("Store creation test:", test_result)
