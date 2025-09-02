"""
📢 Marketer Agent - AI CEO Multi-Agent Intelligence
Generates social posts, ad copy, hashtags and manages marketing campaigns
"""

import logging
from datetime import datetime, timedelta
from models import db, SocialPost, AdEntity, AgentMemory
from config import OPENROUTER_API_KEY, META_ACCESS_TOKEN, META_AD_ACCOUNT_ID
import requests
import json
from typing import Dict, List, Optional
import random

logger = logging.getLogger(__name__)

class MarketerAgent:
    """AI marketer that creates and manages marketing content"""
    
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.platforms = ["instagram", "twitter", "tiktok", "linkedin", "facebook"]
        self.content_types = ["social_post", "ad_copy", "email_subject", "hashtags"]
    
    def generate_social_content(self, product_data: Dict, platform: str = "instagram") -> Dict:
        """Generate social media content for a product"""
        try:
            prompt = f"""
            Create engaging {platform} content for this product:
            
            Product: {product_data.get('title', 'Digital Product')}
            Description: {product_data.get('description', 'Premium digital product')}
            Price: ${product_data.get('price', 9.99)}
            Category: {product_data.get('category', 'digital')}
            
            Generate:
            1. Catchy caption (2-3 sentences, {platform} style)
            2. 8-10 relevant hashtags
            3. Call-to-action
            
            Format as JSON:
            {{
                "caption": "Your engaging caption here",
                "hashtags": ["hashtag1", "hashtag2", ...],
                "cta": "Your call to action"
            }}
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
                    "max_tokens": 500
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content'].strip()
                
                try:
                    parsed_content = json.loads(content)
                    return {
                        "platform": platform,
                        "content": parsed_content,
                        "generated_at": datetime.utcnow().isoformat(),
                        "success": True
                    }
                except json.JSONDecodeError:
                    return self._fallback_social_content(product_data, platform)
            else:
                return self._fallback_social_content(product_data, platform)
                
        except Exception as e:
            logger.error(f"Social content generation error: {e}")
            return self._fallback_social_content(product_data, platform)
    
    def _fallback_social_content(self, product_data: Dict, platform: str) -> Dict:
        """Fallback social content when AI fails"""
        title = product_data.get('title', 'Amazing Digital Product')
        price = product_data.get('price', 9.99)
        
        return {
            "platform": platform,
            "content": {
                "caption": f"🚀 Just launched: {title}! Get instant access for only ${price}. Transform your productivity today!",
                "hashtags": ["#DigitalProduct", "#Productivity", "#OnlineBusiness", "#AIGenerated", "#InstantAccess"],
                "cta": "Link in bio to get yours now!"
            },
            "generated_at": datetime.utcnow().isoformat(),
            "success": True,
            "fallback": True
        }
    
    def generate_ad_copy(self, product_data: Dict, platform: str = "meta") -> Dict:
        """Generate advertising copy for different platforms"""
        try:
            prompt = f"""
            Create high-converting {platform} ad copy for:
            
            Product: {product_data.get('title')}
            Description: {product_data.get('description')}
            Price: ${product_data.get('price')}
            Target: Business owners and entrepreneurs
            
            Generate:
            1. Headline (attention-grabbing, 5-7 words)
            2. Primary text (compelling, benefit-focused, 2-3 sentences)
            3. Call-to-action button text
            4. Description (supporting details)
            
            Format as JSON:
            {{
                "headline": "Your headline",
                "primary_text": "Your primary ad text",
                "cta_button": "Button text",
                "description": "Supporting description"
            }}
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
                    "max_tokens": 400
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content'].strip()
                
                try:
                    parsed_content = json.loads(content)
                    return {
                        "platform": platform,
                        "ad_copy": parsed_content,
                        "generated_at": datetime.utcnow().isoformat(),
                        "success": True
                    }
                except json.JSONDecodeError:
                    return self._fallback_ad_copy(product_data, platform)
            else:
                return self._fallback_ad_copy(product_data, platform)
                
        except Exception as e:
            logger.error(f"Ad copy generation error: {e}")
            return self._fallback_ad_copy(product_data, platform)
    
    def _fallback_ad_copy(self, product_data: Dict, platform: str) -> Dict:
        """Fallback ad copy when AI fails"""
        title = product_data.get('title', 'Premium Digital Product')
        price = product_data.get('price', 9.99)
        
        return {
            "platform": platform,
            "ad_copy": {
                "headline": f"Get {title} Today",
                "primary_text": f"Transform your business with {title}. Proven strategies, instant access, only ${price}.",
                "cta_button": "Get Instant Access",
                "description": "Join thousands who've already transformed their business."
            },
            "generated_at": datetime.utcnow().isoformat(),
            "success": True,
            "fallback": True
        }
    
    def schedule_social_posts(self, content_list: List[Dict]) -> Dict:
        """Schedule social media posts in local database"""
        scheduled_posts = []
        
        try:
            for i, content_data in enumerate(content_list):
                # Schedule posts over next few days
                post_time = datetime.utcnow() + timedelta(hours=i*6)  # Every 6 hours
                
                social_post = SocialPost(
                    user_id=self.user_id,
                    platform=content_data.get("platform", "instagram"),
                    post_id=f"scheduled_{datetime.utcnow().timestamp()}_{i}",
                    status="scheduled",
                    caption=content_data.get("content", {}).get("caption", ""),
                    created_at=post_time
                )
                
                db.session.add(social_post)
                scheduled_posts.append({
                    "platform": social_post.platform,
                    "scheduled_time": post_time.isoformat(),
                    "caption": social_post.caption[:100] + "..." if len(social_post.caption) > 100 else social_post.caption
                })
            
            db.session.commit()
            
            return {
                "success": True,
                "posts_scheduled": len(scheduled_posts),
                "posts": scheduled_posts,
                "next_post": min(scheduled_posts, key=lambda x: x["scheduled_time"])["scheduled_time"]
            }
            
        except Exception as e:
            logger.error(f"Post scheduling error: {e}")
            return {"success": False, "error": str(e)}
    
    def create_campaign_strategy(self, product_data: Dict) -> Dict:
        """Create comprehensive marketing campaign strategy"""
        try:
            # Generate content for multiple platforms
            campaign_content = {}
            
            for platform in self.platforms[:3]:  # Limit to 3 platforms to avoid rate limits
                social_content = self.generate_social_content(product_data, platform)
                ad_content = self.generate_ad_copy(product_data, platform)
                
                campaign_content[platform] = {
                    "social": social_content,
                    "ads": ad_content
                }
            
            # Create campaign timeline
            campaign_timeline = self._create_campaign_timeline()
            
            # Save campaign strategy to memory
            campaign_data = {
                "product_id": product_data.get("id"),
                "product_title": product_data.get("title"),
                "content": campaign_content,
                "timeline": campaign_timeline,
                "budget_recommendation": self._recommend_budget(product_data),
                "created_at": datetime.utcnow().isoformat()
            }
            
            memory = AgentMemory(
                user_id=self.user_id,
                key="campaign_strategy",
                value=json.dumps(campaign_data)
            )
            db.session.add(memory)
            db.session.commit()
            
            return {
                "success": True,
                "campaign": campaign_data,
                "platforms": list(campaign_content.keys()),
                "estimated_reach": random.randint(5000, 25000)  # Simulated reach
            }
            
        except Exception as e:
            logger.error(f"Campaign strategy error: {e}")
            return {"success": False, "error": str(e)}
    
    def _create_campaign_timeline(self) -> List[Dict]:
        """Create marketing campaign timeline"""
        timeline = []
        start_date = datetime.utcnow()
        
        # Week 1: Teaser content
        timeline.append({
            "week": 1,
            "start_date": start_date.isoformat(),
            "focus": "Teaser & Awareness",
            "activities": ["Social media teasers", "Email list building", "Influencer outreach"]
        })
        
        # Week 2: Launch
        timeline.append({
            "week": 2, 
            "start_date": (start_date + timedelta(days=7)).isoformat(),
            "focus": "Product Launch",
            "activities": ["Launch announcement", "Paid ads campaign", "PR outreach"]
        })
        
        # Week 3: Amplification
        timeline.append({
            "week": 3,
            "start_date": (start_date + timedelta(days=14)).isoformat(),
            "focus": "Amplification",
            "activities": ["Customer testimonials", "Content marketing", "Retargeting campaigns"]
        })
        
        return timeline
    
    def _recommend_budget(self, product_data: Dict) -> Dict:
        """Recommend marketing budget based on product"""
        price = product_data.get("price", 9.99)
        
        # Budget based on product price
        if price < 20:
            daily_budget = 10
        elif price < 100:
            daily_budget = 25
        else:
            daily_budget = 50
        
        return {
            "daily_budget": daily_budget,
            "weekly_budget": daily_budget * 7,
            "platform_split": {
                "facebook": 0.4,
                "instagram": 0.3,
                "google": 0.3
            },
            "expected_roas": 3.5  # Return on ad spend
        }
    
    def execute_marketing_campaign(self, product_data: Dict) -> Dict:
        """Main method: Execute complete marketing campaign"""
        try:
            # Create campaign strategy
            strategy = self.create_campaign_strategy(product_data)
            
            if not strategy.get("success"):
                return strategy
            
            # Generate content for immediate posting
            immediate_content = []
            for platform in ["instagram", "twitter", "linkedin"]:
                content = self.generate_social_content(product_data, platform)
                immediate_content.append(content)
            
            # Schedule posts
            scheduling_result = self.schedule_social_posts(immediate_content)
            
            # Simulate ad campaign creation (would integrate with real APIs in production)
            ad_campaign = self._simulate_ad_campaign(product_data)
            
            result = {
                "success": True,
                "strategy": strategy["campaign"],
                "content_generated": len(immediate_content),
                "posts_scheduled": scheduling_result.get("posts_scheduled", 0),
                "ad_campaign": ad_campaign,
                "timestamp": datetime.utcnow().isoformat(),
                "estimated_results": {
                    "reach": random.randint(10000, 50000),
                    "engagement_rate": round(random.uniform(2.5, 8.5), 2),
                    "estimated_conversions": random.randint(50, 200)
                }
            }
            
            logger.info(f"Marketing campaign executed for: {product_data.get('title')}")
            return result
            
        except Exception as e:
            logger.error(f"Marketing campaign error: {e}")
            return {
                "success": False,
                "error": str(e),
                "product": product_data.get("title", "unknown"),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def _simulate_ad_campaign(self, product_data: Dict) -> Dict:
        """Simulate ad campaign creation (replace with real API calls)"""
        # In production, this would create real Facebook/Google ads
        campaign_data = {
            "campaign_id": f"sim_campaign_{datetime.utcnow().timestamp()}",
            "status": "active",
            "daily_budget": self._recommend_budget(product_data)["daily_budget"],
            "target_audience": {
                "age_range": "25-55",
                "interests": ["entrepreneurship", "online business", "productivity"],
                "location": "United States, Canada, UK, Australia"
            },
            "ad_sets": 3,
            "total_ads": 6
        }
        
        # Save to database
        try:
            ad_entity = AdEntity(
                user_id=self.user_id,
                platform="meta",
                campaign_id=campaign_data["campaign_id"],
                objective="conversions"
            )
            db.session.add(ad_entity)
            db.session.commit()
        except Exception as e:
            logger.error(f"Ad entity save error: {e}")
        
        return campaign_data

def execute_marketing_campaign(user_id: int, product_data: Dict) -> Dict:
    """Convenience function to execute marketing campaign"""
    marketer = MarketerAgent(user_id)
    return marketer.execute_marketing_campaign(product_data)

def generate_social_content(user_id: int, product_data: Dict, platform: str = "instagram") -> Dict:
    """Convenience function to generate social content"""
    marketer = MarketerAgent(user_id)
    return marketer.generate_social_content(product_data, platform)

if __name__ == "__main__":
    # Test the marketer
    print("📢 Testing Marketer Agent...")
    test_product = {
        "title": "AI Productivity Masterclass",
        "description": "Complete guide to AI productivity tools",
        "price": 29.99,
        "category": "course"
    }
    
    result = execute_marketing_campaign(1, test_product)
    print(f"Campaign: {result.get('success')}")
    print(f"Content pieces: {result.get('content_generated')}")
    print(f"Posts scheduled: {result.get('posts_scheduled')}")