"""
🎯 Strategist Agent - AI CEO Multi-Agent Intelligence
Decides what kind of product/business to build based on trends and memory
"""

import logging
from datetime import datetime, timedelta
from models import db, AgentMemory
from config import OPENROUTER_API_KEY
import requests
import json
from typing import Dict, List, Optional
from pytrends.request import TrendReq

logger = logging.getLogger(__name__)

class StrategistAgent:
    """AI strategist that decides what products/businesses to build"""
    
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.pytrends = TrendReq(hl='en-US', tz=360)
        
    def get_memory(self, key: str = None) -> List[Dict]:
        """Pull strategic insights from local database memory"""
        try:
            query = db.session.query(AgentMemory).filter_by(user_id=self.user_id)
            if key:
                query = query.filter_by(key=key)
            
            memories = query.order_by(AgentMemory.created_at.desc()).limit(50).all()
            return [{"key": m.key, "value": m.value, "created_at": m.created_at} for m in memories]
        except Exception as e:
            logger.error(f"Error retrieving memory: {e}")
            return []
    
    def save_memory(self, key: str, value: str):
        """Save strategic insight to local database"""
        try:
            memory = AgentMemory(user_id=self.user_id, key=key, value=value)
            db.session.add(memory)
            db.session.commit()
            logger.info(f"Saved memory: {key}")
        except Exception as e:
            logger.error(f"Error saving memory: {e}")
    
    def analyze_google_trends(self, keywords: List[str]) -> Dict:
        """Get Google Trends data for strategic analysis"""
        try:
            self.pytrends.build_payload(keywords, cat=0, timeframe='today 7-d')
            interest_over_time = self.pytrends.interest_over_time()
            
            if not interest_over_time.empty:
                # Get top trending keyword
                latest_data = interest_over_time.iloc[-1]
                top_keyword = latest_data.drop('isPartial').idxmax()
                trend_score = latest_data[top_keyword]
                
                return {
                    "top_keyword": top_keyword,
                    "trend_score": int(trend_score),
                    "trending_up": trend_score > 50,
                    "data": interest_over_time.to_dict()
                }
            
            return {"error": "No trend data available"}
            
        except Exception as e:
            logger.error(f"Google Trends error: {e}")
            return {"error": str(e)}
    
    def get_market_insights(self) -> Dict:
        """Analyze market trends and opportunities"""
        # Common profitable niches
        trending_niches = [
            "AI tools", "productivity apps", "digital marketing", 
            "health supplements", "online courses", "templates",
            "automation software", "crypto tools", "fitness programs"
        ]
        
        trend_data = self.analyze_google_trends(trending_niches[:5])
        
        # Get historical performance from memory
        past_strategies = self.get_memory("strategy_result")
        successful_strategies = []
        
        for memory in past_strategies:
            try:
                data = json.loads(memory["value"])
                if data.get("profit", 0) > 0:
                    successful_strategies.append(data.get("strategy"))
            except:
                continue
        
        return {
            "trending_keyword": trend_data.get("top_keyword", "AI tools"),
            "trend_score": trend_data.get("trend_score", 75),
            "successful_past_strategies": successful_strategies[:3],
            "market_opportunity": "high" if trend_data.get("trend_score", 0) > 60 else "medium"
        }
    
    def generate_strategy_with_ai(self, market_data: Dict) -> str:
        """Use OpenRouter AI to generate strategic recommendation"""
        try:
            prompt = f"""
            As an AI business strategist, analyze this market data and recommend the best product strategy:
            
            Market Data:
            - Trending keyword: {market_data.get('trending_keyword')}
            - Trend score: {market_data.get('trend_score')}
            - Past successes: {market_data.get('successful_past_strategies')}
            - Market opportunity: {market_data.get('market_opportunity')}
            
            Recommend ONE specific product type to create (ebook, course, template, tool, etc.)
            and the exact niche/topic. Be specific and actionable.
            
            Format: Just return the strategy as a single sentence.
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
                    "max_tokens": 150
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                strategy = result['choices'][0]['message']['content'].strip()
                return strategy
            else:
                logger.error(f"OpenRouter API error: {response.status_code}")
                return self._fallback_strategy(market_data)
                
        except Exception as e:
            logger.error(f"AI strategy generation error: {e}")
            return self._fallback_strategy(market_data)
    
    def _fallback_strategy(self, market_data: Dict) -> str:
        """Fallback strategy when AI fails"""
        trending = market_data.get('trending_keyword', 'productivity')
        return f"Create an ebook about {trending} for beginners with actionable tips and templates"
    
    def decide_strategy(self) -> Dict:
        """Main method: Decide what product/business to build"""
        try:
            # Analyze market
            market_data = self.get_market_insights()
            
            # Generate AI-powered strategy
            recommended_strategy = self.generate_strategy_with_ai(market_data)
            
            # Save strategy decision to memory
            strategy_data = {
                "strategy": recommended_strategy,
                "market_data": market_data,
                "timestamp": datetime.utcnow().isoformat(),
                "confidence": 0.8
            }
            
            self.save_memory("strategy_decision", json.dumps(strategy_data))
            
            result = {
                "recommended_strategy": recommended_strategy,
                "market_insight": market_data,
                "confidence": 0.8,
                "strategy_type": self._extract_strategy_type(recommended_strategy),
                "timestamp": datetime.utcnow().isoformat()
            }
            
            logger.info(f"Strategy decided: {recommended_strategy}")
            return result
            
        except Exception as e:
            logger.error(f"Strategy decision error: {e}")
            return {
                "recommended_strategy": "Create an ebook about AI productivity tools with templates",
                "market_insight": {"trending_keyword": "AI tools", "trend_score": 70},
                "confidence": 0.5,
                "strategy_type": "ebook",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def _extract_strategy_type(self, strategy: str) -> str:
        """Extract product type from strategy"""
        strategy_lower = strategy.lower()
        if "ebook" in strategy_lower:
            return "ebook"
        elif "course" in strategy_lower:
            return "course"
        elif "template" in strategy_lower:
            return "template"
        elif "tool" in strategy_lower or "software" in strategy_lower:
            return "tool"
        elif "bundle" in strategy_lower:
            return "bundle"
        else:
            return "ebook"  # Default

def get_strategy_recommendation(user_id: int) -> Dict:
    """Convenience function to get strategy recommendation"""
    strategist = StrategistAgent(user_id)
    return strategist.decide_strategy()

if __name__ == "__main__":
    # Test the strategist
    print("🎯 Testing Strategist Agent...")
    result = get_strategy_recommendation(1)
    print(f"Strategy: {result['recommended_strategy']}")
    print(f"Type: {result['strategy_type']}")
    print(f"Confidence: {result['confidence']}")