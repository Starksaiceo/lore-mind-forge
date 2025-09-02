
import os
import json
import requests
from datetime import datetime, timedelta
from collections import defaultdict, Counter
from profit_tracker import get_profit_data, calculate_total_profit, get_profit_by_source

def get_all_memories(filter_by=None):
    """Get memories from Xano with optional filtering"""
    try:
        xano_url = os.getenv("XANO_BASE_URL", "https://x8ki-letl-twmt.n7.xano.io/api:8fyoFbLh")
        
        # Get profit data as memories
        response = requests.get(f"{xano_url}/profit", timeout=10)
        response.raise_for_status()
        
        memories = response.json()
        if not isinstance(memories, list):
            return []
        
        # Filter if requested
        if filter_by:
            filtered = []
            for memory in memories:
                if filter_by.lower() in str(memory).lower():
                    filtered.append(memory)
            return filtered
        
        return memories
        
    except Exception as e:
        print(f"❌ Error getting memories: {e}")
        return []

def write_memory(category, data):
    """Write a memory/insight to Xano"""
    try:
        xano_url = os.getenv("XANO_BASE_URL", "https://x8ki-letl-twmt.n7.xano.io/api:8fyoFbLh")
        
        payload = {
            "category": category,
            "data": str(data)[:500],  # Limit length
            "timestamp": datetime.now().isoformat(),
            "is_insight": True
        }
        
        # Use the profit endpoint for now, or create a memories endpoint
        response = requests.post(f"{xano_url}/profit", json={
            "amount": 0.0,
            "source": f"AI_Insight_{category}",
            "description": str(data)[:200],
            "timestamp": datetime.now().isoformat(),
            "is_real": False,
            "is_insight": True
        })
        
        print(f"💭 Memory stored: {category}")
        return True
        
    except Exception as e:
        print(f"❌ Error writing memory: {e}")
        return False

def get_current_goals():
    """Get current goals from Xano"""
    try:
        xano_url = os.getenv("XANO_BASE_URL", "https://x8ki-letl-twmt.n7.xano.io/api:8fyoFbLh")
        response = requests.get(f"{xano_url}/ai_goal", timeout=10)
        response.raise_for_status()
        
        goals = response.json()
        return goals if isinstance(goals, list) else []
        
    except Exception as e:
        print(f"❌ Error getting goals: {e}")
        return []

def set_new_goals(new_goals):
    """Set new goals in Xano"""
    try:
        xano_url = os.getenv("XANO_BASE_URL", "https://x8ki-letl-twmt.n7.xano.io/api:8fyoFbLh")
        
        for goal in new_goals:
            payload = {
                "description": goal.get("title", ""),
                "details": goal.get("details", ""),
                "status": goal.get("status", "pending"),
                "priority": goal.get("priority", 5),
                "created_at": datetime.now().isoformat()
            }
            
            response = requests.post(f"{xano_url}/ai_goal", json=payload)
            response.raise_for_status()
            print(f"🎯 New goal set: {goal.get('title', '')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error setting goals: {e}")
        return False

def analyze_performance():
    """Analyze AI CEO performance metrics"""
    try:
        print("🧠 Analyzing AI CEO performance...")
        
        # Get profit data and goals
        profit_logs = get_all_memories(filter_by="profit")
        goals = get_current_goals()
        profit_by_source = get_profit_by_source()
        total_profit = calculate_total_profit()
        
        # Calculate performance metrics
        performance = {
            "total_profit": total_profit,
            "goal_count": len(goals),
            "successful_goals": 0,
            "failed_goals": 0,
            "pending_goals": 0,
            "top_performers": [],
            "profit_sources": profit_by_source,
            "analysis_date": datetime.now().isoformat()
        }
        
        # Analyze goal completion rates
        for goal in goals:
            status = goal.get("status", "pending").lower()
            if status in ["complete", "completed", "success"]:
                performance["successful_goals"] += 1
            elif status in ["failed", "error", "cancelled"]:
                performance["failed_goals"] += 1
            else:
                performance["pending_goals"] += 1
        
        # Find top performing sources
        if profit_by_source:
            sorted_sources = sorted(profit_by_source.items(), key=lambda x: x[1], reverse=True)
            performance["top_performers"] = sorted_sources[:5]
        
        # Calculate success rates
        total_completed = performance["successful_goals"] + performance["failed_goals"]
        if total_completed > 0:
            performance["success_rate"] = performance["successful_goals"] / total_completed
        else:
            performance["success_rate"] = 0.0
        
        print(f"📊 Performance Analysis:")
        print(f"   Total Profit: ${performance['total_profit']:.2f}")
        print(f"   Success Rate: {performance['success_rate']:.1%}")
        print(f"   Goals: {performance['successful_goals']} success, {performance['failed_goals']} failed")
        
        return performance
        
    except Exception as e:
        print(f"❌ Error analyzing performance: {e}")
        return {
            "total_profit": 0.0,
            "goal_count": 0,
            "successful_goals": 0,
            "failed_goals": 0,
            "top_performers": [],
            "success_rate": 0.0
        }

def generate_insights(performance):
    """Generate strategic insights from performance data"""
    insights = []
    
    # Profit-based insights
    if performance["total_profit"] > 100:
        insights.append({
            "type": "success_pattern",
            "message": f"Strong profit performance (${performance['total_profit']:.2f}). Focus on scaling top performers.",
            "action": "scale_successful_strategies"
        })
    elif performance["total_profit"] > 0:
        insights.append({
            "type": "growth_opportunity",
            "message": f"Modest profit (${performance['total_profit']:.2f}). Identify and replicate successful patterns.",
            "action": "optimize_current_strategies"
        })
    else:
        insights.append({
            "type": "strategy_pivot",
            "message": "No profit yet. Need to pivot strategy and focus on proven methods.",
            "action": "pivot_to_proven_methods"
        })
    
    # Goal completion insights
    if performance["success_rate"] > 0.7:
        insights.append({
            "type": "execution_strength",
            "message": f"High success rate ({performance['success_rate']:.1%}). Can handle more ambitious goals.",
            "action": "increase_goal_complexity"
        })
    elif performance["success_rate"] < 0.3 and performance["failed_goals"] > 0:
        insights.append({
            "type": "execution_issue",
            "message": f"Low success rate ({performance['success_rate']:.1%}). Simplify goals and improve execution.",
            "action": "simplify_and_focus"
        })
    
    # Source performance insights
    if performance["top_performers"]:
        top_source, top_amount = performance["top_performers"][0]
        insights.append({
            "type": "top_performer",
            "message": f"Best performing source: {top_source} (${top_amount:.2f})",
            "action": f"double_down_on_{top_source.lower().replace(' ', '_')}"
        })
    
    return insights

def evolve_strategy():
    """Evolve AI strategy based on performance analysis"""
    try:
        print("🧠 AI CEO Self-Improvement Starting...")
        
        # Analyze current performance
        perf = analyze_performance()
        insights = generate_insights(perf)
        
        # Store insights as memories
        write_memory("performance_analysis", json.dumps(perf))
        write_memory("strategic_insights", json.dumps(insights))
        
        new_goals = []
        
        # Generate new goals based on insights
        for insight in insights:
            if insight["action"] == "scale_successful_strategies":
                if perf["top_performers"]:
                    top_sources = [source for source, amount in perf["top_performers"][:3] if amount > 10]
                    new_goals.append({
                        "title": "Scale Top Performing Strategies",
                        "details": f"Focus resources on: {', '.join(top_sources)}",
                        "status": "active",
                        "priority": 9
                    })
            
            elif insight["action"] == "optimize_current_strategies":
                new_goals.append({
                    "title": "Optimize Current Revenue Streams",
                    "details": "Analyze and improve existing profit sources for better ROI",
                    "status": "active",
                    "priority": 7
                })
            
            elif insight["action"] == "pivot_to_proven_methods":
                new_goals.append({
                    "title": "Research and Implement Proven Business Models",
                    "details": "Study successful e-commerce and digital product strategies",
                    "status": "active",
                    "priority": 8
                })
            
            elif insight["action"] == "simplify_and_focus":
                new_goals.append({
                    "title": "Simplify Operations and Focus on Core Activities",
                    "details": "Reduce complexity, focus on 1-2 main revenue streams",
                    "status": "active",
                    "priority": 8
                })
        
        # Set risk management goals if needed
        if perf["failed_goals"] > perf["successful_goals"]:
            new_goals.append({
                "title": "Implement Risk Management Protocol",
                "details": "Add validation steps and smaller test campaigns before scaling",
                "status": "active",
                "priority": 6
            })
            write_memory("strategy_warning", "High failure rate detected. Implementing conservative approach.")
        
        # Apply new goals if any were generated
        if new_goals:
            set_new_goals(new_goals)
            print(f"🎯 AI CEO evolved: {len(new_goals)} new strategic goals set")
        
        # Log the evolution
        evolution_log = {
            "timestamp": datetime.now().isoformat(),
            "performance_snapshot": perf,
            "insights_generated": len(insights),
            "new_goals_created": len(new_goals),
            "evolution_trigger": "weekly_self_analysis"
        }
        
        write_memory("evolution_log", json.dumps(evolution_log))
        
        print(f"✅ AI CEO Self-Improvement Complete:")
        print(f"   📊 Performance analyzed")
        print(f"   💡 {len(insights)} insights generated")
        print(f"   🎯 {len(new_goals)} new goals created")
        
        return {
            "success": True,
            "insights_count": len(insights),
            "new_goals_count": len(new_goals),
            "performance": perf
        }
        
    except Exception as e:
        print(f"❌ Error in strategy evolution: {e}")
        return {"success": False, "error": str(e)}

def get_learning_summary():
    """Get a summary of AI learning and improvements"""
    try:
        memories = get_all_memories()
        insights = [m for m in memories if m.get("source", "").startswith("AI_Insight")]
        
        summary = {
            "total_memories": len(memories),
            "insights_generated": len(insights),
            "last_evolution": None,
            "key_learnings": []
        }
        
        # Find last evolution
        evolution_memories = [m for m in insights if "evolution_log" in m.get("source", "")]
        if evolution_memories:
            latest = max(evolution_memories, key=lambda x: x.get("timestamp", ""))
            summary["last_evolution"] = latest.get("timestamp")
        
        # Extract key learnings
        strategy_memories = [m for m in insights if "strategic" in m.get("source", "").lower()]
        for memory in strategy_memories[-5:]:  # Last 5 strategic insights
            summary["key_learnings"].append(memory.get("description", ""))
        
        return summary
        
    except Exception as e:
        print(f"❌ Error getting learning summary: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    print("🧠 Testing AI CEO Self-Improvement System...")
    result = evolve_strategy()
    print(f"✅ Test completed: {result}")
