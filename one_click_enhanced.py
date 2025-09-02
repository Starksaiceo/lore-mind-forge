import os
import time
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
import requests
from config import OPENROUTER_API_KEY, SHOPIFY_DOMAIN, SHOPIFY_ACCESS_TOKEN
from agent_session import AgentSession

# Create SHOPIFY_STORE_URL from SHOPIFY_DOMAIN for compatibility
SHOPIFY_STORE_URL = f"https://{SHOPIFY_DOMAIN}"
from marketing_tools.email_generator import generate_email_sequence
from marketing_tools.ad_writer import generate_ad_copy
import threading

class OneClickBusinessGenerator:
    """Enhanced 1-click business generator with progress tracking"""

    def __init__(self, user_id: int):
        self.user_id = user_id
        self.session = AgentSession(user_id)
        self.progress = 0
        self.status = "idle"
        self.start_time = None
        self.current_step = ""
        self.results = {}

    def generate_complete_business(self, niche: str, target_audience: str = "entrepreneurs") -> Dict[str, Any]:
        """Generate complete business with progress tracking"""
        try:
            self.start_time = datetime.utcnow()
            self.status = "running"
            self.progress = 0

            self.session.log_event("one_click_start", {
                "niche": niche,
                "target_audience": target_audience,
                "start_time": self.start_time.isoformat()
            })

            # Step 1: Generate product ideas (20%)
            self._update_progress(10, "Analyzing market trends...")
            product_ideas = self._generate_product_ideas(niche, target_audience)

            # Step 2: Create detailed products (40%)
            self._update_progress(30, "Creating detailed products...")
            products = self._create_detailed_products(product_ideas, niche)

            # Step 3: Generate marketing content (60%)
            self._update_progress(50, "Generating marketing materials...")
            marketing_content = self._generate_marketing_content(products, target_audience)

            # Step 4: Create store assets (80%)
            self._update_progress(70, "Building store assets...")
            store_assets = self._create_store_assets(products, niche)

            # Step 5: Generate business plan (90%)
            self._update_progress(85, "Creating business strategy...")
            business_plan = self._generate_business_plan(niche, products, target_audience)

            # Step 6: Finalize and package (100%)
            self._update_progress(95, "Finalizing your business...")
            final_package = self._package_business(products, marketing_content, store_assets, business_plan, niche)

            self._update_progress(100, "Complete! Your business is ready.")
            self.status = "completed"

            elapsed_seconds = (datetime.utcnow() - self.start_time).total_seconds()

            self.session.log_event("one_click_complete", {
                "niche": niche,
                "products_count": len(products),
                "marketing_assets": len(marketing_content),
                "elapsed_seconds": elapsed_seconds,
                "success": True
            })

            return final_package

        except Exception as e:
            self.status = "failed"
            self.session.log_event("one_click_failed", {"error": str(e)}, success=False)
            return {"error": str(e), "status": "failed"}

    def _update_progress(self, progress: int, step: str):
        """Update progress and current step"""
        self.progress = progress
        self.current_step = step
        print(f"🔄 {progress}% - {step}")

        # Small delay for realistic progress
        time.sleep(0.5)

    def _generate_product_ideas(self, niche: str, target_audience: str) -> List[Dict[str, Any]]:
        """Generate product ideas for the niche"""
        try:
            headers = {
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            }

            prompt = f"""Generate 5 high-demand digital product ideas for the {niche} niche targeting {target_audience}.

For each product, provide:
- title: Compelling product name
- description: Clear value proposition
- price: Competitive pricing (25-297 range)
- type: ebook|course|template|software|membership
- difficulty: beginner|intermediate|advanced
- market_demand: high|medium|low

Focus on solving real problems and providing immediate value.
Format as JSON array."""

            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json={
                    "model": "openai/gpt-3.5-turbo",
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 1500,
                    "temperature": 0.7
                },
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']

                try:
                    # Extract JSON from response
                    start_idx = content.find('[')
                    end_idx = content.rfind(']') + 1
                    if start_idx != -1 and end_idx != -1:
                        json_str = content[start_idx:end_idx]
                        products = json.loads(json_str)
                        return products[:5]
                except json.JSONDecodeError:
                    pass

            # Fallback products
            return self._create_fallback_products(niche)

        except Exception as e:
            print(f"❌ Product idea generation failed: {e}")
            return self._create_fallback_products(niche)

    def _create_fallback_products(self, niche: str) -> List[Dict[str, Any]]:
        """Create fallback products when AI fails"""
        return [
            {
                "title": f"The Ultimate {niche.title()} Guide",
                "description": f"Complete guide to mastering {niche} with proven strategies.",
                "price": 47,
                "type": "ebook",
                "difficulty": "beginner",
                "market_demand": "high"
            },
            {
                "title": f"{niche.title()} Mastery Course",
                "description": f"Step-by-step video course for {niche} success.",
                "price": 197,
                "type": "course",
                "difficulty": "intermediate",
                "market_demand": "high"
            },
            {
                "title": f"{niche.title()} Templates Pack",
                "description": f"Ready-to-use templates for {niche} professionals.",
                "price": 27,
                "type": "template",
                "difficulty": "beginner",
                "market_demand": "medium"
            }
        ]

    def _create_detailed_products(self, product_ideas: List[Dict], niche: str) -> List[Dict[str, Any]]:
        """Create detailed product specifications"""
        detailed_products = []

        for i, idea in enumerate(product_ideas[:3]):  # Top 3 products
            self._update_progress(30 + (i * 5), f"Detailing product: {idea.get('title', 'Product')}")

            detailed_product = {
                **idea,
                "id": f"product_{int(time.time())}_{i}",
                "niche": niche,
                "created_at": datetime.utcnow().isoformat(),
                "features": self._generate_product_features(idea),
                "outline": self._generate_product_outline(idea),
                "sales_copy": self._generate_sales_copy(idea),
                "tags": self._generate_product_tags(idea, niche)
            }

            detailed_products.append(detailed_product)

            # Log product creation
            self.session.log_event("product_created", {
                "product_name": idea.get('title'),
                "price": idea.get('price'),
                "type": idea.get('type'),
                "niche": niche
            })

        return detailed_products

    def _generate_product_features(self, product: Dict) -> List[str]:
        """Generate product features"""
        product_type = product.get('type', 'ebook')

        feature_templates = {
            "ebook": [
                "Comprehensive guide with actionable strategies",
                "Real-world case studies and examples",
                "Step-by-step implementation roadmap",
                "Bonus templates and worksheets",
                "Lifetime updates and revisions"
            ],
            "course": [
                "Video lessons with clear explanations",
                "Downloadable resources and materials",
                "Interactive exercises and quizzes",
                "Private community access",
                "Certificate of completion"
            ],
            "template": [
                "Ready-to-use professional templates",
                "Multiple format options (PDF, DOC, etc.)",
                "Customization instructions included",
                "Commercial use rights included",
                "24/7 download access"
            ]
        }

        return feature_templates.get(product_type, feature_templates["ebook"])

    def _generate_product_outline(self, product: Dict) -> List[str]:
        """Generate product outline/table of contents"""
        title = product.get('title', 'Product')
        product_type = product.get('type', 'ebook')

        if product_type == 'course':
            return [
                "Module 1: Foundation and Basics",
                "Module 2: Core Strategies",
                "Module 3: Advanced Techniques",
                "Module 4: Implementation Guide",
                "Module 5: Case Studies and Examples",
                "Bonus: Templates and Resources"
            ]
        else:
            return [
                "Chapter 1: Introduction and Overview",
                "Chapter 2: Getting Started",
                "Chapter 3: Core Principles",
                "Chapter 4: Advanced Strategies",
                "Chapter 5: Implementation Guide",
                "Chapter 6: Case Studies",
                "Chapter 7: Next Steps",
                "Appendix: Resources and Tools"
            ]

    def _generate_sales_copy(self, product: Dict) -> str:
        """Generate basic sales copy"""
        title = product.get('title', 'Amazing Product')
        price = product.get('price', 47)
        description = product.get('description', 'High-value product')

        return f"""🚀 {title}

{description}

✅ What You'll Get:
• Complete step-by-step system
• Proven strategies that work
• Real-world examples and case studies
• Actionable implementation guide
• Lifetime access and updates

💰 Special Launch Price: Just ${price}
(Regular price: ${price + 50})

⏰ Limited Time Offer - Don't Miss Out!

Get instant access and start transforming your results today."""

    def _generate_product_tags(self, product: Dict, niche: str) -> List[str]:
        """Generate product tags for SEO"""
        base_tags = [niche, product.get('type', 'digital'), 'guide', 'training']

        if product.get('difficulty') == 'beginner':
            base_tags.extend(['beginner', 'getting started', 'basics'])
        elif product.get('difficulty') == 'advanced':
            base_tags.extend(['advanced', 'expert', 'professional'])

        return base_tags[:10]

    def _generate_marketing_content(self, products: List[Dict], target_audience: str) -> Dict[str, Any]:
        """Generate marketing content for products"""
        marketing_content = {
            "email_sequences": [],
            "ad_campaigns": [],
            "social_posts": []
        }

        for product in products:
            self._update_progress(50 + len(marketing_content["email_sequences"]) * 5, 
                                f"Creating marketing for {product.get('title')}")

            # Generate email sequence
            try:
                email_sequence = generate_email_sequence(product, target_audience)
                marketing_content["email_sequences"].append({
                    "product_id": product.get('id'),
                    "product_name": product.get('title'),
                    "emails": email_sequence
                })
            except Exception as e:
                print(f"❌ Email generation failed: {e}")

            # Generate ad copy
            try:
                ad_copy = generate_ad_copy(product, "facebook")
                marketing_content["ad_campaigns"].append({
                    "product_id": product.get('id'),
                    "product_name": product.get('title'),
                    "platform": "facebook",
                    "ads": ad_copy
                })
            except Exception as e:
                print(f"❌ Ad generation failed: {e}")

        return marketing_content

    def _create_store_assets(self, products: List[Dict], niche: str) -> Dict[str, Any]:
        """Create store assets and branding"""
        return {
            "store_name": f"{niche.title()} Success Hub",
            "tagline": f"Your #1 Resource for {niche.title()} Success",
            "color_scheme": {
                "primary": "#2563eb",
                "secondary": "#7c3aed",
                "accent": "#f59e0b"
            },
            "logo_concept": f"Modern, professional logo incorporating {niche} elements",
            "product_images": [
                f"product_cover_{product.get('id')}.jpg" 
                for product in products
            ],
            "store_policies": {
                "return_policy": "30-day money-back guarantee",
                "privacy_policy": "We protect your privacy and data",
                "terms_of_service": "Standard digital product terms"
            }
        }

    def _generate_business_plan(self, niche: str, products: List[Dict], target_audience: str) -> Dict[str, Any]:
        """Generate basic business plan"""
        total_value = sum(product.get('price', 0) for product in products)

        return {
            "business_name": f"{niche.title()} Success Hub",
            "mission": f"Help {target_audience} achieve success in {niche}",
            "target_market": target_audience,
            "revenue_model": "Digital product sales + recurring subscriptions",
            "pricing_strategy": "Competitive pricing with value-based positioning",
            "marketing_channels": ["Social media", "Email marketing", "Content marketing", "Paid ads"],
            "financial_projections": {
                "month_1_revenue": total_value * 5,
                "month_3_revenue": total_value * 15,
                "month_6_revenue": total_value * 35,
                "year_1_revenue": total_value * 100
            },
            "success_metrics": [
                "Monthly recurring revenue",
                "Customer acquisition cost",
                "Customer lifetime value",
                "Product conversion rates"
            ]
        }

    def _package_business(self, products: List[Dict], marketing: Dict, assets: Dict, plan: Dict, niche: str) -> Dict[str, Any]:
        """Package everything into final deliverable"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")

        package = {
            "business_name": f"{niche.title()} Success Hub",
            "created_at": datetime.utcnow().isoformat(),
            "elapsed_time": (datetime.utcnow() - self.start_time).total_seconds(),
            "niche": niche,
            "products": products,
            "marketing_content": marketing,
            "store_assets": assets,
            "business_plan": plan,
            "summary": {
                "total_products": len(products),
                "total_value": sum(p.get('price', 0) for p in products),
                "marketing_assets": len(marketing.get('email_sequences', [])) + len(marketing.get('ad_campaigns', [])),
                "projected_monthly_revenue": plan.get('financial_projections', {}).get('month_1_revenue', 0)
            },
            "next_steps": [
                "Review and customize your products",
                "Set up your store with the provided assets",
                "Launch your email marketing campaigns",
                "Start your advertising campaigns",
                "Monitor metrics and optimize"
            ]
        }

        # Save complete package
        saved_filename = self._save_business_package(package, timestamp)

        # Create downloadable file for user
        download_filename = self.create_downloadable_business_file(package)
        package['download_file'] = download_filename

        return package

    def _save_business_package(self, package: Dict, timestamp: str) -> str:
        """Save business package to file"""
        try:
            os.makedirs("generated_businesses", exist_ok=True)
            filename = f"generated_businesses/business_{package['niche']}_{timestamp}.json"

            with open(filename, 'w') as f:
                json.dump(package, f, indent=2, default=str)

            print(f"📦 Business package saved: {filename}")
            return filename

        except Exception as e:
            print(f"❌ Save business package failed: {e}")
            return ""

    def create_downloadable_business_file(self, package: Dict) -> str:
        """Create a comprehensive downloadable file with all business information"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            business_name = package.get('business_name', 'MyBusiness').replace(' ', '_')

            # Create downloads directory
            os.makedirs("downloads", exist_ok=True)

            # Generate comprehensive business document
            content = f"""
# {package.get('business_name', 'Your Business')} - Complete Business Package

## 🚀 Business Overview
- **Business Name:** {package.get('business_name', 'N/A')}
- **Niche:** {package.get('niche', 'N/A')}
- **Created:** {package.get('created_at', 'N/A')}
- **Total Products:** {package.get('summary', {}).get('total_products', 0)}
- **Total Value:** ${package.get('summary', {}).get('total_value', 0)}
- **Projected Monthly Revenue:** ${package.get('summary', {}).get('projected_monthly_revenue', 0)}

## 📋 Business Plan
{package.get('business_plan', {}).get('content', 'Business plan not available')}

## 🎯 Products Created

"""

            # Add each product
            for i, product in enumerate(package.get('products', []), 1):
                content += f"""
### Product {i}: {product.get('title', 'Untitled')}
- **Price:** ${product.get('price', 0)}
- **Category:** {product.get('category', 'N/A')}
- **Description:** {product.get('description', 'No description available')}
- **Target Audience:** {product.get('target_audience', 'Not specified')}

**Full Content:**
```
{product.get('content', 'Content not available')}
```

---
"""

            # Add marketing content
            marketing = package.get('marketing_content', {})
            content += f"""
## 📢 Marketing Materials

### Email Sequences
"""

            for i, email in enumerate(marketing.get('email_sequences', []), 1):
                content += f"""
#### Email {i}: {email.get('subject', 'No Subject')}
```
{email.get('content', 'No content')}
```

"""

            content += """
### Ad Campaigns
"""

            for i, ad in enumerate(marketing.get('ad_campaigns', []), 1):
                content += f"""
#### Campaign {i}: {ad.get('headline', 'No Headline')}
**Platform:** {ad.get('platform', 'Not specified')}
**Target Audience:** {ad.get('target_audience', 'Not specified')}
**Budget:** ${ad.get('budget', 0)}

**Ad Copy:**
```
{ad.get('copy', 'No copy available')}
```

"""

            # Add store assets
            store_assets = package.get('store_assets', {})
            content += f"""
## 🏪 Store Setup

### Store Information
- **Store Name:** {store_assets.get('store_name', 'Not specified')}
- **Theme:** {store_assets.get('theme', 'Default')}
- **Colors:** {store_assets.get('brand_colors', 'Not specified')}

### Pages Content
"""

            for page_name, page_content in store_assets.get('pages', {}).items():
                content += f"""
#### {page_name.title()} Page
```
{page_content}
```

"""

            # Add next steps
            content += f"""
## ✅ Next Steps

"""
            for step in package.get('next_steps', []):
                content += f"- {step}\n"

            # Add financial projections
            financial = package.get('business_plan', {}).get('financial_projections', {})
            if financial:
                content += f"""
## 💰 Financial Projections

- **Month 1 Revenue:** ${financial.get('month_1_revenue', 0)}
- **Month 3 Revenue:** ${financial.get('month_3_revenue', 0)}
- **Month 6 Revenue:** ${financial.get('month_6_revenue', 0)}
- **Month 12 Revenue:** ${financial.get('month_12_revenue', 0)}
- **Startup Costs:** ${financial.get('startup_costs', 0)}
- **Monthly Operating Costs:** ${financial.get('monthly_costs', 0)}
"""

            # Save the comprehensive file
            filename = f"downloads/{business_name}_Complete_Package_{timestamp}.md"

            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)

            # Also create a JSON version for programmatic use
            json_filename = f"downloads/{business_name}_Data_{timestamp}.json"
            with open(json_filename, 'w', encoding='utf-8') as f:
                json.dump(package, f, indent=2, default=str)

            print(f"📁 Downloadable files created:")
            print(f"   📄 Markdown: {filename}")
            print(f"   📊 JSON: {json_filename}")

            return filename

        except Exception as e:
            print(f"❌ Create downloadable file failed: {e}")
            return ""

    def get_progress(self) -> Dict[str, Any]:
        """Get current progress status"""
        return {
            "progress": self.progress,
            "status": self.status,
            "current_step": self.current_step,
            "elapsed_time": (datetime.utcnow() - self.start_time).total_seconds() if self.start_time else 0
        }

# Helper functions
def start_one_click_generation(user_id: int, niche: str, target_audience: str = "entrepreneurs") -> OneClickBusinessGenerator:
    """Start one-click business generation in background"""
    generator = OneClickBusinessGenerator(user_id)

    # Run generation in background thread
    def run_generation():
        generator.generate_complete_business(niche, target_audience)

    thread = threading.Thread(target=run_generation)
    thread.daemon = True
    thread.start()

    return generator

# Export functions
__all__ = ['OneClickBusinessGenerator', 'start_one_click_generation']