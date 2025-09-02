"""
🔨 Builder Agent - AI CEO Multi-Agent Intelligence  
Creates products using current AI tools and uploads to marketplaces
"""

import logging
from datetime import datetime
from models import db, ProductStore
from config import OPENROUTER_API_KEY
import requests
import json
from typing import Dict, Optional
import os
import uuid

logger = logging.getLogger(__name__)

class BuilderAgent:
    """AI builder that creates products based on strategy"""
    
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.output_dir = "generated_products"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate_ebook_content(self, topic: str, title: str) -> str:
        """Generate ebook content using AI"""
        try:
            prompt = f"""
            Create a comprehensive ebook about "{topic}" with the title "{title}".
            
            Include:
            1. Table of Contents
            2. Introduction (2 paragraphs)
            3. 5 main chapters (500 words each)
            4. Conclusion
            5. Actionable tips and resources
            
            Make it valuable, actionable, and professional.
            Format as markdown with proper headings.
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
                    "max_tokens": 4000
                },
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                logger.error(f"OpenRouter API error: {response.status_code}")
                return self._fallback_ebook_content(topic, title)
                
        except Exception as e:
            logger.error(f"Ebook generation error: {e}")
            return self._fallback_ebook_content(topic, title)
    
    def _fallback_ebook_content(self, topic: str, title: str) -> str:
        """Fallback ebook content when AI fails"""
        return f"""
# {title}

## Table of Contents
1. Introduction to {topic}
2. Getting Started
3. Best Practices
4. Advanced Techniques
5. Case Studies
6. Resources and Tools

## Introduction

Welcome to the complete guide on {topic}. This ebook will provide you with actionable insights and practical strategies to master {topic}.

In today's digital world, understanding {topic} is essential for success. This guide breaks down complex concepts into easy-to-follow steps.

## Chapter 1: Getting Started with {topic}

The foundation of {topic} begins with understanding the core principles...

## Chapter 2: Best Practices

Here are the proven strategies that work...

## Chapter 3: Advanced Techniques

Take your {topic} skills to the next level...

## Conclusion

You now have the tools and knowledge to succeed with {topic}. Apply these strategies consistently for best results.
        """
    
    def generate_template_bundle(self, niche: str) -> Dict:
        """Generate template bundle for a specific niche"""
        templates = {
            "social_media": ["Instagram Post Template", "Facebook Ad Template", "LinkedIn Post Template"],
            "business": ["Business Plan Template", "Pitch Deck Template", "Invoice Template"],
            "marketing": ["Email Sequence Template", "Landing Page Template", "Sales Funnel Template"],
            "productivity": ["Daily Planner Template", "Goal Setting Template", "Task Management Template"]
        }
        
        template_list = templates.get(niche, templates["business"])
        
        return {
            "bundle_name": f"{niche.title()} Template Bundle",
            "templates": template_list,
            "description": f"Professional {niche} templates to boost your productivity"
        }
    
    def create_product_file(self, content: str, filename: str, product_type: str) -> str:
        """Save product content to file"""
        try:
            file_id = str(uuid.uuid4())[:8]
            full_filename = f"{file_id}_{filename}"
            file_path = os.path.join(self.output_dir, full_filename)
            
            if product_type == "ebook":
                # Save as markdown
                file_path += ".md"
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
            elif product_type == "template":
                # Save as JSON for template data
                file_path += ".json"
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(content, f, indent=2)
            
            logger.info(f"Product file created: {file_path}")
            return file_path
            
        except Exception as e:
            logger.error(f"File creation error: {e}")
            return ""
    
    def save_to_database(self, product_data: Dict) -> int:
        """Save product to local database"""
        try:
            product = ProductStore(
                user_id=self.user_id,
                title=product_data["title"],
                description=product_data["description"],
                price=product_data.get("price", 9.99),
                category=product_data.get("category", "digital"),
                file_path=product_data.get("file_path", ""),
                status="draft"
            )
            
            db.session.add(product)
            db.session.commit()
            
            logger.info(f"Product saved to database: {product.id}")
            return product.id
            
        except Exception as e:
            logger.error(f"Database save error: {e}")
            return 0
    
    def upload_to_shopify(self, product_data: Dict) -> Dict:
        """Upload product to Shopify (using existing integration)"""
        try:
            from marketplace_uploader import ShopifyUploader
            
            uploader = ShopifyUploader()
            result = uploader.create_product({
                "title": product_data["title"],
                "body_html": product_data["description"],
                "vendor": "AI CEO",
                "product_type": product_data.get("category", "Digital Product"),
                "price": product_data.get("price", 9.99),
                "inventory_quantity": 999,  # Digital products have unlimited inventory
                "tags": f"AI-generated, {product_data.get('category', 'digital')}"
            })
            
            if result.get("product"):
                return {
                    "success": True,
                    "product_id": result["product"]["id"],
                    "product_url": f"https://ai-ceo-agent-store.myshopify.com/products/{result['product']['handle']}",
                    "handle": result["product"]["handle"]
                }
            else:
                return {"success": False, "error": "Failed to create Shopify product"}
                
        except Exception as e:
            logger.error(f"Shopify upload error: {e}")
            return {"success": False, "error": str(e)}
    
    def build_product(self, strategy: str, strategy_type: str = "ebook") -> Dict:
        """Main method: Build product based on strategy"""
        try:
            # Extract topic and generate title
            topic = self._extract_topic(strategy)
            title = self._generate_title(strategy, strategy_type)
            
            result = {
                "title": title,
                "topic": topic,
                "strategy_type": strategy_type,
                "created_at": datetime.utcnow().isoformat(),
                "user_id": self.user_id
            }
            
            if strategy_type == "ebook":
                # Generate ebook content
                content = self.generate_ebook_content(topic, title)
                file_path = self.create_product_file(content, f"{title.replace(' ', '_')}", "ebook")
                
                result.update({
                    "content_length": len(content),
                    "file_path": file_path,
                    "description": f"Comprehensive ebook about {topic} with actionable insights and practical strategies.",
                    "price": 9.99,
                    "category": "ebook"
                })
                
            elif strategy_type == "template":
                # Generate template bundle
                template_data = self.generate_template_bundle(topic)
                file_path = self.create_product_file(template_data, f"{title.replace(' ', '_')}", "template")
                
                result.update({
                    "templates_included": len(template_data["templates"]),
                    "file_path": file_path,
                    "description": template_data["description"],
                    "price": 19.99,
                    "category": "template"
                })
            
            # Save to local database
            product_id = self.save_to_database(result)
            result["database_id"] = product_id
            
            # Upload to Shopify
            shopify_result = self.upload_to_shopify(result)
            result["shopify"] = shopify_result
            
            if shopify_result.get("success"):
                result["product_link"] = shopify_result["product_url"]
                result["shopify_id"] = shopify_result["product_id"]
            
            logger.info(f"Product built successfully: {title}")
            return result
            
        except Exception as e:
            logger.error(f"Product building error: {e}")
            return {
                "error": str(e),
                "success": False,
                "strategy": strategy,
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def _extract_topic(self, strategy: str) -> str:
        """Extract main topic from strategy"""
        # Simple topic extraction
        keywords = strategy.lower().split()
        topic_words = []
        
        skip_words = {"create", "an", "ebook", "about", "for", "with", "and", "the", "a"}
        
        for word in keywords:
            if word not in skip_words and len(word) > 2:
                topic_words.append(word)
                if len(topic_words) >= 3:  # Take first 3 meaningful words
                    break
        
        return " ".join(topic_words) if topic_words else "productivity"
    
    def _generate_title(self, strategy: str, product_type: str) -> str:
        """Generate product title from strategy"""
        topic = self._extract_topic(strategy)
        
        if product_type == "ebook":
            return f"The Complete Guide to {topic.title()}"
        elif product_type == "template":
            return f"Ultimate {topic.title()} Template Bundle"
        elif product_type == "course":
            return f"Master {topic.title()}: Complete Course"
        else:
            return f"{topic.title()} Mastery Kit"

def build_product_from_strategy(user_id: int, strategy: str, strategy_type: str = "ebook") -> Dict:
    """Convenience function to build product"""
    builder = BuilderAgent(user_id)
    return builder.build_product(strategy, strategy_type)

if __name__ == "__main__":
    # Test the builder
    print("🔨 Testing Builder Agent...")
    result = build_product_from_strategy(1, "Create an ebook about AI productivity tools", "ebook")
    print(f"Product: {result.get('title')}")
    print(f"File: {result.get('file_path')}")
    print(f"Shopify: {result.get('shopify', {}).get('success', False)}")