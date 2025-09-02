from pytrends.request import TrendReq
from langchain.tools import Tool
import pandas as pd
import time
import requests
import os
from datetime import datetime
import warnings
from typing import List, Dict

# Suppress warnings for cleaner output
warnings.filterwarnings("ignore")

def fetch_google_trends(keyword: str, timeframe: str = "today 3-m") -> dict:
    """
    Returns Google Trends interest-over-time for `keyword` (default last 3 months).
    Includes rate limiting to avoid Google blocking requests.
    """
    try:
        # Add delay to avoid rate limiting
        time.sleep(1)

        # Initialize TrendReq with minimal parameters to avoid urllib3 issues
        pytrends = TrendReq(hl='en-US', tz=360, timeout=(10,25), retries=2, backoff_factor=0.1)
        pytrends.build_payload([keyword], timeframe=timeframe, geo='', gprop='')

        df = pytrends.interest_over_time()
        if df.empty:
            return {"error": f"No trend data found for '{keyword}'"}

        # Clean the data and convert to dict
        df = df.drop(columns=["isPartial"], errors="ignore")
        trend_data = df[keyword].to_dict()

        # Calculate some basic stats
        values = list(trend_data.values())
        avg_interest = sum(values) / len(values) if values else 0
        max_interest = max(values) if values else 0
        min_interest = min(values) if values else 0

        return {
            "keyword": keyword,
            "timeframe": timeframe,
            "trend_data": trend_data,
            "avg_interest": round(avg_interest, 2),
            "max_interest": max_interest,
            "min_interest": min_interest,
            "data_points": len(trend_data)
        }

    except Exception as e:
        return {"error": f"Failed to fetch trends for '{keyword}': {str(e)}"}

def fetch_related_queries(keyword: str) -> dict:
    """
    Get related queries for a keyword from Google Trends
    """
    try:
        time.sleep(1)  # Rate limiting

        # Initialize with minimal parameters to avoid urllib3 issues
        pytrends = TrendReq(hl='en-US', tz=360, timeout=(10,25), retries=2, backoff_factor=0.1)
        pytrends.build_payload([keyword], timeframe='today 3-m')

        related_queries = pytrends.related_queries()

        if keyword in related_queries and related_queries[keyword]:
            top_queries = related_queries[keyword].get('top', pd.DataFrame())
            rising_queries = related_queries[keyword].get('rising', pd.DataFrame())

            result = {
                "keyword": keyword,
                "top_queries": top_queries.to_dict('records') if not top_queries.empty else [],
                "rising_queries": rising_queries.to_dict('records') if not rising_queries.empty else []
            }
            return result
        else:
            return {"error": f"No related queries found for '{keyword}'"}

    except Exception as e:
        return {"error": f"Failed to fetch related queries for '{keyword}': {str(e)}"}

# Create LangChain tools
google_trends_tool = Tool(
    name="GoogleTrends",
    func=lambda keyword: fetch_google_trends(keyword, "today 3-m"),
    description="Fetch Google Trends interest-over-time data for a keyword over the last 3 months. Use this to research market demand and trending topics."
)

related_queries_tool = Tool(
    name="RelatedQueries", 
    func=fetch_related_queries,
    description="Get related and rising search queries for a keyword from Google Trends. Use this to discover related market opportunities."
)

def get_trending_searches(geo='US'):
    """
    Get current trending searches in a specific geography
    """
    try:
        time.sleep(1)
        pytrends = TrendReq(hl='en-US', tz=360, timeout=(10,25), retries=2, backoff_factor=0.1)
        trending = pytrends.trending_searches(pn=geo)
        return trending.head(10).values.flatten().tolist()
    except Exception as e:
        return [f"Error fetching trending searches: {str(e)}"]

trending_searches_tool = Tool(
    name="TrendingSearches",
    func=lambda geo='US': get_trending_searches(geo),
    description="Get current trending searches. Default is US, but you can specify other countries like 'GB', 'CA', 'AU', etc."
)

def store_market_trends_data(keyword: str, trend_data: dict, xano_url: str = None) -> dict:
    """
    Store market trends data in Xano under market_trends endpoint
    """
    try:
        if not xano_url:
            xano_url = os.getenv("XANO_BASE_URL", "https://x8ki-letl-twmt.n7.xano.io/api:8fyoFbLh")

        # Prepare data for storage
        payload = {
            "keyword": keyword,
            "timeframe": trend_data.get("timeframe", "today 12-m"),
            "avg_interest": trend_data.get("avg_interest", 0),
            "max_interest": trend_data.get("max_interest", 0),
            "min_interest": trend_data.get("min_interest", 0),
            "data_points": trend_data.get("data_points", 0),
            "trend_data_json": str(trend_data.get("trend_data", {})),
            "created_at": datetime.now().isoformat(),
            "analysis_summary": ""
        }

        # Store in Xano
        response = requests.post(f"{xano_url}/market_trends", json=payload, timeout=15)

        if response.status_code == 201:
            return {
                "success": True,
                "message": f"Market trends data for '{keyword}' stored successfully",
                "data": response.json()
            }
        else:
            return {
                "success": False,
                "error": f"Failed to store data. Status: {response.status_code}"
            }

    except Exception as e:
        return {
            "success": False,
            "error": f"Error storing market trends: {str(e)}"
        }

def fetch_and_store_market_data(keyword: str, timeframe: str = "today 12-m") -> dict:
    """
    Fetch Google Trends data and store it in Xano
    """
    try:
        # Fetch trends data
        trend_result = fetch_google_trends(keyword, timeframe)

        if "error" in trend_result:
            return trend_result

        # Store in Xano
        storage_result = store_market_trends_data(keyword, trend_result)

        # Combine results
        return {
            "keyword": keyword,
            "trend_data": trend_result,
            "storage_result": storage_result,
            "success": storage_result.get("success", False)
        }

    except Exception as e:
        return {"error": f"Failed to fetch and store market data: {str(e)}"}

def analyze_trend_insights(trend_data: dict) -> dict:
    """
    Analyze trend data and provide key insights
    """
    try:
        if "trend_data" not in trend_data or not trend_data["trend_data"]:
            return {"error": "No trend data to analyze"}

        data_points = trend_data["trend_data"]
        values = list(data_points.values())

        if not values:
            return {"error": "No data values found"}

        # Calculate insights
        avg_interest = sum(values) / len(values)
        max_interest = max(values)
        min_interest = min(values)
        peak_dates = [date for date, value in data_points.items() if value == max_interest]

        # Detect trends
        recent_values = values[-4:] if len(values) >= 4 else values
        earlier_values = values[:4] if len(values) >= 4 else values

        recent_avg = sum(recent_values) / len(recent_values)
        earlier_avg = sum(earlier_values) / len(earlier_values)

        trend_direction = "rising" if recent_avg > earlier_avg else "declining" if recent_avg < earlier_avg else "stable"

        insights = {
            "top_insights": [
                f"Peak interest of {max_interest} occurred on {peak_dates[0] if peak_dates else 'unknown date'}",
                f"Average interest level: {avg_interest:.1f}/100 with {trend_direction} trend",
                f"Interest range: {min_interest}-{max_interest} (volatility: {max_interest - min_interest})"
            ],
            "metrics": {
                "avg_interest": round(avg_interest, 1),
                "max_interest": max_interest,
                "min_interest": min_interest,
                "trend_direction": trend_direction,
                "peak_dates": peak_dates[:3],  # Top 3 peak dates
                "volatility": max_interest - min_interest
            }
        }

        return insights

    except Exception as e:
        return {"error": f"Failed to analyze trends: {str(e)}"}

def get_trending_keywords(keyword: str, timeframe: str = "today 3-m") -> List[Dict]:
    """
    Get trending keywords and related queries for a given keyword
    Returns a list of trending keyword data
    """
    try:
        # Get main trend data
        trend_data = fetch_google_trends(keyword, timeframe)
        if "error" in trend_data:
            return []
        
        # Get related queries
        related_data = fetch_related_queries(keyword)
        
        # Combine into trending keywords list
        trending_keywords = []
        
        # Add main keyword with its data
        trending_keywords.append({
            "keyword": keyword,
            "interest_score": trend_data.get("avg_interest", 0),
            "max_interest": trend_data.get("max_interest", 0),
            "trend_direction": "stable",  # Could be enhanced with trend analysis
            "date": datetime.now().isoformat(),
            "volume": trend_data.get("avg_interest", 0)
        })
        
        # Add related queries if available
        if not related_data.get("error") and "top_queries" in related_data:
            for query in related_data["top_queries"][:5]:  # Top 5 related
                if "query" in query:
                    trending_keywords.append({
                        "keyword": query["query"],
                        "interest_score": query.get("value", 0),
                        "max_interest": query.get("value", 0),
                        "trend_direction": "related",
                        "date": datetime.now().isoformat(),
                        "volume": query.get("value", 0)
                    })
        
        return trending_keywords
        
    except Exception as e:
        print(f"Error getting trending keywords: {e}")
        return []

# Enhanced LangChain tool for market data integration
market_data_tool = Tool(
    name="MarketDataIntegration",
    func=lambda keyword: fetch_and_store_market_data(keyword, "today 12-m"),
    description="Fetch Google Trends data for a keyword over 12 months and store it in Xano market_trends endpoint. Returns trend data and storage confirmation."
)