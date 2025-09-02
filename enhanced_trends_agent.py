
#!/usr/bin/env python3

import warnings
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType
from google_trends_tool import fetch_google_trends, fetch_related_queries, get_trending_searches
from profit_tracker import post_profit
import os
from dotenv import load_dotenv

# Suppress warnings
warnings.filterwarnings("ignore", message=".*Scale bindings.*")
warnings.filterwarnings("ignore", message=".*Infinite extent.*")

load_dotenv()

def fetch_trends_for_goal(keyword: str) -> list:
    """Enhanced trends fetching with error handling"""
    try:
        trends_result = fetch_google_trends(keyword, "now 7-d")
        if 'error' in trends_result:
            return []
        
        related_result = fetch_related_queries(keyword)
        if 'error' in related_result:
            return []
        
        # Extract top queries
        top_queries = related_result.get('top_queries', [])
        return [q.get('query', '') for q in top_queries[:5] if q.get('query')]
    
    except Exception as e:
        print(f"❌ Error fetching trends for {keyword}: {e}")
        return []

def setup_enhanced_langchain_agent():
    """Set up LangChain agent with enhanced Google Trends integration"""
    llm = ChatOpenAI(
        model="openai/gpt-4",
        temperature=0,
        openai_api_key=os.getenv("OPENROUTER_API_KEY"),
        openai_api_base="https://openrouter.ai/api/v1"
    )
    
    def enhanced_trends_tool(input_str):
        """Enhanced trends tool with market analysis"""
        try:
            trends = fetch_trends_for_goal(input_str)
            if trends:
                print(f"👉 Top trends for '{input_str}': {trends}")
                # Track market research completion
                post_profit(5.0, f"Market Research: {input_str}")
                return f"Found {len(trends)} trending topics: {', '.join(trends[:3])}"
            else:
                return f"No trends found for '{input_str}'"
        except Exception as e:
            return f"Error fetching trends: {e}"
    
    def profit_tracker_tool(input_str):
        """Enhanced profit tracking tool"""
        try:
            import re
            amount_match = re.search(r'\$?(\d+(?:\.\d{2})?)', input_str)
            if amount_match:
                amount = float(amount_match.group(1))
                post_profit(amount, "LangChain Agent Goal")
                return f"Tracked ${amount} profit successfully"
            else:
                post_profit(25.0, "LangChain Agent Goal Completion")
                return "Tracked $25 default completion bonus"
        except Exception as e:
            return f"Error tracking profit: {e}"
    
    tools = [
        Tool(
            name="GoogleTrends",
            func=enhanced_trends_tool,
            description="Get top related search queries and trends for a keyword. Use this for market research."
        ),
        Tool(
            name="ProfitTracker",
            func=profit_tracker_tool,
            description="Track profit when goals generate revenue or are completed successfully"
        )
    ]
    
    agent = initialize_agent(
        tools,
        llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True
    )
    
    return agent

def process_goal_with_trends(goal: str):
    """Process a goal with initial trends research"""
    try:
        agent = setup_enhanced_langchain_agent()
        
        print(f"\n🛰️ Fetching current trends for '{goal}'...")
        
        # First, research trends
        trends_result = agent.run(f"Use GoogleTrends to research market opportunities for: {goal}")
        print(f"📊 Trends analysis: {trends_result}")
        
        # Then process the main goal with context
        enhanced_goal = f"""
        {goal}
        
        Market context from trends research: {trends_result}
        
        Based on this market data, identify profitable opportunities and create an action plan.
        Use ProfitTracker when you complete profitable actions or identify revenue opportunities.
        """
        
        print(f"\n🔄 Processing enhanced goal...")
        result = agent.run(enhanced_goal)
        
        return {
            "goal": goal,
            "trends_analysis": trends_result,
            "result": result,
            "status": "completed"
        }
        
    except Exception as e:
        print(f"❌ Error processing goal: {e}")
        return {
            "goal": goal,
            "error": str(e),
            "status": "failed"
        }

def main():
    """Main execution function"""
    goals = [
        "ecommerce opportunities",
        "social media marketing trends", 
        "product sourcing automation"
    ]
    
    results = []
    for idx, goal in enumerate(goals, 1):
        print(f"\n🔄 Working on goal #{idx}: {goal}")
        result = process_goal_with_trends(goal)
        results.append(result)
        
        if result['status'] == 'completed':
            print(f"✅ Goal completed: {goal}")
        else:
            print(f"❌ Goal failed: {goal}")
    
    print(f"\n📊 Summary: {len([r for r in results if r['status'] == 'completed'])}/{len(results)} goals completed")
    return results

if __name__ == "__main__":
    main()
