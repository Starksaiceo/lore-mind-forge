# Applying the requested changes to integrate the store builder tool into the agent setup.
import os
import requests
from pytrends.request import TrendReq
from langchain.tools import Tool
from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from google_trends_tool import (
    fetch_google_trends, 
    fetch_related_queries, 
    get_trending_searches,
    market_data_tool,
    fetch_and_store_market_data,
    analyze_trend_insights
)

# Load environment variables
load_dotenv()

# Xano configuration
XANO_BASE_URL = os.getenv("XANO_BASE_URL", "https://x8ki-letl-twmt.n7.xano.io/api:8fyoFbLh")

# Amazon Products API configuration  
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY", "your-rapidapi-key-here")
RAPIDAPI_HOST = "amazon-product-reviews.p.rapidapi.com"

# ————————————————————————————————
# Amazon Products fetcher (enhanced)
def fetch_amazon_products(keyword: str, max_results: int = 5) -> dict:
    """
    Search Amazon for products matching `keyword` via RapidAPI,
    returning up to `max_results` items with title, price, and URL.
    """
    try:
        if not RAPIDAPI_KEY or RAPIDAPI_KEY == "your-rapidapi-key-here":
            return {
                "success": False,
                "keyword": keyword,
                "error": "RAPIDAPI_KEY not configured. Please set it in your .env file.",
                "products": []
            }

        url = f"https://{RAPIDAPI_HOST}/product/amazon/search"
        headers = {
            "X-RapidAPI-Key": RAPIDAPI_KEY,
            "X-RapidAPI-Host": RAPIDAPI_HOST
        }
        params = {"keywords": keyword}

        response = requests.get(url, headers=headers, params=params, timeout=15)
        response.raise_for_status()

        data = response.json()
        results = data.get("results", [])[:max_results]

        # Format product data with enhanced details
        products = []
        for product in results:
            price_info = product.get("price", {})
            products.append({
                "title": product.get("title", "No title"),
                "price": price_info.get("value") if isinstance(price_info, dict) else price_info,
                "currency": price_info.get("currency", "USD") if isinstance(price_info, dict) else "USD",
                "rating": product.get("rating", "N/A"),
                "url": product.get("link", product.get("url", "")),
                "image": product.get("image", ""),
                "availability": product.get("availability", "Unknown"),
                "reviews_count": product.get("reviews_count", "N/A")
            })

        return {
            "success": True,
            "keyword": keyword,
            "products_found": len(products),
            "products": products,
            "message": f"Found {len(products)} products for '{keyword}'"
        }

    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "keyword": keyword,
            "error": f"API request failed: {str(e)}",
            "products": []
        }
    except Exception as e:
        return {
            "success": False,
            "keyword": keyword,
            "error": f"Failed to fetch Amazon products: {str(e)}",
            "products": []
        }

# ————————————————————————————————
# Google Trends fetcher (existing)
def fetch_google_trends(keyword: str, timeframe: str = "today 3-m") -> dict:
    """
    Returns Google Trends interest-over-time for `keyword` (default last 3 months).
    """
    try:
        pytrends = TrendReq()
        pytrends.build_payload([keyword], timeframe=timeframe)
        df = pytrends.interest_over_time()
        if df.empty:
            return {"error": "no data returned"}

        # Clean and convert to dict
        df = df.drop(columns=["isPartial"], errors="ignore")
        trend_data = df[keyword].to_dict()

        # Calculate basic stats
        values = list(trend_data.values())
        avg_interest = sum(values) / len(values) if values else 0

        return {
            "keyword": keyword,
            "timeframe": timeframe,
            "trend_data": trend_data,
            "avg_interest": round(avg_interest, 2),
            "data_points": len(trend_data)
        }
    except Exception as e:
        return {"error": f"Failed to fetch trends for '{keyword}': {str(e)}"}

# ————————————————————————————————
# Xano "fetch goals" tool
def fetch_goals_from_xano(query: str = "") -> dict:
    """Fetch all AI goals from Xano database"""
    try:
        url = f"{XANO_BASE_URL}/ai_goal"
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        goals_data = response.json()

        # Handle different response formats
        if isinstance(goals_data, list):
            goals = goals_data
        elif isinstance(goals_data, dict) and 'result1' in goals_data:
            goals = goals_data['result1']
        else:
            goals = []

        # Extract relevant goal information
        formatted_goals = []
        for goal in goals:
            if isinstance(goal, dict):
                formatted_goals.append({
                    "id": goal.get("id"),
                    "description": goal.get("description", goal.get("goal_text", "No description")),
                    "status": goal.get("status", "pending"),
                    "priority": goal.get("priority", 1),
                    "created_at": goal.get("created_at")
                })

        return {
            "success": True,
            "goals_count": len(formatted_goals),
            "goals": formatted_goals
        }

    except Exception as e:
        return {"success": False, "error": f"Failed to fetch goals: {str(e)}"}

# ————————————————————————————————
# Xano "log profit" tool
def log_profit_to_xano(profit_data: str) -> dict:
    """
    Log profit entry to Xano. 
    Input format: 'amount:25.0,source:Market research completion,goal_id:1'
    """
    try:
        # Parse the profit data string
        data_parts = profit_data.split(',')
        parsed_data = {}

        for part in data_parts:
            if ':' in part:
                key, value = part.split(':', 1)
                key = key.strip()
                value = value.strip()

                if key == 'amount':
                    parsed_data['amount'] = float(value)
                elif key == 'goal_id':
                    parsed_data['ai_goal_id'] = int(value) if value.isdigit() else None
                else:
                    parsed_data[key] = value

        # Ensure required fields
        if 'amount' not in parsed_data:
            return {"success": False, "error": "Amount is required"}
        if 'source' not in parsed_data:
            parsed_data['source'] = "AI Agent Task"

        url = f"{XANO_BASE_URL}/profit"
        headers = {"Content-Type": "application/json"}

        response = requests.post(url, json=parsed_data, headers=headers, timeout=10)
        response.raise_for_status()

        result = response.json()
        return {
            "success": True,
            "message": f"Logged ${parsed_data['amount']:.2f} profit from {parsed_data['source']}",
            "profit_id": result.get("id"),
            "data": result
        }

    except ValueError as e:
        return {"success": False, "error": f"Invalid profit data format: {str(e)}"}
    except Exception as e:
        return {"success": False, "error": f"Failed to log profit: {str(e)}"}

# ————————————————————————————————
# Import store builder
try:
    from store_tools import store_builder_tool
except ImportError:
    store_builder_tool = None

# Register all tools
google_trends_tool = Tool(
    name="GoogleTrends",
    func=fetch_google_trends,
    description="Fetch interest-over-time for a keyword via Google Trends. Usage: GoogleTrends('keyword')"
)

amazon_products_tool = Tool(
    name="AmazonProducts",
    func=fetch_amazon_products,
    description="Search Amazon for products by keyword. Returns product titles, prices, ratings, and URLs. Usage: AmazonProducts('wireless earbuds')"
)

fetch_goals_tool = Tool(
    name="FetchGoals",
    func=fetch_goals_from_xano,
    description="Retrieve all AI goals from Xano database."
)

log_profit_tool = Tool(
    name="LogProfit",
    func=log_profit_to_xano,
    description="Record a profit entry to Xano. Format: 'amount:25.0,source:description,goal_id:1'"
)

# ————————————————————————————————
# Initialize your AI CEO agent with all tools
def setup_agent():
    llm = ChatOpenAI(
        model="anthropic/claude-3-opus",
        temperature=0,
        openai_api_key=os.getenv("OPENROUTER_API_KEY"),
        openai_api_base="https://openrouter.ai/api/v1"
    )

    # Import multi-platform store builder tools
    from store_builder import ALL_STORE_TOOLS
    
    # Import comprehensive tools system
    from tools import tools as comprehensive_tools
    from risk_tool import risk_check_tool, compliance_check_tool

    all_tools = [
        google_trends_tool, 
        amazon_products_tool, 
        fetch_goals_tool, 
        log_profit_tool,
        risk_check_tool,
        compliance_check_tool
    ] + ALL_STORE_TOOLS + comprehensive_tools

    agent = initialize_agent(
        tools=all_tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )

    return agent

# ————————————————————————————————
# Main execution and testing
if __name__ == "__main__":
    print("🔍 Testing integrated tools...")

    # Test Google Trends
    print("\n1. Testing Google Trends...")
    trends_result = fetch_google_trends("AI business tools", "today 12-m")
    print("Trends result:", trends_result)

    # Test Amazon Products
    print("\n2. Testing Amazon Products...")
    products_result = fetch_amazon_products("wireless earbuds", 3)
    print("Products result:", products_result)

    if products_result.get("success"):
        print("✅ Amazon API working! Found products:")
        for i, product in enumerate(products_result.get("products", []), 1):
            print(f"  {i}. {product['title']} - ${product['price']} ({product['currency']})")
    else:
        print("❌ Amazon API test failed:", products_result.get("error"))

    # Test Fetch Goals
    print("\n3. Testing Fetch Goals...")
    goals_result = fetch_goals_from_xano("")
    print("Goals result:", goals_result)

    # Test Log Profit
    print("\n4. Testing Log Profit...")
    profit_result = log_profit_to_xano("amount:15.0,source:Tool integration test,goal_id:1")
    print("Profit result:", profit_result)

    print("\n🤖 Setting up AI agent with all tools...")
    try:
        agent = setup_agent()

        # Run comprehensive agent task
        print("\n🎯 Running comprehensive AI CEO task...")
        comprehensive_task = """
        Execute this complete business automation workflow:
        1. Use FetchGoals to get all current goals from the database
        2. For each goal, use GoogleTrends to research relevant market opportunities
        3. Use AmazonProducts to find actual products in trending niches
        4. Analyze both trend data and product availability to estimate potential ROI
        5. Use LogProfit to record estimated profits for promising opportunities
        6. Provide a summary of all actions taken, trends analyzed, products found, and profits logged
        """

        agent_result = agent.run(comprehensive_task)
        print("Agent result:", agent_result)

    except Exception as e:
        print(f"❌ Error setting up agent: {e}")
        print("Make sure your OPENROUTER_API_KEY and XANO_BASE_URL are set in the .env file")