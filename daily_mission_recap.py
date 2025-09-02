
import os
import json
import requests
from datetime import datetime, timedelta
from typing import Dict, List
from profit_tracker import get_profit_data, calculate_total_real_revenue
from performance_tracker import performance_tracker

class DailyMissionRecap:
    """Generates daily mission recaps and reports"""
    
    def __init__(self):
        self.xano_url = os.getenv("XANO_BASE_URL", "https://x8ki-letl-twmt.n7.xano.io/api:8fyoFbLh")
        
    def get_todays_activities(self) -> Dict:
        """Get all activities from today"""
        try:
            today = datetime.now().date()
            activities = {
                "profit_entries": [],
                "goals_completed": [],
                "products_created": [],
                "campaigns_launched": [],
                "stores_built": [],
                "content_posted": []
            }
            
            # Get profit data from today
            profit_data = get_profit_data()
            for entry in profit_data:
                entry_date = datetime.fromisoformat(entry.get('timestamp', '')).date()
                if entry_date == today:
                    activities["profit_entries"].append(entry)
            
            # Get performance data from today
            perf_data = performance_tracker.get_performance_data(1)  # Last 1 day
            for entry in perf_data:
                entry_date = datetime.fromisoformat(entry.get('timestamp', '')).date()
                if entry_date == today:
                    strategy_type = entry.get('strategy_type', '')
                    if 'product' in strategy_type.lower():
                        activities["products_created"].append(entry)
                    elif 'campaign' in strategy_type.lower() or 'ad' in strategy_type.lower():
                        activities["campaigns_launched"].append(entry)
                    elif 'store' in strategy_type.lower():
                        activities["stores_built"].append(entry)
            
            return activities
            
        except Exception as e:
            print(f"❌ Error getting today's activities: {e}")
            return {"error": str(e)}
    
    def calculate_daily_metrics(self, activities: Dict) -> Dict:
        """Calculate key daily metrics"""
        try:
            metrics = {
                "total_profit": 0.0,
                "total_revenue": 0.0,
                "activities_completed": 0,
                "success_rate": 0.0,
                "top_performer": None,
                "roi": 0.0
            }
            
            # Calculate profit and revenue
            for entry in activities.get("profit_entries", []):
                amount = entry.get('amount', 0)
                metrics["total_profit"] += amount
                metrics["total_revenue"] += amount
            
            # Count activities
            activities_count = sum([
                len(activities.get("goals_completed", [])),
                len(activities.get("products_created", [])),
                len(activities.get("campaigns_launched", [])),
                len(activities.get("stores_built", [])),
                len(activities.get("content_posted", []))
            ])
            metrics["activities_completed"] = activities_count
            
            # Calculate success rate
            perf_data = performance_tracker.get_performance_data(1)
            if perf_data:
                successful = sum(1 for d in perf_data if d.get('success', False))
                metrics["success_rate"] = successful / len(perf_data)
            
            # Find top performer
            if activities.get("profit_entries"):
                top_entry = max(activities["profit_entries"], key=lambda x: x.get('amount', 0))
                metrics["top_performer"] = {
                    "source": top_entry.get('source', 'Unknown'),
                    "amount": top_entry.get('amount', 0)
                }
            
            return metrics
            
        except Exception as e:
            print(f"❌ Error calculating daily metrics: {e}")
            return {"error": str(e)}
    
    def get_next_missions(self) -> List[str]:
        """Determine next missions based on performance and trends"""
        try:
            missions = []
            
            # Get current performance analysis
            analysis = performance_tracker.analyze_performance()
            
            # Based on success rate, suggest different missions
            success_rate = analysis.get("success_rate", 0.5)
            
            if success_rate > 0.7:
                missions.extend([
                    "Scale successful strategies with 2x budget",
                    "Expand to new high-performing platforms",
                    "Launch premium product line"
                ])
            elif success_rate > 0.4:
                missions.extend([
                    "Optimize current strategies for better ROI",
                    "A/B test new product variations",
                    "Research trending market opportunities"
                ])
            else:
                missions.extend([
                    "Focus on proven low-risk strategies",
                    "Validate ideas before full launch",
                    "Analyze successful competitors"
                ])
            
            # Add platform-specific missions
            platform_perf = analysis.get("platform_performance", {})
            if platform_perf:
                best_platform = max(platform_perf.items(), key=lambda x: x[1].get("avg_roi", 0))[0]
                missions.append(f"Double down on {best_platform} - our best performing platform")
            
            # Add time-based missions
            current_hour = datetime.now().hour
            if 9 <= current_hour <= 17:  # Business hours
                missions.append("Launch new product during high-traffic hours")
            else:
                missions.append("Prepare content and campaigns for tomorrow")
            
            return missions[:5]  # Return top 5 missions
            
        except Exception as e:
            print(f"❌ Error getting next missions: {e}")
            return ["Continue profit generation activities", "Monitor performance metrics"]
    
    def generate_daily_recap(self) -> Dict:
        """Generate complete daily recap"""
        try:
            print("📋 Generating daily mission recap...")
            
            activities = self.get_todays_activities()
            if "error" in activities:
                return activities
            
            metrics = self.calculate_daily_metrics(activities)
            next_missions = self.get_next_missions()
            
            recap = {
                "date": datetime.now().strftime("%Y-%m-%d"),
                "summary": {
                    "total_profit": metrics.get("total_profit", 0),
                    "activities_completed": metrics.get("activities_completed", 0),
                    "success_rate": metrics.get("success_rate", 0),
                    "top_performer": metrics.get("top_performer")
                },
                "activities": {
                    "profits_generated": len(activities.get("profit_entries", [])),
                    "products_created": len(activities.get("products_created", [])),
                    "campaigns_launched": len(activities.get("campaigns_launched", [])),
                    "stores_built": len(activities.get("stores_built", []))
                },
                "wins": [],
                "challenges": [],
                "next_missions": next_missions,
                "generated_at": datetime.now().isoformat()
            }
            
            # Identify wins
            if metrics["total_profit"] > 0:
                recap["wins"].append(f"Generated ${metrics['total_profit']:.2f} in profit")
            if metrics["success_rate"] > 0.6:
                recap["wins"].append(f"High success rate: {metrics['success_rate']:.1%}")
            if metrics["activities_completed"] > 3:
                recap["wins"].append(f"Completed {metrics['activities_completed']} business activities")
            
            # Identify challenges
            if metrics["total_profit"] == 0:
                recap["challenges"].append("No profit generated today - need to optimize strategies")
            if metrics["success_rate"] < 0.4:
                recap["challenges"].append("Low success rate - review and improve processes")
            if metrics["activities_completed"] < 2:
                recap["challenges"].append("Low activity level - increase automation frequency")
            
            # Store recap
            self.store_recap(recap)
            
            return recap
            
        except Exception as e:
            print(f"❌ Error generating daily recap: {e}")
            return {"error": str(e)}
    
    def store_recap(self, recap: Dict):
        """Store daily recap to Xano"""
        try:
            payload = {
                "date": recap["date"],
                "recap_data": json.dumps(recap),
                "total_profit": recap["summary"]["total_profit"],
                "activities_completed": recap["summary"]["activities_completed"],
                "success_rate": recap["summary"]["success_rate"]
            }
            
            response = requests.post(f"{self.xano_url}/daily_recap", json=payload, timeout=10)
            if response.status_code == 200:
                print("✅ Daily recap stored successfully")
            else:
                print(f"⚠️ Failed to store recap: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error storing recap: {e}")
    
    def get_recent_recaps(self, days: int = 7) -> List[Dict]:
        """Get recent daily recaps"""
        try:
            response = requests.get(f"{self.xano_url}/daily_recap", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    # Sort by date and return recent ones
                    sorted_data = sorted(data, key=lambda x: x.get('date', ''), reverse=True)
                    return sorted_data[:days]
            return []
            
        except Exception as e:
            print(f"❌ Error getting recent recaps: {e}")
            return []
    
    def print_daily_recap(self, recap: Dict):
        """Print formatted daily recap"""
        print(f"\n📋 AI CEO Daily Mission Recap - {recap['date']}")
        print("=" * 50)
        
        print(f"\n💰 FINANCIAL SUMMARY:")
        print(f"   Total Profit: ${recap['summary']['total_profit']:.2f}")
        print(f"   Success Rate: {recap['summary']['success_rate']:.1%}")
        
        print(f"\n🎯 ACTIVITIES COMPLETED:")
        activities = recap['activities']
        print(f"   • {activities['profits_generated']} profit entries")
        print(f"   • {activities['products_created']} products created")
        print(f"   • {activities['campaigns_launched']} campaigns launched")
        print(f"   • {activities['stores_built']} stores built")
        
        print(f"\n🏆 WINS:")
        for win in recap['wins']:
            print(f"   ✅ {win}")
        
        if recap['challenges']:
            print(f"\n⚠️ CHALLENGES:")
            for challenge in recap['challenges']:
                print(f"   ❌ {challenge}")
        
        print(f"\n🚀 NEXT MISSIONS:")
        for i, mission in enumerate(recap['next_missions'], 1):
            print(f"   {i}. {mission}")
        
        print("=" * 50)

# Global instance
daily_recap = DailyMissionRecap()

def generate_daily_recap():
    """Generate and return daily recap"""
    return daily_recap.generate_daily_recap()

def print_daily_recap():
    """Generate and print daily recap"""
    recap = generate_daily_recap()
    if "error" not in recap:
        daily_recap.print_daily_recap(recap)
        return recap
    else:
        print(f"❌ Failed to generate recap: {recap['error']}")
        return None

if __name__ == "__main__":
    print("📋 Testing Daily Mission Recap...")
    recap = print_daily_recap()
    print(f"✅ Test completed: {recap is not None}")
