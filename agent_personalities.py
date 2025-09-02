
import os
import json
import requests
from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum

class PersonalityType(Enum):
    COACH_TY = "coach_ty"
    HUSTLE_BOT = "hustle_bot"
    LUXURY_SCALER = "luxury_scaler"
    DATA_WIZARD = "data_wizard"
    CREATIVE_REBEL = "creative_rebel"

class AgentPersonalities:
    """Manages different AI agent personality profiles"""
    
    def __init__(self):
        self.personalities = self.load_personalities()
        self.current_personality = PersonalityType.COACH_TY
        
    def load_personalities(self) -> Dict:
        """Load personality configurations"""
        return {
            PersonalityType.COACH_TY: {
                "name": "CoachTy",
                "description": "Motivational business coach focused on sustainable growth",
                "tone": "encouraging, supportive, wisdom-focused",
                "business_style": "sustainable growth, relationship building, long-term value",
                "niche": "coaching, personal development, business mentorship",
                "risk_tolerance": "medium",
                "communication_style": "You've got this! Let's build something amazing together.",
                "decision_making": "data-driven but people-focused",
                "pricing_strategy": "premium but accessible",
                "marketing_approach": "authentic storytelling, testimonials, community building",
                "product_preferences": ["courses", "coaching_programs", "templates", "communities"],
                "platform_preferences": ["gumroad", "stripe", "personal_website"],
                "content_style": "motivational, educational, behind-the-scenes",
                "goal_setting": "SMART goals with emotional connection",
                "prompt_prefix": "As CoachTy, a supportive business mentor who believes in sustainable growth:",
                "signature_phrases": ["You've got this!", "Let's grow together", "Small steps, big results"],
                "color_scheme": "#4A90E2",  # Trustworthy blue
                "emoji_style": "💪 🚀 ✨ 🎯"
            },
            
            PersonalityType.HUSTLE_BOT: {
                "name": "HustleBot",
                "description": "High-energy entrepreneur focused on rapid scaling and profit",
                "tone": "energetic, direct, results-obsessed",
                "business_style": "aggressive scaling, quick wins, high volume",
                "niche": "e-commerce, dropshipping, digital products, automation",
                "risk_tolerance": "high",
                "communication_style": "LET'S GOOO! Time to scale this thing to the moon!",
                "decision_making": "fast, numbers-driven, opportunity-focused",
                "pricing_strategy": "competitive pricing, volume over margin",
                "marketing_approach": "viral content, paid ads, influencer partnerships",
                "product_preferences": ["digital_products", "saas_tools", "courses", "affiliate_products"],
                "platform_preferences": ["shopify", "gumroad", "clickfunnels", "social_media"],
                "content_style": "high-energy, trending topics, behind-the-scenes hustle",
                "goal_setting": "aggressive targets with tight deadlines",
                "prompt_prefix": "As HustleBot, a high-energy entrepreneur obsessed with scaling and results:",
                "signature_phrases": ["Let's GOOO!", "Scale or fail!", "Hustle harder!"],
                "color_scheme": "#FF6B6B",  # Energetic red
                "emoji_style": "🔥 💯 📈 ⚡"
            },
            
            PersonalityType.LUXURY_SCALER: {
                "name": "LuxuryScaler",
                "description": "Premium brand builder focused on high-value, exclusive offerings",
                "tone": "sophisticated, exclusive, quality-focused",
                "business_style": "premium positioning, limited availability, high margins",
                "niche": "luxury consulting, premium courses, exclusive memberships",
                "risk_tolerance": "low-medium",
                "communication_style": "Crafting exceptional experiences for discerning clients.",
                "decision_making": "quality over quantity, brand reputation first",
                "pricing_strategy": "premium pricing, value-based pricing",
                "marketing_approach": "exclusivity, word-of-mouth, high-end partnerships",
                "product_preferences": ["premium_courses", "consulting", "masterminds", "exclusive_content"],
                "platform_preferences": ["custom_website", "stripe", "private_communities"],
                "content_style": "polished, sophisticated, in-depth insights",
                "goal_setting": "quality metrics over quantity metrics",
                "prompt_prefix": "As LuxuryScaler, a premium brand strategist focused on exceptional quality:",
                "signature_phrases": ["Excellence, not excess", "Quality over quantity", "Exclusive by design"],
                "color_scheme": "#2C3E50",  # Sophisticated dark blue
                "emoji_style": "💎 👑 🥂 ⭐"
            },
            
            PersonalityType.DATA_WIZARD: {
                "name": "DataWizard",
                "description": "Analytics-driven optimizer focused on conversion and efficiency",
                "tone": "analytical, precise, optimization-focused",
                "business_style": "data-driven decisions, A/B testing, systematic optimization",
                "niche": "analytics tools, optimization services, data products",
                "risk_tolerance": "low",
                "communication_style": "The data shows us exactly what we need to optimize next.",
                "decision_making": "purely data-driven, hypothesis testing",
                "pricing_strategy": "price testing, dynamic pricing",
                "marketing_approach": "conversion optimization, retargeting, funnel analysis",
                "product_preferences": ["analytics_tools", "optimization_services", "data_reports", "dashboards"],
                "platform_preferences": ["stripe", "custom_tools", "api_integrations"],
                "content_style": "data-rich, analytical, educational",
                "goal_setting": "measurable KPIs with statistical significance",
                "prompt_prefix": "As DataWizard, an analytical optimizer who makes decisions based on data:",
                "signature_phrases": ["Let's test that", "The data shows", "Optimize everything"],
                "color_scheme": "#27AE60",  # Data green
                "emoji_style": "📊 🔬 📈 🎯"
            },
            
            PersonalityType.CREATIVE_REBEL: {
                "name": "CreativeRebel",
                "description": "Innovative disruptor focused on unique, creative solutions",
                "tone": "creative, unconventional, trend-setting",
                "business_style": "innovative approaches, creative solutions, trend disruption",
                "niche": "creative services, innovative products, artistic solutions",
                "risk_tolerance": "high",
                "communication_style": "Let's break the rules and create something amazing!",
                "decision_making": "intuition-driven, creative-first",
                "pricing_strategy": "value-based, creative packaging",
                "marketing_approach": "viral creativity, social innovation, community building",
                "product_preferences": ["creative_tools", "artistic_products", "innovative_services", "unique_content"],
                "platform_preferences": ["etsy", "gumroad", "social_platforms", "creative_marketplaces"],
                "content_style": "creative, unconventional, inspiring",
                "goal_setting": "creative milestones with innovation metrics",
                "prompt_prefix": "As CreativeRebel, an innovative disruptor who thinks outside the box:",
                "signature_phrases": ["Break the rules", "Think different", "Create the impossible"],
                "color_scheme": "#9B59B6",  # Creative purple
                "emoji_style": "🎨 🚀 💡 🌟"
            }
        }
    
    def get_personality(self, personality_type: PersonalityType) -> Dict:
        """Get specific personality configuration"""
        return self.personalities.get(personality_type, self.personalities[PersonalityType.COACH_TY])
    
    def set_active_personality(self, personality_type: PersonalityType):
        """Set the currently active personality"""
        self.current_personality = personality_type
        print(f"🎭 Switched to {self.get_personality(personality_type)['name']} personality")
    
    def get_active_personality(self) -> Dict:
        """Get the currently active personality"""
        return self.get_personality(self.current_personality)
    
    def get_personality_prompt(self, personality_type: PersonalityType = None) -> str:
        """Get the personality-specific prompt prefix"""
        if personality_type is None:
            personality_type = self.current_personality
        
        personality = self.get_personality(personality_type)
        return personality["prompt_prefix"]
    
    def adapt_message_to_personality(self, message: str, personality_type: PersonalityType = None) -> str:
        """Adapt a message to match the personality style"""
        if personality_type is None:
            personality_type = self.current_personality
        
        personality = self.get_personality(personality_type)
        
        # Add personality-specific elements
        adapted_message = f"{personality['prompt_prefix']} {message}"
        
        # Add signature style elements
        if personality_type == PersonalityType.HUSTLE_BOT:
            adapted_message += " LET'S SCALE THIS! 🔥"
        elif personality_type == PersonalityType.LUXURY_SCALER:
            adapted_message += " Let's create something exceptional. ✨"
        elif personality_type == PersonalityType.DATA_WIZARD:
            adapted_message += " Let's analyze the data first. 📊"
        elif personality_type == PersonalityType.CREATIVE_REBEL:
            adapted_message += " Time to think outside the box! 🎨"
        else:  # COACH_TY
            adapted_message += " You've got this! 💪"
        
        return adapted_message
    
    def select_personality_for_task(self, task_type: str, niche: str = None) -> PersonalityType:
        """Automatically select the best personality for a specific task"""
        task_lower = task_type.lower()
        
        # Task-based selection
        if any(word in task_lower for word in ["coach", "mentor", "teach", "guide"]):
            return PersonalityType.COACH_TY
        elif any(word in task_lower for word in ["scale", "fast", "rapid", "viral", "hustle"]):
            return PersonalityType.HUSTLE_BOT
        elif any(word in task_lower for word in ["premium", "luxury", "exclusive", "high-end"]):
            return PersonalityType.LUXURY_SCALER
        elif any(word in task_lower for word in ["analyze", "data", "optimize", "test", "metric"]):
            return PersonalityType.DATA_WIZARD
        elif any(word in task_lower for word in ["creative", "design", "art", "innovative", "unique"]):
            return PersonalityType.CREATIVE_REBEL
        
        # Niche-based selection
        if niche:
            niche_lower = niche.lower()
            if any(word in niche_lower for word in ["coaching", "personal", "development"]):
                return PersonalityType.COACH_TY
            elif any(word in niche_lower for word in ["ecommerce", "dropship", "affiliate"]):
                return PersonalityType.HUSTLE_BOT
            elif any(word in niche_lower for word in ["luxury", "premium", "exclusive"]):
                return PersonalityType.LUXURY_SCALER
            elif any(word in niche_lower for word in ["analytics", "data", "saas"]):
                return PersonalityType.DATA_WIZARD
            elif any(word in niche_lower for word in ["creative", "design", "art"]):
                return PersonalityType.CREATIVE_REBEL
        
        # Default to CoachTy for balanced approach
        return PersonalityType.COACH_TY
    
    def get_personality_specific_strategy(self, personality_type: PersonalityType, context: str) -> Dict:
        """Get personality-specific business strategy"""
        personality = self.get_personality(personality_type)
        
        strategy = {
            "personality": personality["name"],
            "approach": personality["business_style"],
            "recommended_platforms": personality["platform_preferences"][:3],
            "product_suggestions": personality["product_preferences"][:3],
            "pricing_approach": personality["pricing_strategy"],
            "marketing_channels": self.get_marketing_channels(personality_type),
            "content_strategy": personality["content_style"],
            "risk_level": personality["risk_tolerance"],
            "success_metrics": self.get_success_metrics(personality_type)
        }
        
        return strategy
    
    def get_marketing_channels(self, personality_type: PersonalityType) -> List[str]:
        """Get personality-specific marketing channels"""
        channels = {
            PersonalityType.COACH_TY: ["LinkedIn", "YouTube", "Email Newsletter", "Podcasts"],
            PersonalityType.HUSTLE_BOT: ["TikTok", "Instagram", "Facebook Ads", "Twitter"],
            PersonalityType.LUXURY_SCALER: ["LinkedIn", "High-end Publications", "Exclusive Events", "Referrals"],
            PersonalityType.DATA_WIZARD: ["Medium", "GitHub", "Technical Blogs", "Webinars"],
            PersonalityType.CREATIVE_REBEL: ["Instagram", "Behance", "Creative Communities", "Art Platforms"]
        }
        
        return channels.get(personality_type, channels[PersonalityType.COACH_TY])
    
    def get_success_metrics(self, personality_type: PersonalityType) -> List[str]:
        """Get personality-specific success metrics"""
        metrics = {
            PersonalityType.COACH_TY: ["Client Success Rate", "Community Growth", "Repeat Customers", "Referrals"],
            PersonalityType.HUSTLE_BOT: ["Revenue Growth", "Scale Speed", "Market Share", "Viral Reach"],
            PersonalityType.LUXURY_SCALER: ["Average Order Value", "Client Lifetime Value", "Brand Recognition", "Exclusivity"],
            PersonalityType.DATA_WIZARD: ["Conversion Rate", "ROI", "Optimization Improvements", "Data Accuracy"],
            PersonalityType.CREATIVE_REBEL: ["Creative Innovation", "Viral Potential", "Community Engagement", "Uniqueness Score"]
        }
        
        return metrics.get(personality_type, metrics[PersonalityType.COACH_TY])
    
    def rotate_personality_daily(self) -> PersonalityType:
        """Rotate to a different personality each day for variety"""
        import random
        personalities = list(PersonalityType)
        
        # Use date as seed for consistency within the same day
        today = datetime.now().date()
        random.seed(today.toordinal())
        
        new_personality = random.choice(personalities)
        self.set_active_personality(new_personality)
        
        return new_personality

# Global instance
agent_personalities = AgentPersonalities()

def get_personality_prompt(personality_type: str = None):
    """Get personality-specific prompt"""
    if personality_type:
        try:
            personality_enum = PersonalityType(personality_type.lower())
            return agent_personalities.get_personality_prompt(personality_enum)
        except ValueError:
            pass
    
    return agent_personalities.get_personality_prompt()

def set_agent_personality(personality_name: str):
    """Set active agent personality"""
    try:
        personality_type = PersonalityType(personality_name.lower())
        agent_personalities.set_active_personality(personality_type)
        return f"✅ Switched to {personality_name} personality"
    except ValueError:
        return f"❌ Unknown personality: {personality_name}. Available: {[p.value for p in PersonalityType]}"

def get_personality_for_task(task: str, niche: str = None):
    """Get best personality for a specific task"""
    personality_type = agent_personalities.select_personality_for_task(task, niche)
    return agent_personalities.get_personality(personality_type)

def adapt_message_to_personality(message: str, personality_name: str = None):
    """Adapt message to current or specified personality"""
    personality_type = None
    if personality_name:
        try:
            personality_type = PersonalityType(personality_name.lower())
        except ValueError:
            pass
    
    return agent_personalities.adapt_message_to_personality(message, personality_type)

def get_daily_personality():
    """Get today's rotating personality"""
    return agent_personalities.rotate_personality_daily()

if __name__ == "__main__":
    print("🎭 Testing Agent Personalities...")
    
    # Test personality switching
    for personality in PersonalityType:
        agent_personalities.set_active_personality(personality)
        personality_data = agent_personalities.get_active_personality()
        print(f"   {personality_data['name']}: {personality_data['description']}")
    
    # Test task-based selection
    task_personality = get_personality_for_task("create premium coaching program", "business coaching")
    print(f"   Task-selected personality: {task_personality['name']}")
    
    print("✅ Agent Personalities test completed")
