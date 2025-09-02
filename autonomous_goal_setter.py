
import os
import json
import requests
from datetime import datetime, timedelta
from typing import Dict, List
from profit_tracker import get_profit_data, calculate_total_real_revenue, get_profit_by_source
from performance_tracker import performance_tracker
from google_trends_tool import google_trends_tool

class AutonomousGoalSetter:
    """Automatically sets new goals based on performance, profits, and trends"""
    
    def __init__(self):
        self.xano_url = os.getenv("XANO_BASE_URL", "https://x8ki-letl-twmt.n7.xano.io/api:8fyoFbLh")
        
    def analyze_profit_patterns(self) -> Dict:
        """Analyze profit patterns to identify successful strategies"""
        try:
            profit_by_source = get_profit_by_source()
            total_profit = calculate_total_real_revenue()
            
            patterns = {
                "top_sources": [],
                "emerging_sources": [],
                "total_profit": total_profit,
                "profit_trend": "stable"
            }
            
            if profit_by_source:
                # Sort by profit amount
                sorted_sources = sorted(profit_by_source.items(), key=lambda x: x[1], reverse=True)
                patterns["top_sources"] = sorted_sources[:3]
                
                # Find emerging sources (sources with recent activity)
                recent_profits = get_profit_data()[-10:]  # Last 10 entries
                recent_sources = [p.get('source', '') for p in recent_profits]
                source_frequency = {}
                for source in recent_sources:
                    source_frequency[source] = source_frequency.get(source, 0) + 1
                
                # Emerging sources are those with high recent frequency but not in top performers
                top_source_names = [s[0] for s in patterns["top_sources"]]
                for source, freq in source_frequency.items():
                    if freq >= 2 and source not in top_source_names:
                        patterns["emerging_sources"].append((source, freq))
            
            return patterns
            
        except Exception as e:
            print(f"❌ Error analyzing profit patterns: {e}")
            return {"error": str(e)}
    
    def identify_trending_opportunities(self) -> List[str]:
        """Identify trending opportunities using Google Trends"""
        try:
            trending_keywords = [
                "AI business tools", "digital marketing", "productivity apps",
                "online course", "Notion templates", "social media tools",
                "automation software", "passive income", "side hustle"
            ]
            
            opportunities = []
            
            for keyword in trending_keywords:
                try:
                    trend_data = google_trends_tool(keyword)
                    if trend_data.get("success") and trend_data.get("trend_score", 0) > 50:
                        opportunities.append({
                            "keyword": keyword,
                            "trend_score": trend_data.get("trend_score", 0),
                            "opportunity_type": self.categorize_opportunity(keyword)
                        })
                except Exception as e:
                    print(f"⚠️ Trend analysis failed for {keyword}: {e}")
                    continue
            
            # Sort by trend score
            opportunities.sort(key=lambda x: x["trend_score"], reverse=True)
            return opportunities[:5]  # Top 5 opportunities
            
        except Exception as e:
            print(f"❌ Error identifying trending opportunities: {e}")
            return []
    
    def categorize_opportunity(self, keyword: str) -> str:
        """Categorize opportunity type based on keyword"""
        if any(word in keyword.lower() for word in ["template", "notion", "spreadsheet"]):
            return "digital_template"
        elif any(word in keyword.lower() for word in ["course", "tutorial", "training"]):
            return "educational_content"
        elif any(word in keyword.lower() for word in ["tool", "software", "app"]):
            return "software_product"
        elif any(word in keyword.lower() for word in ["service", "consulting", "coaching"]):
            return "service_offering"
        else:
            return "general_product"
    
    def generate_goals_from_profits(self, profit_patterns: Dict) -> List[Dict]:
        """Generate new goals based on profit patterns"""
        goals = []
        
        try:
            # Goals based on top performing sources
            for source, amount in profit_patterns.get("top_sources", []):
                if amount > 10:  # Only if source made significant profit
                    if "notion" in source.lower():
                        goals.append({
                            "title": "Scale Notion Template Business",
                            "description": f"Create 3 more Notion templates similar to successful {source} (${amount:.2f} profit)",
                            "priority": 9,
                            "category": "scale_success",
                            "expected_roi": amount * 2
                        })
                    elif "gumroad" in source.lower():
                        goals.append({
                            "title": "Expand Gumroad Product Line",
                            "description": f"Launch 2 new products on Gumroad based on {source} success (${amount:.2f} profit)",
                            "priority": 8,
                            "category": "platform_expansion",
                            "expected_roi": amount * 1.5
                        })
                    elif "stripe" in source.lower():
                        goals.append({
                            "title": "Scale Stripe Product Sales",
                            "description": f"Increase marketing for successful Stripe product from {source} (${amount:.2f} profit)",
                            "priority": 8,
                            "category": "scale_success",
                            "expected_roi": amount * 3
                        })
            
            # Goals for emerging sources
            for source, frequency in profit_patterns.get("emerging_sources", []):
                goals.append({
                    "title": f"Optimize {source} Strategy",
                    "description": f"Research and optimize {source} which shows promise ({frequency} recent activities)",
                    "priority": 6,
                    "category": "optimization",
                    "expected_roi": 50
                })
            
            return goals
            
        except Exception as e:
            print(f"❌ Error generating goals from profits: {e}")
            return []
    
    def generate_goals_from_trends(self, opportunities: List[Dict]) -> List[Dict]:
        """Generate goals based on trending opportunities"""
        goals = []
        
        try:
            for opp in opportunities:
                keyword = opp["keyword"]
                trend_score = opp["trend_score"]
                opp_type = opp["opportunity_type"]
                
                if opp_type == "digital_template":
                    goals.append({
                        "title": f"Create {keyword.title()} Templates",
                        "description": f"Build and sell {keyword} templates (trending at {trend_score}/100)",
                        "priority": 7,
                        "category": "trend_opportunity",
                        "expected_roi": trend_score * 2
                    })
                elif opp_type == "educational_content":
                    goals.append({
                        "title": f"Launch {keyword.title()} Course",
                        "description": f"Create online course about {keyword} (trending at {trend_score}/100)",
                        "priority": 8,
                        "category": "trend_opportunity",
                        "expected_roi": trend_score * 3
                    })
                elif opp_type == "software_product":
                    goals.append({
                        "title": f"Develop {keyword.title()} Solution",
                        "description": f"Build simple {keyword} solution (trending at {trend_score}/100)",
                        "priority": 6,
                        "category": "trend_opportunity",
                        "expected_roi": trend_score * 4
                    })
            
            return goals
            
        except Exception as e:
            print(f"❌ Error generating goals from trends: {e}")
            return []
    
    def generate_time_based_goals(self) -> List[Dict]:
        """Generate goals based on time and calendar"""
        goals = []
        
        try:
            now = datetime.now()
            
            # Weekly goals
            if now.weekday() == 0:  # Monday
                goals.append({
                    "title": "Weekly Performance Review",
                    "description": "Analyze last week's performance and optimize strategies",
                    "priority": 7,
                    "category": "maintenance",
                    "expected_roi": 0
                })
            
            # Monthly goals
            if now.day == 1:  # First of month
                goals.append({
                    "title": "Monthly Revenue Target",
                    "description": f"Set and execute plan to achieve $500 revenue this month",
                    "priority": 9,
                    "category": "revenue_target",
                    "expected_roi": 500
                })
            
            # Seasonal opportunities
            month = now.month
            if 11 <= month <= 12:  # Holiday season
                goals.append({
                    "title": "Holiday Season Product Launch",
                    "description": "Create and launch holiday-themed products for seasonal demand",
                    "priority": 8,
                    "category": "seasonal",
                    "expected_roi": 200
                })
            elif 1 <= month <= 2:  # New Year
                goals.append({
                    "title": "New Year Productivity Products",
                    "description": "Launch productivity and goal-setting products for New Year resolutions",
                    "priority": 8,
                    "category": "seasonal",
                    "expected_roi": 150
                })
            
            return goals
            
        except Exception as e:
            print(f"❌ Error generating time-based goals: {e}")
            return []
    
    def set_autonomous_goals(self) -> Dict:
        """Main function to set autonomous goals"""
        try:
            print("🎯 Setting autonomous goals based on AI analysis...")
            
            # Analyze current situation
            profit_patterns = self.analyze_profit_patterns()
            trending_opportunities = self.identify_trending_opportunities()
            
            # Generate different types of goals
            profit_goals = self.generate_goals_from_profits(profit_patterns)
            trend_goals = self.generate_goals_from_trends(trending_opportunities)
            time_goals = self.generate_time_based_goals()
            
            # Combine and prioritize all goals
            all_goals = profit_goals + trend_goals + time_goals
            
            # Sort by priority and expected ROI
            all_goals.sort(key=lambda x: (x.get("priority", 5), x.get("expected_roi", 0)), reverse=True)
            
            # Select top goals to avoid overwhelming the system
            selected_goals = all_goals[:5]
            
            # Add metadata
            for goal in selected_goals:
                goal.update({
                    "status": "pending",
                    "created_by": "autonomous_goal_setter",
                    "created_at": datetime.now().isoformat(),
                    "auto_generated": True
                })
            
            # Store goals in Xano
            goals_stored = 0
            for goal in selected_goals:
                try:
                    response = requests.post(f"{self.xano_url}/ai_goal", json=goal, timeout=10)
                    if response.status_code == 200:
                        goals_stored += 1
                        print(f"✅ Goal set: {goal['title']}")
                    else:
                        print(f"⚠️ Failed to store goal: {goal['title']}")
                except Exception as e:
                    print(f"❌ Error storing goal {goal['title']}: {e}")
            
            result = {
                "success": True,
                "goals_generated": len(all_goals),
                "goals_stored": goals_stored,
                "selected_goals": selected_goals,
                "profit_patterns": profit_patterns,
                "trending_opportunities": trending_opportunities
            }
            
            print(f"🎯 Autonomous goal setting completed:")
            print(f"   Generated: {len(all_goals)} total goals")
            print(f"   Stored: {goals_stored} goals")
            print(f"   Categories: {len(set(g.get('category') for g in selected_goals))} different types")
            
            return result
            
        except Exception as e:
            print(f"❌ Error in autonomous goal setting: {e}")
            return {"success": False, "error": str(e)}
    
    def should_set_new_goals(self) -> bool:
        """Determine if new goals should be set"""
        try:
            # Get recent goals
            response = requests.get(f"{self.xano_url}/ai_goal", timeout=10)
            if response.status_code == 200:
                goals = response.json()
                if isinstance(goals, list):
                    # Check if we have pending goals
                    pending_goals = [g for g in goals if g.get('status') == 'pending']
                    
                    # Set new goals if we have fewer than 3 pending goals
                    if len(pending_goals) < 3:
                        return True
                    
                    # Set new goals if last goal was set more than 24 hours ago
                    recent_goals = [g for g in goals if 'created_at' in g]
                    if recent_goals:
                        latest_goal = max(recent_goals, key=lambda x: x.get('created_at', ''))
                        latest_time = datetime.fromisoformat(latest_goal['created_at'])
                        if (datetime.now() - latest_time).total_seconds() > 86400:  # 24 hours
                            return True
            
            # Default: set goals if we can't determine status
            return True
            
        except Exception as e:
            print(f"❌ Error checking if goals should be set: {e}")
            return True

# Global instance
autonomous_goal_setter = AutonomousGoalSetter()

def set_autonomous_goals():
    """Set autonomous goals based on current situation"""
    return autonomous_goal_setter.set_autonomous_goals()

def should_set_new_goals():
    """Check if new goals should be set"""
    return autonomous_goal_setter.should_set_new_goals()

if __name__ == "__main__":
    print("🎯 Testing Autonomous Goal Setter...")
    setter = AutonomousGoalSetter()
    result = setter.set_autonomous_goals()
    print(f"✅ Test completed: {result.get('success', False)}")
