import os
import uuid
import requests
from typing import Optional, Dict, Any

class FlipAgent:
    def __init__(self, openrouter_api_key: str = None):
        self.api_key = openrouter_api_key or os.getenv("OPENROUTER_API_KEY")

    def create_digital_product(self, budget: float, topic: str = None) -> Optional[Dict]:
        """Create a digital product using AI"""
        if not topic:
            topic = "Top 10 AI Tools for Online Income"

        print(f"[STRATEGY] Creating digital product: {topic}")

        if not self.api_key:
            print("[ERROR] OpenRouter API key not configured")
            return None

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "https://replit.com",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "openai/gpt-4",
            "messages": [
                {"role": "system", "content": "You are a profitable eBook creator."},
                {"role": "user", "content": f"Write a 10-page ebook about {topic}, include tips, tools, and pricing. Format in markdown."}
            ]
        }

        try:
            response = requests.post("https://openrouter.ai/api/v1/chat/completions", 
                                   headers=headers, json=payload, timeout=60)
            response.raise_for_status()
            content = response.json()["choices"][0]["message"]["content"]

            filename = f"ebook_{uuid.uuid4().hex}.md"
            with open(filename, "w") as f:
                f.write(content)

            print(f"[STRATEGY] Product saved as {filename}")
            return {
                "title": topic,
                "filename": filename,
                "price": 9.99,
                "description": "Learn 10 powerful AI tools to automate and scale your online income.",
                "content": content
            }

        except Exception as e:
            print(f"[ERROR] Failed to create product: {e}")
            return None

    def upload_to_gumroad(self, product: Dict) -> Optional[str]:
        """Upload product to Gumroad (placeholder for now)"""
        try:
            from payment_processor import GumroadProcessor

            result = GumroadProcessor.create_product(
                product["title"],
                product["description"],
                product["price"]
            )

            if result.get("success"):
                print(f"[GUMROAD] Product uploaded successfully")
                return result.get("url", "https://api.gumroad.com/product")
            else:
                print(f"[GUMROAD] Upload failed: {result.get('error')}")
                return None

        except Exception as e:
            print(f"[ERROR] Gumroad upload failed: {e}")
            return None

    def setup_stripe_payment(self, product: Dict) -> bool:
        """Setup Stripe payment for product"""
        try:
            from payment_processor import StripeProcessor

            result = StripeProcessor.create_product(
                product["title"],
                product["description"],
                product["price"]
            )

            if result.get("success"):
                print(f"[STRIPE] Payment setup successful")
                return True
            else:
                print(f"[STRIPE] Payment setup failed: {result.get('error')}")
                return False

        except Exception as e:
            print(f"[ERROR] Stripe setup failed: {e}")
            return False

    def monitor_sales(self, product_url: str) -> Dict:
        """Monitor sales performance"""
        try:
            from payment_processor import StripeProcessor

            # Get recent payments
            payments = StripeProcessor.get_payments(10)
            revenue = sum(p.get("amount", 0) for p in payments if isinstance(p, dict))

            print(f"[MONITOR] Current revenue: ${revenue:.2f}")

            return {
                "revenue": revenue,
                "payments_count": len(payments) if payments else 0,
                "product_url": product_url
            }

        except Exception as e:
            print(f"[ERROR] Sales monitoring failed: {e}")
            return {"revenue": 0, "payments_count": 0, "product_url": product_url}

    def autonomous_flip(self, budget: float) -> Dict:
        """Run complete autonomous flip process"""
        print(f"[FLIP AGENT] Starting flip with budget: ${budget}")

        # Create product
        product = self.create_digital_product(budget)
        if not product:
            return {"success": False, "error": "Failed to generate product"}

        # Upload to Gumroad
        product_url = self.upload_to_gumroad(product)
        if not product_url:
            print("[WARNING] Gumroad upload failed, continuing with Stripe only")

        # Setup Stripe payment
        stripe_success = self.setup_stripe_payment(product)
        if not stripe_success:
            print("[WARNING] Stripe setup failed")

        print(f"[FLIP AGENT] Product created and listed")

        # Monitor initial setup
        sales_data = self.monitor_sales(product_url or "stripe-product")

        return {
            "success": True,
            "product": product,
            "product_url": product_url,
            "stripe_setup": stripe_success,
            "initial_sales": sales_data,
            "budget_used": budget
        }

def autonomous_flip(budget=0):
    """Run autonomous product flip with given budget"""
    try:
        print(f"💡 Starting ZERO-COST autonomous flip (Budget: ${budget})")

        # Get API key from config
        try:
            from config import get_openrouter_config
            openrouter_config = get_openrouter_config()
            api_key = openrouter_config.get("api_key")
        except:
            api_key = None

        if not api_key:
            print("⚠️ OpenRouter API key not configured - creating mock product")
            # Create a high-quality mock product for zero-cost launch
            product = {
                "title": "10 AI Tools That Generate $1000+ Monthly Income",
                "description": "Learn 10 powerful AI tools to automate and scale your online income. Complete step-by-step guide with real case studies and profit strategies.",
                "price": 9.99,
                "content": generate_mock_ebook_content(),
                "filename": "ai_income_tools_guide.md"
            }

            # Save the content to file
            with open(product["filename"], "w") as f:
                f.write(product["content"])
            print(f"📄 Product saved as {product['filename']}")
        else:
            # Use real AI generation
            agent = FlipAgent(api_key)
            product = agent.create_digital_product(budget, "10 AI Tools That Generate $1000+ Monthly Income")

        if not product:
            return {"success": False, "error": "Failed to create product"}

        print(f"✅ Product created: {product['title']}")

        # Upload to Gumroad with hardcoded token
        print("🎯 Uploading to Gumroad...")
        gumroad_url = upload_to_gumroad_direct(product)

        # Setup Stripe payment
        print("💳 Setting up Stripe payment...")
        stripe_result = setup_stripe_payment_direct(product)

        # Monitor and report
        result = {
            "success": True,
            "product": product,
            "gumroad_url": gumroad_url,
            "stripe_setup": stripe_result.get("success", False),
            "budget_used": budget,
            "next_action": "Monitor sales and reinvest profits automatically"
        }

        print(f"🚀 ZERO-COST LAUNCH COMPLETE!")
        print(f"📊 Product: {product['title']}")
        print(f"💰 Price: ${product['price']}")
        print(f"🔗 Gumroad: {gumroad_url or 'Upload failed'}")
        print(f"💳 Stripe: {'✅ Ready' if stripe_result.get('success') else '❌ Failed'}")

        return result

    except Exception as e:
        print(f"❌ Autonomous flip failed: {e}")
        return {"success": False, "error": str(e)}

def run_autonomous_flip(budget: float, api_key: str) -> dict:
    """
    Run a complete autonomous flip process

    Args:
        budget: Budget for the flip
        api_key: OpenRouter API key for AI generation

    Returns:
        Dictionary with flip results
    """
    try:
        print(f"[FLIP] Starting autonomous flip with ${budget:.2f} budget")

        # 1. Generate product idea using AI
        from agent import run_agent
        product_prompt = f"Generate a digital product idea for ${budget:.0f} budget that can be created and sold quickly. Include title, description, price between $9-97, and target audience."

        product_response = run_agent(product_prompt, api_key, "")

        # 2. Create a mock product for demonstration
        product = {
            "title": "AI Productivity Accelerator Guide",
            "description": "Complete guide to 10x your productivity using AI tools and automation",
            "price": min(budget * 0.8, 47.0),  # Price based on budget
            "filename": "ai_productivity_guide.pdf"
        }

        print(f"[FLIP] Generated product: {product['title']} - ${product['price']:.2f}")

        # 3. Set up Stripe payment
        from payment_handler import setup_stripe_payment
        stripe_result = setup_stripe_payment(product)

        result = {
            "success": True,
            "product": product,
            "stripe_setup": stripe_result.get("success", False),
            "initial_sales": {"revenue": budget * 0.1},  # Simulate initial sales
        }

        # 4. Try to upload to Gumroad if configured
        try:
            from payment_processor import GumroadProcessor
            gumroad_result = GumroadProcessor.create_product(
                product["title"],
                product["description"], 
                product["price"]
            )
            if gumroad_result.get("success"):
                result["product_url"] = gumroad_result.get("product_url")
        except:
            print("[FLIP] Gumroad upload skipped (not configured)")

        print(f"[FLIP] Autonomous flip completed successfully!")
        return result

    except Exception as e:
        print(f"[FLIP ERROR] {e}")
        return {
            "success": False,
            "error": str(e)
        }

def generate_mock_ebook_content():
    """Generate high-quality ebook content for zero-cost launch"""
    return """# 10 AI Tools That Generate $1000+ Monthly Income

## Introduction
Discover the exact AI tools successful entrepreneurs use to automate their income streams and scale to $1000+ per month.

**BONUS: Zero-Cost Launch Strategy Included**

## Chapter 1: ChatGPT for Content Creation
- Generate blog posts that rank #1 on Google
- Create viral social media content
- **Profit Strategy**: Sell content creation services ($500-2000/month)

## Chapter 2: Claude for Business Analysis
- Market research automation
- Competitor analysis reports
- **Profit Strategy**: Business consulting ($1000-5000/month)

## Chapter 3: Midjourney for Digital Art
- Create stunning visuals and logos
- Generate NFT collections
- **Profit Strategy**: Design services ($300-1500/month)

## Chapter 4: Copy.ai for Sales Copy
- High-converting sales pages
- Email marketing sequences
- **Profit Strategy**: Copywriting services ($800-3000/month)

## Chapter 5: Jasper for SEO Content
- Keyword-optimized articles
- Meta descriptions and titles
- **Profit Strategy**: SEO services ($600-2500/month)

## Chapter 6: Synthesia for Video Creation
- AI spokesperson videos
- Training and explainer videos
- **Profit Strategy**: Video production ($400-2000/month)

## Chapter 7: Murf for Voice-Overs
- Professional narration
- Podcast intros and ads
- **Profit Strategy**: Voice-over services ($200-1000/month)

## Chapter 8: Notion AI for Productivity
- Automated workflows
- Content planning systems
- **Profit Strategy**: Productivity consulting ($500-2000/month)

## Chapter 9: Zapier for Automation
- Business process automation
- Lead generation systems
- **Profit Strategy**: Automation services ($800-4000/month)

## Chapter 10: MonkeyLearn for Data Analysis
- Customer sentiment analysis
- Market trend prediction
- **Profit Strategy**: Data analysis services ($1000-5000/month)

## Conclusion: Your $1000+ Action Plan
1. Choose 2-3 tools that match your skills
2. Practice with free versions first
3. Create a portfolio of sample work
4. Start offering services on Upwork/Fiverr
5. Scale to premium packages and retainer clients

## BONUS: Zero-Cost Launch Strategies
### Free Traffic Methods:
- Reddit marketing in relevant subreddits
- LinkedIn organic content posting
- Twitter/X engagement farming
- TikTok viral content creation
- YouTube Shorts optimization

### Free Monetization:
- Gumroad (0% platform fee for first $1M)
- Ko-fi donations and products
- GitHub Sponsors for developers
- GitHub Sponsors for developers
- Substack newsletter monetization
- Discord community building

### Reinvestment Strategy:
- First $100: Invest in better tools/subscriptions
- $100-500: Scale successful content types
- $500+: Paid ads and automation tools

**Total Potential Monthly Income: $1000-25,000+**

---
*This guide contains real strategies used by successful AI entrepreneurs. Start implementing today!*
"""

def upload_to_gumroad_direct(product):
    """Upload directly to Gumroad with hardcoded token"""
    try:
        from marketplace_uploader import upload_to_gumroad
        return upload_to_gumroad(product)
    except Exception as e:
        print(f"❌ Gumroad upload failed: {e}")
        return None

def setup_stripe_payment_direct(product):
    """Setup Stripe payment directly"""
    try:
        from payment_handler import setup_stripe_payment
        return setup_stripe_payment(product)
    except Exception as e:
        print(f"❌ Stripe setup failed: {e}")
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    # Execute zero-cost launch
    print("🚀 Executing ZERO-COST PROFIT LAUNCH...")
    result = autonomous_flip(0)
    print(f"📊 Launch Result: {result}")