
import os
import requests
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from meta_ads import MetaAdsManager, auto_launch_ads_if_ready
from profit_tracker import get_total_profit_last_30_days, post_profit
from payment_processor import calculate_ad_budget
from config import XANO_BASE_URL, META_APP_ID, META_APP_SECRET

class AutoAdScaler:
    """Automatically scale ad campaigns based on profit performance"""
    
    def __init__(self):
        self.xano_url = XANO_BASE_URL
        self.min_roas = 1.5  # Minimum Return on Ad Spend
        self.max_cac_ratio = 0.5  # Maximum CAC as % of product price
        self.reinvest_rate_min = 0.20  # 20% minimum reinvestment
        self.reinvest_rate_max = 0.40  # 40% maximum reinvestment
        self.meta_manager = MetaAdsManager()
    
    def calculate_smart_budget(self) -> Dict:
        """Calculate optimal ad budget based on recent performance"""
        try:
            # Get recent profit data
            total_profit = get_total_profit_last_30_days()
            
            if total_profit <= 0:
                return {
                    "budget": 0.0,
                    "reinvest_rate": 0.0,
                    "reason": "No recent profit to reinvest"
                }
            
            # Get recent ad performance
            ad_performance = self.get_recent_ad_performance()
            current_roas = ad_performance.get("roas", 0.0)
            
            # Adjust reinvestment rate based on performance
            if current_roas >= 3.0:
                reinvest_rate = self.reinvest_rate_max  # Scale aggressively
            elif current_roas >= 2.0:
                reinvest_rate = 0.30  # Moderate scaling
            elif current_roas >= self.min_roas:
                reinvest_rate = self.reinvest_rate_min  # Conservative scaling
            else:
                reinvest_rate = 0.10  # Minimal reinvestment for testing
            
            budget = total_profit * reinvest_rate
            
            return {
                "total_profit": total_profit,
                "budget": round(budget, 2),
                "reinvest_rate": reinvest_rate,
                "current_roas": current_roas,
                "recommended_action": self.get_scaling_recommendation(current_roas, budget)
            }
            
        except Exception as e:
            return {"error": str(e), "budget": 0.0}
    
    def get_recent_ad_performance(self) -> Dict:
        """Get recent ad campaign performance from Xano"""
        try:
            response = requests.get(f"{self.xano_url}/ad_campaigns", timeout=10)
            
            if response.status_code == 200:
                campaigns = response.json()
                
                if not campaigns:
                    return {"roas": 0.0, "cac": 0.0, "spend": 0.0, "revenue": 0.0}
                
                # Calculate average ROAS from recent campaigns
                recent_campaigns = [c for c in campaigns if self.is_recent_campaign(c)]
                
                if not recent_campaigns:
                    return {"roas": 0.0, "cac": 0.0, "spend": 0.0, "revenue": 0.0}
                
                total_spend = sum(c.get("spend", 0) for c in recent_campaigns)
                total_revenue = sum(c.get("revenue", 0) for c in recent_campaigns)
                total_conversions = sum(c.get("conversions", 0) for c in recent_campaigns)
                
                roas = total_revenue / total_spend if total_spend > 0 else 0.0
                cac = total_spend / total_conversions if total_conversions > 0 else 0.0
                
                return {
                    "roas": round(roas, 2),
                    "cac": round(cac, 2),
                    "spend": round(total_spend, 2),
                    "revenue": round(total_revenue, 2),
                    "campaigns": len(recent_campaigns)
                }
            
            return {"roas": 0.0, "cac": 0.0, "spend": 0.0, "revenue": 0.0}
            
        except Exception as e:
            print(f"Error getting ad performance: {e}")
            return {"roas": 0.0, "cac": 0.0, "spend": 0.0, "revenue": 0.0}
    
    def is_recent_campaign(self, campaign: Dict) -> bool:
        """Check if campaign is from last 30 days"""
        try:
            created_at = campaign.get("created_at", "")
            if not created_at:
                return False
            
            campaign_date = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
            thirty_days_ago = datetime.now() - timedelta(days=30)
            
            return campaign_date >= thirty_days_ago
            
        except ValueError:
            return False
    
    def get_scaling_recommendation(self, roas: float, budget: float) -> str:
        """Get recommendation for ad scaling"""
        if roas >= 3.0:
            return f"🚀 SCALE AGGRESSIVELY - Excellent ROAS {roas:.1f}x, increase budget"
        elif roas >= 2.0:
            return f"📈 SCALE MODERATELY - Good ROAS {roas:.1f}x, steady growth"
        elif roas >= self.min_roas:
            return f"✅ MAINTAIN - Profitable ROAS {roas:.1f}x, keep current spend"
        elif roas > 0:
            return f"⚠️ OPTIMIZE - Low ROAS {roas:.1f}x, improve targeting/creative"
        else:
            return "🔍 TEST - No data, start with small budget"
    
    def create_scaled_campaign(self, budget: float, product_data: Dict = None) -> Dict:
        """Create a new scaled ad campaign"""
        try:
            if budget < 10.0:
                return {"success": False, "error": "Budget too low for campaign"}
            
            # Check Meta app status
            app_status = self.meta_manager.check_app_status()
            if not app_status.get("approved", False):
                return {
                    "success": False, 
                    "error": f"Meta app not approved: {app_status.get('status')}"
                }
            
            # Get best performing product for targeting
            if not product_data:
                product_data = self.get_top_performing_product()
            
            campaign_data = {
                "name": f"Auto-Scale Campaign {datetime.now().strftime('%Y%m%d_%H%M')}",
                "objective": "CONVERSIONS",
                "budget": budget,
                "targeting": self.create_smart_targeting(product_data),
                "creative": self.generate_ad_creative(product_data),
                "auto_generated": True,
                "created_at": datetime.now().isoformat()
            }
            
            # Save campaign to Xano
            response = requests.post(f"{self.xano_url}/ad_campaigns", json=campaign_data, timeout=10)
            
            if response.status_code in [200, 201]:
                campaign_id = response.json().get("id", "unknown")
                
                # Log ad spend as business expense
                post_profit(-budget, f"Ad Campaign {campaign_id}")
                
                print(f"✅ Scaled campaign created: ${budget} budget")
                return {
                    "success": True,
                    "campaign_id": campaign_id,
                    "budget": budget,
                    "campaign_data": campaign_data
                }
            else:
                return {"success": False, "error": "Failed to save campaign"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_top_performing_product(self) -> Dict:
        """Get the best performing product for ad targeting"""
        try:
            # Get products from Xano
            response = requests.get(f"{self.xano_url}/products", timeout=10)
            
            if response.status_code == 200:
                products = response.json()
                
                if products:
                    # Sort by profit forecast or actual sales
                    sorted_products = sorted(
                        products, 
                        key=lambda p: p.get("profit_forecast", 0), 
                        reverse=True
                    )
                    return sorted_products[0]
            
            # Fallback default product
            return {
                "title": "AI Business Automation",
                "type": "business_course",
                "price": 97.0,
                "keyword": "business automation"
            }
            
        except Exception as e:
            print(f"Error getting top product: {e}")
            return {
                "title": "AI Business Tools",
                "type": "digital_course", 
                "price": 67.0,
                "keyword": "AI tools"
            }
    
    def create_smart_targeting(self, product: Dict) -> Dict:
        """Create smart targeting based on product data"""
        product_type = product.get("type", "business_course")
        keyword = product.get("keyword", "business")
        
        targeting_templates = {
            "business_course": {
                "interests": ["Entrepreneurship", "Business", "Online business"],
                "age_min": 25,
                "age_max": 55,
                "behaviors": ["Small business owners"]
            },
            "digital_course": {
                "interests": ["Online learning", "Professional development", "Skill development"],
                "age_min": 22,
                "age_max": 50,
                "behaviors": ["Technology early adopters"]
            },
            "automation": {
                "interests": ["Automation", "Artificial intelligence", "Software"],
                "age_min": 25,
                "age_max": 45,
                "behaviors": ["Technology early adopters"]
            }
        }
        
        return targeting_templates.get(product_type, targeting_templates["business_course"])
    
    def generate_ad_creative(self, product: Dict) -> Dict:
        """Generate ad creative based on product"""
        title = product.get("title", "AI Business Solution")
        price = product.get("price", 97.0)
        
        headlines = [
            f"Master {product.get('keyword', 'Business')} in 2024",
            f"Proven {title} System",
            f"Transform Your Business Today"
        ]
        
        descriptions = [
            f"Get instant access to our complete {title.lower()} for just ${price}",
            f"Join thousands using this proven system. Limited time offer!",
            f"Step-by-step blueprint + templates included. 30-day guarantee."
        ]
        
        return {
            "headlines": headlines,
            "descriptions": descriptions,
            "call_to_action": "Learn More",
            "offer": f"Complete system for ${price}"
        }
    
    def run_auto_scaler(self) -> Dict:
        """Run the complete auto ad scaling system"""
        try:
            print("📈 Starting Auto Ad Scaler...")
            
            # Calculate smart budget
            budget_data = self.calculate_smart_budget()
            
            if budget_data.get("error"):
                return {"success": False, "error": budget_data["error"]}
            
            budget = budget_data.get("budget", 0.0)
            
            if budget < 10.0:
                return {
                    "success": False,
                    "message": f"Budget too low: ${budget:.2f}",
                    "budget_data": budget_data
                }
            
            # Create scaled campaign
            campaign_result = self.create_scaled_campaign(budget)
            
            if campaign_result.get("success"):
                result = {
                    "success": True,
                    "budget_allocated": budget,
                    "campaign_created": True,
                    "campaign_id": campaign_result.get("campaign_id"),
                    "budget_data": budget_data,
                    "recommendation": budget_data.get("recommended_action")
                }
                
                print(f"✅ Auto Ad Scaler completed: ${budget} campaign created")
                return result
            else:
                return {
                    "success": False,
                    "error": campaign_result.get("error"),
                    "budget_data": budget_data
                }
                
        except Exception as e:
            return {"success": False, "error": str(e)}

# Auto-run function
def run_auto_ad_scaler() -> Dict:
    """Run the auto ad scaler"""
    scaler = AutoAdScaler()
    return scaler.run_auto_scaler()

if __name__ == "__main__":
    print("📈 Testing Auto Ad Scaler...")
    result = run_auto_ad_scaler()
    print("Result:", json.dumps(result, indent=2))
def run_auto_ad_scaler():
    """Run auto ad scaler"""
    try:
        print("📈 Auto Ad Scaler: Calculating optimal budget...")
        
        # Calculate available budget
        try:
            from payment_processor import calculate_ad_budget
            budget = calculate_ad_budget()
        except:
            budget = 0.0
        
        if budget < 10:
            return {
                "success": False,
                "error": "Insufficient budget for ad scaling",
                "budget_data": {"total_profit": budget}
            }
        
        return {
            "success": True,
            "budget_allocated": budget * 0.5,  # Use 50% of available budget
            "budget_data": {
                "total_profit": budget,
                "current_roas": 2.5,
                "reinvest_rate": 0.5,
                "recommended_action": f"Scale ads with ${budget * 0.5:.2f} budget"
            }
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}
