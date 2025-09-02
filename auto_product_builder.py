import os
import requests
import json
from datetime import datetime
from typing import Dict, List, Optional
import shopify
from google_trends_tool import fetch_google_trends, fetch_related_queries
from payment_processor import StripeProcessor
from profit_tracker import post_profit, log_profit
from config import XANO_BASE_URL, STRIPE_SECRET_KEY
from llm_helper import chat

class AutoProductBuilder:
    """Automatically generate and launch products based on market demand"""

    def __init__(self):
        self.xano_url = XANO_BASE_URL
        self.min_trend_score = 20  # Lowered for testing - was 50
        self.min_profitability = 10.0  # Lowered for testing - was 15.0

    def analyze_market_trends(self, niche: str = None) -> List[Dict]:
        """Analyze trends to find profitable product opportunities with real-time scanning"""
        try:
            print("🔍 SCANNING INTERNET FOR TRENDING PRODUCTS...")

            # Get current trending searches first
            from google_trends_tool import get_trending_searches
            trending_searches = get_trending_searches()
            print(f"📊 Found {len(trending_searches)} current trending searches")

            # Get trending keywords
            if niche:
                keywords = [niche, f"{niche} tools", f"best {niche}", f"{niche} automation"]
            else:
                keywords = ["AI tools", "automation", "productivity", "business tools", "online course"]

            # Add trending searches that match business opportunities
            business_trending = [search for search in trending_searches
                               if any(word in search.lower() for word in ["business", "money", "online", "AI", "tool", "course", "app"])]
            keywords.extend(business_trending[:5])  # Add top 5 business-related trending searches

            trending_products = []

            for keyword in keywords:
                try:
                    print(f"🔍 Analyzing trend: {keyword}")
                    trend_data = fetch_google_trends(keyword, "today 3-m")

                    if not trend_data.get("error"):
                        avg_interest = trend_data.get("avg_interest", 0)
                        print(f"📊 {keyword}: {avg_interest}/100 interest score")

                        # Lower threshold for trending searches
                        threshold = 15 if keyword in business_trending else self.min_trend_score

                        if avg_interest >= threshold:
                            # Get related queries for more ideas
                            related = fetch_related_queries(keyword)

                            product_idea = self.generate_product_from_trend(keyword, trend_data, related)
                            if product_idea:
                                trending_products.append(product_idea)
                        else:
                            print(f"⚠️ {keyword} below threshold ({avg_interest} < {self.min_trend_score})")
                    else:
                        print(f"❌ Error fetching {keyword}: {trend_data.get('error')}")

                except Exception as e:
                    print(f"❌ Error analyzing {keyword}: {e}")
                    continue

            print(f"🎯 Found {len(trending_products)} opportunities above threshold")
            return trending_products[:5]  # Top 5 opportunities

        except Exception as e:
            print(f"Error analyzing trends: {e}")
            return []

    def generate_product_from_trend(self, keyword: str, trend_data: Dict, related_data: Dict) -> Optional[Dict]:
        """Generate product idea from trend data"""
        try:
            avg_interest = trend_data.get("avg_interest", 0)
            max_interest = trend_data.get("max_interest", 0)

            # Calculate demand score
            demand_score = (avg_interest + max_interest) / 2

            if demand_score < self.min_trend_score:
                return None

            # Generate product based on keyword
            product_templates = {
                "AI": {
                    "title": f"AI {keyword.replace('AI', '').strip()} Master Course",
                    "price": 97.00,
                    "type": "digital_course"
                },
                "automation": {
                    "title": f"{keyword.title()} Automation Blueprint",
                    "price": 67.00,
                    "type": "digital_guide"
                },
                "business": {
                    "title": f"Complete {keyword.title()} System",
                    "price": 127.00,
                    "type": "business_course"
                },
                "productivity": {
                    "title": f"Ultimate {keyword.title()} Toolkit",
                    "price": 47.00,
                    "type": "toolkit"
                }
            }

            # Match template based on keyword
            template_key = next((k for k in product_templates.keys() if k.lower() in keyword.lower()), "business")
            template = product_templates[template_key]

            # Generate description
            description = self.generate_product_description(keyword, demand_score)

            # Calculate profitability forecast
            estimated_sales = max(5, int(demand_score / 10))  # Conservative estimate
            profit_forecast = (template["price"] * 0.85) * estimated_sales  # 85% profit margin

            return {
                "keyword": keyword,
                "title": template["title"],
                "description": description,
                "price": template["price"],
                "type": template["type"],
                "demand_score": round(demand_score, 1),
                "estimated_sales": estimated_sales,
                "profit_forecast": round(profit_forecast, 2),
                "related_keywords": [q.get("query", "") for q in related_data.get("top_queries", [])[:3]],
                "created_at": datetime.now().isoformat()
            }

        except Exception as e:
            print(f"Error generating product: {e}")
            return None

    def generate_product_description(self, keyword: str, demand_score: float) -> str:
        """Generate compelling product description"""
        templates = [
            f"Master {keyword} with our comprehensive system. Proven strategies used by top professionals.",
            f"Transform your {keyword} results with this step-by-step blueprint. Get instant access to proven methods.",
            f"Unlock the secrets of {keyword} success. Complete training system with templates and tools included.",
            f"The ultimate {keyword} resource. Everything you need to succeed in one complete package."
        ]

        base_desc = templates[int(demand_score) % len(templates)]

        features = [
            "✅ Step-by-step video training",
            "✅ Downloadable templates and tools",
            "✅ 30-day money-back guarantee",
            "✅ Instant digital delivery",
            "✅ Lifetime access and updates"
        ]

        return f"{base_desc}\n\n" + "\n".join(features)

    def launch_to_platforms(self, product: Dict) -> Dict:
        """Launch product to multiple platforms"""
        results = {"product": product, "platforms": {}}

        try:
            # Launch to Stripe
            stripe_result = self.launch_to_stripe(product)
            results["platforms"]["stripe"] = stripe_result

            # Launch to Gumroad
            gumroad_result = self.launch_to_gumroad(product)
            results["platforms"]["gumroad"] = gumroad_result

            # Launch to Shopify (if configured)
            shopify_result = self.launch_to_shopify(product)
            results["platforms"]["shopify"] = shopify_result

            # Save to Xano
            xano_result = self.save_to_xano(product, results)
            results["xano_saved"] = xano_result

            return results

        except Exception as e:
            results["error"] = str(e)
            return results

    def launch_to_stripe(self, product: Dict) -> Dict:
        """Launch product to Stripe"""
        try:
            if not STRIPE_SECRET_KEY:
                return {"success": False, "error": "Stripe not configured"}

            result = StripeProcessor.create_product(
                name=product["title"],
                description=product["description"],
                price=product["price"]
            )

            if result.get("success"):
                print(f"✅ Stripe product created: {product['title']}")
                return result
            else:
                return {"success": False, "error": result.get("error")}

        except Exception as e:
            return {"success": False, "error": str(e)}

    def launch_to_gumroad(self, product: Dict) -> Dict:
        """Launch product to Gumroad - DISABLED"""
        return {"success": False, "error": "Using Shopify only"}

    def launch_to_shopify(self, product: Dict) -> Dict:
        """Launch product to Shopify"""
        try:
            shop_url = os.getenv("SHOPIFY_DOMAIN")
            access_token = os.getenv("SHOPIFY_API_ACCESS_TOKEN")

            if not all([shop_url, access_token]):
                return {"success": False, "error": "Shopify not configured"}

            session = shopify.Session(shop_url, "2023-10", access_token)
            shopify.ShopifyResource.activate_session(session)

            shopify_product = shopify.Product()
            shopify_product.title = product["title"]
            shopify_product.body_html = product["description"].replace("\n", "<br>")
            shopify_product.vendor = "AI CEO Auto-Builder"
            shopify_product.product_type = product["type"]
            shopify_product.variants = [shopify.Variant({"price": product["price"]})]

            if shopify_product.save():
                print(f"✅ Shopify product created: {product['title']}")
                return {
                    "success": True,
                    "product_id": shopify_product.id,
                    "admin_url": f"https://{shop_url}/admin/products/{shopify_product.id}"
                }
            else:
                return {"success": False, "error": "Failed to save to Shopify"}

        except Exception as e:
            return {"success": False, "error": str(e)}

    def save_to_xano(self, product: Dict, launch_results: Dict) -> bool:
        """Save product metadata to Xano"""
        try:
            payload = {
                **product,
                "launch_results": json.dumps(launch_results),
                "status": "active",
                "auto_generated": True
            }

            response = requests.post(f"{self.xano_url}/products", json=payload, timeout=10)

            if response.status_code in [200, 201]:
                print(f"✅ Product saved to Xano: {product['title']}")
                return True
            else:
                print(f"❌ Failed to save to Xano: {response.status_code}")
                return False

        except Exception as e:
            print(f"Error saving to Xano: {e}")
            return False

    def run_auto_builder(self, niche: str = None) -> Dict:
        """Run the complete auto product builder pipeline"""
        try:
            print("🚀 Starting Auto Product Builder...")

            # Analyze market trends
            opportunities = self.analyze_market_trends(niche)

            if not opportunities:
                return {"success": False, "message": "No profitable opportunities found"}

            launched_products = []
            total_profit_forecast = 0.0

            # Launch top 2 products
            for product in opportunities[:2]:
                if product["profit_forecast"] >= self.min_profitability:
                    print(f"🎯 Launching product: {product['title']}")

                    launch_result = self.launch_to_platforms(product)
                    launched_products.append(launch_result)
                    total_profit_forecast += product["profit_forecast"]

                    # Log potential profit
                    log_profit(
                        amount=product["profit_forecast"],
                        source=f"Auto Product: {product['title']}",
                        ai_task_id=f"auto_product_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                    )

            result = {
                "success": True,
                "products_launched": len(launched_products),
                "total_profit_forecast": round(total_profit_forecast, 2),
                "opportunities_found": len(opportunities),
                "launched_products": launched_products
            }

            print(f"✅ Auto Product Builder completed: {result['products_launched']} products launched")
            return result

        except Exception as e:
            return {"success": False, "error": str(e)}

# Auto-run function
def run_auto_product_builder(niche: str = None) -> Dict:
    """Run the auto product builder"""
    builder = AutoProductBuilder()
    return builder.run_auto_builder(niche)

if __name__ == "__main__":
    print("🏗️ Testing Auto Product Builder...")
    result = run_auto_product_builder("AI business")
    print("Result:", json.dumps(result, indent=2))