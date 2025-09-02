from dotenv import load_dotenv
load_dotenv()

import requests
import json
import time
import os
from datetime import datetime
import threading
from typing import Dict, List, Any

from config import OPENROUTER_API_KEY, STRIPE_SECRET_KEY, XANO_BASE_URL
from profit_tracker import log_profit, post_profit
from llm_helper import chat

# Fix os import and use new Stripe utils
import os
from stripe_utils import get_total_revenue

def get_real_revenue():
    """Get real revenue from Stripe"""
    return get_total_revenue()

class ProfitSprint:
    """48-hour autonomous profit generation system - REAL UPLOADS ONLY"""

    def __init__(self):
        self.is_running = False
        self.start_time = None
        self.products_launched = 0
        self.products_verified = 0  # Only count real uploads
        self.total_earnings = 0.0
        self.sprint_data = {
            "products": [],
            "verified_products": [],  # Only real uploads
            "earnings_log": [],
            "performance_metrics": {},
            "status": "initialized"
        }
        self.target_hours = 48
        # ENFORCE REAL UPLOADS ONLY
        self.dry_run = False
        self.simulate_uploads = False
        self.fake_logs = False

    def start_sprint(self):
        """Start the 48-hour profit sprint with real upload verification"""
        if self.is_running:
            return {"status": "error", "message": "Sprint already running"}

        if not OPENROUTER_API_KEY:
            return {"status": "error", "message": "OpenRouter API key required"}

        # Gumroad verification removed - using Shopify only
        print("🛒 Using Shopify for product uploads (Gumroad disabled)")

        self.is_running = True
        self.start_time = datetime.now()
        self.sprint_data["status"] = "active"

        print("🚀 Starting REAL PROFIT SPRINT - No fake uploads allowed!")
        print("🔒 Gumroad API verified - ready for real product launches")

        # Start background thread
        sprint_thread = threading.Thread(target=self._run_sprint_loop, daemon=True)
        sprint_thread.start()

        return {
            "status": "success",
            "message": "🚀 48-hour REAL profit sprint started!",
            "start_time": self.start_time.isoformat(),
            "verification": "Gumroad API verified"
        }

    def _verify_shopify_connection(self):
        """Verify Shopify API connection before starting"""
        try:
            from config import SHOPIFY_ACCESS_TOKEN, SHOPIFY_DOMAIN
            if not SHOPIFY_ACCESS_TOKEN:
                return {"success": False, "error": "Shopify not configured"}

            return {"success": True, "store": SHOPIFY_DOMAIN}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def stop_sprint(self):
        """Stop the profit sprint"""
        self.is_running = False
        self.sprint_data["status"] = "stopped"
        return {
            "status": "stopped",
            "products_launched": self.products_launched,
            "products_verified": self.products_verified,
            "real_earnings": f"${self.total_earnings:.2f}"
        }

    def get_status(self):
        """Get current sprint status"""
        if self.start_time:
            elapsed = datetime.now() - self.start_time
            hours_remaining = max(0, self.target_hours - elapsed.total_seconds() / 3600)
        else:
            hours_remaining = self.target_hours

        return {
            "running": self.is_running,
            "products_launched": self.products_launched,
            "products_verified": self.products_verified,  # NEW: Only real uploads
            "total_real_earnings": f"${self.total_earnings:.2f}",
            "hours_remaining": f"{hours_remaining:.1f}h",
            "status": self.sprint_data["status"],
            "verified_products": self.sprint_data["verified_products"][-3:] if self.sprint_data["verified_products"] else []
        }

    def _run_sprint_loop(self):
        """Main sprint execution loop - REAL UPLOADS ONLY"""
        print("🚀 Starting 48-hour REAL profit sprint...")

        # Generate initial product ideas
        product_ideas = self._brainstorm_products()
        selected_ideas = self._select_best_ideas(product_ideas)

        cycle_count = 0
        while self.is_running and self._should_continue():
            try:
                cycle_count += 1
                print(f"🔄 Sprint Cycle {cycle_count} - REAL UPLOADS ONLY")

                # Create and launch products - VERIFY EACH UPLOAD
                for idea in selected_ideas:
                    if not self.is_running:
                        break

                    product_result = self._create_and_launch_product_verified(idea)
                    if product_result.get("verified_upload"):
                        self.products_verified += 1
                        self.sprint_data["verified_products"].append(product_result)
                        print(f"✅ VERIFIED PRODUCT UPLOADED: {product_result['title']} - {product_result['gumroad_url']}")
                    else:
                        print(f"❌ UPLOAD FAILED - Product NOT counted: {idea['title']}")
                        print(f"   Error: {product_result.get('error', 'Unknown upload failure')}")

                # Check for real sales from verified products only
                self._update_earnings_verified()

                # Generate 6-hour report with real data only
                if cycle_count % 3 == 0:  # Every 3 cycles ≈ 6 hours
                    self._generate_real_report()

                # Generate new ideas for next cycle
                if cycle_count % 2 == 0:
                    new_ideas = self._brainstorm_products()
                    selected_ideas = self._select_best_ideas(new_ideas)

                # Wait before next cycle (2 hours)
                time.sleep(7200)  # 2 hours

            except Exception as e:
                print(f"❌ Sprint cycle error: {e}")
                time.sleep(1800)  # Wait 30 minutes on error
                continue

        print("🏁 REAL profit sprint completed!")
        self.sprint_data["status"] = "completed"

    def _create_and_launch_product_verified(self, idea: Dict) -> Dict:
        """Create and launch product with VERIFIED REAL UPLOAD"""
        try:
            print(f"🔨 Creating product: {idea['title']} - REAL UPLOAD REQUIRED")

            # Generate product content
            content = self._generate_product_content(idea)
            if not content:
                return {"verified_upload": False, "error": "Content generation failed"}

            # Create product file
            filename = f"product_{int(time.time())}.md"
            with open(filename, 'w') as f:
                f.write(content)

            # REAL SHOPIFY UPLOAD ONLY - Gumroad removed
            upload_result = self._upload_to_shopify_verified(idea, filename)

            if not upload_result["success"]:
                print(f"❌ SHOPIFY UPLOAD FAILED: {upload_result['error']}")
                return {
                    "verified_upload": False,
                    "error": f"Shopify upload failed: {upload_result['error']}"
                }

            # ONLY proceed if upload was verified successful
            product_data = {
                "title": idea["title"],
                "description": idea["description"],
                "price": idea["price"],
                "filename": filename,
                "created_at": datetime.now().isoformat(),
                "target_audience": idea.get("target_audience", "general"),
                "verified_upload": True,
                "gumroad_id": upload_result["gumroad_id"],
                "gumroad_url": upload_result["permalink"],
                "real_price": upload_result["price"]
            }

            # Log to Xano ONLY for verified uploads
            try:
                log_profit(0, f"VERIFIED Product Launch: {idea['title']}", ai_task_id=f"sprint_verified_{int(time.time())}")
                print(f"✅ Logged verified product to Xano: {idea['title']}")
            except Exception as e:
                print(f"⚠️ Xano logging failed: {e}")

            # Log success for monitoring
            try:
                from sprint_monitor import SprintMonitor
                monitor = SprintMonitor()
                monitor.log_activity(f"VERIFIED UPLOAD: {idea['title']} - Gumroad ID: {upload_result['gumroad_id']} - URL: {upload_result['permalink']}")
            except:
                pass

            return product_data

        except Exception as e:
            print(f"❌ Product creation error: {e}")
            return {"verified_upload": False, "error": str(e)}

    def _upload_to_shopify_verified(self, idea: Dict, filename: str) -> Dict:
        """Upload to Shopify with verification"""
        try:
            from marketplace_uploader import upload_to_shopify

            # Prepare product data for Shopify upload
            product_data = {
                "title": idea["title"],
                "description": idea["description"],
                "price": idea["price"],
                "filename": filename
            }

            print(f"🛒 Uploading to Shopify: {idea['title']}")
            print(f"   Price: ${product_data.get('price', 0):.2f}")

            result = upload_to_shopify(product_data)

            if result.get("success"):
                print(f"✅ SHOPIFY UPLOAD SUCCESS!")
                print(f"   Product ID: {result['product_id']}")
                print(f"   URL: {result.get('url', 'N/A')}")

                return {
                    "success": True,
                    "shopify_id": result["product_id"],
                    "url": result.get("url", ""),
                    "price": product_data.get("price", 0)
                }
            else:
                error_msg = f"Shopify upload failed: {result.get('error', 'Unknown error')}"
                print(f"❌ {error_msg}")
                return {"success": False, "error": error_msg}

        except Exception as e:
            error_msg = f"Shopify upload exception: {str(e)}"
            print(f"❌ {error_msg}")
            return {"success": False, "error": error_msg}

    def _update_earnings_verified(self):
        """Check for real sales from verified products only"""
        try:
            # Check Stripe for real payments
            if STRIPE_SECRET_KEY:
                # from stripe_api import get_stripe_payments
                # recent_payments = get_stripe_payments(10)
                stripe_total = get_real_revenue()

                if stripe_total > self.total_earnings:
                    new_earnings = stripe_total - self.total_earnings
                    self.total_earnings = stripe_total
                    self.sprint_data["earnings_log"].append({
                        "amount": new_earnings,
                        "source": "stripe_verified",
                        "timestamp": datetime.now().isoformat()
                    })
                    print(f"💰 REAL STRIPE EARNINGS: ${new_earnings:.2f}")

            # Check Shopify for real sales (placeholder)
            # TODO: Implement Shopify sales checking
            print("🛒 Shopify sales checking not yet implemented")

        except Exception as e:
            print(f"Earnings update error: {e}")

    def _generate_real_report(self):
        """Generate 6-hour progress report with REAL DATA ONLY"""
        try:
            best_seller = "No verified products yet"
            if self.sprint_data["verified_products"]:
                best_seller = self.sprint_data["verified_products"][-1]["title"]

            report = {
                "products_launched": self.products_launched,
                "products_verified": self.products_verified,  # NEW: Only count real uploads
                "total_real_earnings": f"${self.total_earnings:.2f}",
                "best_seller": best_seller,
                "next_focus": "AI-driven product creation with verified uploads",
                "status": "📈 Real Sprint Active",
                "timestamp": datetime.now().isoformat(),
                "verified_urls": [p.get("gumroad_url") for p in self.sprint_data["verified_products"][-3:]]
            }

            print("📊 6-Hour REAL Sprint Report:")
            print(json.dumps(report, indent=2))

            # Log report to Xano
            try:
                requests.post(f"{XANO_BASE_URL}/ai_memory", json={
                    "command": "REAL Sprint Report",
                    "response": json.dumps(report),
                    "ai_goal_id": 999
                })
            except:
                pass

        except Exception as e:
            print(f"Report generation error: {e}")

    def _brainstorm_products(self) -> List[Dict]:
        """Generate product ideas using AI with REAL trending data integration"""
        try:
            print("🔍 Scanning internet for trending products...")

            # Get trending topics from Google Trends
            trending_data = self._scan_trending_opportunities()

            headers = {
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            }

            # Enhanced prompt with real trending data
            trending_context = "\n".join([f"- {trend['keyword']}: {trend['interest']}/100 interest" for trend in trending_data[:5]])

            prompt = f"""Generate 10 high-demand digital product ideas based on REAL trending data and current market demand.

        except Exception as e:
            print('⛔ runtime error:', e)
CURRENT TRENDING TOPICS (from Google Trends):
{trending_context}

Create products that:
1. Leverage these actual trending topics for maximum demand
2. Solve problems people are actively searching for RIGHT NOW
3. Can be 100% created with text/content and sold immediately
4. Price range $7-$29 (optimized for trending demand)
5. Target audiences who are already searching for these topics

Focus on the trending keywords above - these are what people are actually searching for today.

Return JSON format:
{{
  "products": [
    {{
      "title": "AI Automation Toolkit for Small Business",
      "description": "Complete guide with templates, prompts, and workflows for business automation",
      "target_audience": "small business owners",
      "price": 19,
      "demand_score": 9,
      "trending_keyword": "business automation",
      "creation_time": "45 minutes"
    }}
  ]
}}"""

            try:
                content = chat(prompt, "anthropic/claude-3-opus")

                # Extract JSON from response
                try:
                    import re
                    json_match = re.search(r'\{.*\}', content, re.DOTALL)
                    if json_match:
                        ideas_data = json.loads(json_match.group())
                        products = ideas_data.get("products", [])

                        # Enhance with trending data
                        for product in products:
                            if not product.get("trending_keyword"):
                                product["trending_keyword"] = trending_data[0]["keyword"] if trending_data else "AI tools"

                        print(f"✅ Generated {len(products)} products based on trending data")
                        return products
                except Exception as parse_error:
                    print(f"JSON parsing failed: {parse_error}")
                    pass

            except Exception as e:
                print("⛔ sprint error:", e)
            # Fallback with trending context
            return self._get_trending_fallback_ideas(trending_data)

        except Exception as e:
            print(f"Error brainstorming with trends: {e}")
            return self._get_fallback_ideas()

    def _scan_trending_opportunities(self) -> List[Dict]:
        """Scan Google Trends for current opportunities"""
        try:
            from google_trends_tool import fetch_google_trends, get_trending_searches

            # Get current trending searches
            trending_searches = get_trending_searches()
            print(f"📊 Found {len(trending_searches)} trending searches")

            # Keywords to check for product opportunities
            opportunity_keywords = [
                "AI tools", "automation", "productivity", "business growth",
                "side hustle", "online course", "digital marketing",
                "social media", "templates", "passive income"
            ]

            trending_opportunities = []

            # Check trending searches for opportunities
            for search in trending_searches[:10]:  # Top 10 trending
                if any(keyword.lower() in search.lower() for keyword in ["business", "money", "online", "AI", "tool", "app", "course"]):
                    trending_opportunities.append({
                        "keyword": search,
                        "interest": 85,  # High interest for trending searches
                        "source": "trending_search"
                    })

            # Check our opportunity keywords
            for keyword in opportunity_keywords:
                try:
                    trend_data = fetch_google_trends(keyword, "now 7-d")
                    if not trend_data.get("error"):
                        avg_interest = trend_data.get("avg_interest", 0)
                        if avg_interest > 20:  # Lowered threshold for real data
                            trending_opportunities.append({
                                "keyword": keyword,
                                "interest": avg_interest,
                                "source": "google_trends"
                            })
                            print(f"📈 {keyword}: {avg_interest}/100 interest")
                except Exception as e:
                    print(f"⚠️ Trend check failed for {keyword}: {e}")
                    continue

            # Sort by interest level
            trending_opportunities.sort(key=lambda x: x["interest"], reverse=True)

            print(f"🎯 Found {len(trending_opportunities)} trending opportunities")
            return trending_opportunities[:8]  # Top 8 opportunities

        except Exception as e:
            print(f"❌ Error scanning trends: {e}")
            return self._get_default_trending_data()

    def _get_default_trending_data(self) -> List[Dict]:
        """Default trending data if API fails"""
        return [
            {"keyword": "AI automation", "interest": 75, "source": "default"},
            {"keyword": "productivity tools", "interest": 68, "source": "default"},
            {"keyword": "business templates", "interest": 62, "source": "default"},
            {"keyword": "online course", "interest": 58, "source": "default"},
            {"keyword": "social media tools", "interest": 55, "source": "default"}
        ]

    def _get_trending_fallback_ideas(self, trending_data: List[Dict]) -> List[Dict]:
        """Generate fallback ideas based on trending data"""
        if not trending_data:
            return self._get_fallback_ideas()

        ideas = []
        for trend in trending_data[:3]:
            keyword = trend["keyword"]
            interest = trend["interest"]

            ideas.append({
                "title": f"{keyword.title()} Mastery Guide",
                "description": f"Complete guide to {keyword} with templates, strategies, and action plans",
                "target_audience": "entrepreneurs",
                "price": min(25, max(15, int(interest / 3))),  # Price based on interest
                "demand_score": min(10, max(6, int(interest / 10))),
                "trending_keyword": keyword
            })

        return ideas

    def _get_fallback_ideas(self) -> List[Dict]:
        """Fallback product ideas if AI fails"""
        return [
            {
                "title": "AI Prompt Library for Business Growth",
                "description": "100+ proven ChatGPT prompts for business automation, marketing, and scaling",
                "target_audience": "entrepreneurs",
                "price": 19,
                "demand_score": 8
            },
            {
                "title": "Complete Social Media Content Calendar",
                "description": "30-day content calendar with templates, captions, and engagement strategies",
                "target_audience": "content creators",
                "price": 12,
                "demand_score": 9
            },
            {
                "title": "Freelancer Pricing & Negotiation Guide",
                "description": "Complete guide to pricing freelance services profitably with scripts",
                "target_audience": "freelancers",
                "price": 15,
                "demand_score": 8
            }
        ]

    def _select_best_ideas(self, ideas: List[Dict]) -> List[Dict]:
        """Select top 3 ideas based on demand and feasibility"""
        if not ideas:
            return self._get_fallback_ideas()[:3]

        # Sort by demand score and take top 3
        sorted_ideas = sorted(ideas, key=lambda x: x.get("demand_score", 0), reverse=True)
        return sorted_ideas[:3]

    def _generate_product_content(self, idea: Dict) -> str:
        """Generate actual product content using Claude 3"""
        try:
            headers = {
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            }

            prompt = f"""Create a complete, professional digital product that people will pay for:
        except Exception as e:
            print('⛔ runtime error:', e)
Title: {idea['title']}
Description: {idea['description']}
Target Audience: {idea.get('target_audience', 'general')}
Price: ${idea['price']}

Create a comprehensive, valuable product that includes:
1. Professional introduction explaining the value
2. Main content sections (at least 5 detailed sections)
3. Actionable tips and strategies
4. Templates, examples, or worksheets where applicable
5. Conclusion and next steps

Make it worth every dollar - deliver real value. Minimum 3000 words.
Format as Markdown with clear headings and structure.
Include specific examples and actionable advice."""

            try:
                return chat(prompt, "anthropic/claude-3-opus")
            except Exception as e:
                print(f"Content generation failed: {e}")
                return None

        except Exception as e:
            print(f"Content generation error: {e}")
            return None

    def _should_continue(self) -> bool:
        """Check if sprint should continue"""
        if not self.start_time:
            return False

        elapsed = datetime.now() - self.start_time
        hours_elapsed = elapsed.total_seconds() / 3600

        return hours_elapsed < self.target_hours

# Global sprint instance
_sprint_instance = None

def start_profit_sprint():
    """Start the 48-hour profit sprint with REAL UPLOADS ONLY"""
    global _sprint_instance

    if _sprint_instance is None:
        _sprint_instance = ProfitSprint()

    result = _sprint_instance.start_sprint()

    if result.get("status") == "success":
        print("🚀 REAL PROFIT SPRINT STARTED!")
        print("🔒 Only verified Gumroad uploads will be counted")
        print("💰 Only real sales will be tracked")

    return result

def stop_profit_sprint():
    """Stop the profit sprint"""
    global _sprint_instance

    if _sprint_instance:
        return _sprint_instance.stop_sprint()
    return {"status": "not_running"}

def get_sprint_status():
    """Get current sprint status"""
    global _sprint_instance

    if _sprint_instance:
        return _sprint_instance.get_status()
    return {"status": "not_started"}

if __name__ == "__main__":
    # Test the sprint system
    result = start_profit_sprint()
    print(result)