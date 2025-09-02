"""
🌐 Data Scraper - AI CEO Multi-Agent Intelligence
Real-time trend data collection from multiple sources for strategic insights
"""

import logging
from datetime import datetime, timedelta
from models import db, TrendData
import requests
import json
from typing import Dict, List, Optional
import time
import random
from pytrends.request import TrendReq
from bs4 import BeautifulSoup
import feedparser

logger = logging.getLogger(__name__)

class DataScraperAgent:
    """Multi-source trend data collection agent"""
    
    def __init__(self):
        self.pytrends = TrendReq(hl='en-US', tz=360)
        self.sources = {
            'google': self.scrape_google_trends,
            'amazon': self.scrape_amazon_bestsellers,
            'producthunt': self.scrape_producthunt_launches,
            'tiktok': self.scrape_tiktok_trends
        }
    
    def scrape_google_trends(self, keywords: List[str] = None) -> List[Dict]:
        """Scrape Google Trends data"""
        try:
            if not keywords:
                keywords = [
                    "AI tools", "digital marketing", "productivity apps", 
                    "online courses", "automation software", "crypto trading",
                    "health supplements", "fitness programs", "templates"
                ]
            
            trends_data = []
            
            # Process keywords in batches of 5 (Google Trends limit)
            for i in range(0, len(keywords), 5):
                batch = keywords[i:i+5]
                
                try:
                    self.pytrends.build_payload(batch, timeframe='today 7-d')
                    interest_data = self.pytrends.interest_over_time()
                    
                    if not interest_data.empty:
                        latest_data = interest_data.iloc[-1]
                        
                        for keyword in batch:
                            if keyword in latest_data.index:
                                trend_score = latest_data[keyword] if not pd.isna(latest_data[keyword]) else 0
                                
                                trends_data.append({
                                    'source': 'google',
                                    'keyword': keyword,
                                    'trend_score': float(trend_score),
                                    'rank': self._calculate_rank(trend_score, 100),
                                    'category': self._categorize_keyword(keyword),
                                    'additional_data': json.dumps({
                                        'timeframe': '7d',
                                        'region': 'US',
                                        'scraped_at': datetime.utcnow().isoformat()
                                    })
                                })
                    
                    # Rate limiting
                    time.sleep(1)
                    
                except Exception as e:
                    logger.warning(f"Google Trends batch error: {e}")
                    continue
            
            logger.info(f"Scraped {len(trends_data)} Google Trends data points")
            return trends_data
            
        except Exception as e:
            logger.error(f"Google Trends scraping error: {e}")
            return []
    
    def scrape_amazon_bestsellers(self, categories: List[str] = None) -> List[Dict]:
        """Scrape Amazon Best Sellers (simulated for compliance)"""
        try:
            if not categories:
                categories = [
                    "Books", "Electronics", "Health & Personal Care", 
                    "Software", "Home & Kitchen", "Sports & Outdoors"
                ]
            
            trends_data = []
            
            # Simulate Amazon data (replace with real scraping if authorized)
            simulated_products = [
                "AI Productivity Planner", "Digital Marketing Course", "Home Office Setup",
                "Fitness Tracker", "Cryptocurrency Guide", "Language Learning App",
                "Cooking Templates", "Project Management Tool", "Health Supplement",
                "Tech Gadget", "Online Course Platform", "Marketing Automation"
            ]
            
            for i, product in enumerate(simulated_products):
                category = random.choice(categories)
                rank = i + 1
                
                # Simulate trend score based on rank
                trend_score = max(100 - (rank * 5), 10)
                
                trends_data.append({
                    'source': 'amazon',
                    'keyword': product,
                    'trend_score': trend_score,
                    'rank': rank,
                    'category': category,
                    'additional_data': json.dumps({
                        'bestseller_rank': rank,
                        'category': category,
                        'simulated': True,
                        'scraped_at': datetime.utcnow().isoformat()
                    })
                })
            
            logger.info(f"Generated {len(trends_data)} Amazon trend data points (simulated)")
            return trends_data
            
        except Exception as e:
            logger.error(f"Amazon scraping error: {e}")
            return []
    
    def scrape_producthunt_launches(self) -> List[Dict]:
        """Scrape Product Hunt launches via RSS"""
        try:
            trends_data = []
            
            # Use Product Hunt RSS feed
            rss_url = "https://www.producthunt.com/feed"
            
            try:
                feed = feedparser.parse(rss_url)
                
                for i, entry in enumerate(feed.entries[:20]):  # Latest 20 launches
                    title = entry.get('title', 'Unknown Product')
                    
                    # Extract keywords from title and description
                    keywords = self._extract_keywords_from_text(f"{title} {entry.get('summary', '')}")
                    
                    for keyword in keywords[:3]:  # Top 3 keywords per product
                        trends_data.append({
                            'source': 'producthunt',
                            'keyword': keyword,
                            'trend_score': max(90 - (i * 3), 10),  # Decay score by position
                            'rank': i + 1,
                            'category': 'product_launch',
                            'additional_data': json.dumps({
                                'product_title': title,
                                'launch_date': entry.get('published', ''),
                                'url': entry.get('link', ''),
                                'scraped_at': datetime.utcnow().isoformat()
                            })
                        })
                
            except Exception as e:
                logger.warning(f"ProductHunt RSS error: {e}")
                # Fallback to simulated data
                trends_data = self._generate_fallback_producthunt_data()
            
            logger.info(f"Scraped {len(trends_data)} ProductHunt data points")
            return trends_data
            
        except Exception as e:
            logger.error(f"ProductHunt scraping error: {e}")
            return []
    
    def scrape_tiktok_trends(self) -> List[Dict]:
        """Scrape TikTok trends (simulated for compliance)"""
        try:
            # Simulate TikTok trending hashtags/topics
            simulated_trends = [
                "#productivity", "#sidehustle", "#entrepreneur", "#digitalmarketing",
                "#AI", "#automation", "#onlinebusiness", "#makemoneyonline", 
                "#passiveincome", "#workfromhome", "#digitalproducts", "#crypto",
                "#fitness", "#mindset", "#success", "#businesstips"
            ]
            
            trends_data = []
            
            for i, trend in enumerate(simulated_trends):
                # Simulate engagement metrics
                trend_score = random.randint(60, 95)
                
                trends_data.append({
                    'source': 'tiktok',
                    'keyword': trend,
                    'trend_score': trend_score,
                    'rank': i + 1,
                    'category': 'social_trend',
                    'additional_data': json.dumps({
                        'hashtag': trend,
                        'platform': 'tiktok',
                        'simulated_views': random.randint(10000, 1000000),
                        'simulated': True,
                        'scraped_at': datetime.utcnow().isoformat()
                    })
                })
            
            logger.info(f"Generated {len(trends_data)} TikTok trend data points (simulated)")
            return trends_data
            
        except Exception as e:
            logger.error(f"TikTok scraping error: {e}")
            return []
    
    def _generate_fallback_producthunt_data(self) -> List[Dict]:
        """Generate fallback ProductHunt data when RSS fails"""
        fallback_products = [
            "AI Writing Assistant", "No-Code Website Builder", "Social Media Scheduler",
            "Project Management App", "Design Tool", "Marketing Analytics", 
            "Customer Support Bot", "E-commerce Platform", "Video Editor",
            "Password Manager", "Note Taking App", "Time Tracker"
        ]
        
        trends_data = []
        for i, product in enumerate(fallback_products):
            keywords = self._extract_keywords_from_text(product)
            
            for keyword in keywords:
                trends_data.append({
                    'source': 'producthunt',
                    'keyword': keyword,
                    'trend_score': max(85 - (i * 2), 15),
                    'rank': i + 1,
                    'category': 'product_launch',
                    'additional_data': json.dumps({
                        'product_title': product,
                        'simulated': True,
                        'scraped_at': datetime.utcnow().isoformat()
                    })
                })
        
        return trends_data[:30]  # Limit to 30 data points
    
    def _extract_keywords_from_text(self, text: str) -> List[str]:
        """Extract meaningful keywords from text"""
        import re
        
        # Remove special characters and split
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        
        # Filter out common stop words
        stop_words = {
            'the', 'and', 'for', 'with', 'app', 'tool', 'software', 'platform',
            'new', 'best', 'top', 'your', 'you', 'can', 'get', 'use', 'now'
        }
        
        keywords = [word for word in words if word not in stop_words]
        
        # Return top 5 most relevant keywords
        return keywords[:5]
    
    def _categorize_keyword(self, keyword: str) -> str:
        """Categorize keyword into business category"""
        keyword_lower = keyword.lower()
        
        if any(term in keyword_lower for term in ['ai', 'automation', 'tech', 'software']):
            return 'technology'
        elif any(term in keyword_lower for term in ['marketing', 'social', 'ads', 'seo']):
            return 'marketing'
        elif any(term in keyword_lower for term in ['health', 'fitness', 'wellness']):
            return 'health'
        elif any(term in keyword_lower for term in ['business', 'entrepreneur', 'money']):
            return 'business'
        elif any(term in keyword_lower for term in ['education', 'course', 'learning']):
            return 'education'
        else:
            return 'general'
    
    def _calculate_rank(self, score: float, max_score: float) -> int:
        """Calculate rank based on score"""
        if score >= max_score * 0.8:
            return 1
        elif score >= max_score * 0.6:
            return 2
        elif score >= max_score * 0.4:
            return 3
        elif score >= max_score * 0.2:
            return 4
        else:
            return 5
    
    def save_trends_to_database(self, trends_data: List[Dict]) -> int:
        """Save scraped trend data to database"""
        try:
            saved_count = 0
            
            for trend in trends_data:
                # Check if similar trend already exists (avoid duplicates)
                existing = db.session.query(TrendData).filter(
                    TrendData.source == trend['source'],
                    TrendData.keyword == trend['keyword'],
                    TrendData.timestamp >= datetime.utcnow() - timedelta(hours=6)
                ).first()
                
                if not existing:
                    trend_record = TrendData(
                        source=trend['source'],
                        keyword=trend['keyword'],
                        rank=trend['rank'],
                        trend_score=trend['trend_score'],
                        category=trend.get('category', 'general'),
                        additional_data=trend['additional_data']
                    )
                    
                    db.session.add(trend_record)
                    saved_count += 1
            
            db.session.commit()
            logger.info(f"Saved {saved_count} new trend data points to database")
            return saved_count
            
        except Exception as e:
            logger.error(f"Database save error: {e}")
            db.session.rollback()
            return 0
    
    def cleanup_old_trends(self, days_to_keep: int = 7) -> int:
        """Clean up old trend data to keep database efficient"""
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days_to_keep)
            
            old_trends = db.session.query(TrendData).filter(
                TrendData.timestamp < cutoff_date
            )
            
            count = old_trends.count()
            old_trends.delete()
            db.session.commit()
            
            logger.info(f"Cleaned up {count} old trend records")
            return count
            
        except Exception as e:
            logger.error(f"Cleanup error: {e}")
            return 0
    
    def scrape_all_sources(self) -> Dict:
        """Main method: Scrape all configured sources"""
        try:
            all_trends_data = []
            scrape_results = {}
            
            for source_name, scraper_func in self.sources.items():
                try:
                    logger.info(f"Scraping {source_name}...")
                    trends = scraper_func()
                    
                    scrape_results[source_name] = {
                        'success': True,
                        'data_points': len(trends),
                        'trends': trends
                    }
                    
                    all_trends_data.extend(trends)
                    
                    # Rate limiting between sources
                    time.sleep(2)
                    
                except Exception as e:
                    logger.error(f"Error scraping {source_name}: {e}")
                    scrape_results[source_name] = {
                        'success': False,
                        'error': str(e),
                        'data_points': 0
                    }
            
            # Save all data to database
            saved_count = self.save_trends_to_database(all_trends_data)
            
            # Cleanup old data
            cleaned_count = self.cleanup_old_trends()
            
            summary = {
                'scrape_timestamp': datetime.utcnow().isoformat(),
                'sources_scraped': len(self.sources),
                'total_data_points': len(all_trends_data),
                'saved_to_db': saved_count,
                'cleaned_old_records': cleaned_count,
                'source_results': scrape_results,
                'success': True
            }
            
            logger.info(f"Trend scraping completed: {saved_count} new data points saved")
            return summary
            
        except Exception as e:
            logger.error(f"Scraping process error: {e}")
            return {
                'scrape_timestamp': datetime.utcnow().isoformat(),
                'success': False,
                'error': str(e)
            }
    
    def get_top_trends(self, limit: int = 20, category: str = None) -> List[Dict]:
        """Get top trending keywords from database"""
        try:
            query = db.session.query(TrendData).filter(
                TrendData.timestamp >= datetime.utcnow() - timedelta(hours=24)
            )
            
            if category:
                query = query.filter(TrendData.category == category)
            
            trends = query.order_by(
                TrendData.trend_score.desc(),
                TrendData.rank.asc()
            ).limit(limit).all()
            
            return [{
                'keyword': trend.keyword,
                'source': trend.source,
                'trend_score': trend.trend_score,
                'rank': trend.rank,
                'category': trend.category,
                'timestamp': trend.timestamp.isoformat()
            } for trend in trends]
            
        except Exception as e:
            logger.error(f"Error fetching top trends: {e}")
            return []

def scrape_trend_data() -> Dict:
    """Convenience function to scrape all trend data"""
    scraper = DataScraperAgent()
    return scraper.scrape_all_sources()

def get_trending_keywords(limit: int = 20, category: str = None) -> List[Dict]:
    """Convenience function to get trending keywords"""
    scraper = DataScraperAgent()
    return scraper.get_top_trends(limit, category)

if __name__ == "__main__":
    # Test the data scraper
    print("🌐 Testing Data Scraper Agent...")
    
    try:
        import pandas as pd
    except ImportError:
        print("Installing pandas for Google Trends...")
        import subprocess
        subprocess.check_call(['pip', 'install', 'pandas'])
        import pandas as pd
    
    result = scrape_trend_data()
    print(f"Scraping success: {result.get('success')}")
    print(f"Data points collected: {result.get('total_data_points', 0)}")
    print(f"Saved to database: {result.get('saved_to_db', 0)}")
    
    # Get top trends
    top_trends = get_trending_keywords(10)
    print(f"Top trends available: {len(top_trends)}")