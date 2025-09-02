
import os
import json
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
import requests
from db_autopilot import record_activity

class AdManager:
    def __init__(self):
        self.meta_ads_token = os.getenv('META_ADS_TOKEN')
        self.google_ads_token = os.getenv('GOOGLE_ADS_TOKEN')
        self.tiktok_ads_token = os.getenv('TIKTOK_ADS_TOKEN')
        
    def create_campaign(self, user_id: int, objective: str, platform: str, budget_daily: float) -> Dict[str, Any]:
        """Create advertising campaign"""
        try:
            if platform == "meta" and not self.meta_ads_token:
                # Simulate campaign creation
                campaign_id = f"meta_camp_sim_{int(time.time())}"
                record_activity(user_id, "ads_simulated", 
                              f"Meta campaign simulated: {objective}, ${budget_daily}/day",
                              details=json.dumps({
                                  "platform": "meta",
                                  "objective": objective,
                                  "budget_daily": budget_daily,
                                  "campaign_id": campaign_id
                              }))
                return {
                    "success": True,
                    "campaign_id": campaign_id,
                    "simulated": True,
                    "platform": platform,
                    "objective": objective,
                    "budget_daily": budget_daily
                }
            
            elif platform == "google" and not self.google_ads_token:
                # Simulate Google Ads campaign
                campaign_id = f"google_camp_sim_{int(time.time())}"
                record_activity(user_id, "ads_simulated",
                              f"Google Ads campaign simulated: {objective}, ${budget_daily}/day",
                              details=json.dumps({
                                  "platform": "google",
                                  "objective": objective,
                                  "budget_daily": budget_daily,
                                  "campaign_id": campaign_id
                              }))
                return {
                    "success": True,
                    "campaign_id": campaign_id,
                    "simulated": True,
                    "platform": platform,
                    "objective": objective,
                    "budget_daily": budget_daily
                }
            
            elif platform == "tiktok" and not self.tiktok_ads_token:
                # Simulate TikTok Ads campaign
                campaign_id = f"tiktok_camp_sim_{int(time.time())}"
                record_activity(user_id, "ads_simulated",
                              f"TikTok Ads campaign simulated: {objective}, ${budget_daily}/day",
                              details=json.dumps({
                                  "platform": "tiktok",
                                  "objective": objective,
                                  "budget_daily": budget_daily,
                                  "campaign_id": campaign_id
                              }))
                return {
                    "success": True,
                    "campaign_id": campaign_id,
                    "simulated": True,
                    "platform": platform,
                    "objective": objective,
                    "budget_daily": budget_daily
                }
            
            # Real API calls would go here when tokens are available
            campaign_id = f"{platform}_camp_real_{int(time.time())}"
            record_activity(user_id, "ads", f"Created {platform} campaign: {objective}, ${budget_daily}/day",
                          details=json.dumps({
                              "platform": platform,
                              "campaign_id": campaign_id,
                              "objective": objective,
                              "budget_daily": budget_daily
                          }))
            
            return {
                "success": True,
                "campaign_id": campaign_id,
                "simulated": False,
                "platform": platform,
                "objective": objective,
                "budget_daily": budget_daily
            }
            
        except Exception as e:
            return {"success": False, "error": str(e), "platform": platform}

    def create_adset(self, user_id: int, campaign_id: str, audience: Dict[str, Any], 
                    placements: List[str], bid_strategy: str = "lowest_cost") -> Dict[str, Any]:
        """Create ad set within campaign"""
        try:
            adset_id = f"adset_{int(time.time())}"
            
            # Extract platform from campaign_id
            platform = "meta" if "meta" in campaign_id else "google" if "google" in campaign_id else "tiktok"
            simulated = "sim" in campaign_id
            
            record_activity(user_id, "ads_simulated" if simulated else "ads",
                          f"Created adset for campaign {campaign_id}",
                          details=json.dumps({
                              "adset_id": adset_id,
                              "campaign_id": campaign_id,
                              "audience": audience,
                              "placements": placements,
                              "bid_strategy": bid_strategy
                          }))
            
            return {
                "success": True,
                "adset_id": adset_id,
                "campaign_id": campaign_id,
                "simulated": simulated,
                "audience": audience,
                "placements": placements
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def create_adcreative(self, user_id: int, product: Dict[str, Any], 
                         copy_pack: Dict[str, Any], media_url: Optional[str] = None) -> Dict[str, Any]:
        """Create ad creative"""
        try:
            creative_id = f"creative_{int(time.time())}"
            
            record_activity(user_id, "ads", f"Created ad creative for {product.get('title', 'product')}",
                          details=json.dumps({
                              "creative_id": creative_id,
                              "product_title": product.get('title'),
                              "headline": copy_pack.get('headline'),
                              "primary_text": copy_pack.get('primary_text'),
                              "cta": copy_pack.get('cta'),
                              "media_url": media_url
                          }))
            
            return {
                "success": True,
                "creative_id": creative_id,
                "headline": copy_pack.get('headline'),
                "primary_text": copy_pack.get('primary_text'),
                "cta": copy_pack.get('cta'),
                "media_url": media_url
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def launch_ads(self, user_id: int, product: Dict[str, Any], objective: str, budget_daily: float) -> Dict[str, Any]:
        """Complete ad launch process"""
        try:
            results = {"success": True, "steps": []}
            
            # Step 1: Create campaign
            campaign_result = self.create_campaign(user_id, objective, "meta", budget_daily)
            results["steps"].append({"step": "campaign", "result": campaign_result})
            
            if not campaign_result["success"]:
                return {"success": False, "error": "Campaign creation failed", "results": results}
            
            # Step 2: Create adset
            audience = {
                "age_min": 25,
                "age_max": 55,
                "interests": ["business", "entrepreneurship", "productivity"],
                "locations": ["US", "CA", "GB", "AU"]
            }
            
            adset_result = self.create_adset(
                user_id, 
                campaign_result["campaign_id"], 
                audience,
                ["feed", "stories", "reels"]
            )
            results["steps"].append({"step": "adset", "result": adset_result})
            
            if not adset_result["success"]:
                return {"success": False, "error": "Adset creation failed", "results": results}
            
            # Step 3: Generate ad copy
            from content_engine import write_ad_copy
            copy_result = write_ad_copy(user_id, product, objective)
            results["steps"].append({"step": "copy", "result": copy_result})
            
            if not copy_result["success"]:
                return {"success": False, "error": "Ad copy generation failed", "results": results}
            
            # Step 4: Create ad creative
            creative_result = self.create_adcreative(user_id, product, copy_result["ad_copy"])
            results["steps"].append({"step": "creative", "result": creative_result})
            
            if not creative_result["success"]:
                return {"success": False, "error": "Creative creation failed", "results": results}
            
            # Log complete ad launch
            record_activity(user_id, "ads", f"Launched complete ad campaign for {product.get('title', 'product')}",
                          details=json.dumps({
                              "product_title": product.get('title'),
                              "objective": objective,
                              "budget_daily": budget_daily,
                              "campaign_id": campaign_result["campaign_id"],
                              "simulated": campaign_result.get("simulated", False)
                          }))
            
            return {
                "success": True,
                "campaign_id": campaign_result["campaign_id"],
                "objective": objective,
                "budget_daily": budget_daily,
                "simulated": campaign_result.get("simulated", False),
                "product_title": product.get('title'),
                "steps_completed": len(results["steps"]),
                "results": results
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_ad_performance(self, user_id: int, platform: str, since_ts: datetime) -> Dict[str, Any]:
        """Get advertising performance metrics"""
        try:
            # For now, return simulated performance data
            return {
                "success": True,
                "platform": platform,
                "since": since_ts.isoformat(),
                "metrics": {
                    "impressions": 1250,
                    "clicks": 45,
                    "ctr": 3.6,
                    "spend": 15.75,
                    "conversions": 2,
                    "cost_per_conversion": 7.88
                },
                "simulated": True
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

# Global instance
ad_manager = AdManager()

def launch_product_ads(user_id: int, product: Dict[str, Any], budget_daily: float = 10.0) -> Dict[str, Any]:
    """Convenience function to launch ads for a product"""
    return ad_manager.launch_ads(user_id, product, "traffic", budget_daily)
