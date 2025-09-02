
import os
import json
from datetime import datetime, timedelta
from typing import Dict, List
from marketplace_uploader import check_shopify_connection
from payment_processor import StripeProcessor

class AnalyticsPanel:
    def __init__(self):
        self.metrics_file = "analytics_metrics.json"
        self.load_metrics()
    
    def collect_all_metrics(self) -> Dict:
        """Collect metrics from all sources"""
        metrics = {
            "timestamp": datetime.now().isoformat(),
            "stores": self.get_store_metrics(),
            "revenue": self.get_revenue_metrics(),
            "marketing": self.get_marketing_metrics(),
            "products": self.get_product_metrics()
        }
        
        self.save_metrics(metrics)
        return metrics
    
    def get_store_metrics(self) -> Dict:
        """Get store-related metrics"""
        try:
            shopify_status = check_shopify_connection()
            
            return {
                "stores_connected": 1 if shopify_status.get("connected") else 0,
                "total_stores": 1,
                "store_name": shopify_status.get("store_name", "Unknown"),
                "products_count": shopify_status.get("products_count", 0),
                "status": "active" if shopify_status.get("connected") else "inactive"
            }
        except Exception as e:
            return {
                "stores_connected": 0,
                "total_stores": 1,
                "error": str(e),
                "status": "error"
            }
    
    def get_revenue_metrics(self) -> Dict:
        """Get revenue metrics from Stripe"""
        try:
            stripe_processor = StripeProcessor()
            
            if not stripe_processor.is_configured():
                return {
                    "total_revenue": 0.0,
                    "monthly_revenue": 0.0,
                    "transactions": 0,
                    "status": "not_configured"
                }
            
            # Get recent payments
            payments = stripe_processor.get_payments(limit=100)
            
            total_revenue = sum(p.get("amount", 0) / 100 for p in payments if p.get("status") == "succeeded")
            
            # Calculate monthly revenue (last 30 days)
            thirty_days_ago = datetime.now() - timedelta(days=30)
            monthly_payments = [
                p for p in payments 
                if p.get("status") == "succeeded" and 
                datetime.fromtimestamp(p.get("created", 0)) >= thirty_days_ago
            ]
            monthly_revenue = sum(p.get("amount", 0) / 100 for p in monthly_payments)
            
            return {
                "total_revenue": total_revenue,
                "monthly_revenue": monthly_revenue,
                "transactions": len([p for p in payments if p.get("status") == "succeeded"]),
                "recent_transactions": len(monthly_payments),
                "status": "active"
            }
            
        except Exception as e:
            return {
                "total_revenue": 0.0,
                "monthly_revenue": 0.0,
                "transactions": 0,
                "error": str(e),
                "status": "error"
            }
    
    def get_marketing_metrics(self) -> Dict:
        """Get marketing metrics"""
        try:
            # Check for marketing files
            email_count = self.count_files("email_sequences")
            ad_count = self.count_files("ad_campaigns")
            
            # Check scheduled posts
            from scheduler import SocialMediaScheduler
            scheduler = SocialMediaScheduler()
            scheduled_posts = len(scheduler.get_scheduled_posts())
            published_posts = len([p for p in scheduler.get_scheduled_posts() if p["status"] == "published"])
            
            return {
                "emails_generated": email_count,
                "ads_created": ad_count,
                "posts_scheduled": scheduled_posts,
                "posts_published": published_posts,
                "status": "active"
            }
            
        except Exception as e:
            return {
                "emails_generated": 0,
                "ads_created": 0,
                "posts_scheduled": 0,
                "posts_published": 0,
                "error": str(e),
                "status": "error"
            }
    
    def get_product_metrics(self) -> Dict:
        """Get product creation metrics"""
        try:
            # Count product files
            product_files = [f for f in os.listdir(".") if f.startswith("product_") and f.endswith(".md")]
            
            # Count export files
            export_dir = "export"
            export_count = 0
            if os.path.exists(export_dir):
                export_count = len([f for f in os.listdir(export_dir) if f.endswith(".csv")])
            
            return {
                "products_created": len(product_files),
                "exports_generated": export_count,
                "last_product_created": self.get_latest_product_time(),
                "status": "active"
            }
            
        except Exception as e:
            return {
                "products_created": 0,
                "exports_generated": 0,
                "error": str(e),
                "status": "error"
            }
    
    def count_files(self, directory: str) -> int:
        """Count files in a directory"""
        try:
            if os.path.exists(directory):
                return len([f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))])
            return 0
        except:
            return 0
    
    def get_latest_product_time(self) -> str:
        """Get timestamp of latest product creation"""
        try:
            product_files = [f for f in os.listdir(".") if f.startswith("product_") and f.endswith(".md")]
            if product_files:
                # Extract timestamp from filename
                latest_file = max(product_files)
                timestamp = latest_file.replace("product_", "").replace(".md", "")
                return datetime.fromtimestamp(int(timestamp)).isoformat()
            return "Never"
        except:
            return "Unknown"
    
    def load_metrics(self):
        """Load historical metrics"""
        try:
            if os.path.exists(self.metrics_file):
                with open(self.metrics_file, 'r') as f:
                    self.historical_metrics = json.load(f)
            else:
                self.historical_metrics = []
        except:
            self.historical_metrics = []
    
    def save_metrics(self, metrics: Dict):
        """Save metrics to file"""
        try:
            self.historical_metrics.append(metrics)
            
            # Keep only last 30 entries
            if len(self.historical_metrics) > 30:
                self.historical_metrics = self.historical_metrics[-30:]
            
            with open(self.metrics_file, 'w') as f:
                json.dump(self.historical_metrics, f, indent=2)
        except Exception as e:
            print(f"Error saving metrics: {e}")
    
    def get_analytics_summary(self) -> Dict:
        """Get complete analytics summary"""
        current_metrics = self.collect_all_metrics()
        
        summary = {
            "overview": {
                "total_revenue": current_metrics["revenue"]["total_revenue"],
                "active_stores": current_metrics["stores"]["stores_connected"],
                "products_created": current_metrics["products"]["products_created"],
                "marketing_active": current_metrics["marketing"]["status"] == "active"
            },
            "performance": {
                "monthly_revenue": current_metrics["revenue"]["monthly_revenue"],
                "recent_transactions": current_metrics["revenue"].get("recent_transactions", 0),
                "posts_published": current_metrics["marketing"]["posts_published"],
                "conversion_rate": self.calculate_conversion_rate(current_metrics)
            },
            "trends": self.get_trends(),
            "last_updated": current_metrics["timestamp"]
        }
        
        return summary
    
    def calculate_conversion_rate(self, metrics: Dict) -> float:
        """Calculate basic conversion rate"""
        try:
            transactions = metrics["revenue"]["transactions"]
            products = metrics["products"]["products_created"]
            
            if products > 0:
                return round((transactions / products) * 100, 2)
            return 0.0
        except:
            return 0.0
    
    def get_trends(self) -> Dict:
        """Get trend analysis from historical data"""
        try:
            if len(self.historical_metrics) < 2:
                return {"status": "insufficient_data"}
            
            current = self.historical_metrics[-1]
            previous = self.historical_metrics[-2]
            
            revenue_trend = current["revenue"]["total_revenue"] - previous["revenue"]["total_revenue"]
            product_trend = current["products"]["products_created"] - previous["products"]["products_created"]
            
            return {
                "revenue_change": revenue_trend,
                "product_change": product_trend,
                "trend_direction": "up" if revenue_trend > 0 else "down" if revenue_trend < 0 else "stable"
            }
        except:
            return {"status": "error"}

# Helper function for easy access
def get_analytics_dashboard() -> Dict:
    """Get complete analytics dashboard data"""
    panel = AnalyticsPanel()
    return panel.get_analytics_summary()
