
#!/usr/bin/env python3

from google_trends_tool import fetch_google_trends, fetch_related_queries, get_trending_searches
import json

def test_google_trends():
    """Test the Google Trends integration"""
    print("🔍 Testing Google Trends Integration...")
    
    # Test 1: Basic trends data
    print("\n1. Testing basic trends for 'AI productivity tools':")
    result = fetch_google_trends("AI productivity tools", "today 3-m")
    print(json.dumps(result, indent=2, default=str))
    
    # Test 2: Related queries
    print("\n2. Testing related queries for 'shopify':")
    related = fetch_related_queries("shopify")
    print(json.dumps(related, indent=2, default=str))
    
    # Test 3: Trending searches
    print("\n3. Testing current trending searches:")
    trending = get_trending_searches('US')
    print(f"Current trending searches: {trending}")
    
    print("\n✅ Google Trends integration test completed!")

if __name__ == "__main__":
    test_google_trends()
