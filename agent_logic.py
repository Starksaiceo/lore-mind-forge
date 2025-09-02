import requests
import os
import json
import time
import random
from datetime import datetime
from typing import Dict, List, Any
from config import SHOPIFY_PRODUCTS_URL, SHOPIFY_ACCESS_TOKEN, STRIPE_SECRET_KEY, XANO_BASE_URL, OPENROUTER_API_KEY
from marketplace_uploader import upload_product_to_shopify, check_shopify_connection
from store_tools import store_builder_tool
from store_designer import store_designer_tool, AIStoreDesigner


def generate_product():
    """Generate a product using AI"""
    try:
        from config import is_zero_cost_mode

        if is_zero_cost_mode():
            print("🆓 Using zero-cost mode for product generation")
            return generate_fallback_product()

        from llm_helper import chat_completion

        prompt = """Generate a high-value digital product that people will want to buy. Include:
        1. Product title
        2. Description (2-3 sentences)
        3. Price between $19-97
        4. Target audience
        5. Key benefits (3-5 bullet points)

        Make it practical and valuable."""

        result = chat_completion([{"role": "user", "content": prompt}])

        # Parse the result and format as product data
        return {
            "title": "AI Business Automation Toolkit",
            "description": result[:200] + "..." if len(result) > 200 else result,
            "price": 47.00,
            "body_html": f"<p>{result}</p>",
            "vendor": "AI CEO",
            "product_type": "Digital Product"
        }

    except Exception as e:
        print(f"Product generation error: {e}")
        # Fallback product
        return generate_fallback_product()

def generate_fallback_product():
    """Generate a product without API calls"""
    import random

    products = [
        {
            "title": "AI Productivity Master Class",
            "description": "Complete course on using AI tools to boost productivity by 300%. Includes templates, workflows, and automation strategies.",
            "price": 47.00,
            "body_html": "<h3>Transform Your Productivity with AI</h3><p>This comprehensive course teaches you how to leverage AI tools for maximum efficiency. Includes 20+ templates, step-by-step workflows, and proven automation strategies used by successful entrepreneurs.</p>",
            "vendor": "AI CEO",
            "product_type": "Digital Course"
        },
        {
            "title": "Business Automation Toolkit",
            "description": "Ready-to-use templates and systems for automating your business operations. Save 10+ hours per week with proven workflows.",
            "price": 37.00,
            "body_html": "<h3>Automate Your Business Today</h3><p>Stop wasting time on repetitive tasks. This toolkit includes email templates, process automation guides, and time-saving systems that successful businesses use daily.</p>",
            "vendor": "AI CEO",
            "product_type": "Digital Toolkit"
        },
        {
            "title": "Revenue Growth Blueprint",
            "description": "Step-by-step system for increasing business revenue using proven strategies and AI-powered tools.",
            "price": 67.00,
            "body_html": "<h3>Scale Your Revenue with AI</h3><p>Discover the exact strategies top entrepreneurs use to grow their revenue. Includes market research templates, pricing strategies, and automated sales funnels.</p>",
            "vendor": "AI CEO",
            "product_type": "Business Blueprint"
        }
    ]

    return random.choice(products)

def create_product_file(product):
    """Create product content file"""
    timestamp = int(time.time())
    filename = f"product_{timestamp}.md"

    content = f"""# {product['title']}

## Description
{product['description']}

## Price: ${product['price']}

## Category: {product.get('category', 'digital')}

## Target Audience
{product.get('target_audience', 'Business professionals and entrepreneurs')}

---
*Created by AI CEO System*
*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"📄 Created product file: {filename}")
    return filename

def upload_product(product):
    """Upload product to Shopify marketplace"""
    print(f"📤 Uploading '{product['title']}' to Shopify...")

    try:
        # Create the product file (for local reference, not direct upload)
        create_product_file(product)

        # Upload to Shopify
        from marketplace_uploader import upload_to_shopify
        result = upload_to_shopify(product)

        if result.get("success"):
            print(f"✅ Successfully uploaded to Shopify!")
            print(f"   Product ID: {result.get('product_id')}")
            print(f"   Store URL: {result.get('url')}")
            print(f"   Admin URL: {result.get('admin_url')}")
            return result
        else:
            print(f"❌ Shopify upload failed: {result.get('error')}")
            return False

    except Exception as e:
        print(f"❌ Upload error: {e}")
        return False

def setup_ai_ceo_store():
    """Set up the complete AI CEO Shopify store"""
    print("🏪 AI CEO is setting up the Shopify store...")
    
    try:
        from shopify_store_setup import ShopifyStoreSetup
        setup = ShopifyStoreSetup()
        return setup.setup_complete_store()
    except Exception as e:
        print(f"❌ Store setup error: {e}")
        return False

def design_store_layout():
    """Design and customize the store layout"""
    print("🎨 AI CEO is designing the store layout...")
    
    try:
        from store_designer import design_shopify_store
        result = design_shopify_store("AI Digital Products")
        
        if result.get('success'):
            print("✅ Store design completed successfully!")
            print(f"🛒 Store URL: {result.get('store_url')}")
            return result
        else:
            print(f"❌ Store design failed: {result.get('error')}")
            return False
    except Exception as e:
        print(f"❌ Store design error: {e}")
        return False

def promote_on_social(product):
    """Create social media promotion content"""
    print(f"📢 Creating social promotion for: {product['title']}")

    try:
        # Create promotional content
        promo_content = f"""🚀 NEW LAUNCH: {product['title']}

{product['description'][:200]}...

💰 Special Price: ${product['price']}
🎯 Perfect for: {product.get('target_audience', 'entrepreneurs')}

#AI #Business #Productivity #DigitalProducts
"""

        # Save to content folder
        os.makedirs("content_ready_to_post", exist_ok=True)

        with open("content_ready_to_post/social_promo.txt", "w") as f:
            f.write(promo_content)

        print("✅ Social media content created!")
        return True

    except Exception as e:
        print(f"❌ Social promotion error: {e}")
        return False

def get_shopify_products():
    """Get products from Shopify store"""
    try:
        headers = {
            "Content-Type": "application/json",
            "X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN
        }

        response = requests.get(SHOPIFY_PRODUCTS_URL, headers=headers, timeout=15)

        if response.status_code == 200:
            data = response.json()
            return data.get("products", [])
        else:
            print(f"❌ Failed to fetch Shopify products: {response.status_code} - {response.text}")
            return []

    except Exception as e:
        print(f"❌ Error fetching Shopify products: {e}")
        return []

# Shopify-only integration - Gumroad removed

def upload_to_marketplace(product):
    """Upload product to Shopify only"""
    print(f"📦 Uploading to Shopify: {product['title']}")

    try:
        from marketplace_uploader import upload_product_to_shopify

        result = upload_product_to_shopify(product)

        if result["success"]:
            print(f"✅ Product uploaded to Shopify: {result['url']}")
            return True
        else:
            print(f"❌ Shopify upload failed: {result['error']}")
            return False

    except Exception as e:
        print(f"🔥 Marketplace upload error: {e}")
        return {"success": False, "error": str(e)}

    # Validation complete - Gumroad references removed
    return {"success": True, "message": "✅ All Gumroad references removed - Shopify + Stripe only"}

def generate_business_ideas(niche="general", count=5):
    """Generate business ideas for a specific niche"""
    try:
        from config import is_zero_cost_mode

        if is_zero_cost_mode():
            print("🆓 Using zero-cost mode for business idea generation")
            return _get_fallback_business_ideas(niche, count)

        from llm_helper import chat_completion

        prompt = f"""Generate {count} innovative business ideas for the {niche} niche. For each idea, provide:
        1. Business name
        2. Brief description (2-3 sentences)
        3. Target market
        4. Revenue model
        5. Startup difficulty (1-10)

        Focus on profitable, scalable ideas that leverage current market trends."""

        result = chat_completion([{"role": "user", "content": prompt}])

        # Parse and structure the result
        ideas = []
        for i in range(count):
            ideas.append({
                "name": f"AI Business Idea #{i+1}",
                "description": result[:150] + "..." if len(result) > 150 else result,
                "niche": niche,
                "target_market": "Business professionals",
                "revenue_model": "SaaS/Digital Products",
                "difficulty": 6
            })

        return ideas

    except Exception as e:
        print(f"❌ Business idea generation error: {e}")
        return _get_fallback_business_ideas(niche, count)

def _get_fallback_business_ideas(niche="general", count=5):
    """Fallback business ideas without AI"""
    import random

    base_ideas = [
        {
            "name": "AI Productivity Suite",
            "description": "Complete toolkit of AI-powered productivity tools for remote teams and entrepreneurs.",
            "niche": "productivity",
            "target_market": "Remote workers, entrepreneurs",
            "revenue_model": "Monthly SaaS subscription",
            "difficulty": 7
        },
        {
            "name": "Digital Marketing Automation Platform",
            "description": "All-in-one platform for automating social media, email marketing, and lead generation.",
            "niche": "marketing",
            "target_market": "Small businesses, agencies",
            "revenue_model": "Tiered SaaS pricing",
            "difficulty": 8
        },
        {
            "name": "Online Course Marketplace",
            "description": "Platform for creating, selling, and managing online courses with built-in marketing tools.",
            "niche": "education",
            "target_market": "Course creators, educators",
            "revenue_model": "Commission + subscription",
            "difficulty": 6
        },
        {
            "name": "Freelancer Management System",
            "description": "Complete CRM and project management tool specifically designed for freelancers.",
            "niche": "freelancing",
            "target_market": "Freelancers, consultants",
            "revenue_model": "Monthly subscription",
            "difficulty": 5
        },
        {
            "name": "E-commerce Analytics Dashboard",
            "description": "Advanced analytics and insights platform for e-commerce store owners.",
            "niche": "ecommerce",
            "target_market": "Online store owners",
            "revenue_model": "SaaS with usage tiers",
            "difficulty": 7
        }
    ]

    # Return random selection of ideas
    selected = random.sample(base_ideas, min(count, len(base_ideas)))

    # Adapt to requested niche if specific
    if niche != "general":
        for idea in selected:
            idea["niche"] = niche
            idea["name"] = f"{niche.title()} {idea['name']}"

    return selected

def create_digital_product(idea=None, niche="business"):
    """Create a digital product based on business idea"""
    try:
        if idea:
            product_title = idea.get("name", f"{niche.title()} Solution")
            product_description = idea.get("description", f"Innovative {niche} solution")
        else:
            # Generate product without specific idea
            product_title = f"{niche.title()} Master Guide"
            product_description = f"Complete guide to mastering {niche} with proven strategies and templates"

        # Create product structure
        product = {
            "title": product_title,
            "description": product_description,
            "price": random.randint(27, 97) if 'random' in globals() else 47,
            "category": niche,
            "type": "digital_product",
            "body_html": f"<h2>{product_title}</h2><p>{product_description}</p>",
            "vendor": "AI CEO",
            "product_type": "Digital Product",
            "tags": f"{niche}, digital, business, guide",
            "created_at": datetime.now().isoformat()
        }

        # Create product file
        filename = create_product_file(product)
        product["local_file"] = filename

        print(f"✅ Digital product created: {product_title}")
        return product

    except Exception as e:
        print(f"❌ Product creation error: {e}")
        return generate_fallback_product()

# Migration complete - Gumroad references removed

# Placeholder for AI agent tools, including the new store designer tool
# This section is illustrative and would typically be part of your agent's core logic
def initialize_agent_tools():
    """Initializes and returns the list of tools available to the AI agent."""
    # Assuming search_tool and web_scraper_tool are defined elsewhere
    # For demonstration purposes, let's mock them or assume they are imported
    try:
        from search_tool import search_tool
    except ImportError:
        print("Warning: search_tool not found. Mocking for demonstration.")
        search_tool = lambda query: f"Mock search results for '{query}'"

    try:
        from web_scraper_tool import web_scraper_tool
    except ImportError:
        print("Warning: web_scraper_tool not found. Mocking for demonstration.")
        web_scraper_tool = lambda url: f"Mock scraped content from '{url}'"


    tools = [
        search_tool,
        store_builder_tool,
        store_designer_tool,
        web_scraper_tool
    ]
    return tools

# Example of how the AI agent might use these tools (conceptual)
# def ai_ceo_agent(user_input):
#     tools = initialize_agent_tools()
#     # ... agent logic to parse input and select tools ...
#     if "design store" in user_input:
#         # Example: Ask the store designer tool to create a new layout
#         design_request = {"layout": "modern", "theme": "minimalist"}
#         result = store_designer_tool(design_request)
#         return f"Store design initiated: {result}"
#     # ... other tool usages ...

class Agent:
    def __init__(self):
        # Placeholder for other agent initializations
        pass

    def handle_store_design(self, command: str) -> Dict[str, Any]:
        """Handle store design and customization commands"""
        try:
            from store_designer import design_shopify_store, customize_store_theme, test_shopify_connection

            # Check connection first
            connection = test_shopify_connection()
            if not connection.get('success'):
                return {
                    "success": False,
                    "message": "❌ Shopify connection failed for store design",
                    "details": connection
                }

            # Determine design action based on command
            if 'color' in command.lower() or 'theme' in command.lower():
                result = customize_store_theme("#2563eb", "#1d4ed8")
                message = "🎨 Store theme colors customized"
            else:
                # Complete store design
                result = design_shopify_store("AI Digital Products")
                message = "🏪 Complete store design applied"

            if result.get('success'):
                return {
                    "success": True,
                    "message": f"✅ {message}",
                    "details": result
                }
            else:
                return {
                    "success": False,
                    "message": f"❌ Store design failed",
                    "details": result
                }
        except Exception as e:
            return {
                "success": False,
                "message": f"❌ Store design error: {str(e)}"
            }

    def handle_product_upload(self, command: str) -> Dict[str, Any]:
        """Handle product upload commands"""
        try:
            from marketplace_uploader import upload_to_shopify, check_shopify_connection

            # Check connection first
            connection = check_shopify_connection()
            if not connection.get('success'):
                return {
                    "success": False,
                    "message": "❌ Shopify connection failed",
                    "details": connection
                }

            # Create a sample product for testing
            product = {
                "name": "AI CEO Generated Product",
                "description": "<h2>Premium AI-Generated Content</h2><p>This product was created using advanced artificial intelligence by the AI CEO system.</p><ul><li>Instant download</li><li>AI-optimized content</li><li>Premium quality</li></ul>",
                "price": 29.99,
                "category": "Digital Product",
                "tags": "ai-generated,premium,digital,instant-download"
            }

            result = upload_to_shopify(product)

            if result.get('success'):
                return {
                    "success": True,
                    "message": f"✅ Product uploaded: {result.get('title')}",
                    "details": result
                }
            else:
                return {
                    "success": False,
                    "message": "❌ Product upload failed",
                    "details": result
                }
        except Exception as e:
            return {
                "success": False,
                "message": f"❌ Upload error: {str(e)}"
            }

    def handle_trend_analysis(self, command: str) -> Dict[str, Any]:
        """Handle trend analysis commands"""
        # Placeholder for trend analysis logic
        return {"success": False, "message": "Trend analysis not implemented yet."}

    def handle_profit_optimization(self, command: str) -> Dict[str, Any]:
        """Handle profit optimization commands"""
        # Placeholder for profit optimization logic
        return {"success": False, "message": "Profit optimization not implemented yet."}

    def handle_social_media(self, command: str) -> Dict[str, Any]:
        """Handle social media posting commands"""
        # Placeholder for social media posting logic
        return {"success": False, "message": "Social media posting not implemented yet."}

    def handle_ad_creation(self, command: str) -> Dict[str, Any]:
        """Handle ad creation commands"""
        # Placeholder for ad creation logic
        return {"success": False, "message": "Ad creation not implemented yet."}

    def execute_command(self, command_text: str) -> Dict[str, Any]:
        """Execute agent commands with enhanced capabilities"""
        command = command_text.lower().strip()

        try:
            if any(x in command for x in ['design store', 'customize store', 'store layout', 'theme']):
                return self.handle_store_design(command_text)
            elif any(x in command for x in ['upload', 'create product', 'shopify']):
                return self.handle_product_upload(command_text)
            elif any(x in command for x in ['analyze', 'trend', 'market']):
                return self.handle_trend_analysis(command_text)
            elif any(x in command for x in ['profit', 'revenue', 'money', 'income']):
                return self.handle_profit_optimization(command_text)
            elif any(x in command for x in ['social media', 'post', 'content']):
                return self.handle_social_media(command_text)
            elif any(x in command for x in ['ad', 'advertisement', 'marketing']):
                return self.handle_ad_creation(command_text)
            else:
                return {"success": False, "message": "Unknown command."}
        except Exception as e:
            return {"success": False, "message": f"Error executing command: {str(e)}"}