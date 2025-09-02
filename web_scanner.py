
import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime
from typing import List, Dict
import random
from google_trends_tool import fetch_google_trends, get_trending_searches

class TrendingProductScanner:
    """Advanced web scanner for trending products and market opportunities"""
    
    def __init__(self):
        self.sources = [
            "https://trends.google.com/trends/trendingsearches/daily",
            "https://www.producthunt.com/",
            "https://www.kickstarter.com/discover/advanced"
        ]
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        ]
    
    def scan_trending_products(self) -> List[Dict]:
        """Scan multiple sources for trending products"""
        trending_products = []
        
        # Get Google trending searches
        try:
            google_trends = get_trending_searches()
            for trend in google_trends[:10]:
                product_opportunity = self.analyze_trend_for_product(trend)
                if product_opportunity:
                    trending_products.append(product_opportunity)
        except Exception as e:
            print(f"Google trends error: {e}")
        
        # Analyze Reddit trending topics
        reddit_products = self.scan_reddit_trends()
        trending_products.extend(reddit_products)
        
        # Check Amazon best sellers categories
        amazon_trends = self.scan_amazon_bestsellers()
        trending_products.extend(amazon_trends)
        
        return trending_products[:20]  # Top 20 opportunities
    
    def analyze_trend_for_product(self, trend: str) -> Dict:
        """Analyze if a trend can become a digital product"""
        try:
            # Get trend data
            trend_data = fetch_google_trends(trend, "today 1-m")
            
            if trend_data.get("avg_interest", 0) < 30:
                return None
            
            # Determine product type based on keywords
            product_types = {
                "course": ["learn", "how to", "tutorial", "guide", "training"],
                "ebook": ["tips", "secrets", "ultimate", "complete", "master"],
                "template": ["template", "worksheet", "planner", "toolkit"],
                "software": ["app", "tool", "software", "automation", "AI"]
            }
            
            product_type = "ebook"  # default
            for ptype, keywords in product_types.items():
                if any(keyword in trend.lower() for keyword in keywords):
                    product_type = ptype
                    break
            
            return {
                "trend": trend,
                "product_type": product_type,
                "title": f"{trend.title()} {product_type.title()}",
                "interest_score": trend_data.get("avg_interest", 0),
                "market_size": "medium",
                "competition": "low",
                "suggested_price": self.calculate_price(product_type, trend_data.get("avg_interest", 0)),
                "description": f"Complete {product_type} covering everything about {trend}",
                "discovered_at": datetime.now().isoformat()
            }
        except Exception as e:
            print(f"Trend analysis error: {e}")
            return None
    
    def scan_reddit_trends(self) -> List[Dict]:
        """Scan Reddit for trending topics that could become products"""
        try:
            # Simulate Reddit trending topics (replace with actual Reddit API)
            reddit_trends = [
                "AI productivity hacks",
                "Remote work setup",
                "Cryptocurrency trading",
                "Fitness tracking apps",
                "Meal prep automation"
            ]
            
            products = []
            for trend in reddit_trends:
                product = {
                    "trend": trend,
                    "product_type": "course",
                    "title": f"Master {trend}",
                    "interest_score": random.randint(40, 80),
                    "market_size": "large",
                    "competition": "medium",
                    "suggested_price": random.randint(47, 127),
                    "description": f"Comprehensive guide to {trend}",
                    "source": "reddit",
                    "discovered_at": datetime.now().isoformat()
                }
                products.append(product)
            
            return products[:5]
        except Exception as e:
            print(f"Reddit scan error: {e}")
            return []
    
    def scan_amazon_bestsellers(self) -> List[Dict]:
        """Scan Amazon bestsellers for product inspiration"""
        try:
            # Simulate Amazon bestseller categories
            bestseller_categories = [
                "Business & Investing",
                "Health & Fitness",
                "Self-Help",
                "Technology",
                "Education"
            ]
            
            products = []
            for category in bestseller_categories:
                product = {
                    "trend": f"{category} bestseller",
                    "product_type": "ebook",
                    "title": f"Ultimate {category} Guide",
                    "interest_score": random.randint(50, 90),
                    "market_size": "large",
                    "competition": "high",
                    "suggested_price": random.randint(27, 67),
                    "description": f"Professional {category} resource",
                    "source": "amazon",
                    "discovered_at": datetime.now().isoformat()
                }
                products.append(product)
            
            return products
        except Exception as e:
            print(f"Amazon scan error: {e}")
            return []
    
    def calculate_price(self, product_type: str, interest_score: int) -> float:
        """Calculate optimal price based on product type and market interest"""
        base_prices = {
            "ebook": 19.99,
            "course": 67.00,
            "template": 14.99,
            "software": 97.00
        }
        
        base_price = base_prices.get(product_type, 47.00)
        
        # Adjust based on interest score
        if interest_score > 70:
            multiplier = 1.5
        elif interest_score > 50:
            multiplier = 1.2
        else:
            multiplier = 1.0
        
        return round(base_price * multiplier, 2)

def scan_for_trending_products() -> List[Dict]:
    """Main function to scan for trending products"""
    scanner = TrendingProductScanner()
    return scanner.scan_trending_products()
