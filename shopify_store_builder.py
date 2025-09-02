
import requests
from config import get_shopify_config
import json

class ShopifyStoreBuilder:
    """Complete Shopify store building and customization"""
    
    def __init__(self):
        self.config = get_shopify_config()
        self.headers = {
            "Content-Type": "application/json",
            "X-Shopify-Access-Token": self.config["access_token"]
        }
        self.base_url = f"https://{self.config['store_url']}/admin/api/{self.config['api_version']}"
    
    def setup_store_theme(self, theme_style="modern"):
        """Configure store theme and branding"""
        try:
            # Get current theme
            response = requests.get(f"{self.base_url}/themes.json", headers=self.headers)
            
            if response.status_code == 200:
                themes = response.json()["themes"]
                main_theme = next((t for t in themes if t["role"] == "main"), None)
                
                if main_theme:
                    # Customize theme settings
                    theme_settings = {
                        "asset": {
                            "key": "config/settings_data.json",
                            "value": json.dumps({
                                "current": {
                                    "sections": {
                                        "header": {
                                            "type": "header",
                                            "settings": {
                                                "logo_width": 200,
                                                "menu": "main-menu"
                                            }
                                        }
                                    }
                                }
                            })
                        }
                    }
                    
                    theme_url = f"{self.base_url}/themes/{main_theme['id']}/assets.json"
                    requests.put(theme_url, json=theme_settings, headers=self.headers)
                    
                return {"success": True, "theme_id": main_theme["id"]}
            
            return {"success": False, "error": "Could not access themes"}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def create_collections(self, product_categories):
        """Create product collections for better organization"""
        collections_created = []
        
        try:
            for category in product_categories:
                collection_data = {
                    "collection": {
                        "title": category["name"],
                        "body_html": f"<p>{category['description']}</p>",
                        "collection_type": "smart",
                        "rules": [
                            {
                                "column": "tag",
                                "relation": "equals",
                                "condition": category["tag"]
                            }
                        ]
                    }
                }
                
                response = requests.post(
                    f"{self.base_url}/collections.json",
                    json=collection_data,
                    headers=self.headers
                )
                
                if response.status_code == 201:
                    collection = response.json()["collection"]
                    collections_created.append(collection)
            
            return {"success": True, "collections": collections_created}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def setup_store_policies(self):
        """Set up essential store policies"""
        try:
            policies = [
                {
                    "title": "Privacy Policy",
                    "body": "Your privacy is important to us. This policy explains how we collect, use, and protect your information when you use our services."
                },
                {
                    "title": "Terms of Service",
                    "body": "By using our services, you agree to these terms. Please read them carefully."
                },
                {
                    "title": "Refund Policy",
                    "body": "We offer refunds within 30 days of purchase for digital products that don't meet your expectations."
                }
            ]
            
            created_policies = []
            for policy in policies:
                policy_data = {
                    "policy": {
                        "title": policy["title"],
                        "body": policy["body"]
                    }
                }
                
                response = requests.post(
                    f"{self.base_url}/policies.json",
                    json=policy_data,
                    headers=self.headers
                )
                
                if response.status_code == 201:
                    created_policies.append(response.json()["policy"])
            
            return {"success": True, "policies": created_policies}
            
        except Exception as e:
            return {"success": False, "error": str(e)}

def build_complete_store():
    """Build a complete Shopify store with AI CEO branding"""
    builder = ShopifyStoreBuilder()
    
    # Define product categories
    categories = [
        {"name": "AI Business Tools", "description": "Automated business solutions", "tag": "ai-business"},
        {"name": "Productivity Software", "description": "Tools to boost productivity", "tag": "productivity"},
        {"name": "Digital Courses", "description": "Educational content and training", "tag": "courses"},
        {"name": "Marketing Templates", "description": "Ready-to-use marketing materials", "tag": "marketing"}
    ]
    
    results = {
        "theme_setup": builder.setup_store_theme("modern"),
        "collections": builder.create_collections(categories),
        "policies": builder.setup_store_policies()
    }
    
    return results
