"""
📈 Flipper Agent - AI CEO Multi-Agent Intelligence
Uses flipping strategies for ebooks, templates, bundles with profit optimization
"""

import logging
from datetime import datetime, timedelta
from models import db, ProductStore, AgentMemory
from config import OPENROUTER_API_KEY
import requests
import json
from typing import Dict, List, Optional
import random

logger = logging.getLogger(__name__)

class FlipperAgent:
    """AI flipper that implements profitable flipping strategies"""
    
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.flip_strategies = [
            "bundle_existing_products",
            "seasonal_repricing",
            "cross_platform_expansion", 
            "premium_version_upsell",
            "niche_variant_creation"
        ]
    
    def get_existing_products(self) -> List[Dict]:
        """Get user's existing products for flipping"""
        try:
            products = db.session.query(ProductStore).filter_by(
                user_id=self.user_id
            ).order_by(ProductStore.created_at.desc()).limit(20).all()
            
            return [{
                "id": p.id,
                "title": p.title,
                "price": p.price,
                "category": p.category,
                "revenue": p.revenue,
                "status": p.status,
                "created_at": p.created_at
            } for p in products]
            
        except Exception as e:
            logger.error(f"Error fetching products: {e}")
            return []
    
    def save_flip_memory(self, strategy: str, result: Dict):
        """Save flip results to memory for learning"""
        try:
            memory_data = {
                "strategy": strategy,
                "result": result,
                "timestamp": datetime.utcnow().isoformat(),
                "profit": result.get("profit", 0)
            }
            
            memory = AgentMemory(
                user_id=self.user_id,
                key="flip_result",
                value=json.dumps(memory_data)
            )
            db.session.add(memory)
            db.session.commit()
            
        except Exception as e:
            logger.error(f"Error saving flip memory: {e}")
    
    def analyze_flip_opportunities(self) -> Dict:
        """Analyze best flipping opportunities"""
        products = self.get_existing_products()
        
        if not products:
            return {"strategy": "create_new_products", "reason": "No existing products to flip"}
        
        # Analyze performance
        total_revenue = sum(p["revenue"] for p in products)
        avg_price = sum(p["price"] for p in products) / len(products) if products else 0
        
        # Find underperforming products
        underperforming = [p for p in products if p["revenue"] < p["price"]]
        top_performers = [p for p in products if p["revenue"] > p["price"] * 2]
        
        opportunities = {
            "total_products": len(products),
            "total_revenue": total_revenue,
            "avg_price": avg_price,
            "underperforming_count": len(underperforming),
            "top_performers": len(top_performers),
            "recommended_strategy": self._select_best_strategy(products)
        }
        
        return opportunities
    
    def _select_best_strategy(self, products: List[Dict]) -> str:
        """Select best flipping strategy based on product analysis"""
        if len(products) >= 3:
            return "bundle_existing_products"
        elif any(p["revenue"] > p["price"] * 3 for p in products):
            return "premium_version_upsell"
        elif datetime.now().month in [11, 12, 1]:  # Holiday season
            return "seasonal_repricing"
        else:
            return "niche_variant_creation"
    
    def create_product_bundle(self, products: List[Dict]) -> Dict:
        """Create profitable bundle from existing products"""
        try:
            if len(products) < 2:
                return {"error": "Need at least 2 products to bundle"}
            
            # Select best products for bundle
            selected = sorted(products, key=lambda x: x["revenue"], reverse=True)[:4]
            
            bundle_title = f"Ultimate {selected[0]['category'].title()} Bundle"
            individual_price = sum(p["price"] for p in selected)
            bundle_price = round(individual_price * 0.7, 2)  # 30% discount
            
            bundle_data = {
                "title": bundle_title,
                "description": f"Complete bundle including {len(selected)} premium resources",
                "price": bundle_price,
                "individual_price": individual_price,
                "savings": round(individual_price - bundle_price, 2),
                "products_included": [p["title"] for p in selected],
                "category": "bundle",
                "profit_margin": 0.85  # Higher margin for bundles
            }
            
            # Create bundle product in database
            bundle_product = ProductStore(
                user_id=self.user_id,
                title=bundle_data["title"],
                description=bundle_data["description"],
                price=bundle_data["price"],
                category="bundle",
                status="draft"
            )
            
            db.session.add(bundle_product)
            db.session.commit()
            
            # Upload to Shopify
            shopify_result = self._upload_bundle_to_shopify(bundle_data)
            
            result = {
                **bundle_data,
                "database_id": bundle_product.id,
                "shopify": shopify_result,
                "strategy": "bundle_existing_products",
                "created_at": datetime.utcnow().isoformat()
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Bundle creation error: {e}")
            return {"error": str(e), "strategy": "bundle_existing_products"}
    
    def create_premium_upsell(self, base_product: Dict) -> Dict:
        """Create premium version of successful product"""
        try:
            premium_title = f"{base_product['title']} - PREMIUM Edition"
            premium_price = base_product["price"] * 2.5
            
            # Generate premium content using AI
            premium_features = self._generate_premium_features(base_product)
            
            premium_data = {
                "title": premium_title,
                "description": f"Premium version with exclusive content: {', '.join(premium_features)}",
                "price": premium_price,
                "base_price": base_product["price"],
                "category": f"premium_{base_product['category']}",
                "premium_features": premium_features
            }
            
            # Create premium product
            premium_product = ProductStore(
                user_id=self.user_id,
                title=premium_data["title"],
                description=premium_data["description"],
                price=premium_data["price"],
                category=premium_data["category"],
                status="draft"
            )
            
            db.session.add(premium_product)
            db.session.commit()
            
            result = {
                **premium_data,
                "database_id": premium_product.id,
                "strategy": "premium_version_upsell",
                "created_at": datetime.utcnow().isoformat()
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Premium upsell error: {e}")
            return {"error": str(e), "strategy": "premium_version_upsell"}
    
    def _generate_premium_features(self, base_product: Dict) -> List[str]:
        """Generate premium features using AI"""
        try:
            prompt = f"""
            For a product titled "{base_product['title']}" in category "{base_product['category']}", 
            suggest 5 premium features that would justify a 2.5x price increase.
            
            Return only a JSON array of feature names, like:
            ["Feature 1", "Feature 2", "Feature 3", "Feature 4", "Feature 5"]
            """
            
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "anthropic/claude-3-haiku",
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 200
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content'].strip()
                features = json.loads(content)
                return features[:5]  # Ensure we have exactly 5
            
        except Exception as e:
            logger.error(f"AI premium features error: {e}")
        
        # Fallback features
        return [
            "Bonus Templates Pack",
            "Video Tutorial Series", 
            "1-on-1 Consultation Call",
            "Private Community Access",
            "Lifetime Updates"
        ]
    
    def seasonal_repricing_strategy(self, products: List[Dict]) -> Dict:
        """Implement seasonal pricing optimization"""
        current_month = datetime.now().month
        
        # Holiday season (Nov-Jan): Premium pricing
        if current_month in [11, 12, 1]:
            multiplier = 1.4
            reason = "Holiday premium pricing"
        # Back-to-school (Aug-Sep): Educational focus
        elif current_month in [8, 9]:
            multiplier = 1.2
            reason = "Back-to-school season"
        # Summer discount (Jun-Jul): Clearance pricing  
        elif current_month in [6, 7]:
            multiplier = 0.8
            reason = "Summer clearance"
        # Regular season
        else:
            multiplier = 1.1
            reason = "Standard optimization"
        
        repriced_products = []
        total_potential_increase = 0
        
        for product in products:
            old_price = product["price"]
            new_price = round(old_price * multiplier, 2)
            increase = new_price - old_price
            
            repriced_products.append({
                "id": product["id"],
                "title": product["title"],
                "old_price": old_price,
                "new_price": new_price,
                "increase": increase
            })
            
            total_potential_increase += increase
        
        return {
            "strategy": "seasonal_repricing",
            "season": reason,
            "multiplier": multiplier,
            "products_affected": len(repriced_products),
            "total_potential_increase": total_potential_increase,
            "repriced_products": repriced_products
        }
    
    def _upload_bundle_to_shopify(self, bundle_data: Dict) -> Dict:
        """Upload bundle to Shopify marketplace"""
        try:
            from marketplace_uploader import ShopifyUploader
            
            uploader = ShopifyUploader()
            result = uploader.create_product({
                "title": bundle_data["title"],
                "body_html": f"{bundle_data['description']}<br><br>Save ${bundle_data['savings']}!",
                "vendor": "AI CEO",
                "product_type": "Bundle",
                "price": bundle_data["price"],
                "compare_at_price": bundle_data["individual_price"],
                "inventory_quantity": 999,
                "tags": "bundle, premium, AI-generated"
            })
            
            if result.get("product"):
                return {
                    "success": True,
                    "product_id": result["product"]["id"],
                    "product_url": f"https://ai-ceo-agent-store.myshopify.com/products/{result['product']['handle']}"
                }
            else:
                return {"success": False, "error": "Bundle upload failed"}
                
        except Exception as e:
            logger.error(f"Shopify bundle upload error: {e}")
            return {"success": False, "error": str(e)}
    
    def execute_flip_strategy(self, strategy: str = None) -> Dict:
        """Main method: Execute chosen flipping strategy"""
        try:
            # Analyze opportunities
            opportunities = self.analyze_flip_opportunities()
            
            if not strategy:
                strategy = opportunities["recommended_strategy"]
            
            products = self.get_existing_products()
            result = {"strategy": strategy, "timestamp": datetime.utcnow().isoformat()}
            
            if strategy == "bundle_existing_products":
                result = self.create_product_bundle(products)
                
            elif strategy == "premium_version_upsell":
                top_product = max(products, key=lambda x: x["revenue"]) if products else None
                if top_product:
                    result = self.create_premium_upsell(top_product)
                else:
                    result = {"error": "No products available for premium upsell"}
                    
            elif strategy == "seasonal_repricing":
                result = self.seasonal_repricing_strategy(products)
                
            else:
                result = {"error": f"Strategy {strategy} not implemented yet"}
            
            # Calculate profit potential
            if "error" not in result:
                result["profit_potential"] = self._calculate_profit_potential(result)
                self.save_flip_memory(strategy, result)
            
            logger.info(f"Flip strategy executed: {strategy}")
            return result
            
        except Exception as e:
            logger.error(f"Flip execution error: {e}")
            return {
                "error": str(e),
                "strategy": strategy or "unknown",
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def _calculate_profit_potential(self, result: Dict) -> float:
        """Calculate potential profit from flip strategy"""
        if result["strategy"] == "bundle_existing_products":
            return result.get("price", 0) * 0.85  # 85% profit margin
        elif result["strategy"] == "premium_version_upsell":
            return result.get("price", 0) * 0.90  # 90% profit margin (digital)
        elif result["strategy"] == "seasonal_repricing":
            return result.get("total_potential_increase", 0) * 0.80
        else:
            return 0

def execute_flip_strategy(user_id: int, strategy: str = None) -> Dict:
    """Convenience function to execute flip strategy"""
    flipper = FlipperAgent(user_id)
    return flipper.execute_flip_strategy(strategy)

if __name__ == "__main__":
    # Test the flipper
    print("📈 Testing Flipper Agent...")
    result = execute_flip_strategy(1, "bundle_existing_products")
    print(f"Strategy: {result.get('strategy')}")
    print(f"Profit potential: ${result.get('profit_potential', 0):.2f}")