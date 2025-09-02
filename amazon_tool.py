
import os
import requests
from typing import List, Dict
from langchain.agents import Tool

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_HOST = "amazon-product-reviews.p.rapidapi.com"

def fetch_amazon_bestsellers(category: str, count: int = 10) -> List[Dict]:
    """
    Returns the top `count` best-selling products in the given Amazon category.
    """
    if not RAPIDAPI_KEY:
        return [{"error": "RAPIDAPI_KEY not set in environment"}]
    
    url = f"https://{RAPIDAPI_HOST}/product/bestsellers"
    params = {"category": category, "limit": count}
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": RAPIDAPI_HOST
    }
    
    try:
        resp = requests.get(url, headers=headers, params=params, timeout=10)
        resp.raise_for_status()
        return resp.json().get("results", [])
    except Exception as e:
        return [{"error": f"Failed to fetch Amazon bestsellers: {str(e)}"}]

def search_amazon_products(keyword: str, max_results: int = 10) -> List[Dict]:
    """
    Search Amazon products by keyword
    """
    if not RAPIDAPI_KEY:
        return [{"error": "RAPIDAPI_KEY not set in environment"}]
    
    url = f"https://{RAPIDAPI_HOST}/product/search"
    params = {"keyword": keyword, "limit": max_results}
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": RAPIDAPI_HOST
    }
    
    try:
        resp = requests.get(url, headers=headers, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        products = data.get("results", [])
        
        return [
            {
                "title": p.get("title", "No title"),
                "price": p.get("price", "N/A"),
                "rating": p.get("rating", "N/A"),
                "url": p.get("url", ""),
                "image": p.get("image", ""),
                "availability": p.get("availability", "Unknown")
            }
            for p in products[:max_results]
        ]
    except Exception as e:
        return [{"error": f"Failed to search Amazon products: {str(e)}"}]

# LangChain Tools
amazon_bestsellers_tool = Tool(
    name="FetchAmazonBestsellers",
    func=fetch_amazon_bestsellers,
    description="Get top best-selling Amazon products for a category (electronics, books, home, etc.)"
)

amazon_search_tool = Tool(
    name="SearchAmazonProducts",
    func=search_amazon_products,
    description="Search Amazon products by keyword and get product details including price, rating, and availability"
)
