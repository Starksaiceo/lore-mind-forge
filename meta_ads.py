
import requests
from typing import Dict, List, Optional
from config import META_APP_ID, META_APP_SECRET, THREADS_APP_ID
from payment_processor import calculate_ad_budget, log_business_event

class MetaAdsManager:
    """Handle Meta (Facebook/Instagram) ad campaigns"""
    
    def __init__(self, access_token: str = None):
        self.access_token = access_token
        self.base_url = "https://graph.facebook.com/v18.0"
        self.app_id = META_APP_ID
        self.app_secret = META_APP_SECRET
    
    def get_app_access_token(self) -> Optional[str]:
        """Get app access token for Meta API"""
        try:
            response = requests.get(
                f"{self.base_url}/oauth/access_token",
                params={
                    "client_id": self.app_id,
                    "client_secret": self.app_secret,
                    "grant_type": "client_credentials"
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get("access_token")
            
            return None
            
        except Exception as e:
            print(f"Meta token error: {e}")
            return None
    
    def create_campaign(self, ad_account_id: str, campaign_name: str, objective: str = "CONVERSIONS") -> Dict:
        """Create a Meta ad campaign"""
        try:
            if not self.access_token:
                return {"success": False, "error": "No access token"}
            
            url = f"{self.base_url}/act_{ad_account_id}/campaigns"
            
            data = {
                "name": campaign_name,
                "objective": objective,
                "status": "PAUSED",  # Start paused for review
                "access_token": self.access_token
            }
            
            response = requests.post(url, data=data)
            
            if response.status_code == 200:
                result = response.json()
                log_business_event("meta_campaign_created", result)
                return {"success": True, "campaign": result}
            else:
                return {"success": False, "error": response.text}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def create_ad_set(self, ad_account_id: str, campaign_id: str, ad_set_name: str, budget: float, targeting: Dict) -> Dict:
        """Create an ad set with targeting and budget"""
        try:
            if not self.access_token:
                return {"success": False, "error": "No access token"}
            
            url = f"{self.base_url}/act_{ad_account_id}/adsets"
            
            data = {
                "name": ad_set_name,
                "campaign_id": campaign_id,
                "daily_budget": int(budget * 100),  # Convert to cents
                "billing_event": "IMPRESSIONS",
                "optimization_goal": "REACH",
                "targeting": targeting,
                "status": "PAUSED",
                "access_token": self.access_token
            }
            
            response = requests.post(url, data=data)
            
            if response.status_code == 200:
                result = response.json()
                log_business_event("meta_adset_created", result)
                return {"success": True, "ad_set": result}
            else:
                return {"success": False, "error": response.text}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def check_app_status(self) -> Dict:
        """Check if Meta app is approved for ads"""
        try:
            app_token = self.get_app_access_token()
            if not app_token:
                return {"approved": False, "status": "No app token"}
            
            response = requests.get(
                f"{self.base_url}/{self.app_id}",
                params={"access_token": app_token}
            )
            
            if response.status_code == 200:
                app_data = response.json()
                # Check if app is approved for marketing API
                restrictions = app_data.get("restrictions", {})
                return {
                    "approved": len(restrictions) == 0,
                    "status": "approved" if len(restrictions) == 0 else "in_review",
                    "app_data": app_data
                }
            else:
                return {"approved": False, "status": "error", "error": response.text}
                
        except Exception as e:
            return {"approved": False, "status": "error", "error": str(e)}

def auto_launch_ads_if_ready() -> Dict:
    """Automatically launch ads if conditions are met"""
    try:
        # Check if we have enough budget
        available_budget = calculate_ad_budget()
        
        if available_budget < 50:  # Minimum $50
            return {
                "launched": False,
                "reason": f"Insufficient budget: ${available_budget:.2f} (min $50)"
            }
        
        # Check Meta app status
        meta_manager = MetaAdsManager()
        app_status = meta_manager.check_app_status()
        
        if not app_status.get("approved", False):
            return {
                "launched": False,
                "reason": f"Meta app not approved: {app_status.get('status')}"
            }
        
        # If conditions are met, we would launch ads here
        # For now, just return that we're ready
        return {
            "launched": False,
            "ready": True,
            "budget": available_budget,
            "reason": "All conditions met for ad launch"
        }

    except Exception as e:
        return {
            "launched": False,
            "ready": False,
            "reason": f"Error checking launch conditions: {str(e)}"
        }

def auto_launch_ads_if_ready():
    """Check if conditions are met to auto-launch ads"""
    try:
        # Check available budget
        budget = calculate_ad_budget()
        min_budget = 50.0
        
        if budget >= min_budget:
            manager = MetaAdsManager()
            status = manager.check_app_status()
            
            if status.get("approved"):
                return {
                    "ready": True,
                    "budget": budget,
                    "message": f"Ready to launch with ${budget:.2f} budget"
                }
            else:
                return {
                    "ready": False,
                    "reason": f"Meta app not approved: {status.get('status')}"
                }
        else:
            needed = min_budget - budget
            return {
                "ready": False,
                "reason": f"Need ${needed:.2f} more budget (current: ${budget:.2f})"
            }
            
    except Exception as e:
        return {
            "ready": False,
            "reason": f"Error checking launch readiness: {str(e)}"
        }

# Targeting templates for different business niches
TARGETING_TEMPLATES = {
    "entrepreneurs": {
        "interests": ["Entrepreneurship", "Business", "Startup company"],
        "age_min": 25,
        "age_max": 55
    },
    "automation": {
        "interests": ["Automation", "Artificial intelligence", "Software"],
        "age_min": 22,
        "age_max": 50
    },
    "ecommerce": {
        "interests": ["E-commerce", "Online shopping", "Retail"],
        "age_min": 18,
        "age_max": 65
    }
}
