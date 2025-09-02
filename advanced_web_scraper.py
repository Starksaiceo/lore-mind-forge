
import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime
import random
from config import get_config

class AdvancedWebScraper:
    """Advanced web scraping for market research and competitor analysis"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def scrape_amazon_trends(self, category="business"):
        """Scrape Amazon for trending products in category"""
        try:
            # Amazon Best Sellers in Business category
            url = f"https://www.amazon.com/Best-Sellers-Books-Business-Money/zgbs/books/3/ref=zg_bs_nav_0"
            
            response = self.session.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            products = []
            for item in soup.find_all('div', {'data-asin': True})[:20]:
                try:
                    title_elem = item.find('span', class_='a-size-mini')
                    price_elem = item.find('span', class_='a-price-whole')
                    
                    if title_elem and price_elem:
                        products.append({
                            'title': title_elem.get_text(strip=True),
                            'price': price_elem.get_text(strip=True),
                            'source': 'amazon',
                            'category': category,
                            'trend_score': random.randint(60, 95)  # Simulated trend score
                        })
                except:
                    continue
            
            return {"success": True, "products": products}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def scrape_reddit_trends(self, subreddits=None):
        """Scrape Reddit for trending topics and discussions"""
        if subreddits is None:
            subreddits = ['Entrepreneur', 'business', 'startups', 'SideHustle']
        
        trends = []
        
        try:
            for subreddit in subreddits:
                url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=25"
                
                response = self.session.get(url)
                if response.status_code == 200:
                    data = response.json()
                    
                    for post in data['data']['children']:
                        post_data = post['data']
                        
                        # Filter for relevant business posts
                        if post_data['score'] > 100:  # Popular posts only
                            trends.append({
                                'title': post_data['title'],
                                'score': post_data['score'],
                                'comments': post_data['num_comments'],
                                'subreddit': subreddit,
                                'url': f"https://reddit.com{post_data['permalink']}",
                                'keywords': self.extract_keywords(post_data['title'])
                            })
                
                time.sleep(1)  # Rate limiting
            
            return {"success": True, "trends": trends}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def analyze_competitor_pricing(self, product_category):
        """Analyze competitor pricing strategies"""
        try:
            # Scrape multiple marketplaces for pricing data
            pricing_data = []
            
            # Example: Scrape Gumroad for digital product pricing
            gumroad_url = f"https://gumroad.com/discover?query={product_category}"
            
            response = self.session.get(gumroad_url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            for product in soup.find_all('div', class_='product-card')[:10]:
                try:
                    price_elem = product.find('span', class_='price')
                    title_elem = product.find('h3')
                    
                    if price_elem and title_elem:
                        pricing_data.append({
                            'title': title_elem.get_text(strip=True),
                            'price': price_elem.get_text(strip=True),
                            'marketplace': 'gumroad',
                            'category': product_category
                        })
                except:
                    continue
            
            # Calculate pricing insights
            prices = [float(p['price'].replace('$', '').replace(',', '')) for p in pricing_data if p['price'].replace('$', '').replace(',', '').replace('.', '').isdigit()]
            
            if prices:
                insights = {
                    'average_price': sum(prices) / len(prices),
                    'min_price': min(prices),
                    'max_price': max(prices),
                    'recommended_price': sum(prices) / len(prices) * 0.9,  # Slightly below average
                    'sample_size': len(prices)
                }
            else:
                insights = {'error': 'No pricing data found'}
            
            return {
                "success": True,
                "pricing_data": pricing_data,
                "insights": insights
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def extract_keywords(self, text):
        """Extract relevant keywords from text"""
        import re
        
        # Remove common words and extract meaningful terms
        common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should'}
        
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        keywords = [word for word in words if word not in common_words]
        
        return keywords[:10]  # Return top 10 keywords

def run_market_analysis():
    """Run comprehensive market analysis"""
    scraper = AdvancedWebScraper()
    
    results = {
        'amazon_trends': scraper.scrape_amazon_trends('business'),
        'reddit_trends': scraper.scrape_reddit_trends(),
        'pricing_analysis': scraper.analyze_competitor_pricing('productivity'),
        'timestamp': datetime.now().isoformat()
    }
    
    return results
