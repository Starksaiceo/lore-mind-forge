import os
import requests
from typing import Dict, List, Optional
from config import META_APP_ID, META_APP_SECRET, THREADS_APP_ID
from meta_ads_stub import get_meta_token

class MetaAPI:
    """Meta/Facebook API service for ads and social media management"""

    def __init__(self):
        self.app_id = META_APP_ID
        self.app_secret = META_APP_SECRET
        self.threads_app_id = THREADS_APP_ID
        self.base_url = "https://graph.facebook.com/v18.0"

    def is_configured(self) -> bool:
        """Check if Meta API is properly configured"""
        return bool(self.app_id and self.app_secret)

    def get_app_access_token(self) -> Optional[str]:
        """Get app access token"""
        try:
            if not self.is_configured():
                return None

            url = f"{self.base_url}/oauth/access_token"
            params = {
                "client_id": self.app_id,
                "client_secret": self.app_secret,
                "grant_type": "client_credentials"
            }

            response = requests.get(url, params=params, timeout=15)
            response.raise_for_status()

            data = response.json()
            return data.get("access_token")

        except Exception as e:
            print(f"Error getting Meta access token: {e}")
            return None

    def check_app_status(self) -> Dict:
        """Check Meta app approval status"""
        try:
            if not self.is_configured():
                return {"approved": False, "status": "not_configured"}

            access_token = self.get_app_access_token()
            if not access_token:
                return {"approved": False, "status": "token_error"}

            url = f"{self.base_url}/{self.app_id}"
            params = {"access_token": access_token}

            response = requests.get(url, params=params, timeout=15)
            response.raise_for_status()

            data = response.json()
            app_status = data.get("status", "unknown")

            return {
                "approved": app_status == "LIVE",
                "status": app_status,
                "name": data.get("name", "Unknown"),
                "category": data.get("category", "Unknown")
            }

        except Exception as e:
            return {"approved": False, "status": f"error: {str(e)}"}

    def create_ad_campaign(self, campaign_data: Dict) -> Dict:
        """Create an ad campaign (requires additional setup)"""
        try:
            if not self.is_configured():
                return {"success": False, "error": "Meta API not configured"}

            # This is a simplified version - full implementation requires:
            # - Ad account setup
            # - Business verification
            # - Proper permissions

            return {
                "success": False,
                "error": "Ad campaign creation requires business verification and ad account setup",
                "next_steps": [
                    "Complete Facebook Business verification",
                    "Set up Ad Account",
                    "Get marketing API permissions"
                ]
            }

        except Exception as e:
            return {"success": False, "error": f"Meta ad campaign error: {str(e)}"}

    def post_to_threads(self, content: str, access_token: str) -> Dict:
        """Post content to Threads (requires user access token)"""
        try:
            if not self.threads_app_id:
                return {"success": False, "error": "Threads app not configured"}

            # This requires user authentication and proper setup
            return {
                "success": False,
                "error": "Threads posting requires user authentication",
                "next_steps": [
                    "Implement Threads OAuth flow",
                    "Get user access token",
                    "Complete Threads API setup"
                ]
            }

        except Exception as e:
            return {"success": False, "error": f"Threads posting error: {str(e)}"}

# Global instance
meta_api = MetaAPI()

# Convenience functions
def check_meta_app_status():
    """Check Meta app status with proper error handling"""
    token = get_meta_token()
    if not token:
        return {'approved': False, 'status': 'awaiting_approval'}
    return {'approved': True, 'status': 'ready'}

def create_meta_ad_campaign(campaign_data: Dict) -> Dict:
    """Create Meta ad campaign"""
    return meta_api.create_ad_campaign(campaign_data)

def post_to_threads(content: str, access_token: str) -> Dict:
    """Post to Threads"""
    return meta_api.post_to_threads(content, access_token)