
#!/usr/bin/env python3
"""
Shopify Store Setup Script for AI CEO
Handles connection, product creation, and theme updates using Admin API
"""

import requests
import json
import os
from datetime import datetime

class ShopifyStoreSetup:
    def __init__(self):
        from config import SHOPIFY_STORE_URL, SHOPIFY_ACCESS_TOKEN
        self.store_url = SHOPIFY_STORE_URL
        self.admin_token = SHOPIFY_ACCESS_TOKEN
        self.base_url = f"https://{self.store_url}/admin/api/2025-01"
        self.headers = {
            "X-Shopify-Access-Token": self.admin_token,
            "Content-Type": "application/json"
        }
        
    def test_connection(self):
        """Test connection to Shopify Admin API"""
        print("🔍 Testing Shopify Admin API connection...")
        
        try:
            response = requests.get(f"{self.base_url}/products.json", headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                products = response.json().get('products', [])
                print(f"✅ Connection successful - Found {len(products)} existing products")
                return True
            else:
                print(f"❌ Connection failed: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"❌ Connection error: {str(e)}")
            return False
    
    def create_product(self, title, description, price, product_type="Digital"):
        """Create a product using Shopify Admin API"""
        print(f"📦 Creating product: {title}")
        
        product_data = {
            "product": {
                "title": title,
                "body_html": f"<h2>{title}</h2><p>{description}</p>",
                "vendor": "AI CEO",
                "product_type": product_type,
                "status": "active",
                "published": True,
                "tags": "ai-generated,digital,instant-download",
                "variants": [{
                    "price": str(price),
                    "inventory_management": None,
                    "inventory_tracking": False,
                    "requires_shipping": False,
                    "weight": 0,
                    "weight_unit": "kg"
                }]
            }
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/products.json", 
                headers=self.headers, 
                json=product_data,
                timeout=15
            )
            
            if response.status_code == 201:
                product = response.json().get('product', {})
                product_id = product.get('id')
                product_handle = product.get('handle')
                print(f"✅ Product created with ID: {product_id}")
                print(f"🔗 Product URL: https://{self.store_url}/products/{product_handle}")
                return {"success": True, "id": product_id, "handle": product_handle}
            else:
                print(f"❌ Product creation failed: {response.status_code} - {response.text}")
                return {"success": False, "error": response.text}
        except Exception as e:
            print(f"❌ Product creation error: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def get_main_theme(self):
        """Get the main/active theme"""
        print("🎨 Fetching active theme...")
        
        try:
            response = requests.get(f"{self.base_url}/themes.json", headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                themes = response.json().get('themes', [])
                for theme in themes:
                    if theme.get('role') == 'main':
                        theme_id = theme.get('id')
                        theme_name = theme.get('name')
                        print(f"✅ Found main theme: {theme_name} (ID: {theme_id})")
                        return {"success": True, "id": theme_id, "name": theme_name}
                
                # Fallback to first theme if no main theme found
                if themes:
                    theme = themes[0]
                    theme_id = theme.get('id')
                    theme_name = theme.get('name')
                    print(f"✅ Using first available theme: {theme_name} (ID: {theme_id})")
                    return {"success": True, "id": theme_id, "name": theme_name}
                else:
                    print("❌ No themes found")
                    return {"success": False, "error": "No themes found"}
            else:
                print(f"❌ Theme fetch failed: {response.status_code} - {response.text}")
                return {"success": False, "error": response.text}
        except Exception as e:
            print(f"❌ Theme fetch error: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def update_homepage_header(self, theme_id):
        """Update the homepage header text"""
        print("🏠 Updating homepage header...")
        
        # Create a custom section with AI CEO branding
        homepage_section = """
        <div class="ai-ceo-hero" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 60px 20px; text-align: center; margin-bottom: 40px;">
            <div style="max-width: 800px; margin: 0 auto;">
                <h1 style="font-size: 2.5em; margin-bottom: 20px;">Welcome to the AI CEO Store – Powered by Automation</h1>
                <p style="font-size: 1.2em; margin-bottom: 30px;">Experience the future of e-commerce with AI-generated products and automated business systems</p>
                <a href="/collections/all" style="background: #10b981; color: white; padding: 15px 30px; text-decoration: none; border-radius: 8px; font-weight: bold; display: inline-block;">Explore AI Products</a>
            </div>
        </div>
        """
        
        asset_data = {
            "asset": {
                "key": "sections/ai-ceo-hero.liquid",
                "value": homepage_section
            }
        }
        
        try:
            response = requests.put(
                f"{self.base_url}/themes/{theme_id}/assets.json",
                headers=self.headers,
                json=asset_data,
                timeout=15
            )
            
            if response.status_code == 200:
                print("✅ Theme updated successfully - AI CEO homepage header added")
                return {"success": True}
            else:
                print(f"❌ Theme update failed: {response.status_code} - {response.text}")
                return {"success": False, "error": response.text}
        except Exception as e:
            print(f"❌ Theme update error: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def setup_complete_store(self):
        """Complete store setup process"""
        print("🚀 Starting AI CEO Shopify Store Setup")
        print("=" * 50)
        
        # Step 1: Test connection
        if not self.test_connection():
            print("❌ Setup failed - Cannot connect to Shopify")
            return False
        
        # Step 2: Create products
        products_created = []
        
        # Product 1
        product1 = self.create_product(
            title="AI CEO Smart Blueprint",
            description="A digital strategy guide automatically generated by the AI CEO Agent.",
            price=29.99
        )
        if product1.get('success'):
            products_created.append(product1)
        
        # Product 2
        product2 = self.create_product(
            title="AI CEO Success Toolkit", 
            description="A collection of templates and tools built by the AI CEO Agent to grow your online business.",
            price=49.99
        )
        if product2.get('success'):
            products_created.append(product2)
        
        # Step 3: Update theme
        theme_result = self.get_main_theme()
        if theme_result.get('success'):
            theme_id = theme_result['id']
            self.update_homepage_header(theme_id)
        
        # Summary
        print("\n" + "=" * 50)
        print("🎯 AI CEO Store Setup Complete!")
        print(f"✅ Connection: Successful")
        print(f"✅ Products created: {len(products_created)}")
        print(f"✅ Theme updated: {'Yes' if theme_result.get('success') else 'No'}")
        print(f"🛒 Store URL: https://{self.store_url}")
        print(f"🔧 Admin URL: https://{self.store_url}/admin")
        
        return True

def main():
    """Main execution function"""
    setup = ShopifyStoreSetup()
    setup.setup_complete_store()

if __name__ == "__main__":
    main()
