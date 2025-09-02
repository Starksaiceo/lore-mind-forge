
import requests
from config import get_meta_config
import json
from datetime import datetime, timedelta

class AdvancedMetaAdsManager:
    """Advanced Meta Ads automation and optimization"""
    
    def __init__(self):
        self.config = get_meta_config()
        self.base_url = "https://graph.facebook.com/v18.0"
        self.access_token = self.config.get("access_token")
        self.ad_account_id = self.config.get("ad_account_id")
    
    def create_automated_campaign(self, product_data, budget=50):
        """Create a complete automated ad campaign for a product"""
        try:
            if not self.access_token or not self.ad_account_id:
                return {"success": False, "error": "Meta credentials not configured"}
            
            # Step 1: Create Campaign
            campaign_data = {
                "name": f"AI CEO - {product_data['title']}",
                "objective": "CONVERSIONS",
                "status": "PAUSED",
                "access_token": self.access_token
            }
            
            campaign_response = requests.post(
                f"{self.base_url}/act_{self.ad_account_id}/campaigns",
                data=campaign_data
            )
            
            if campaign_response.status_code != 200:
                return {"success": False, "error": f"Campaign creation failed: {campaign_response.text}"}
            
            campaign_id = campaign_response.json()["id"]
            
            # Step 2: Create Ad Set
            ad_set_data = {
                "name": f"AdSet - {product_data['title']}",
                "campaign_id": campaign_id,
                "daily_budget": int(budget * 100),  # Convert to cents
                "billing_event": "IMPRESSIONS",
                "optimization_goal": "CONVERSIONS",
                "targeting": json.dumps({
                    "geo_locations": {"countries": ["US", "CA", "GB", "AU"]},
                    "age_min": 25,
                    "age_max": 55,
                    "interests": [
                        {"id": "6003107902433", "name": "Entrepreneurship"},
                        {"id": "6003056178903", "name": "Business"}
                    ]
                }),
                "status": "PAUSED",
                "access_token": self.access_token
            }
            
            ad_set_response = requests.post(
                f"{self.base_url}/act_{self.ad_account_id}/adsets",
                data=ad_set_data
            )
            
            if ad_set_response.status_code != 200:
                return {"success": False, "error": f"Ad set creation failed: {ad_set_response.text}"}
            
            ad_set_id = ad_set_response.json()["id"]
            
            # Step 3: Generate AI-powered ad copy
            ad_copy = self.generate_ad_copy(product_data)
            
            return {
                "success": True,
                "campaign_id": campaign_id,
                "ad_set_id": ad_set_id,
                "ad_copy": ad_copy,
                "status": "created_paused"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def generate_ad_copy(self, product_data):
        """Generate compelling ad copy for products"""
        headlines = [
            f"🚀 {product_data['title']} - Transform Your Business",
            f"💰 Boost Revenue with {product_data['title']}",
            f"⚡ Automate Success with {product_data['title']}"
        ]
        
        descriptions = [
            f"Discover {product_data['title']} - the AI-powered solution that's helping entrepreneurs scale faster than ever.",
            f"Join thousands who've transformed their business with {product_data['title']}. Limited time offer!",
            f"Stop struggling with manual processes. {product_data['title']} automates everything you need."
        ]
        
        return {
            "headlines": headlines,
            "descriptions": descriptions,
            "cta": "Get Started Now",
            "price": product_data.get('price', 47)
        }
    
    def optimize_campaigns(self):
        """Automatically optimize running campaigns based on performance"""
        try:
            # Get campaign insights
            insights_url = f"{self.base_url}/act_{self.ad_account_id}/insights"
            
            params = {
                "fields": "campaign_id,spend,clicks,conversions,cost_per_conversion",
                "time_range": json.dumps({
                    "since": (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d"),
                    "until": datetime.now().strftime("%Y-%m-%d")
                }),
                "access_token": self.access_token
            }
            
            response = requests.get(insights_url, params=params)
            
            if response.status_code == 200:
                insights = response.json().get("data", [])
                optimizations = []
                
                for insight in insights:
                    campaign_id = insight["campaign_id"]
                    cost_per_conversion = float(insight.get("cost_per_conversion", 0))
                    
                    # Optimization logic
                    if cost_per_conversion > 50:  # Too expensive
                        optimizations.append({
                            "campaign_id": campaign_id,
                            "action": "reduce_budget",
                            "reason": f"High cost per conversion: ${cost_per_conversion}"
                        })
                    elif cost_per_conversion < 10:  # Very efficient
                        optimizations.append({
                            "campaign_id": campaign_id,
                            "action": "increase_budget",
                            "reason": f"Low cost per conversion: ${cost_per_conversion}"
                        })
                
                return {"success": True, "optimizations": optimizations}
            
            return {"success": False, "error": "Could not fetch insights"}
            
        except Exception as e:
            return {"success": False, "error": str(e)}

def launch_product_campaign(product_data, budget=50):
    """Launch a complete automated campaign for a product"""
    manager = AdvancedMetaAdsManager()
    return manager.create_automated_campaign(product_data, budget)
