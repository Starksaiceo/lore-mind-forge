
import os
import requests
import json
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)

class ShopifyStoreDesigner:
    """
    Shopify Store Designer using Admin API
    Handles theme customization, product management, and store layout design
    """
    
    def __init__(self):
        # Use credentials from config system
        from config import SHOPIFY_STORE_URL, SHOPIFY_ACCESS_TOKEN, SHOPIFY_API_KEY, SHOPIFY_API_SECRET
        self.store_url = SHOPIFY_STORE_URL
        self.admin_token = SHOPIFY_ACCESS_TOKEN
        self.api_key = SHOPIFY_API_KEY
        self.api_secret = SHOPIFY_API_SECRET
        
        self.base_url = f"https://{self.store_url}/admin/api/2025-01"
        self.headers = {
            "X-Shopify-Access-Token": self.admin_token,
            "Content-Type": "application/json"
        }
        
    def check_connection(self) -> Dict[str, Any]:
        """Test Shopify Admin API connection"""
        try:
            response = requests.get(f"{self.base_url}/shop.json", headers=self.headers)
            if response.status_code == 200:
                shop_data = response.json()
                return {
                    "success": True,
                    "shop_name": shop_data.get('shop', {}).get('name'),
                    "domain": shop_data.get('shop', {}).get('domain'),
                    "status": "Connected to Shopify Admin API"
                }
            else:
                return {"success": False, "error": f"Connection failed: {response.status_code}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_themes(self) -> List[Dict[str, Any]]:
        """Get all themes from the store"""
        try:
            response = requests.get(f"{self.base_url}/themes.json", headers=self.headers)
            if response.status_code == 200:
                themes = response.json().get('themes', [])
                logger.info(f"✅ Found {len(themes)} themes")
                return themes
            else:
                logger.error(f"Failed to get themes: {response.status_code}")
                return []
        except Exception as e:
            logger.error(f"Error getting themes: {e}")
            return []
    
    def get_main_theme(self) -> Optional[Dict[str, Any]]:
        """Get the main/published theme"""
        themes = self.get_themes()
        for theme in themes:
            if theme.get('role') == 'main':
                return theme
        return themes[0] if themes else None
    
    def update_theme_asset(self, theme_id: int, asset_key: str, value: str) -> Dict[str, Any]:
        """Update a theme asset (CSS, Liquid, etc.)"""
        try:
            asset_data = {
                "asset": {
                    "key": asset_key,
                    "value": value
                }
            }
            
            response = requests.put(
                f"{self.base_url}/themes/{theme_id}/assets.json",
                headers=self.headers,
                json=asset_data
            )
            
            if response.status_code == 200:
                return {"success": True, "message": f"Updated {asset_key}"}
            else:
                return {"success": False, "error": f"Failed to update asset: {response.status_code}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def customize_store_colors(self, primary_color: str = "#2563eb", secondary_color: str = "#1d4ed8") -> Dict[str, Any]:
        """Customize store color scheme"""
        theme = self.get_main_theme()
        if not theme:
            return {"success": False, "error": "No theme found"}
        
        # Custom CSS for color customization
        custom_css = f"""
/* AI CEO Store Custom Colors */
:root {{
    --primary-color: {primary_color};
    --secondary-color: {secondary_color};
    --accent-color: #10b981;
}}

.btn-primary, .product-form__cart-submit {{
    background-color: var(--primary-color) !important;
    border-color: var(--primary-color) !important;
}}

.btn-primary:hover {{
    background-color: var(--secondary-color) !important;
    border-color: var(--secondary-color) !important;
}}

.site-header {{
    background-color: var(--primary-color) !important;
}}

.product-single__price {{
    color: var(--accent-color) !important;
    font-weight: bold;
}}

.collection-grid-item__title a {{
    color: var(--secondary-color) !important;
}}

.footer {{
    background-color: #f8fafc;
    border-top: 1px solid #e2e8f0;
}}
"""
        
        result = self.update_theme_asset(theme['id'], "assets/ai-ceo-custom.css", custom_css)
        if result['success']:
            # Also update the theme.liquid to include our custom CSS
            self.inject_custom_css_link(theme['id'])
        
        return result
    
    def inject_custom_css_link(self, theme_id: int) -> Dict[str, Any]:
        """Inject custom CSS link into theme.liquid"""
        try:
            # Get current theme.liquid
            response = requests.get(
                f"{self.base_url}/themes/{theme_id}/assets.json?asset[key]=layout/theme.liquid",
                headers=self.headers
            )
            
            if response.status_code == 200:
                current_liquid = response.json().get('asset', {}).get('value', '')
                
                # Add custom CSS link before </head>
                css_link = '\n  {{ "ai-ceo-custom.css" | asset_url | stylesheet_tag }}'
                if css_link not in current_liquid and '</head>' in current_liquid:
                    updated_liquid = current_liquid.replace('</head>', f'{css_link}\n</head>')
                    
                    return self.update_theme_asset(theme_id, "layout/theme.liquid", updated_liquid)
            
            return {"success": False, "error": "Could not update theme.liquid"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def create_custom_homepage(self, business_type: str = "Digital Products") -> Dict[str, Any]:
        """Create a custom homepage with AI CEO branding"""
        homepage_content = f"""
<div class="ai-ceo-hero" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 80px 20px; text-align: center;">
    <div style="max-width: 800px; margin: 0 auto;">
        <h1 style="font-size: 3em; margin-bottom: 20px;">AI CEO Store</h1>
        <p style="font-size: 1.2em; margin-bottom: 30px;">Powered by Artificial Intelligence • {business_type}</p>
        <a href="/collections/all" style="background: #10b981; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; font-weight: bold;">Shop Now</a>
    </div>
</div>

<div style="padding: 60px 20px; max-width: 1200px; margin: 0 auto;">
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 40px;">
        <div style="text-align: center;">
            <h3>🤖 AI-Powered Products</h3>
            <p>Every product is created and optimized using advanced artificial intelligence.</p>
        </div>
        <div style="text-align: center;">
            <h3>⚡ Instant Delivery</h3>
            <p>Digital products delivered immediately after purchase.</p>
        </div>
        <div style="text-align: center;">
            <h3>🎯 Personalized Experience</h3>
            <p>AI algorithms ensure you get the most relevant products for your needs.</p>
        </div>
    </div>
</div>
"""
        
        try:
            page_data = {
                "page": {
                    "title": "AI CEO Homepage",
                    "body_html": homepage_content,
                    "handle": "ai-ceo-homepage",
                    "published": True
                }
            }
            
            response = requests.post(
                f"{self.base_url}/pages.json",
                headers=self.headers,
                json=page_data
            )
            
            if response.status_code == 201:
                return {"success": True, "message": "Custom homepage created"}
            else:
                return {"success": False, "error": f"Failed to create page: {response.status_code}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def setup_product_collections(self) -> Dict[str, Any]:
        """Set up organized product collections"""
        collections = [
            {
                "title": "AI-Generated Content",
                "handle": "ai-content",
                "body_html": "<p>Premium content created by artificial intelligence</p>"
            },
            {
                "title": "Digital Tools & Templates", 
                "handle": "digital-tools",
                "body_html": "<p>Productivity tools and templates for modern professionals</p>"
            },
            {
                "title": "Business Resources",
                "handle": "business-resources", 
                "body_html": "<p>Everything you need to grow your business</p>"
            }
        ]
        
        results = []
        for collection in collections:
            try:
                collection_data = {
                    "collection": {
                        **collection,
                        "published": True
                    }
                }
                
                response = requests.post(
                    f"{self.base_url}/collections.json",
                    headers=self.headers,
                    json=collection_data
                )
                
                if response.status_code == 201:
                    results.append(f"✅ Created collection: {collection['title']}")
                else:
                    results.append(f"❌ Failed to create: {collection['title']}")
            except Exception as e:
                results.append(f"❌ Error creating {collection['title']}: {str(e)}")
        
        return {"success": True, "results": results}
    
    def customize_product_layout(self) -> Dict[str, Any]:
        """Customize product page layout"""
        theme = self.get_main_theme()
        if not theme:
            return {"success": False, "error": "No theme found"}
        
        # Enhanced product page CSS
        product_css = """
/* AI CEO Product Page Enhancements */
.product-single {
    max-width: 1200px;
    margin: 0 auto;
    padding: 40px 20px;
}

.product-single__media {
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 10px 25px rgba(0,0,0,0.1);
}

.product-single__title {
    font-size: 2.5em;
    color: #1f2937;
    margin-bottom: 20px;
}

.product-single__price {
    font-size: 2em;
    color: #10b981 !important;
    font-weight: bold;
    margin-bottom: 20px;
}

.product-form__cart-submit {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border: none;
    padding: 15px 40px;
    font-size: 1.1em;
    border-radius: 8px;
    transition: all 0.3s ease;
}

.product-form__cart-submit:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
}

.product-single__description {
    font-size: 1.1em;
    line-height: 1.8;
    color: #4b5563;
}

/* Trust badges */
.ai-ceo-badges {
    display: flex;
    justify-content: center;
    gap: 20px;
    margin: 30px 0;
    flex-wrap: wrap;
}

.trust-badge {
    display: flex;
    align-items: center;
    gap: 8px;
    background: #f0f9ff;
    padding: 10px 15px;
    border-radius: 25px;
    font-size: 0.9em;
    color: #0369a1;
}
"""
        
        return self.update_theme_asset(theme['id'], "assets/ai-ceo-products.css", product_css)
    
    def add_trust_elements(self) -> Dict[str, Any]:
        """Add trust elements and guarantees to the store"""
        theme = self.get_main_theme()
        if not theme:
            return {"success": False, "error": "No theme found"}
        
        # Trust elements snippet
        trust_snippet = """
<div class="ai-ceo-badges">
    <div class="trust-badge">
        <span>🔒</span>
        <span>Secure Checkout</span>
    </div>
    <div class="trust-badge">
        <span>⚡</span>
        <span>Instant Download</span>
    </div>
    <div class="trust-badge">
        <span>🤖</span>
        <span>AI-Generated</span>
    </div>
    <div class="trust-badge">
        <span>💯</span>
        <span>Money-Back Guarantee</span>
    </div>
</div>
"""
        
        return self.update_theme_asset(theme['id'], "snippets/ai-ceo-trust-badges.liquid", trust_snippet)
    
    def design_complete_store(self, business_type: str = "Digital Products") -> Dict[str, Any]:
        """Complete store design setup"""
        results = []
        
        # Step 1: Check connection
        connection = self.check_connection()
        if not connection.get('success'):
            return {"success": False, "error": "Could not connect to Shopify"}
        results.append("✅ Connected to Shopify Admin API")
        
        # Step 2: Customize colors
        colors_result = self.customize_store_colors()
        results.append("✅ Store colors customized" if colors_result.get('success') else "❌ Color customization failed")
        
        # Step 3: Create homepage
        homepage_result = self.create_custom_homepage(business_type)
        results.append("✅ Custom homepage created" if homepage_result.get('success') else "❌ Homepage creation failed")
        
        # Step 4: Setup collections
        collections_result = self.setup_product_collections()
        results.append("✅ Product collections created")
        
        # Step 5: Customize product layout
        layout_result = self.customize_product_layout()
        results.append("✅ Product layout customized" if layout_result.get('success') else "❌ Layout customization failed")
        
        # Step 6: Add trust elements
        trust_result = self.add_trust_elements()
        results.append("✅ Trust elements added" if trust_result.get('success') else "❌ Trust elements failed")
        
        return {
            "success": True,
            "message": "Store design completed",
            "results": results,
            "store_url": f"https://{self.store_url}"
        }

# Convenience functions for the AI CEO agent
def design_shopify_store(business_type: str = "Digital Products") -> Dict[str, Any]:
    """Design and customize the Shopify store"""
    designer = ShopifyStoreDesigner()
    return designer.design_complete_store(business_type)

def test_shopify_connection() -> Dict[str, Any]:
    """Test Shopify Admin API connection"""
    designer = ShopifyStoreDesigner()
    return designer.check_connection()

def customize_store_theme(primary_color: str = "#2563eb", secondary_color: str = "#1d4ed8") -> Dict[str, Any]:
    """Customize store theme colors"""
    designer = ShopifyStoreDesigner()
    return designer.customize_store_colors(primary_color, secondary_color)
