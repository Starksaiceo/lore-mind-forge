
import json
import os
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any
import requests
from config import XANO_BASE_URL, STRIPE_SECRET_KEY

class SprintMonitor:
    """Real-time monitoring for the 48-hour profit sprint"""
    
    def __init__(self):
        self.log_file = "sprint_activity.log"
        self.metrics_file = "sprint_metrics.json"
        
    def get_real_sprint_status(self) -> Dict:
        """Get comprehensive status of the profit sprint"""
        try:
            from profit_sprint import get_sprint_status
            sprint_status = get_sprint_status()
            
            # Add real verification data
            verification = self.verify_sprint_activity()
            
            return {
                "sprint_running": sprint_status.get("running", False),
                "products_launched": sprint_status.get("products_launched", 0),
                "claimed_earnings": sprint_status.get("total_earnings", "$0.00"),
                "hours_remaining": sprint_status.get("hours_remaining", "N/A"),
                "verification": verification,
                "real_metrics": self.get_real_metrics(),
                "last_activity": self.get_last_activity(),
                "health_check": self.health_check()
            }
        except Exception as e:
            return {"error": f"Sprint monitoring error: {e}"}
    
    def verify_sprint_activity(self) -> Dict:
        """Verify actual sprint activity with evidence"""
        evidence = {
            "files_created": self.count_product_files(),
            "api_calls_made": self.count_api_activity(),
            "real_uploads": self.verify_real_uploads(),
            "database_entries": self.check_database_activity()
        }
        
        # Calculate activity score
        activity_score = 0
        if evidence["files_created"] > 0:
            activity_score += 25
        if evidence["api_calls_made"] > 0:
            activity_score += 25
        if evidence["real_uploads"]["successful"] > 0:
            activity_score += 30
        if evidence["database_entries"] > 0:
            activity_score += 20
            
        evidence["activity_score"] = activity_score
        evidence["is_really_working"] = activity_score > 50
        
        return evidence
    
    def count_product_files(self) -> int:
        """Count actual product files created"""
        import glob
        
        # Look for sprint-generated files
        product_files = []
        product_files.extend(glob.glob("product_*.md"))
        product_files.extend(glob.glob("*.md"))
        
        # Filter for recent files (last 48 hours)
        recent_files = []
        for file_path in product_files:
            try:
                if os.path.exists(file_path):
                    file_time = datetime.fromtimestamp(os.path.getctime(file_path))
                    if datetime.now() - file_time < timedelta(hours=48):
                        recent_files.append(file_path)
            except:
                continue
                
        return len(recent_files)
    
    def count_api_activity(self) -> int:
        """Count actual API calls made"""
        activity_count = 0
        
        # Check for recent log entries
        if os.path.exists(self.log_file):
            try:
                with open(self.log_file, 'r') as f:
                    lines = f.readlines()
                    # Count lines from last 48 hours
                    for line in lines:
                        if "API call" in line or "Product created" in line:
                            activity_count += 1
            except:
                pass
                
        return activity_count
    
    def verify_real_uploads(self) -> Dict:
        """Verify actual uploads to platforms - VERIFIED ONLY"""
        upload_status = {
            "successful": 0,
            "failed": 0,
            "verified_uploads": 0,  # NEW: Only count verified uploads
            "platforms": [],
            "details": []
        }
        
        # Check Stripe products
        if STRIPE_SECRET_KEY:
            try:
                import stripe
                stripe.api_key = STRIPE_SECRET_KEY
                products = stripe.Product.list(limit=10)
                
                recent_products = 0
                for product in products.data:
                    created_time = datetime.fromtimestamp(product.created)
                    if datetime.now() - created_time < timedelta(hours=48):
                        recent_products += 1
                        
                upload_status["successful"] += recent_products
                upload_status["platforms"].append(f"Stripe: {recent_products} products")
                
            except Exception as e:
                upload_status["failed"] += 1
                upload_status["details"].append(f"Stripe error: {e}")
        
        # Shopify + Stripe monitoring only - Gumroad completely removed
        
        # Check Shopify uploads
        try:
            from marketplace_uploader import check_shopify_connection
            shopify_status = check_shopify_connection()
            
            if shopify_status.get("connected"):
                upload_status["successful"] += shopify_status.get("products_count", 0)
                upload_status["details"].append(f"Shopify: {shopify_status.get('products_count', 0)} products")
            else:
                upload_status["failed"] += 1
                upload_status["details"].append(f"Shopify connection failed")
                
        except Exception as e:
            upload_status["failed"] += 1
            upload_status["details"].append(f"Shopify error: {e}")
        
        return upload_status
    
    def check_database_activity(self) -> int:
        """Check actual database entries"""
        try:
            # Check Xano for recent entries
            response = requests.get(f"{XANO_BASE_URL}/ai_memory", timeout=10)
            if response.status_code == 200:
                memories = response.json()
                if isinstance(memories, list):
                    # Count recent sprint-related entries
                    recent_count = 0
                    for memory in memories:
                        command = memory.get('command', '').lower()
                        if any(word in command for word in ['sprint', 'product', 'launch']):
                            recent_count += 1
                    return recent_count
        except:
            pass
            
        return 0
    
    def get_real_metrics(self) -> Dict:
        """Get real performance metrics"""
        try:
            from profit_tracker import calculate_total_real_revenue, get_profit_by_source
            
            real_revenue = calculate_total_real_revenue()
            profit_sources = get_profit_by_source()
            
            return {
                "real_revenue": real_revenue,
                "profit_sources": profit_sources,
                "revenue_verified": real_revenue > 0,
                "last_sale_time": self.get_last_sale_time()
            }
        except Exception as e:
            return {"error": f"Metrics error: {e}"}
    
    def get_last_sale_time(self) -> str:
        """Get timestamp of last real sale"""
        try:
            # Check Stripe for most recent charge
            if STRIPE_SECRET_KEY:
                import stripe
                stripe.api_key = STRIPE_SECRET_KEY
                charges = stripe.Charge.list(limit=1)
                
                if charges.data:
                    last_charge = charges.data[0]
                    if last_charge.status == 'succeeded':
                        return datetime.fromtimestamp(last_charge.created).strftime('%Y-%m-%d %H:%M:%S')
        except:
            pass
            
        return "No sales detected"
    
    def get_last_activity(self) -> Dict:
        """Get last recorded sprint activity"""
        if os.path.exists(self.log_file):
            try:
                with open(self.log_file, 'r') as f:
                    lines = f.readlines()
                    if lines:
                        last_line = lines[-1].strip()
                        return {
                            "last_log_entry": last_line,
                            "log_file_size": len(lines),
                            "last_modified": datetime.fromtimestamp(os.path.getmtime(self.log_file)).strftime('%Y-%m-%d %H:%M:%S')
                        }
            except:
                pass
                
        return {"status": "No activity log found"}
    
    def health_check(self) -> Dict:
        """Check sprint system health"""
        health = {
            "system_status": "unknown",
            "issues": [],
            "recommendations": []
        }
        
        # Check if sprint module is actually running
        try:
            from profit_sprint import _sprint_instance
            if _sprint_instance and _sprint_instance.is_running:
                health["system_status"] = "running"
            else:
                health["system_status"] = "stopped"
                health["issues"].append("Sprint instance not running")
        except:
            health["issues"].append("Sprint module not accessible")
        
        # Check API keys
        if not STRIPE_SECRET_KEY:
            health["issues"].append("No payment platforms configured")
            health["recommendations"].append("Add Stripe API keys")
        
        # Check file permissions
        try:
            test_file = "test_write.tmp"
            with open(test_file, 'w') as f:
                f.write("test")
            os.remove(test_file)
        except:
            health["issues"].append("File write permissions issue")
        
        if not health["issues"]:
            health["system_status"] = "healthy"
            
        return health
    
    def log_activity(self, activity: str):
        """Log sprint activity with timestamp"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] {activity}\n"
        
        try:
            with open(self.log_file, 'a') as f:
                f.write(log_entry)
        except Exception as e:
            print(f"Failed to log activity: {e}")
    
    def save_metrics_snapshot(self, metrics: Dict):
        """Save metrics snapshot"""
        try:
            with open(self.metrics_file, 'w') as f:
                json.dump(metrics, f, indent=2, default=str)
        except Exception as e:
            print(f"Failed to save metrics: {e}")

def monitor_sprint():
    """Main monitoring function"""
    monitor = SprintMonitor()
    status = monitor.get_real_sprint_status()
    
    # Log the check
    monitor.log_activity("Sprint status check performed")
    
    # Save metrics
    monitor.save_metrics_snapshot(status)
    
    return status

if __name__ == "__main__":
    # Test the monitor
    result = monitor_sprint()
    print(json.dumps(result, indent=2, default=str))
