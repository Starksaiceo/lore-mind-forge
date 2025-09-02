
import time
from datetime import datetime
from typing import Dict, List
import json

from web_scanner import scan_for_trending_products
from store_builder import build_automated_store
from agent_logic import create_digital_product
from marketplace_uploader import upload_product_to_shopify
from ai_memory_system import record_ai_experience, get_ai_recommendations, get_ai_intelligence
from marketing_tools.ad_writer import generate_ad_copy
from marketing_tools.email_generator import generate_email_sequence
from profit_tracker import log_profit, get_total_revenue

class FullAutomationController:
    """Master controller for 100% automated business operations"""
    
    def __init__(self):
        self.running = False
        self.cycle_count = 0
        self.total_revenue = 0.0
        self.products_created = 0
        self.campaigns_launched = 0
        
    def run_full_automation_cycle(self) -> Dict:
        """Run one complete automation cycle"""
        cycle_start = time.time()
        self.cycle_count += 1
        
        results = {
            "cycle_number": self.cycle_count,
            "success": False,
            "steps_completed": [],
            "products_created": 0,
            "stores_built": 0,
            "campaigns_launched": 0,
            "revenue_generated": 0.0,
            "duration": 0.0,
            "errors": []
        }
        
        try:
            print(f"\n🚀 === FULL AUTOMATION CYCLE #{self.cycle_count} ===")
            print(f"⏰ Started at: {datetime.now().strftime('%H:%M:%S')}")
            
            # STEP 1: Scan for trending products
            print("\n🔍 Step 1: Scanning for trending products...")
            trending_products = scan_for_trending_products()
            
            if trending_products:
                results["steps_completed"].append(f"Found {len(trending_products)} trending opportunities")
                print(f"✅ Found {len(trending_products)} trending opportunities")
                
                # Get AI recommendations for best opportunities
                best_opportunities = self.rank_opportunities_with_ai(trending_products)
                
            else:
                results["errors"].append("No trending products found")
                print("❌ No trending products found")
                return results
            
            # STEP 2: Create digital products for top opportunities
            print("\n🎯 Step 2: Creating digital products...")
            created_products = []
            
            for opportunity in best_opportunities[:3]:  # Top 3 opportunities
                try:
                    # Use AI memory to optimize product creation
                    context = {
                        "niche": opportunity.get("trend", "unknown"),
                        "price": opportunity.get("suggested_price", 47.00),
                        "keywords": [opportunity.get("trend", "")]
                    }
                    
                    ai_rec = get_ai_recommendations("product_creation", context)
                    
                    # Create product based on opportunity
                    product = create_digital_product(opportunity, opportunity.get("trend", "business"))
                    
                    if product:
                        created_products.append(product)
                        results["products_created"] += 1
                        print(f"✅ Created: {product['title']}")
                        
                        # Record experience for AI learning
                        record_ai_experience("product_creation", context, {
                            "success": True,
                            "product_id": product.get("title"),
                            "revenue_generated": 0.0  # Will be updated later
                        })
                    
                except Exception as e:
                    results["errors"].append(f"Product creation error: {str(e)}")
                    print(f"❌ Product creation error: {e}")
            
            results["steps_completed"].append(f"Created {len(created_products)} products")
            
            # STEP 3: Build automated stores
            print("\n🏪 Step 3: Building automated stores...")
            store_results = []
            
            # Group products by niche for store building
            niches = {}
            for product in created_products:
                niche = product.get("category", "business")
                if niche not in niches:
                    niches[niche] = []
                niches[niche].append(product)
            
            for niche, products in niches.items():
                try:
                    store_result = build_automated_store(niche, products)
                    if store_result.get("success"):
                        store_results.append(store_result)
                        results["stores_built"] += 1
                        print(f"✅ Built store for {niche}: {store_result.get('products_added', 0)} products")
                except Exception as e:
                    results["errors"].append(f"Store building error: {str(e)}")
                    print(f"❌ Store building error: {e}")
            
            results["steps_completed"].append(f"Built {len(store_results)} automated stores")
            
            # STEP 4: Upload products to marketplace
            print("\n📦 Step 4: Uploading to marketplace...")
            upload_results = []
            
            for product in created_products:
                try:
                    upload_result = upload_product_to_shopify(product)
                    if upload_result.get("success"):
                        upload_results.append(upload_result)
                        print(f"✅ Uploaded: {product['title']}")
                except Exception as e:
                    results["errors"].append(f"Upload error: {str(e)}")
                    print(f"❌ Upload error: {e}")
            
            results["steps_completed"].append(f"Uploaded {len(upload_results)} products")
            
            # STEP 5: Create and launch marketing campaigns
            print("\n📢 Step 5: Creating marketing campaigns...")
            campaign_results = []
            
            for product in created_products:
                try:
                    # Generate ad copy
                    ad_copy = generate_ad_copy(
                        product_name=product["title"],
                        target_audience=f"{product.get('category', 'business')} professionals",
                        key_benefits=["High quality", "Instant download", "Proven strategies"]
                    )
                    
                    # Generate email sequence
                    email_sequence = generate_email_sequence(
                        product_name=product["title"],
                        target_audience=f"{product.get('category', 'business')} enthusiasts"
                    )
                    
                    campaign_results.append({
                        "product": product["title"],
                        "ad_copy": ad_copy,
                        "email_sequence": email_sequence,
                        "status": "launched"
                    })
                    
                    results["campaigns_launched"] += 1
                    print(f"✅ Campaign created for: {product['title']}")
                    
                except Exception as e:
                    results["errors"].append(f"Campaign error: {str(e)}")
                    print(f"❌ Campaign error: {e}")
            
            results["steps_completed"].append(f"Launched {len(campaign_results)} marketing campaigns")
            
            # STEP 6: Update revenue tracking
            print("\n💰 Step 6: Updating revenue tracking...")
            try:
                current_revenue = get_total_revenue()
                revenue_increase = current_revenue - self.total_revenue
                self.total_revenue = current_revenue
                results["revenue_generated"] = revenue_increase
                
                # Log potential profit from new products
                estimated_profit = len(created_products) * 47.00 * 0.1  # Conservative estimate
                log_profit(
                    amount=estimated_profit,
                    source=f"Automation Cycle {self.cycle_count}",
                    ai_task_id=f"auto_cycle_{self.cycle_count}"
                )
                
                print(f"✅ Revenue updated: +${revenue_increase:.2f}")
                
            except Exception as e:
                results["errors"].append(f"Revenue tracking error: {str(e)}")
                print(f"❌ Revenue tracking error: {e}")
            
            # STEP 7: Update AI intelligence
            print("\n🧠 Step 7: Updating AI intelligence...")
            try:
                intelligence = get_ai_intelligence()
                print(f"✅ AI Intelligence: {intelligence.get('total_experiences', 0)} experiences recorded")
                results["steps_completed"].append("AI intelligence updated")
            except Exception as e:
                results["errors"].append(f"AI intelligence error: {str(e)}")
                print(f"❌ AI intelligence error: {e}")
            
            # Calculate cycle results
            cycle_duration = time.time() - cycle_start
            results["duration"] = round(cycle_duration, 2)
            results["success"] = len(results["errors"]) == 0
            
            print(f"\n🎉 Cycle {self.cycle_count} completed in {cycle_duration:.1f}s")
            print(f"📊 Results: {results['products_created']} products, {results['campaigns_launched']} campaigns")
            
            return results
            
        except Exception as e:
            results["errors"].append(f"Cycle error: {str(e)}")
            results["duration"] = time.time() - cycle_start
            print(f"❌ Cycle {self.cycle_count} failed: {e}")
            return results
    
    def rank_opportunities_with_ai(self, opportunities: List[Dict]) -> List[Dict]:
        """Rank opportunities using AI intelligence"""
        try:
            ranked = []
            
            for opp in opportunities:
                context = {
                    "niche": opp.get("trend", ""),
                    "price": opp.get("suggested_price", 47.00),
                    "keywords": [opp.get("trend", "")]
                }
                
                ai_rec = get_ai_recommendations("product_creation", context)
                
                # Calculate ranking score
                score = opp.get("interest_score", 0)
                
                if ai_rec.get("recommendation") == "use_pattern":
                    score += ai_rec.get("expected_success_rate", 0) * 50
                
                opp["ai_score"] = score
                ranked.append(opp)
            
            # Sort by AI score
            ranked.sort(key=lambda x: x.get("ai_score", 0), reverse=True)
            return ranked
            
        except Exception as e:
            print(f"AI ranking error: {e}")
            return opportunities
    
    def start_continuous_automation(self, max_cycles: int = None) -> Dict:
        """Start continuous automation cycles"""
        print("\n🤖 === STARTING FULL AUTOMATION SYSTEM ===")
        print("🎯 Goal: 100% automated business operations")
        print("🔄 Scanning → Creating → Building → Selling → Advertising")
        print("🧠 AI learning and optimization enabled")
        
        self.running = True
        cycles_completed = 0
        total_results = {
            "total_cycles": 0,
            "total_products": 0,
            "total_stores": 0,
            "total_campaigns": 0,
            "total_revenue": 0.0,
            "cycle_results": []
        }
        
        try:
            while self.running:
                if max_cycles and cycles_completed >= max_cycles:
                    break
                
                # Run automation cycle
                cycle_result = self.run_full_automation_cycle()
                total_results["cycle_results"].append(cycle_result)
                
                # Update totals
                total_results["total_cycles"] += 1
                total_results["total_products"] += cycle_result.get("products_created", 0)
                total_results["total_stores"] += cycle_result.get("stores_built", 0)
                total_results["total_campaigns"] += cycle_result.get("campaigns_launched", 0)
                total_results["total_revenue"] += cycle_result.get("revenue_generated", 0.0)
                
                cycles_completed += 1
                
                # Wait before next cycle (1 hour)
                if self.running and (not max_cycles or cycles_completed < max_cycles):
                    print(f"\n😴 Waiting 1 hour before next cycle...")
                    time.sleep(3600)  # 1 hour
        
        except KeyboardInterrupt:
            print("\n⏹️ Automation stopped by user")
        except Exception as e:
            print(f"\n❌ Automation error: {e}")
        
        self.running = False
        
        print(f"\n🏁 Full automation completed:")
        print(f"📊 Total: {total_results['total_cycles']} cycles")
        print(f"🎯 Created: {total_results['total_products']} products")
        print(f"🏪 Built: {total_results['total_stores']} stores")
        print(f"📢 Launched: {total_results['total_campaigns']} campaigns")
        print(f"💰 Revenue: ${total_results['total_revenue']:.2f}")
        
        return total_results
    
    def stop_automation(self):
        """Stop the automation system"""
        self.running = False
        print("🛑 Stopping full automation system...")

# Global automation controller
automation_controller = FullAutomationController()

def start_full_automation(max_cycles: int = None) -> Dict:
    """Start the full automation system"""
    return automation_controller.start_continuous_automation(max_cycles)

def stop_full_automation():
    """Stop the full automation system"""
    automation_controller.stop_automation()

def run_single_automation_cycle() -> Dict:
    """Run a single automation cycle for testing"""
    return automation_controller.run_full_automation_cycle()
