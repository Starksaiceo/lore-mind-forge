
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType
import requests
import os
import time
from dotenv import load_dotenv
from profit_tracker import log_profit
from google_trends_tool import google_trends_tool, related_queries_tool, trending_searches_tool

# Load environment variables
load_dotenv()

def setup_langchain_agent():
    """Set up the LangChain agent with OpenRouter"""
    llm = ChatOpenAI(
        model="anthropic/claude-3-opus",
        temperature=0,
        openai_api_key=os.getenv("OPENROUTER_API_KEY"),
        openai_api_base="https://openrouter.ai/api/v1"
    )
    
    # Create custom tools
    def profit_tracker_tool(input_str):
        """Tool to track profit when goals are completed"""
        try:
            # Parse amount from input (simple extraction)
            import re
            amount_match = re.search(r'\$?(\d+(?:\.\d{2})?)', input_str)
            if amount_match:
                amount = float(amount_match.group(1))
                log_profit(amount, "LangChain Agent Goal", ai_task_id=1, ai_goal_id=1)
                return f"Tracked ${amount} profit successfully"
            else:
                log_profit(25.0, "LangChain Agent Goal Completion", ai_task_id=1, ai_goal_id=1)
                return "Tracked $25 default completion bonus"
        except Exception as e:
            return f"Error tracking profit: {e}"
    
    def web_research_tool(query):
        """Simple web research simulation"""
        return f"Researched: {query}. Found relevant market data and opportunities."
    
    tools = [
        Tool(
            name="ProfitTracker",
            func=profit_tracker_tool,
            description="Use this to track profit when a goal generates revenue or is completed successfully"
        ),
        Tool(
            name="WebResearch",
            func=web_research_tool,
            description="Use this to research market trends, opportunities, or gather information"
        ),
        google_trends_tool,
        related_queries_tool,
        trending_searches_tool
    ]
    
    agent = initialize_agent(
        tools,
        llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True
    )
    
    return agent

def fetch_ai_goals():
    """Fetch AI goals from Xano API"""
    xano_url = os.getenv("XANO_BASE_URL", "https://x8ki-letl-twmt.n7.xano.io/api:8fyoFbLh")
    url = f"{xano_url}/ai_goal"
    
    try:
        time.sleep(1)  # Small delay before API call
        response = requests.get(url)
        
        if response.status_code == 429:
            print("⚠️ Rate limited when fetching goals. Using default goal.")
            return [
                "Use GoogleTrends to research current trending topics and identify profitable opportunities",
                "Find rising search queries related to e-commerce and analyze market potential"
            ]
            
        response.raise_for_status()
        data = response.json()
        
        # Handle different response formats
        if isinstance(data, list):
            goals = [item.get('description', item.get('goal_text', str(item))) for item in data]
        elif isinstance(data, dict) and 'result1' in data:
            goals = [item.get('description', item.get('goal_text', str(item))) for item in data['result1']]
        else:
            goals = []
            
        return [goal for goal in goals if goal and goal.strip()]
        
    except Exception as e:
        print(f"❌ Failed to fetch goals from Xano: {e}")
        return ["Analyze current market trends for profitable opportunities"]  # Default goal

def update_goal_status(goal_id, status, result):
    """Update goal status in Xano"""
    xano_url = os.getenv("XANO_BASE_URL", "https://x8ki-letl-twmt.n7.xano.io/api:8fyoFbLh")
    url = f"{xano_url}/ai_goal/{goal_id}"
    
    try:
        response = requests.patch(url, json={
            "status": status,
            "result": result,
            "completed_at": int(__import__('time').time())
        })
        response.raise_for_status()
        print(f"✅ Updated goal {goal_id} status to {status}")
    except Exception as e:
        print(f"❌ Failed to update goal status: {e}")

def run_langchain_agent_on_goals():
    """Main function to run LangChain agent on fetched goals"""
    print("🤖 Initializing LangChain AI CEO Agent...")
    
    try:
        agent = setup_langchain_agent()
        goals = fetch_ai_goals()
        
        if not goals:
            print("⚠️ No goals found, using default goal.")
            goals = ["Research profitable e-commerce opportunities and create an action plan"]
        
        results = []
        
        for i, goal in enumerate(goals[:3]):  # Limit to 3 goals to avoid rate limits
            print(f"\n🤖 AI CEO working on goal {i+1}: {goal}")
            print(f"📋 Goal details: {goal}")
            print(f"⚡ Starting agent execution...")
            
            try:
                # Enhance the goal with profit-tracking instruction
                enhanced_goal = f"""
                {goal}
                
                Use the GoogleTrends, RelatedQueries, and TrendingSearches tools to research market opportunities.
                Look for trending topics, rising search queries, and high-interest keywords that could indicate profitable markets.
                
                After completing this goal, if you identify any revenue opportunities or complete profitable actions, 
                use the ProfitTracker tool to log the profit amount.
                """
                
                print(f"🔄 Processing goal with enhanced prompt...")
                result = agent.run(enhanced_goal)
                print(f"✅ Goal {i+1} completed successfully!")
                print(f"📊 Result: {result}")
                
                results.append({
                    "goal": goal,
                    "result": result,
                    "status": "completed"
                })
                
                # Update goal status if we have goal IDs
                # update_goal_status(i+1, "completed", result)
                
            except Exception as e:
                error_msg = f"❌ Error running agent on goal: {e}"
                print(error_msg)
                results.append({
                    "goal": goal,
                    "result": error_msg,
                    "status": "failed"
                })
        
        return results
        
    except Exception as e:
        print(f"❌ Failed to initialize agent: {e}")
        return []

if __name__ == "__main__":
    run_langchain_agent_on_goals()
