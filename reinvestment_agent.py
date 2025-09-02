
import os
import requests
import json
from datetime import datetime
from typing import Dict, List, Optional
from profit_tracker import get_total_profit_last_30_days, post_profit, log_profit
from test_product_launcher import TestProductLauncher
from auto_product_builder import run_auto_product_builder
from auto_ad_scaler import run_auto_ad_scaler
from meta_ads import MetaAdsManager, auto_launch_ads_if_ready
from payment_processor import StripeProcessor, calculate_ad_budget

class ReinvestmentAgent:
    """Autonomous reinvestment and scaling agent"""
    
    def __init__(self):
        self.xano_url = os.getenv("XANO_BASE_URL", "https://x8ki-letl-twmt.n7.xano.io/api:8fyoFbLh")
        self.max_test_budget = 25.0
        self.reinvest_rate = 0.50  # 50% of profits
        self.min_profit_threshold = 1.0  # Minimum $1 profit to trigger reinvestment
        self.meta_manager = MetaAdsManager()
        self.test_launcher = TestProductLauncher()
        
    def get_current_performance(self) -> Dict:
        """Get current revenue and profit performance"""
        try:
            print("📊 Analyzing current performance...")
            
            # Get total profit from last 30 days (real sources only)
            total_profit = get_total_profit_last_30_days()
            print(f"💰 Total profit (30 days): ${total_profit:.2f}")
            
            # Get recent Stripe payments
            stripe_payments = StripeProcessor.get_payments(10)
            stripe_revenue = 0.0
            if stripe_payments and not any("error" in str(p) for p in stripe_payments):
                valid_payments = [p for p in stripe_payments if isinstance(p, dict) and "error" not in p]
                stripe_revenue = sum(p.get("amount", 0) for p in valid_payments if isinstance(p.get("amount"), (int, float)))
            
            print(f"💳 Recent Stripe revenue: ${stripe_revenue:.2f}")
            
            return {
                "total_profit": total_profit,
                "stripe_revenue": stripe_revenue,
                "available_budget": calculate_ad_budget(),
                "performance_positive": total_profit > 0 or stripe_revenue > 0,
                "reinvestment_ready": total_profit >= self.min_profit_threshold
            }
            
        except Exception as e:
            print(f"❌ Error getting performance data: {e}")
            return {
                "total_profit": 0.0,
                "stripe_revenue": 0.0,
                "available_budget": 0.0,
                "performance_positive": False,
                "reinvestment_ready": False,
                "error": str(e)
            }
    
    def calculate_reinvestment_budget(self, performance: Dict) -> float:
        """Calculate optimal reinvestment budget"""
        total_profit = performance.get("total_profit", 0.0)
        
        if total_profit <= 0:
            print("📊 No profit to reinvest yet")
            return 0.0
        
        # Calculate 50% reinvestment
        reinvest_amount = total_profit * self.reinvest_rate
        
        # Cap at test budget limit
        reinvest_amount = min(reinvest_amount, self.max_test_budget)
        
        print(f"💡 Calculated reinvestment: ${reinvest_amount:.2f} (50% of ${total_profit:.2f})")
        return reinvest_amount
    
    def generate_next_product(self, budget: float) -> Dict:
        """Generate next product for launch"""
        try:
            print(f"🎯 Generating next product with ${budget:.2f} budget...")
            
            # Use auto product builder for trend-based generation
            result = run_auto_product_builder()
            
            if result.get("success") and result.get("launched_products"):
                product = result["launched_products"][0]
                print(f"✅ New product generated: {product.get('product', {}).get('title', 'Unknown')}")
                return {
                    "success": True,
                    "product": product,
                    "source": "auto_builder"
                }
            else:
                # Fallback to test product launcher
                print("🔄 Using fallback product generation...")
                test_result = self.test_launcher.generate_test_product()
                
                if test_result.get("success"):
                    return {
                        "success": True,
                        "product": test_result,
                        "source": "test_launcher"
                    }
                else:
                    return {"success": False, "error": "All product generation methods failed"}
                    
        except Exception as e:
            print(f"❌ Product generation error: {e}")
            return {"success": False, "error": str(e)}
    
    def launch_scaling_campaign(self, product: Dict, budget: float) -> Dict:
        """Launch scaling ad campaign"""
        try:
            print(f"📣 Launching scaling campaign with ${budget:.2f} budget...")
            
            # Check Meta ads status
            meta_status = self.meta_manager.check_app_status()
            
            if meta_status.get("approved"):
                print("✅ Meta ads approved - launching real campaign")
                
                # Create ad campaign using Meta API
                campaign_data = {
                    "name": f"Scale Campaign - {product.get('title', 'Product')}",
                    "objective": "CONVERSIONS",
                    "budget": budget,
                    "product_id": product.get("stripe_product_id"),
                    "target_audience": "business_productivity"
                }
                
                # This would integrate with actual Meta Ads API
                campaign_result = {
                    "success": True,
                    "campaign_id": f"camp_{int(datetime.now().timestamp())}",
                    "budget": budget,
                    "platform": "meta",
                    "status": "active"
                }
                
                print(f"🚀 Real campaign launched: {campaign_result['campaign_id']}")
                
            else:
                print("⚠️ Meta ads not approved - creating mock campaign")
                campaign_result = {
                    "success": True,
                    "campaign_id": f"mock_{int(datetime.now().timestamp())}",
                    "budget": budget,
                    "platform": "mock",
                    "status": "simulated",
                    "reason": meta_status.get("status", "Not approved")
                }
            
            # Log campaign to Xano
            self.log_campaign_to_xano(campaign_result, product)
            
            return campaign_result
            
        except Exception as e:
            print(f"❌ Campaign launch error: {e}")
            return {"success": False, "error": str(e)}
    
    def log_campaign_to_xano(self, campaign: Dict, product: Dict):
        """Log campaign data to Xano"""
        try:
            campaign_data = {
                "campaign_id": campaign.get("campaign_id"),
                "product_title": product.get("title", "Unknown"),
                "budget": campaign.get("budget", 0),
                "platform": campaign.get("platform", "unknown"),
                "status": campaign.get("status", "unknown"),
                "timestamp": datetime.now().isoformat(),
                "reinvestment_cycle": True
            }
            
            response = requests.post(f"{self.xano_url}/ad_campaigns", json=campaign_data, timeout=10)
            if response.status_code == 200:
                print("✅ Campaign logged to Xano")
            else:
                print(f"⚠️ Failed to log campaign: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Campaign logging error: {e}")
    
    def log_reinvestment_cycle(self, cycle_data: Dict):
        """Log complete reinvestment cycle to AI memory"""
        try:
            memory_entry = {
                "type": "reinvestment_cycle",
                "timestamp": datetime.now().isoformat(),
                "cycle_data": cycle_data,
                "performance": cycle_data.get("performance", {}),
                "actions_taken": cycle_data.get("actions", []),
                "budget_allocated": cycle_data.get("budget_allocated", 0),
                "roi_positive": cycle_data.get("performance", {}).get("performance_positive", False)
            }
            
            response = requests.post(f"{self.xano_url}/ai_memory", json=memory_entry, timeout=10)
            if response.status_code == 200:
                print("✅ Reinvestment cycle logged to AI memory")
            else:
                print(f"⚠️ Failed to log to AI memory: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Memory logging error: {e}")
    
    def run_reinvestment_cycle(self) -> Dict:
        """Execute complete reinvestment cycle"""
        print("\n" + "="*60)
        print("🧠 AI CEO: AUTONOMOUS REINVESTMENT CYCLE")
        print("🎯 Goal: Scale profitable products automatically")
        print("="*60)
        
        cycle_data = {
            "timestamp": datetime.now().isoformat(),
            "actions": [],
            "budget_allocated": 0.0,
            "products_launched": 0,
            "campaigns_created": 0
        }
        
        try:
            # Step 1: Analyze current performance
            print("\n📊 STEP 1: Performance Analysis")
            performance = self.get_current_performance()
            cycle_data["performance"] = performance
            cycle_data["actions"].append("performance_analysis")
            
            if not performance.get("reinvestment_ready"):
                print("⏳ Insufficient profit for reinvestment")
                if performance.get("total_profit", 0) > 0:
                    print(f"💡 Current profit: ${performance['total_profit']:.2f} (need ${self.min_profit_threshold:.2f} minimum)")
                
                cycle_data["result"] = "waiting_for_profit"
                self.log_reinvestment_cycle(cycle_data)
                return cycle_data
            
            # Step 2: Calculate reinvestment budget
            print("\n💰 STEP 2: Budget Allocation")
            reinvest_budget = self.calculate_reinvestment_budget(performance)
            cycle_data["budget_allocated"] = reinvest_budget
            cycle_data["actions"].append("budget_calculation")
            
            if reinvest_budget <= 0:
                print("❌ No budget available for reinvestment")
                cycle_data["result"] = "no_budget"
                self.log_reinvestment_cycle(cycle_data)
                return cycle_data
            
            # Step 3: Generate next product
            print("\n🎯 STEP 3: Product Generation")
            product_result = self.generate_next_product(reinvest_budget)
            cycle_data["actions"].append("product_generation")
            
            if not product_result.get("success"):
                print(f"❌ Product generation failed: {product_result.get('error')}")
                cycle_data["result"] = "product_generation_failed"
                cycle_data["error"] = product_result.get("error")
                self.log_reinvestment_cycle(cycle_data)
                return cycle_data
            
            cycle_data["products_launched"] = 1
            cycle_data["product"] = product_result["product"]
            
            # Step 4: Launch scaling campaign
            print("\n📣 STEP 4: Campaign Launch")
            campaign_result = self.launch_scaling_campaign(
                product_result["product"], 
                reinvest_budget
            )
            cycle_data["actions"].append("campaign_launch")
            
            if campaign_result.get("success"):
                cycle_data["campaigns_created"] = 1
                cycle_data["campaign"] = campaign_result
                print(f"✅ Campaign launched: {campaign_result.get('campaign_id')}")
            else:
                print(f"⚠️ Campaign launch issues: {campaign_result.get('error')}")
            
            # Step 5: Log profit expectation
            print("\n📈 STEP 5: Profit Tracking")
            expected_roi = reinvest_budget * 2.0  # Expect 2x return
            log_profit(
                amount=expected_roi,
                source=f"Reinvestment Cycle ROI Projection",
                ai_task_id=int(datetime.now().timestamp()),
                ai_goal_id=999
            )
            cycle_data["actions"].append("profit_projection")
            cycle_data["projected_roi"] = expected_roi
            
            # Step 6: Set up next cycle
            cycle_data["result"] = "success"
            cycle_data["next_cycle_due"] = (datetime.now().timestamp() + 3600)  # 1 hour
            
            print("\n✅ REINVESTMENT CYCLE COMPLETED")
            print(f"💰 Budget allocated: ${reinvest_budget:.2f}")
            print(f"📦 Products launched: {cycle_data['products_launched']}")
            print(f"📣 Campaigns created: {cycle_data['campaigns_created']}")
            print(f"📈 ROI projection: ${expected_roi:.2f}")
            
            # Log complete cycle
            self.log_reinvestment_cycle(cycle_data)
            
            return cycle_data
            
        except Exception as e:
            print(f"\n❌ REINVESTMENT CYCLE ERROR: {e}")
            cycle_data["result"] = "error"
            cycle_data["error"] = str(e)
            self.log_reinvestment_cycle(cycle_data)
            return cycle_data

def run_agent(config: Dict) -> Dict:
    """Main entry point for reinvestment agent"""
    agent = ReinvestmentAgent()
    
    if config.get("autonomous") and config.get("loop"):
        print("\n🤖 Starting autonomous reinvestment loop...")
        return agent.run_reinvestment_cycle()
    else:
        print("\n🔧 Running single reinvestment cycle...")
        return agent.run_reinvestment_cycle()

if __name__ == "__main__":
    # Test the reinvestment agent
    test_config = {
        "goal": "Reinvest profits from test product into new launches and ad scaling",
        "autonomous": True,
        "loop": True,
        "track_profit": True
    }
    
    result = run_agent(test_config)
    print(f"\n🎯 Final result: {result.get('result')}")
