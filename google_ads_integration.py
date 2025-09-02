"""
Google Ads Integration for AI CEO Platform
Handles automated Google Ads campaign creation and management using REST API
"""

import os
import logging
import requests
from typing import Dict, List, Optional, Any
import json

logger = logging.getLogger(__name__)

class GoogleAdsManager:
    """Manages Google Ads campaigns for AI CEO platform using REST API"""
    
    def __init__(self):
        """Initialize Google Ads manager with credentials from environment"""
        self.config = {
            "developer_token": os.getenv("GOOGLE_ADS_DEVELOPER_TOKEN"),
            "client_id": os.getenv("GOOGLE_ADS_CLIENT_ID"), 
            "client_secret": os.getenv("GOOGLE_ADS_CLIENT_SECRET"),
            "refresh_token": os.getenv("GOOGLE_ADS_REFRESH_TOKEN"),
            "login_customer_id": os.getenv("GOOGLE_ADS_LOGIN_CUSTOMER_ID")
        }
        
        self.base_url = "https://googleads.googleapis.com/v17"
        self.access_token = None
        
        # Validate required credentials
        missing_creds = [k for k, v in self.config.items() if not v and k != "login_customer_id"]
        if missing_creds:
            logger.warning(f"Missing Google Ads credentials: {missing_creds}")
            self.connected = False
        else:
            try:
                self.access_token = self._get_access_token()
                self.connected = bool(self.access_token) and self.access_token != "simulation_mode"
                if self.connected:
                    logger.info("✅ Google Ads REST API client initialized successfully")
                elif self.access_token == "simulation_mode":
                    logger.info("⚠️ Google Ads running in simulation mode")
                    self.connected = False
                else:
                    logger.warning("⚠️ Google Ads access token generation failed")
            except Exception as e:
                logger.error(f"❌ Failed to initialize Google Ads client: {e}")
                self.connected = False
    
    def _get_access_token(self) -> Optional[str]:
        """Get access token using refresh token"""
        if not self.config["refresh_token"]:
            return None
            
        try:
            token_url = "https://oauth2.googleapis.com/token"
            data = {
                "client_id": self.config["client_id"],
                "client_secret": self.config["client_secret"],
                "refresh_token": self.config["refresh_token"],
                "grant_type": "refresh_token"
            }
            
            response = requests.post(token_url, data=data)
            if response.status_code == 200:
                token_data = response.json()
                access_token = token_data.get("access_token")
                logger.info("✅ Successfully obtained Google Ads access token")
                return access_token
            else:
                logger.error(f"❌ Failed to get access token: {response.text}")
                # For now, return simulation mode instead of failing completely
                logger.warning("⚠️ Falling back to simulation mode for Google Ads")
                return "simulation_mode"
                
        except Exception as e:
            logger.error(f"❌ Access token request failed: {e}")
            logger.warning("⚠️ Falling back to simulation mode for Google Ads")
            return "simulation_mode"
    
    def is_connected(self) -> bool:
        """Check if Google Ads is properly connected"""
        return self.connected
    
    def _make_api_request(self, endpoint: str, method: str = "GET", data: Dict = None) -> Optional[Dict]:
        """Make authenticated request to Google Ads API"""
        if not self.access_token or self.access_token == "simulation_mode":
            return None
        
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "developer-token": str(self.config["developer_token"]).strip(),
            "Content-Type": "application/json"
        }
        
        if self.config.get("login_customer_id"):
            headers["login-customer-id"] = self.config["login_customer_id"]
        
        url = f"{self.base_url}/{endpoint}"
        
        try:
            if method == "POST":
                response = requests.post(url, headers=headers, json=data)
            else:
                response = requests.get(url, headers=headers)
            
            if response.status_code in [200, 201]:
                return response.json()
            else:
                logger.error(f"API request failed: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"API request exception: {e}")
            return None
    
    def get_customer_accounts(self) -> List[Dict[str, Any]]:
        """Get list of accessible customer accounts using REST API"""
        if not self.access_token or self.access_token == "simulation_mode":
            return []
        
        try:
            # Use the correct Google Ads API endpoint
            url = f"https://googleads.googleapis.com/v17/customers:listAccessibleCustomers"
            
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "developer-token": str(self.config["developer_token"]).strip(),
                "Content-Type": "application/json"
            }
            
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                result = response.json()
                if "resourceNames" in result:
                    accounts = []
                    for resource_name in result["resourceNames"]:
                        customer_id = resource_name.split("/")[-1]
                        accounts.append({
                            "id": customer_id,
                            "resource_name": resource_name
                        })
                    
                    logger.info(f"✅ Found {len(accounts)} Google Ads accounts")
                    return accounts
                else:
                    logger.warning("⚠️ No accessible customers found in response")
                    return []
            else:
                logger.error(f"API request failed: {response.status_code} - {response.text}")
                return []
            
        except Exception as e:
            logger.error(f"❌ Failed to get customer accounts: {e}")
            return []
    
    def create_campaign_rest(self, customer_id: str, campaign_data: Dict[str, Any]) -> Optional[str]:
        """Create a new Google Ads campaign using REST API"""
        if not self.access_token or self.access_token == "simulation_mode":
            logger.info("📝 Simulating Google Ads campaign creation (no real campaign created)")
            return "simulation_campaign_123"
        
        try:
            # First create campaign budget
            budget_data = {
                "operations": [{
                    "create": {
                        "name": f"AI CEO Budget - {campaign_data.get('name', 'Campaign')}",
                        "deliveryMethod": "STANDARD",
                        "amountMicros": str(int(campaign_data.get("daily_budget", 10.00) * 1_000_000))
                    }
                }]
            }
            
            budget_endpoint = f"customers/{customer_id}/campaignBudgets:mutate"
            budget_result = self._make_api_request(budget_endpoint, "POST", budget_data)
            
            if not budget_result or "results" not in budget_result:
                logger.error("❌ Failed to create campaign budget")
                return None
                
            budget_resource = budget_result["results"][0]["resourceName"]
            
            # Create campaign
            campaign_create_data = {
                "operations": [{
                    "create": {
                        "name": campaign_data.get("name", f"AI CEO Campaign - {campaign_data.get('product_name', 'Product')}"),
                        "advertisingChannelType": "SEARCH",
                        "status": "ENABLED",
                        "campaignBudget": budget_resource,
                        "manualCpc": {
                            "enhancedCpcEnabled": True
                        }
                    }
                }]
            }
            
            campaign_endpoint = f"customers/{customer_id}/campaigns:mutate"
            campaign_result = self._make_api_request(campaign_endpoint, "POST", campaign_create_data)
            
            if campaign_result and "results" in campaign_result:
                campaign_resource = campaign_result["results"][0]["resourceName"]
                campaign_id = campaign_resource.split("/")[-1]
                
                logger.info(f"✅ Created Google Ads campaign via REST API: {campaign_data.get('name')} (ID: {campaign_id})")
                
                # Create ad groups and ads
                self._create_ad_groups_rest(customer_id, campaign_id, campaign_data)
                
                return campaign_id
            else:
                logger.error("❌ Campaign creation failed via REST API")
                return None
                
        except Exception as e:
            logger.error(f"❌ Failed to create campaign via REST: {e}")
            return None
    
    def _create_ad_groups_rest(self, customer_id: str, campaign_id: str, campaign_data: Dict[str, Any]):
        """Create ad groups and keywords using REST API"""
        try:
            # Create ad group
            ad_group_data = {
                "operations": [{
                    "create": {
                        "name": f"AI CEO Ad Group - {campaign_data.get('product_name', 'Product')}",
                        "campaign": f"customers/{customer_id}/campaigns/{campaign_id}",
                        "status": "ENABLED",
                        "type": "SEARCH_STANDARD",
                        "cpcBidMicros": "2000000"  # $2.00 default bid
                    }
                }]
            }
            
            ad_group_endpoint = f"customers/{customer_id}/adGroups:mutate"
            ad_group_result = self._make_api_request(ad_group_endpoint, "POST", ad_group_data)
            
            if ad_group_result and "results" in ad_group_result:
                ad_group_resource = ad_group_result["results"][0]["resourceName"]
                ad_group_id = ad_group_resource.split("/")[-1]
                
                # Add keywords
                self._add_keywords_rest(customer_id, ad_group_id, campaign_data.get("keywords", []))
                
                # Create responsive search ads
                self._create_responsive_search_ads_rest(customer_id, ad_group_id, campaign_data)
                
                logger.info(f"✅ Created ad group and ads via REST API")
            else:
                logger.error("❌ Ad group creation failed via REST API")
                
        except Exception as e:
            logger.error(f"❌ Failed to create ad groups via REST: {e}")
    
    def _add_keywords_rest(self, customer_id: str, ad_group_id: str, keywords: List[str]):
        """Add keywords to ad group using REST API"""
        if not keywords:
            keywords = ["entrepreneur", "business success", "online business"]
        
        try:
            operations = []
            for keyword in keywords[:10]:  # Limit to 10 keywords
                operations.append({
                    "create": {
                        "adGroup": f"customers/{customer_id}/adGroups/{ad_group_id}",
                        "status": "ENABLED",
                        "keyword": {
                            "text": keyword,
                            "matchType": "BROAD"
                        }
                    }
                })
            
            keyword_data = {"operations": operations}
            keyword_endpoint = f"customers/{customer_id}/adGroupCriteria:mutate"
            keyword_result = self._make_api_request(keyword_endpoint, "POST", keyword_data)
            
            if keyword_result and "results" in keyword_result:
                logger.info(f"✅ Added {len(operations)} keywords via REST API")
            else:
                logger.error("❌ Keywords creation failed via REST API")
                
        except Exception as e:
            logger.error(f"❌ Failed to add keywords via REST: {e}")
    
    def _create_responsive_search_ads_rest(self, customer_id: str, ad_group_id: str, campaign_data: Dict[str, Any]):
        """Create responsive search ads using REST API"""
        try:
            product_name = campaign_data.get("product_name", "Business Success Product")
            
            # Create responsive search ad
            ad_data = {
                "operations": [{
                    "create": {
                        "adGroup": f"customers/{customer_id}/adGroups/{ad_group_id}",
                        "status": "ENABLED",
                        "ad": {
                            "responsiveSearchAd": {
                                "headlines": [
                                    {"text": f"Master {product_name}"},
                                    {"text": f"{product_name} Guide"},
                                    {"text": "Transform Your Business"},
                                    {"text": "Entrepreneur Success"},
                                    {"text": f"Learn {product_name} Today"}
                                ],
                                "descriptions": [
                                    {"text": "Complete guide to business success. Start your journey today!"},
                                    {"text": "Proven strategies used by successful entrepreneurs worldwide."},
                                    {"text": "Transform your business with expert guidance and tools."},
                                    {"text": "Join thousands of successful entrepreneurs. Get started now!"}
                                ]
                            },
                            "finalUrls": [campaign_data.get("landing_page", "https://example.com")]
                        }
                    }
                }]
            }
            
            ad_endpoint = f"customers/{customer_id}/adGroupAds:mutate"
            ad_result = self._make_api_request(ad_endpoint, "POST", ad_data)
            
            if ad_result and "results" in ad_result:
                logger.info(f"✅ Created responsive search ad via REST API for {product_name}")
            else:
                logger.error("❌ Responsive search ad creation failed via REST API")
                
        except Exception as e:
            logger.error(f"❌ Failed to create responsive search ads via REST: {e}")
    
    def get_campaign_performance_rest(self, customer_id: str, days: int = 30) -> Dict[str, Any]:
        """Get campaign performance metrics using REST API"""
        if not self.access_token or self.access_token == "simulation_mode":
            return {
                "campaigns": [],
                "summary": {
                    "total_campaigns": 0,
                    "total_spend": 0,
                    "total_clicks": 0,
                    "average_cpc": 0
                },
                "simulation": True
            }
        
        try:
            query = f"""
                SELECT
                    campaign.id,
                    campaign.name,
                    metrics.impressions,
                    metrics.clicks,
                    metrics.cost_micros,
                    metrics.conversions
                FROM campaign
                WHERE segments.date DURING LAST_{days}_DAYS
                ORDER BY metrics.impressions DESC
                LIMIT 10
            """
            
            search_data = {
                "query": query
            }
            
            search_endpoint = f"customers/{customer_id}/googleAds:search"
            result = self._make_api_request(search_endpoint, "POST", search_data)
            
            if result and "results" in result:
                campaigns = []
                total_spend = 0
                total_clicks = 0
                
                for row in result["results"]:
                    campaign_data = {
                        "id": row.get("campaign", {}).get("id"),
                        "name": row.get("campaign", {}).get("name"),
                        "impressions": row.get("metrics", {}).get("impressions", 0),
                        "clicks": row.get("metrics", {}).get("clicks", 0),
                        "cost": int(row.get("metrics", {}).get("costMicros", 0)) / 1_000_000,
                        "conversions": row.get("metrics", {}).get("conversions", 0)
                    }
                    campaigns.append(campaign_data)
                    total_spend += campaign_data["cost"]
                    total_clicks += campaign_data["clicks"]
                
                return {
                    "campaigns": campaigns,
                    "summary": {
                        "total_campaigns": len(campaigns),
                        "total_spend": round(total_spend, 2),
                        "total_clicks": total_clicks,
                        "average_cpc": round(total_spend / max(total_clicks, 1), 2)
                    }
                }
            else:
                return {
                    "campaigns": [],
                    "summary": {
                        "total_campaigns": 0,
                        "total_spend": 0,
                        "total_clicks": 0,
                        "average_cpc": 0
                    }
                }
                
        except Exception as e:
            logger.error(f"❌ Failed to get campaign performance via REST: {e}")
            return {"error": str(e)}

# Global instance
google_ads_manager = GoogleAdsManager()

def create_automated_google_campaign(product_data: Dict[str, Any], customer_id: str = None) -> Dict[str, Any]:
    """Create Google Ads campaign for AI-generated product"""
    try:
        if not google_ads_manager.is_connected():
            if google_ads_manager.access_token == "simulation_mode":
                return {
                    "success": True,
                    "simulated": True,
                    "campaign_id": f"sim_campaign_{hash(product_data.get('title', 'product'))}",
                    "message": f"✅ Simulated Google Ads campaign for {product_data.get('title')} - add GOOGLE_ADS_REFRESH_TOKEN for real campaigns",
                    "next_steps": "Configure Google Ads OAuth to enable real campaigns"
                }
            else:
                return {
                    "success": False,
                    "error": "Google Ads not connected - add GOOGLE_ADS_REFRESH_TOKEN to Replit Secrets",
                    "next_steps": "Complete OAuth flow to get refresh token"
                }
        
        if not customer_id:
            accounts = google_ads_manager.get_customer_accounts()
            if not accounts:
                return {
                    "success": False,
                    "error": "No Google Ads accounts accessible",
                    "next_steps": "Connect Google Ads account via OAuth"
                }
            customer_id = accounts[0]["id"]  # Use first account
        
        # Prepare campaign data
        campaign_data = {
            "name": f"AI CEO - {product_data.get('title', 'Product')}",
            "product_name": product_data.get("title", "Business Product"),
            "daily_budget": max(product_data.get("price", 50) * 0.5, 10.0),  # 50% of product price as daily budget, min $10
            "keywords": [
                product_data.get("title", "").lower(),
                "entrepreneur",
                "business success",
                "online business",
                "passive income"
            ] + product_data.get("tags", []),
            "landing_page": f"https://your-domain.com/product/{product_data.get('id', '')}"
        }
        
        # Create the campaign
        campaign_id = google_ads_manager.create_campaign_rest(customer_id, campaign_data)
        
        if campaign_id:
            return {
                "success": True,
                "campaign_id": campaign_id,
                "customer_id": customer_id,
                "campaign_name": campaign_data["name"],
                "daily_budget": campaign_data["daily_budget"],
                "keywords_count": len(campaign_data["keywords"]),
                "message": f"✅ Google Ads campaign created successfully for {product_data.get('title')}",
                "simulated": campaign_id.startswith("sim_")
            }
        else:
            return {
                "success": False,
                "error": "Failed to create Google Ads campaign",
                "product": product_data.get("title")
            }
            
    except Exception as e:
        logger.error(f"❌ Automated Google campaign creation failed: {e}")
        return {
            "success": False,
            "error": str(e),
            "product": product_data.get("title")
        }

def get_google_ads_performance(customer_id: str = None, days: int = 30) -> Dict[str, Any]:
    """Get Google Ads performance metrics"""
    try:
        if not google_ads_manager.is_connected():
            return {
                "error": "Google Ads not connected",
                "metrics": {
                    "total_spend": 0,
                    "total_clicks": 0,
                    "campaigns": 0
                },
                "simulation": True
            }
        
        if not customer_id:
            accounts = google_ads_manager.get_customer_accounts()
            if accounts:
                customer_id = accounts[0]["id"]
            else:
                return {"error": "No Google Ads accounts found"}
        
        return google_ads_manager.get_campaign_performance_rest(customer_id, days)
        
    except Exception as e:
        logger.error(f"❌ Failed to get Google Ads performance: {e}")
        return {"error": str(e)}

# Export functions for use in main app
__all__ = [
    'GoogleAdsManager',
    'google_ads_manager', 
    'create_automated_google_campaign',
    'get_google_ads_performance'
]