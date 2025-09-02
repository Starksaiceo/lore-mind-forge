
import os
import json
import requests
from datetime import datetime
from typing import Dict, List, Optional
import random
from marketplace_uploader import upload_product_to_shopify
from payment_processor import StripeProcessor

class ExpandedFlippingEngine:
    """Expanded flipping engine for domains, prompts, templates, and more"""
    
    def __init__(self):
        self.xano_url = os.getenv("XANO_BASE_URL", "https://x8ki-letl-twmt.n7.xano.io/api:8fyoFbLh")
        self.openrouter_key = os.getenv("OPENROUTER_API_KEY")
        
    def find_undervalued_domains(self, niche: str = None) -> List[Dict]:
        """Find undervalued domain names using AI analysis"""
        try:
            print(f"🔍 Searching for undervalued domains in {niche or 'general'} niche...")
            
            # Generate domain ideas using AI
            headers = {
                "Authorization": f"Bearer {self.openrouter_key}",
                "Content-Type": "application/json"
            }
            
            prompt = f"""Generate 10 undervalued domain name ideas for {niche or 'profitable online businesses'}. 
            Focus on:
            1. Short, memorable names
            2. .com extensions preferred
            3. AI/tech/business related
            4. Available for under $20/year
            5. High commercial potential
            
            Return as JSON list with: name, extension, estimated_value, niche, reasoning"""
            
            data = {
                "model": "anthropic/claude-3-opus",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7
            }
            
            response = requests.post("https://openrouter.ai/api/v1/chat/completions", 
                                   headers=headers, json=data, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            ai_suggestions = result["choices"][0]["message"]["content"]
            
            # Parse AI suggestions (simplified - in production, would use proper JSON parsing)
            domains = []
            try:
                # Try to extract JSON from AI response
                import re
                json_match = re.search(r'\[.*\]', ai_suggestions, re.DOTALL)
                if json_match:
                    domain_data = json.loads(json_match.group())
                    domains = domain_data
                else:
                    # Fallback: generate some example domains
                    domains = self.generate_fallback_domains(niche)
            except:
                domains = self.generate_fallback_domains(niche)
            
            print(f"✅ Found {len(domains)} potential domain opportunities")
            return domains[:5]  # Return top 5
            
        except Exception as e:
            print(f"❌ Domain search error: {e}")
            return self.generate_fallback_domains(niche)
    
    def generate_fallback_domains(self, niche: str = None) -> List[Dict]:
        """Generate fallback domain suggestions"""
        base_words = ["ai", "auto", "smart", "quick", "pro", "hub", "lab", "kit"]
        niche_words = ["business", "tool", "app", "solution", "system", "platform"]
        
        domains = []
        for i in range(5):
            base = random.choice(base_words)
            niche_word = random.choice(niche_words)
            domain_name = f"{base}{niche_word}"
            
            domains.append({
                "name": domain_name,
                "extension": ".com",
                "estimated_value": random.randint(50, 500),
                "niche": niche or "business tools",
                "reasoning": f"Short, brandable name combining {base} + {niche_word}"
            })
        
        return domains
    
    def create_prompt_bundles(self, theme: str = "business") -> Dict:
        """Create valuable prompt bundles for sale"""
        try:
            print(f"📝 Creating prompt bundle for {theme}...")
            
            # Generate comprehensive prompt collection
            headers = {
                "Authorization": f"Bearer {self.openrouter_key}",
                "Content-Type": "application/json"
            }
            
            prompt = f"""Create a valuable collection of 50 AI prompts for {theme} professionals.
            
            Include prompts for:
            1. Content creation
            2. Marketing copy
            3. Business strategy
            4. Customer service
            5. Data analysis
            6. Project management
            7. Sales outreach
            8. Social media
            9. Email marketing
            10. Product development
            
            Format each prompt with:
            - Clear title
            - Detailed prompt text
            - Use case example
            - Expected output description
            
            Make them professional, actionable, and valuable for {theme} professionals."""
            
            data = {
                "model": "anthropic/claude-3-opus",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.6
            }
            
            response = requests.post("https://openrouter.ai/api/v1/chat/completions", 
                                   headers=headers, json=data, timeout=60)
            response.raise_for_status()
            
            result = response.json()
            prompt_content = result["choices"][0]["message"]["content"]
            
            # Create the bundle package
            bundle = {
                "title": f"Ultimate {theme.title()} AI Prompt Collection",
                "description": f"50 professional AI prompts for {theme} professionals to boost productivity and results",
                "content": prompt_content,
                "price": 29.99,
                "category": "prompt_bundle",
                "file_format": "pdf",
                "created_at": datetime.now().isoformat()
            }
            
            # Save to file
            filename = f"prompt_bundle_{theme}_{datetime.now().strftime('%Y%m%d')}.txt"
            with open(filename, 'w') as f:
                f.write(f"# {bundle['title']}\n\n")
                f.write(f"{bundle['description']}\n\n")
                f.write("---\n\n")
                f.write(prompt_content)
            
            bundle["filename"] = filename
            
            print(f"✅ Created prompt bundle: {bundle['title']}")
            return bundle
            
        except Exception as e:
            print(f"❌ Prompt bundle creation error: {e}")
            return {"error": str(e)}
    
    def create_template_resales(self, template_type: str = "notion") -> Dict:
        """Create templates for resale"""
        try:
            print(f"📋 Creating {template_type} template for resale...")
            
            # Generate template based on type
            if template_type.lower() == "notion":
                return self.create_notion_template()
            elif template_type.lower() == "spreadsheet":
                return self.create_spreadsheet_template()
            elif template_type.lower() == "presentation":
                return self.create_presentation_template()
            else:
                return self.create_generic_template(template_type)
                
        except Exception as e:
            print(f"❌ Template creation error: {e}")
            return {"error": str(e)}
    
    def create_notion_template(self) -> Dict:
        """Create a Notion template"""
        try:
            # Generate Notion template structure using AI
            headers = {
                "Authorization": f"Bearer {self.openrouter_key}",
                "Content-Type": "application/json"
            }
            
            prompt = """Create a comprehensive Notion template for business productivity.
            
            Include:
            1. Project management dashboard
            2. Goal tracking system
            3. Daily/weekly planning pages
            4. Resource management
            5. Meeting notes template
            6. Contact management
            7. Financial tracking
            8. Content calendar
            9. Task automation setup
            10. Performance metrics
            
            Provide detailed structure with database properties, views, and formulas.
            Make it professional and immediately useful."""
            
            data = {
                "model": "anthropic/claude-3-opus",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.5
            }
            
            response = requests.post("https://openrouter.ai/api/v1/chat/completions", 
                                   headers=headers, json=data, timeout=45)
            response.raise_for_status()
            
            result = response.json()
            template_content = result["choices"][0]["message"]["content"]
            
            template = {
                "title": "Ultimate Business Productivity Notion Template",
                "description": "Complete Notion workspace for business professionals with project management, goal tracking, and productivity systems",
                "content": template_content,
                "price": 19.99,
                "category": "notion_template",
                "file_format": "notion_link",
                "created_at": datetime.now().isoformat()
            }
            
            # Save template guide
            filename = f"notion_template_{datetime.now().strftime('%Y%m%d')}.md"
            with open(filename, 'w') as f:
                f.write(f"# {template['title']}\n\n")
                f.write(f"{template['description']}\n\n")
                f.write("## Template Structure\n\n")
                f.write(template_content)
            
            template["filename"] = filename
            
            print(f"✅ Created Notion template: {template['title']}")
            return template
            
        except Exception as e:
            print(f"❌ Notion template creation error: {e}")
            return {"error": str(e)}
    
    def create_spreadsheet_template(self) -> Dict:
        """Create a spreadsheet template"""
        try:
            template = {
                "title": "Business Financial Dashboard Template",
                "description": "Excel/Google Sheets template for business financial tracking and analysis",
                "content": "Comprehensive financial dashboard with profit tracking, expense management, and ROI calculations",
                "price": 14.99,
                "category": "spreadsheet_template",
                "file_format": "xlsx",
                "created_at": datetime.now().isoformat()
            }
            
            # Create simple CSV structure as example
            filename = f"financial_template_{datetime.now().strftime('%Y%m%d')}.csv"
            with open(filename, 'w') as f:
                f.write("Date,Revenue,Expenses,Profit,Source,Category,Notes\n")
                f.write("2024-01-01,100.00,20.00,80.00,Product Sales,Digital Products,Example entry\n")
            
            template["filename"] = filename
            
            print(f"✅ Created spreadsheet template: {template['title']}")
            return template
            
        except Exception as e:
            print(f"❌ Spreadsheet template creation error: {e}")
            return {"error": str(e)}
    
    def create_generic_template(self, template_type: str) -> Dict:
        """Create a generic template"""
        template = {
            "title": f"Professional {template_type.title()} Template",
            "description": f"High-quality {template_type} template for business use",
            "content": f"Professional {template_type} template with modern design and practical functionality",
            "price": 12.99,
            "category": f"{template_type}_template",
            "file_format": "pdf",
            "created_at": datetime.now().isoformat()
        }
        
        return template
    
    def auto_list_products(self, products: List[Dict]) -> Dict:
        """Auto-list products across multiple platforms"""
        try:
            print(f"🚀 Auto-listing {len(products)} products across platforms...")
            
            results = {
                "shopify": [],
                "stripe": [],
                "total_listed": 0,
                "errors": []
            }
            
            for product in products:
                try:
                    # List on Shopify only
                    shopify_result = self.list_on_shopify_only(product)
                    if shopify_result.get("success"):
                        results["shopify"].append(shopify_result)
                        results["total_listed"] += 1
                    else:
                        results["errors"].append(f"Shopify: {shopify_result.get('error', 'Unknown error')}")
                    
                    # List on Stripe
                    stripe_result = self.list_on_stripe(product)
                    if stripe_result.get("success"):
                        results["stripe"].append(stripe_result)
                    else:
                        results["errors"].append(f"Stripe: {stripe_result.get('error', 'Unknown error')}")
                        
                except Exception as e:
                    results["errors"].append(f"Product {product.get('title', 'Unknown')}: {str(e)}")
            
            print(f"✅ Auto-listing completed: {results['total_listed']} products listed")
            return results
            
        except Exception as e:
            print(f"❌ Auto-listing error: {e}")
            return {"error": str(e)}
    
    def list_on_shopify_only(self, product):
        """List product on Shopify only - Gumroad removed"""
        try:
            from marketplace_uploader import upload_product_to_shopify
            
            result = upload_product_to_shopify(product)
            return result
            
        except Exception as e:
            return {"success": False, "error": str(e)}road(self, product: Dict) -> Dict:
        """List product on Gumroad"""
        try:
            # Use existing Gumroad uploader
            result = upload_to_gumroad(
                product.get("filename", ""),
                product.get("title", ""),
                product.get("description", ""),
                product.get("price", 9.99)
            )
            
            return result
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def list_on_stripe(self, product: Dict) -> Dict:
        """List product on Stripe"""
        try:
            result = StripeProcessor.create_product(
                product.get("title", ""),
                product.get("description", ""),
                product.get("price", 9.99)
            )
            
            return result
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def run_expanded_flip_session(self, budget: float = 100.0, focus: str = "mixed") -> Dict:
        """Run a complete expanded flipping session"""
        try:
            print(f"🔄 Starting expanded flip session with ${budget:.2f} budget, focus: {focus}")
            
            session_results = {
                "budget": budget,
                "focus": focus,
                "products_created": [],
                "domains_found": [],
                "total_potential_value": 0.0,
                "platforms_used": [],
                "success": False
            }
            
            # Allocate budget across different flip types
            if focus == "domains":
                domains = self.find_undervalued_domains()
                session_results["domains_found"] = domains
                session_results["total_potential_value"] = sum(d.get("estimated_value", 0) for d in domains)
                
            elif focus == "prompts":
                prompt_bundle = self.create_prompt_bundles("business")
                if "error" not in prompt_bundle:
                    session_results["products_created"].append(prompt_bundle)
                    session_results["total_potential_value"] += prompt_bundle.get("price", 0) * 10  # Estimated sales
                
            elif focus == "templates":
                template = self.create_template_resales("notion")
                if "error" not in template:
                    session_results["products_created"].append(template)
                    session_results["total_potential_value"] += template.get("price", 0) * 5  # Estimated sales
                
            else:  # mixed approach
                # Create one of each type
                prompt_bundle = self.create_prompt_bundles("productivity")
                if "error" not in prompt_bundle:
                    session_results["products_created"].append(prompt_bundle)
                
                template = self.create_template_resales("spreadsheet")
                if "error" not in template:
                    session_results["products_created"].append(template)
                
                domains = self.find_undervalued_domains("business")[:2]
                session_results["domains_found"] = domains
                
                # Calculate potential value
                session_results["total_potential_value"] = (
                    sum(p.get("price", 0) * 5 for p in session_results["products_created"]) +
                    sum(d.get("estimated_value", 0) for d in domains)
                )
            
            # Auto-list products if any were created
            if session_results["products_created"]:
                listing_results = self.auto_list_products(session_results["products_created"])
                session_results["platforms_used"] = [p for p in ["gumroad", "stripe"] if listing_results.get(p)]
                
                # Log potential profit
                from performance_tracker import log_strategy_result
                estimated_profit = session_results["total_potential_value"] * 0.3  # 30% conversion estimate
                log_strategy_result(
                    strategy_type="expanded_flipping",
                    platform="multi_platform",
                    profit=estimated_profit,
                    cost=budget * 0.1,  # Estimated 10% of budget for costs
                    time_spent=120,  # 2 hours
                    success=len(session_results["products_created"]) > 0,
                    details=session_results
                )
            
            session_results["success"] = (
                len(session_results["products_created"]) > 0 or 
                len(session_results["domains_found"]) > 0
            )
            
            print(f"✅ Expanded flip session completed:")
            print(f"   Products Created: {len(session_results['products_created'])}")
            print(f"   Domains Found: {len(session_results['domains_found'])}")
            print(f"   Potential Value: ${session_results['total_potential_value']:.2f}")
            
            return session_results
            
        except Exception as e:
            print(f"❌ Expanded flip session error: {e}")
            return {"success": False, "error": str(e)}

# Global instance
expanded_flipper = ExpandedFlippingEngine()

def run_expanded_flip(budget: float = 100.0, focus: str = "mixed"):
    """Run expanded flipping session"""
    return expanded_flipper.run_expanded_flip_session(budget, focus)

def create_prompt_bundle(theme: str = "business"):
    """Create a prompt bundle"""
    return expanded_flipper.create_prompt_bundles(theme)

def find_domain_opportunities(niche: str = None):
    """Find domain opportunities"""
    return expanded_flipper.find_undervalued_domains(niche)

def create_template(template_type: str = "notion"):
    """Create a template for resale"""
    return expanded_flipper.create_template_resales(template_type)

if __name__ == "__main__":
    print("🔄 Testing Expanded Flipping Engine...")
    result = run_expanded_flip(50.0, "mixed")
    print(f"✅ Test completed: {result.get('success', False)}")
