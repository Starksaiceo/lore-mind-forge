
import os
import json
import requests
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Dict, List, Optional
import statistics

class PerformanceTracker:
    """Tracks and analyzes AI CEO performance for self-improvement"""
    
    def __init__(self):
        self.xano_url = os.getenv("XANO_BASE_URL", "https://x8ki-letl-twmt.n7.xano.io/api:8fyoFbLh")
        self.performance_data = []
        
    def log_strategy_result(self, strategy_type: str, platform: str, profit: float, 
                          cost: float, time_spent: int, success: bool, details: dict = None):
        """Log a business strategy result for analysis"""
        try:
            result = {
                "timestamp": datetime.now().isoformat(),
                "strategy_type": strategy_type,  # "flip", "store_launch", "ad_campaign", etc.
                "platform": platform,  # "gumroad", "shopify", "meta_ads", etc.
                "profit": profit,
                "cost": cost,
                "roi": (profit - cost) / cost if cost > 0 else 0,
                "time_spent": time_spent,  # minutes
                "success": success,
                "details": details or {}
            }
            
            # Store to Xano
            response = requests.post(f"{self.xano_url}/performance_log", json=result, timeout=10)
            if response.status_code == 200:
                print(f"✅ Performance logged: {strategy_type} on {platform}, ROI: {result['roi']:.2%}")
                return True
            else:
                print(f"⚠️ Performance log failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Performance logging error: {e}")
            return False
    
    def get_performance_data(self, days: int = 30) -> List[Dict]:
        """Get performance data from last N days"""
        try:
            # Get from Xano or fallback to profit data
            response = requests.get(f"{self.xano_url}/performance_log", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    # Filter by date
                    cutoff = datetime.now() - timedelta(days=days)
                    return [d for d in data if datetime.fromisoformat(d.get('timestamp', '')) >= cutoff]
            
            # Fallback: analyze profit data
            from profit_tracker import get_profit_data
            profit_data = get_profit_data()
            performance_data = []
            
            for entry in profit_data[-50:]:  # Last 50 entries
                performance_data.append({
                    "timestamp": entry.get('timestamp', datetime.now().isoformat()),
                    "strategy_type": "profit_generation",
                    "platform": entry.get('source', 'unknown'),
                    "profit": entry.get('amount', 0),
                    "cost": 0,
                    "roi": 1.0 if entry.get('amount', 0) > 0 else 0,
                    "success": entry.get('amount', 0) > 0
                })
            
            return performance_data
            
        except Exception as e:
            print(f"❌ Error getting performance data: {e}")
            return []
    
    def analyze_performance(self) -> Dict:
        """Analyze performance and generate insights"""
        try:
            data = self.get_performance_data(30)
            if not data:
                return {"error": "No performance data available"}
            
            analysis = {
                "total_strategies": len(data),
                "success_rate": sum(1 for d in data if d.get('success', False)) / len(data),
                "avg_roi": statistics.mean([d.get('roi', 0) for d in data]),
                "total_profit": sum([d.get('profit', 0) for d in data]),
                "total_cost": sum([d.get('cost', 0) for d in data]),
                "platform_performance": defaultdict(list),
                "strategy_performance": defaultdict(list),
                "recommendations": []
            }
            
            # Analyze by platform and strategy
            for entry in data:
                platform = entry.get('platform', 'unknown')
                strategy = entry.get('strategy_type', 'unknown')
                roi = entry.get('roi', 0)
                
                analysis["platform_performance"][platform].append(roi)
                analysis["strategy_performance"][strategy].append(roi)
            
            # Calculate averages
            for platform, rois in analysis["platform_performance"].items():
                analysis["platform_performance"][platform] = {
                    "avg_roi": statistics.mean(rois),
                    "count": len(rois),
                    "success_rate": sum(1 for r in rois if r > 0) / len(rois)
                }
            
            for strategy, rois in analysis["strategy_performance"].items():
                analysis["strategy_performance"][strategy] = {
                    "avg_roi": statistics.mean(rois),
                    "count": len(rois),
                    "success_rate": sum(1 for r in rois if r > 0) / len(rois)
                }
            
            # Generate recommendations
            best_platform = max(analysis["platform_performance"].items(), 
                               key=lambda x: x[1]["avg_roi"])[0] if analysis["platform_performance"] else None
            best_strategy = max(analysis["strategy_performance"].items(), 
                               key=lambda x: x[1]["avg_roi"])[0] if analysis["strategy_performance"] else None
            
            if best_platform:
                analysis["recommendations"].append(f"Focus more on {best_platform} platform (highest ROI)")
            if best_strategy:
                analysis["recommendations"].append(f"Prioritize {best_strategy} strategies")
            if analysis["success_rate"] < 0.5:
                analysis["recommendations"].append("Success rate low - reduce risk, increase validation")
            
            return analysis
            
        except Exception as e:
            print(f"❌ Performance analysis error: {e}")
            return {"error": str(e)}
    
    def modify_future_strategies(self, analysis: Dict) -> Dict:
        """Modify future strategy preferences based on performance"""
        try:
            preferences = {
                "platform_weights": {},
                "strategy_weights": {},
                "risk_tolerance": "medium",
                "budget_allocation": {}
            }
            
            # Set platform preferences
            for platform, metrics in analysis.get("platform_performance", {}).items():
                weight = metrics["avg_roi"] * metrics["success_rate"]
                preferences["platform_weights"][platform] = max(0.1, min(2.0, weight))
            
            # Set strategy preferences
            for strategy, metrics in analysis.get("strategy_performance", {}).items():
                weight = metrics["avg_roi"] * metrics["success_rate"]
                preferences["strategy_weights"][strategy] = max(0.1, min(2.0, weight))
            
            # Adjust risk tolerance
            success_rate = analysis.get("success_rate", 0.5)
            if success_rate > 0.7:
                preferences["risk_tolerance"] = "high"
            elif success_rate < 0.3:
                preferences["risk_tolerance"] = "low"
            
            # Store preferences
            pref_payload = {
                "preferences": json.dumps(preferences),
                "analysis_date": datetime.now().isoformat(),
                "success_rate": success_rate,
                "avg_roi": analysis.get("avg_roi", 0)
            }
            
            response = requests.post(f"{self.xano_url}/ai_preferences", json=pref_payload, timeout=10)
            if response.status_code == 200:
                print("✅ Strategy preferences updated based on performance")
            
            return preferences
            
        except Exception as e:
            print(f"❌ Strategy modification error: {e}")
            return {}
    
    def run_daily_analysis(self):
        """Run the complete daily performance analysis"""
        print("🧠 Running daily performance analysis...")
        
        analysis = self.analyze_performance()
        if "error" not in analysis:
            preferences = self.modify_future_strategies(analysis)
            
            print(f"📊 Performance Analysis Results:")
            print(f"   Success Rate: {analysis['success_rate']:.1%}")
            print(f"   Average ROI: {analysis['avg_roi']:.1%}")
            print(f"   Total Profit: ${analysis['total_profit']:.2f}")
            print(f"   Strategies Tested: {analysis['total_strategies']}")
            
            if analysis['recommendations']:
                print(f"💡 Recommendations:")
                for rec in analysis['recommendations']:
                    print(f"   • {rec}")
            
            return {
                "success": True,
                "analysis": analysis,
                "preferences": preferences
            }
        else:
            print(f"❌ Analysis failed: {analysis['error']}")
            return {"success": False, "error": analysis['error']}

# Global instance
performance_tracker = PerformanceTracker()

def log_strategy_result(strategy_type, platform, profit, cost=0, time_spent=60, success=None, details=None):
    """Convenience function to log strategy results"""
    if success is None:
        success = profit > cost
    return performance_tracker.log_strategy_result(strategy_type, platform, profit, cost, time_spent, success, details)

def run_daily_performance_analysis():
    """Run daily performance analysis"""
    return performance_tracker.run_daily_analysis()

if __name__ == "__main__":
    print("🧠 Testing Performance Tracker...")
    tracker = PerformanceTracker()
    result = tracker.run_daily_analysis()
    print(f"✅ Test completed: {result}")
