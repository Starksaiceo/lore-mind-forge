
import streamlit as st
from datetime import datetime
import json
from typing import Dict, List

def render_system_status():
    """Render comprehensive system status dashboard"""
    st.title("🖥️ AI CEO System Status - Level 5")
    
    # Core System Health
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("System Level", "Level 5", "🚀 Fully Upgraded")
        
    with col2:
        try:
            from market_data import MarketDataEngine
            st.metric("Market Intelligence", "✅ Online", "Real-time data")
        except:
            st.metric("Market Intelligence", "❌ Offline", "Module missing")
            
    with col3:
        try:
            from agent_swarms import AgentSwarm
            st.metric("Agent Swarms", "✅ Active", "5 agents")
        except:
            st.metric("Agent Swarms", "❌ Inactive", "Module missing")
            
    with col4:
        try:
            from finance_optimizer import FinanceOptimizer
            st.metric("Finance AI", "✅ Running", "Auto-budgeting")
        except:
            st.metric("Finance AI", "❌ Down", "Module missing")
    
    # Advanced Capabilities Status
    st.subheader("🧠 Advanced AI Capabilities")
    
    capabilities = [
        ("🌐 Real-time Market Data", check_market_data_status()),
        ("💰 Financial Intelligence", check_finance_status()),
        ("🔥 Marketing Mastermind", check_marketing_status()),
        ("🤖 Self-Improving Agents", check_agent_swarm_status()),
        ("🧠 Customer Psychology", check_psychology_status()),
        ("📈 Predictive Analytics", check_analytics_status()),
        ("⚙️ Advanced Automation", check_automation_status()),
        ("🌱 Reinforcement Learning", check_learning_status()),
        ("🛡️ Compliance & Risk", check_compliance_status()),
        ("🌎 Global Expansion", check_localization_status())
    ]
    
    for capability, status in capabilities:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(capability)
        with col2:
            if status["active"]:
                st.success("✅ Active")
            else:
                st.error("❌ Inactive")
                
        if status["details"]:
            st.caption(status["details"])
    
    # Performance Metrics
    st.subheader("📊 Performance Metrics")
    
    try:
        from profit_tracker import calculate_total_real_revenue
        total_revenue = calculate_total_real_revenue()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Revenue", f"${total_revenue:.2f}")
            
        with col2:
            # Calculate automation efficiency
            automation_score = calculate_automation_score()
            st.metric("Automation Efficiency", f"{automation_score}%")
            
        with col3:
            # Calculate AI sophistication level
            ai_score = calculate_ai_sophistication()
            st.metric("AI Sophistication", f"{ai_score}/100")
            
    except Exception as e:
        st.error(f"Performance metrics error: {e}")
    
    # System Recommendations
    st.subheader("💡 System Recommendations")
    
    recommendations = generate_system_recommendations()
    for rec in recommendations:
        st.info(f"• {rec}")

def check_market_data_status() -> Dict:
    """Check market data module status"""
    try:
        from market_data import MarketDataEngine
        engine = MarketDataEngine()
        # Quick test
        test_result = engine._get_google_trends("test")
        return {"active": True, "details": f"Google Trends: {len(test_result)} keywords available"}
    except Exception as e:
        return {"active": False, "details": f"Error: {str(e)}"}

def check_finance_status() -> Dict:
    """Check finance optimizer status"""
    try:
        from finance_optimizer import FinanceOptimizer
        optimizer = FinanceOptimizer()
        result = optimizer.calculate_optimal_ad_budget()
        if result.get("success"):
            return {"active": True, "details": f"Budget: ${result.get('recommended_budget', 0):.2f}"}
        else:
            return {"active": False, "details": "Budget calculation failed"}
    except Exception as e:
        return {"active": False, "details": f"Error: {str(e)}"}

def check_marketing_status() -> Dict:
    """Check marketing capabilities"""
    # Check for content generation and social posting
    try:
        import os
        content_dir = "content_ready_to_post"
        if os.path.exists(content_dir):
            files = os.listdir(content_dir)
            return {"active": True, "details": f"{len(files)} content pieces ready"}
        else:
            return {"active": False, "details": "No content directory found"}
    except Exception as e:
        return {"active": False, "details": f"Error: {str(e)}"}

def check_agent_swarm_status() -> Dict:
    """Check agent swarm status"""
    try:
        from agent_swarms import AgentSwarm
        swarm = AgentSwarm()
        agent_count = len(swarm.agents)
        return {"active": True, "details": f"{agent_count} specialized agents active"}
    except Exception as e:
        return {"active": False, "details": f"Error: {str(e)}"}

def check_psychology_status() -> Dict:
    """Check psychology engine status"""
    try:
        from psychology_engine import PsychologyEngine
        engine = PsychologyEngine()
        trigger_count = sum(len(triggers) for triggers in engine.emotion_triggers.values())
        return {"active": True, "details": f"{trigger_count} psychological triggers available"}
    except Exception as e:
        return {"active": False, "details": f"Error: {str(e)}"}

def check_analytics_status() -> Dict:
    """Check predictive analytics"""
    try:
        # Check if we have historical data for predictions
        from profit_tracker import get_profit_data
        data = get_profit_data() if callable(get_profit_data) else []
        if len(data) > 0:
            return {"active": True, "details": f"{len(data)} data points for analysis"}
        else:
            return {"active": False, "details": "Insufficient data for predictions"}
    except Exception as e:
        return {"active": False, "details": f"Error: {str(e)}"}

def check_automation_status() -> Dict:
    """Check automation capabilities"""
    try:
        # Check if autopilot functions exist
        from autopilot import get_ai_ceo_status
        status = get_ai_ceo_status()
        if status.get("running"):
            return {"active": True, "details": f"{status.get('cycles_completed', 0)} cycles completed"}
        else:
            return {"active": True, "details": "Automation ready, not currently running"}
    except Exception as e:
        return {"active": False, "details": f"Error: {str(e)}"}

def check_learning_status() -> Dict:
    """Check reinforcement learning"""
    try:
        from self_improvement import get_learning_summary
        summary = get_learning_summary()
        if "error" not in summary:
            return {"active": True, "details": f"{summary.get('total_memories', 0)} memories stored"}
        else:
            return {"active": False, "details": "Learning system initializing"}
    except Exception as e:
        return {"active": False, "details": f"Error: {str(e)}"}

def check_compliance_status() -> Dict:
    """Check compliance system"""
    try:
        from compliance_checker import ComplianceChecker
        checker = ComplianceChecker()
        rule_count = sum(len(rules) for rules in checker.compliance_rules.values())
        return {"active": True, "details": f"{rule_count} compliance rules active"}
    except Exception as e:
        return {"active": False, "details": f"Error: {str(e)}"}

def check_localization_status() -> Dict:
    """Check localization capabilities"""
    # This would be implemented with translation APIs
    return {"active": False, "details": "Translation APIs not yet integrated"}

def calculate_automation_score() -> int:
    """Calculate overall automation efficiency score"""
    score = 0
    
    # Check automated functions
    try:
        from autopilot import get_ai_ceo_status
        status = get_ai_ceo_status()
        if status.get("cycles_completed", 0) > 0:
            score += 30
    except:
        pass
    
    # Check content automation
    try:
        import os
        if os.path.exists("content_ready_to_post"):
            score += 20
    except:
        pass
    
    # Check product automation
    try:
        import glob
        product_files = glob.glob("product_*.md")
        if len(product_files) > 0:
            score += 25
    except:
        pass
    
    # Check financial automation
    try:
        from finance_optimizer import FinanceOptimizer
        score += 25
    except:
        pass
    
    return min(score, 100)

def calculate_ai_sophistication() -> int:
    """Calculate AI sophistication level"""
    score = 20  # Base level
    
    modules = [
        "market_data", "psychology_engine", "agent_swarms", 
        "finance_optimizer", "compliance_checker"
    ]
    
    for module in modules:
        try:
            __import__(module)
            score += 16  # Each advanced module adds 16 points
        except:
            pass
    
    return min(score, 100)

def generate_system_recommendations() -> List[str]:
    """Generate system improvement recommendations"""
    recommendations = []
    
    # Check what's missing and suggest improvements
    try:
        from market_data import MarketDataEngine
    except:
        recommendations.append("Install market data engine for real-time trend analysis")
    
    try:
        from agent_swarms import AgentSwarm
    except:
        recommendations.append("Add agent swarm system for competitive task optimization")
    
    try:
        from compliance_checker import ComplianceChecker
    except:
        recommendations.append("Implement compliance checker to avoid platform violations")
    
    # Check revenue and suggest scaling
    try:
        from profit_tracker import calculate_total_real_revenue
        revenue = calculate_total_real_revenue()
        if revenue < 100:
            recommendations.append("Focus on revenue generation - consider automated product launches")
        elif revenue > 500:
            recommendations.append("Scale advertising budget and expand to new markets")
    except:
        pass
    
    if not recommendations:
        recommendations.append("System fully optimized! Consider expanding to new platforms")
        recommendations.append("Monitor performance metrics and continue scaling successful strategies")
        recommendations.append("Test new AI capabilities as they become available")
    
    return recommendations

if __name__ == "__main__":
    render_system_status()
