# tools.py
import os
import json
import requests
from typing import Any, Dict, List
from langchain.agents import Tool
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import all tool modules
from google_trends_tool import google_trends_tool, related_queries_tool, trending_searches_tool, market_data_tool
from amazon_tool import amazon_bestsellers_tool, amazon_search_tool
from shopify_tools import amazon_products_tool, list_products_tool, create_product_tool
from shopify_analytics_tool import shopify_analytics_tool, shopify_products_tool, shopify_health_tool
from store_tools import create_store_tool
from store_builder import store_builder_tool
from risk_tool import risk_check_tool, compliance_check_tool

# Configuration from environment
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_HOST = "amazon-product-reviews.p.rapidapi.com"
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
SHOPIFY_API_KEY = os.getenv("SHOPIFY_API_KEY")
SHOPIFY_PASSWORD = os.getenv("SHOPIFY_PASSWORD")
SHOPIFY_SHOP_NAME = os.getenv("SHOPIFY_SHOP_NAME")
STRIPE_API_KEY = os.getenv("STRIPE_API_KEY")
PAYPAL_CLIENT_ID = os.getenv("PAYPAL_CLIENT_ID")
PAYPAL_CLIENT_SECRET = os.getenv("PAYPAL_CLIENT_SECRET")
PLAID_CLIENT_ID = os.getenv("PLAID_CLIENT_ID")
PLAID_SECRET = os.getenv("PLAID_SECRET")
COHERE_KEY = os.getenv("COHERE_KEY")
BUFFER_TOKEN = os.getenv("BUFFER_TOKEN")
ZAPIER_WEBHOOK = os.getenv("ZAPIER_WEBHOOK")
XANO_BASE_URL = os.getenv("XANO_BASE_URL", "https://x8ki-letl-twmt.n7.xano.io/api:8fyoFbLh")

# 1) Google Trends implementation
def fetch_google_trends(keyword: str) -> dict:
    """Fetch Google Trends data for keyword"""
    try:
        from pytrends.request import TrendReq
        pytrends = TrendReq()
        pytrends.build_payload([keyword], timeframe="now 7-d")
        df = pytrends.interest_over_time()
        if df.empty:
            return {"error": "No data found", "keyword": keyword}
        return {
            "keyword": keyword,
            "data": df[keyword].to_dict(),
            "success": True
        }
    except Exception as e:
        return {"error": f"Google Trends failed: {str(e)}", "keyword": keyword}

# 2) Amazon Products implementation
def fetch_amazon_products(keyword: str) -> dict:
    """Fetch Amazon products via RapidAPI"""
    if not RAPIDAPI_KEY:
        return {"error": "RAPIDAPI_KEY not configured", "keyword": keyword}

    try:
        url = f"https://{RAPIDAPI_HOST}/product/amazon/search"
        headers = {
            "X-RapidAPI-Key": RAPIDAPI_KEY,
            "X-RapidAPI-Host": RAPIDAPI_HOST
        }
        params = {"keywords": keyword}

        response = requests.get(url, headers=headers, params=params, timeout=15)
        response.raise_for_status()

        data = response.json()
        products = []
        for product in data.get("results", [])[:10]:
            price_info = product.get("price", {})
            products.append({
                "title": product.get("title", "No title"),
                "price": price_info.get("value") if isinstance(price_info, dict) else price_info,
                "currency": price_info.get("currency", "USD") if isinstance(price_info, dict) else "USD",
                "url": product.get("link", product.get("url", ""))
            })

        return {
            "keyword": keyword,
            "products": products,
            "count": len(products),
            "success": True
        }
    except Exception as e:
        return {"error": f"Amazon search failed: {str(e)}", "keyword": keyword}

# 3) Shopify Analytics implementation
def fetch_shopify_analytics(store_id: str) -> dict:
    """Fetch Shopify analytics data"""
    shopify_api_key = os.getenv("SHOPIFY_API_KEY")
    shopify_api_secret = os.getenv("SHOPIFY_API_SECRET")
    shopify_access_token = os.getenv("SHOPIFY_API_ACCESS_TOKEN")
    shopify_shop_url = os.getenv("SHOPIFY_SHOP_URL")

    if not all([shopify_api_key, shopify_api_secret, shopify_access_token, shopify_shop_url]):
        return {"error": "Shopify credentials not configured", "store_id": store_id}

    try:
        import shopify

        # Initialize Shopify session
        api_version = os.getenv("SHOPIFY_API_VERSION", "2023-10")
        shopify.Session.setup(api_key=shopify_api_key, secret=shopify_api_secret)
        session = shopify.Session(shopify_shop_url, api_version, shopify_access_token)
        shopify.ShopifyResource.activate_session(session)

        # Fetch orders and calculate metrics
        orders = shopify.Order.find(limit=250, status='any')
        total_sales = sum(float(order.total_price) for order in orders if order.total_price)
        orders_count = len(orders)
        avg_order_value = total_sales / orders_count if orders_count > 0 else 0

        # Get shop information
        shop = shopify.Shop.current()

        return {
            "store_id": store_id,
            "shop_name": shop.name,
            "shop_domain": shop.domain,
            "total_sales": round(total_sales, 2),
            "orders_count": orders_count,
            "avg_order_value": round(avg_order_value, 2),
            "currency": shop.currency,
            "success": True
        }
    except Exception as e:
        return {"error": f"Shopify analytics failed: {str(e)}", "store_id": store_id}

# 3a) List Shopify Products
def list_shopify_products(limit: int = 10) -> dict:
    """List products from Shopify store"""
    shopify_api_key = os.getenv("SHOPIFY_API_KEY")
    shopify_api_secret = os.getenv("SHOPIFY_API_SECRET")
    shopify_access_token = os.getenv("SHOPIFY_API_ACCESS_TOKEN")
    shopify_shop_url = os.getenv("SHOPIFY_SHOP_URL")

    if not all([shopify_api_key, shopify_api_secret, shopify_access_token, shopify_shop_url]):
        return {"error": "Shopify credentials not configured", "limit": limit}

    try:
        import shopify

        # Initialize Shopify session
        api_version = os.getenv("SHOPIFY_API_VERSION", "2023-10")
        shopify.Session.setup(api_key=shopify_api_key, secret=shopify_api_secret)
        session = shopify.Session(shopify_shop_url, api_version, shopify_access_token)
        shopify.ShopifyResource.activate_session(session)

        # Fetch products
        products = shopify.Product.find(limit=limit)
        product_list = []

        for product in products:
            product_data = {
                "id": product.id,
                "title": product.title,
                "handle": product.handle,
                "product_type": product.product_type,
                "vendor": product.vendor,
                "created_at": str(product.created_at),
                "updated_at": str(product.updated_at),
                "status": product.status,
                "variants": []
            }

            # Add variant information
            for variant in product.variants:
                variant_data = {
                    "id": variant.id,
                    "title": variant.title,
                    "price": variant.price,
                    "sku": variant.sku,
                    "inventory_quantity": variant.inventory_quantity
                }
                product_data["variants"].append(variant_data)

            product_list.append(product_data)

        return {
            "products": product_list,
            "count": len(product_list),
            "limit": limit,
            "success": True
        }
    except Exception as e:
        return {"error": f"Failed to list Shopify products: {str(e)}", "limit": limit}

# 3b) Create Shopify Product
def create_shopify_product(title: str, body_html: str, vendor: str, product_type: str, price: float) -> dict:
    """Create a new product in Shopify store"""
    shopify_api_key = os.getenv("SHOPIFY_API_KEY")
    shopify_api_secret = os.getenv("SHOPIFY_API_SECRET")
    shopify_access_token = os.getenv("SHOPIFY_API_ACCESS_TOKEN")
    shopify_shop_url = os.getenv("SHOPIFY_SHOP_URL")

    if not all([shopify_api_key, shopify_api_secret, shopify_access_token, shopify_shop_url]):
        return {"error": "Shopify credentials not configured", "title": title}

    try:
        import shopify

        # Initialize Shopify session
        api_version = os.getenv("SHOPIFY_API_VERSION", "2023-10")
        shopify.Session.setup(api_key=shopify_api_key, secret=shopify_api_secret)
        session = shopify.Session(shopify_shop_url, api_version, shopify_access_token)
        shopify.ShopifyResource.activate_session(session)

        # Create new product
        product = shopify.Product()
        product.title = title
        product.body_html = body_html
        product.vendor = vendor
        product.product_type = product_type

        # Create variant with price
        variant = shopify.Variant()
        variant.price = str(price)
        variant.inventory_management = "shopify"
        variant.inventory_quantity = 100  # Default inventory

        product.variants = [variant]

        # Save product
        if product.save():
            return {
                "title": title,
                "product_id": product.id,
                "handle": product.handle,
                "price": price,
                "vendor": vendor,
                "product_type": product_type,
                "success": True,
                "message": f"Product '{title}' created successfully"
            }
        else:
            return {
                "error": f"Failed to create product: {product.errors.full_messages()}",
                "title": title
            }
    except Exception as e:
        return {"error": f"Failed to create Shopify product: {str(e)}", "title": title}

# 4) Social Sentiment implementation
def fetch_social_sentiment(query: str) -> dict:
    """Fetch social sentiment via RapidAPI"""
    if not RAPIDAPI_KEY:
        return {"error": "RAPIDAPI_KEY not configured", "query": query}

    try:
        # Using a social sentiment API endpoint
        url = "https://twinword-sentiment-analysis.p.rapidapi.com/analyze/"
        headers = {
            "X-RapidAPI-Key": RAPIDAPI_KEY,
            "X-RapidAPI-Host": "twinword-sentiment-analysis.p.rapidapi.com"
        }
        params = {"text": query}

        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()
        return {
            "query": query,
            "sentiment": data.get("type", "neutral"),
            "score": data.get("score", 0),
            "success": True
        }
    except Exception as e:
        return {"error": f"Sentiment analysis failed: {str(e)}", "query": query}

# 5) Stripe Data implementation
def get_stripe_data(account_id: str) -> dict:
    """Get Stripe account data"""
    if not STRIPE_API_KEY:
        return {"error": "STRIPE_API_KEY not configured", "account_id": account_id}

    try:
        import stripe
        stripe.api_key = STRIPE_API_KEY

        balance = stripe.Balance.retrieve()
        charges = stripe.Charge.list(limit=10)

        return {
            "account_id": account_id,
            "balance": balance.available[0].amount if balance.available else 0,
            "currency": balance.available[0].currency if balance.available else "usd",
            "recent_charges": len(charges.data),
            "success": True
        }
    except Exception as e:
        return {"error": f"Stripe data failed: {str(e)}", "account_id": account_id}

# 6) PayPal Data implementation
def get_paypal_data(account_id: str) -> dict:
    """Get PayPal account data"""
    if not all([PAYPAL_CLIENT_ID, PAYPAL_CLIENT_SECRET]):
        return {"error": "PayPal credentials not configured", "account_id": account_id}

    try:
        # PayPal SDK implementation would go here
        # For now, return a placeholder structure
        return {
            "account_id": account_id,
            "balance": 0.0,
            "currency": "USD",
            "recent_transactions": 0,
            "success": True,
            "note": "PayPal SDK integration pending"
        }
    except Exception as e:
        return {"error": f"PayPal data failed: {str(e)}", "account_id": account_id}

# 7) Plaid Data implementation
def get_plaid_data(entity_id: str) -> dict:
    """Get Plaid banking data"""
    if not all([PLAID_CLIENT_ID, PLAID_SECRET]):
        return {"error": "Plaid credentials not configured", "entity_id": entity_id}

    try:
        # Plaid client implementation would go here
        # For now, return a placeholder structure
        return {
            "entity_id": entity_id,
            "accounts": [],
            "total_balance": 0.0,
            "success": True,
            "note": "Plaid SDK integration pending"
        }
    except Exception as e:
        return {"error": f"Plaid data failed: {str(e)}", "entity_id": entity_id}

# 8) SEO Content Generation
def generate_seo_content(topic: str) -> dict:
    """Generate SEO content using LLM"""
    if not OPENROUTER_API_KEY:
        return {"error": "OPENROUTER_API_KEY not configured", "topic": topic}

    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }

        prompt = f"Write a 500-word SEO-optimized article about {topic} with proper headings, keywords, and meta description."

        data = {
            "model": "openai/gpt-4",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7
        }

        response = requests.post("https://openrouter.ai/api/v1/chat/completions", 
                               headers=headers, json=data, timeout=30)
        response.raise_for_status()

        result = response.json()
        content = result["choices"][0]["message"]["content"]

        return {
            "topic": topic,
            "content": content,
            "word_count": len(content.split()),
            "success": True
        }
    except Exception as e:
        return {"error": f"SEO content generation failed: {str(e)}", "topic": topic}

# 9) Ad Creative Generation
def generate_ad_creative(brief: str) -> dict:
    """Generate ad creatives using LLM"""
    if not OPENROUTER_API_KEY:
        return {"error": "OPENROUTER_API_KEY not configured", "brief": brief}

    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }

        prompt = f"Create 3 Facebook ad headlines and descriptions for: {brief}. Format as JSON with headline and description for each."

        data = {
            "model": "openai/gpt-4",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.8
        }

        response = requests.post("https://openrouter.ai/api/v1/chat/completions", 
                               headers=headers, json=data, timeout=30)
        response.raise_for_status()

        result = response.json()
        content = result["choices"][0]["message"]["content"]

        return {
            "brief": brief,
            "ad_creatives": content,
            "success": True
        }
    except Exception as e:
        return {"error": f"Ad creative generation failed: {str(e)}", "brief": brief}

# 10) Social Media Posting
def post_social(platform: str, message: str) -> dict:
    """Post to social media via Buffer or Zapier webhook"""
    if not any([BUFFER_TOKEN, ZAPIER_WEBHOOK]):
        return {"error": "No social media credentials configured", "platform": platform}

    try:
        if ZAPIER_WEBHOOK:
            data = {"platform": platform, "message": message}
            response = requests.post(ZAPIER_WEBHOOK, json=data, timeout=10)
            response.raise_for_status()

            return {
                "platform": platform,
                "message": message[:50] + "...",
                "success": True,
                "method": "zapier"
            }
        else:
            return {
                "platform": platform,
                "message": message[:50] + "...",
                "success": True,
                "method": "buffer",
                "note": "Buffer integration pending"
            }
    except Exception as e:
        return {"error": f"Social posting failed: {str(e)}", "platform": platform}

# 11) SEO Agent
def seo_agent(task: str) -> dict:
    """SEO optimization agent"""
    if not OPENROUTER_API_KEY:
        return {"error": "OPENROUTER_API_KEY not configured", "task": task}

    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }

        prompt = f"As an SEO expert, provide optimization recommendations for: {task}"

        data = {
            "model": "openai/gpt-4",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3
        }

        response = requests.post("https://openrouter.ai/api/v1/chat/completions", 
                               headers=headers, json=data, timeout=30)
        response.raise_for_status()

        result = response.json()
        recommendations = result["choices"][0]["message"]["content"]

        return {
            "task": task,
            "recommendations": recommendations,
            "success": True
        }
    except Exception as e:
        return {"error": f"SEO agent failed: {str(e)}", "task": task}

# 12) Copy Agent
def copy_agent(prompt: str) -> dict:
    """Marketing copy generation agent"""
    if not OPENROUTER_API_KEY:
        return {"error": "OPENROUTER_API_KEY not configured", "prompt": prompt}

    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }

        system_prompt = f"As a professional copywriter, produce engaging marketing copy for: {prompt}"

        data = {
            "model": "openai/gpt-4",
            "messages": [{"role": "user", "content": system_prompt}],
            "temperature": 0.7
        }

        response = requests.post("https://openrouter.ai/api/v1/chat/completions", 
                               headers=headers, json=data, timeout=30)
        response.raise_for_status()

        result = response.json()
        copy_text = result["choices"][0]["message"]["content"]

        return {
            "prompt": prompt,
            "copy": copy_text,
            "success": True
        }
    except Exception as e:
        return {"error": f"Copy agent failed: {str(e)}", "prompt": prompt}

# 13) Product Agent
def product_agent(criteria: str) -> dict:
    """Product research and recommendation agent"""
    try:
        trends_data = fetch_google_trends(criteria)
        amazon_data = fetch_amazon_products(criteria)

        if not OPENROUTER_API_KEY:
            return {"error": "OPENROUTER_API_KEY not configured", "criteria": criteria}

        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }

        context = f"Trends: {trends_data}, Amazon Products: {amazon_data}"
        prompt = f"Based on this market data, suggest 3 profitable product ideas for: {criteria}. Context: {context}"

        data = {
            "model": "openai/gpt-4",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.6
        }

        response = requests.post("https://openrouter.ai/api/v1/chat/completions", 
                               headers=headers, json=data, timeout=30)
        response.raise_for_status()

        result = response.json()
        product_ideas = result["choices"][0]["message"]["content"]

        return {
            "criteria": criteria,
            "product_ideas": product_ideas,
            "trends_data": trends_data,
            "amazon_data": amazon_data,
            "success": True
        }
    except Exception as e:
        return {"error": f"Product agent failed: {str(e)}", "criteria": criteria}

# 14) Sentiment Analysis
def analyze_sentiment(text: str) -> dict:
    """Analyze sentiment using Cohere or fallback to OpenRouter"""
    if COHERE_KEY:
        try:
            import cohere
            co = cohere.Client(COHERE_KEY)
            response = co.classify(
                model='embed-english-v2.0',
                inputs=[text]
            )
            return {
                "text": text[:50] + "...",
                "sentiment": response.classifications[0].prediction,
                "confidence": response.classifications[0].confidence,
                "success": True
            }
        except Exception as e:
            pass

    # Fallback to OpenRouter
    if not OPENROUTER_API_KEY:
        return {"error": "No sentiment analysis API configured", "text": text[:50]}

    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }

        prompt = f"Analyze the sentiment of this text and return just 'positive', 'negative', or 'neutral': {text}"

        data = {
            "model": "openai/gpt-3.5-turbo",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.1
        }

        response = requests.post("https://openrouter.ai/api/v1/chat/completions", 
                               headers=headers, json=data, timeout=15)
        response.raise_for_status()

        result = response.json()
        sentiment = result["choices"][0]["message"]["content"].strip().lower()

        return {
            "text": text[:50] + "...",
            "sentiment": sentiment,
            "score": 0.8 if sentiment == "positive" else -0.8 if sentiment == "negative" else 0.0,
            "success": True
        }
    except Exception as e:
        return {"error": f"Sentiment analysis failed: {str(e)}", "text": text[:50]}

# 15) Psychology-adapted Copy
def adapt_copy_for_psychology(original: str) -> dict:
    """Adapt copy using psychological principles"""
    if not OPENROUTER_API_KEY:
        return {"error": "OPENROUTER_API_KEY not configured", "original": original[:50]}

    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }

        prompt = f"Rewrite this copy using scarcity, urgency, and reciprocity principles: {original}"

        data = {
            "model": "openai/gpt-4",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.6
        }

        response = requests.post("https://openrouter.ai/api/v1/chat/completions", 
                               headers=headers, json=data, timeout=30)
        response.raise_for_status()

        result = response.json()
        adapted_copy = result["choices"][0]["message"]["content"]

        return {
            "original": original,
            "adapted_copy": adapted_copy,
            "success": True
        }
    except Exception as e:
        return {"error": f"Copy adaptation failed: {str(e)}", "original": original[:50]}

# 16) Sales Forecasting
def forecast_sales(product_id: str) -> dict:
    """Forecast sales using Xano data"""
    try:
        url = f"{XANO_BASE_URL}/forecast_sales"
        params = {"product_id": product_id}

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()
        return {
            "product_id": product_id,
            "forecast": data,
            "success": True
        }
    except Exception as e:
        return {"error": f"Sales forecast failed: {str(e)}", "product_id": product_id}

# 17) Workflow Runner
def run_workflow(recipe_id: str) -> dict:
    """Run workflow via Zapier or HubSpot"""
    if not ZAPIER_WEBHOOK:
        return {"error": "ZAPIER_WEBHOOK not configured", "recipe_id": recipe_id}

    try:
        data = {"recipe_id": recipe_id, "action": "run_workflow"}
        response = requests.post(ZAPIER_WEBHOOK, json=data, timeout=15)
        response.raise_for_status()

        return {
            "recipe_id": recipe_id,
            "status": "running",
            "success": True
        }
    except Exception as e:
        return {"error": f"Workflow execution failed: {str(e)}", "recipe_id": recipe_id}

# 18) RL Feedback Loop
def rl_feedback_loop(metric: str) -> dict:
    """Reinforcement learning feedback loop"""
    if not OPENROUTER_API_KEY:
        return {"error": "OPENROUTER_API_KEY not configured", "metric": metric}

    try:
        # Placeholder for RL feedback implementation
        return {
            "metric": metric,
            "job_id": f"rl_{int(__import__('time').time())}",
            "status": "queued",
            "success": True,
            "note": "RL feedback loop simulation"
        }
    except Exception as e:
        return {"error": f"RL feedback failed: {str(e)}", "metric": metric}

# 20) Text Translation
def translate_text(text: str, target_lang: str) -> dict:
    """Translate text using OpenRouter LLM"""
    if not OPENROUTER_API_KEY:
        return {"error": "OPENROUTER_API_KEY not configured", "text": text[:50]}

    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }

        prompt = f"Translate this text to {target_lang}: {text}"

        data = {
            "model": "openai/gpt-3.5-turbo",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.1
        }

        response = requests.post("https://openrouter.ai/api/v1/chat/completions", 
                               headers=headers, json=data, timeout=20)
        response.raise_for_status()

        result = response.json()
        translated_text = result["choices"][0]["message"]["content"]

        return {
            "original_text": text,
            "target_language": target_lang,
            "translated_text": translated_text,
            "success": True
        }
    except Exception as e:
        return {"error": f"Translation failed: {str(e)}", "text": text[:50]}

# Create LangChain Tools
google_trends_langchain_tool = Tool(
    name="FetchGoogleTrends",
    func=fetch_google_trends,
    description="Fetch Google Trends data for a keyword (7-day timeframe)"
)

amazon_products_langchain_tool = Tool(
    name="FetchAmazonProducts",
    func=fetch_amazon_products,
    description="Search Amazon products by keyword via RapidAPI"
)

shopify_analytics_langchain_tool = Tool(
    name="FetchShopifyAnalytics",
    func=fetch_shopify_analytics,
    description="Get Shopify store analytics including sales, orders, and AOV"
)

social_sentiment_tool = Tool(
    name="FetchSocialSentiment",
    func=fetch_social_sentiment,
    description="Analyze social media sentiment for a query"
)

stripe_data_tool = Tool(
    name="GetStripeData",
    func=get_stripe_data,
    description="Get Stripe account balance and recent charges"
)

paypal_data_tool = Tool(
    name="GetPayPalData",
    func=get_paypal_data,
    description="Get PayPal account data and transactions"
)

plaid_data_tool = Tool(
    name="GetPlaidData",
    func=get_plaid_data,
    description="Get banking data via Plaid integration"
)

seo_content_tool = Tool(
    name="GenerateSEOContent",
    func=generate_seo_content,
    description="Generate SEO-optimized content for a given topic"
)

ad_creative_tool = Tool(
    name="GenerateAdCreative",
    func=generate_ad_creative,
    description="Generate Facebook ad headlines and descriptions"
)

social_posting_tool = Tool(
    name="PostSocial",
    func=lambda platform_message: post_social(*platform_message.split(',', 1)),
    description="Post to social media. Usage: PostSocial('facebook,Your message here')"
)

seo_agent_tool = Tool(
    name="SEOAgent",
    func=seo_agent,
    description="Get SEO optimization recommendations for a task"
)

copy_agent_tool = Tool(
    name="CopyAgent",
    func=copy_agent,
    description="Generate marketing copy for a given prompt"
)

product_agent_tool = Tool(
    name="ProductAgent",
    func=product_agent,
    description="Research and suggest profitable product ideas based on criteria"
)

sentiment_analysis_tool = Tool(
    name="AnalyzeSentiment",
    func=analyze_sentiment,
    description="Analyze sentiment of text using AI"
)

psychology_copy_tool = Tool(
    name="AdaptCopyForPsychology",
    func=adapt_copy_for_psychology,
    description="Adapt copy using psychological principles like scarcity and urgency"
)

sales_forecast_tool = Tool(
    name="ForecastSales",
    func=forecast_sales,
    description="Forecast sales for a product using historical data"
)

workflow_runner_tool = Tool(
    name="RunWorkflow",
    func=run_workflow,
    description="Execute a workflow by recipe ID via Zapier"
)

rl_feedback_tool = Tool(
    name="RLFeedbackLoop",
    func=rl_feedback_loop,
    description="Submit metric for reinforcement learning feedback"
)

translation_tool = Tool(
    name="TranslateText",
    func=lambda text_lang: translate_text(*text_lang.split(',', 1)),
    description="Translate text to target language. Usage: TranslateText('Hello world,spanish')"
)

# New Shopify Tools
shopify_list_tool = Tool(
    name="ListShopifyProducts",
    func=lambda limit_str="10": list_shopify_products(int(limit_str)),
    description="List products from your Shopify store. Usage: ListShopifyProducts('10')"
)

shopify_create_tool = Tool(
    name="CreateShopifyProduct",
    func=lambda params: create_shopify_product(*params.split('|')),
    description="Create a new Shopify product. Usage: CreateShopifyProduct('Title|<p>Description</p>|Vendor|Type|9.99')"
)

# === PAYMENT PROCESSING TOOLS ===
from payment_processor import StripeProcessor, GumroadProcessor, log_profit_to_xano
from meta_ads import MetaAdsManager, auto_launch_ads_if_ready

def create_stripe_product(params):
    """Create Stripe product. Format: 'name|description|price'"""
    try:
        name, description, price = params.split('|')
        return StripeProcessor.create_product(name, description, float(price))
    except Exception as e:
        return {"success": False, "error": str(e)}

def get_stripe_payments(limit="10"):
    """Get recent Stripe payments"""
    try:
        return StripeProcessor.get_payments(int(limit))
    except Exception as e:
        return [{"error": str(e)}]

def create_stripe_checkout(params):
    """Create Stripe checkout. Format: 'price_id|success_url|cancel_url'"""
    try:
        price_id, success_url, cancel_url = params.split('|')
        return StripeProcessor.create_checkout_session(price_id, success_url, cancel_url)
    except Exception as e:
        return {"success": False, "error": str(e)}

def check_meta_ads_status():
    """Check if Meta ads are ready to launch"""
    manager = MetaAdsManager()
    return manager.check_app_status()

def launch_ads_auto():
    """Automatically launch ads if conditions are met"""
    return auto_launch_ads_if_ready()

def log_manual_profit(params):
    """Log manual profit. Format: 'source|amount'"""
    try:
        source, amount = params.split('|')
        success = log_profit_to_xano(source, float(amount))
        return {"success": success, "source": source, "amount": float(amount)}
    except Exception as e:
        return {"success": False, "error": str(e)}

# LangChain Tools for Payment Processing
stripe_product_tool = Tool(
    name="CreateStripeProduct",
    func=create_stripe_product,
    description="Create a new Stripe product. Usage: CreateStripeProduct('Product Name|Product Description|29.99')"
)

stripe_payments_tool = Tool(
    name="GetStripePayments",
    func=get_stripe_payments,
    description="Get recent Stripe payments. Usage: GetStripePayments('10')"
)

stripe_checkout_tool = Tool(
    name="CreateStripeCheckout",
    func=create_stripe_checkout,
    description="Create Stripe checkout session. Usage: CreateStripeCheckout('price_id|success_url|cancel_url')"
)

meta_status_tool = Tool(
    name="CheckMetaAdsStatus",
    func=lambda _: check_meta_ads_status(),
    description="Check if Meta ads app is approved and ready for campaigns"
)

launch_ads_tool = Tool(
    name="LaunchAdsAuto",
    func=lambda _: launch_ads_auto(),
    description="Automatically launch ad campaigns if budget and approval conditions are met"
)

profit_logger_tool = Tool(
    name="LogProfit",
    func=log_manual_profit,
    description="Log profit manually. Usage: LogProfit('stripe|45.99')"
)

# All available tools (original + new implementations)
tools = [
    google_trends_tool,
    related_queries_tool,
    trending_searches_tool,
    market_data_tool,
    amazon_bestsellers_tool,
    amazon_search_tool,
    amazon_products_tool,
    list_products_tool,
    create_product_tool,
    shopify_analytics_tool,
    shopify_products_tool,
    shopify_health_tool,
    create_store_tool,
    store_builder_tool,
    risk_check_tool,
    compliance_check_tool,
    # New implemented tools
    google_trends_langchain_tool,
    amazon_products_langchain_tool,
    shopify_analytics_langchain_tool,
    social_sentiment_tool,
    stripe_data_tool,
    paypal_data_tool,
    plaid_data_tool,
    seo_content_tool,
    ad_creative_tool,
    social_posting_tool,
    seo_agent_tool,
    copy_agent_tool,
    product_agent_tool,
    sentiment_analysis_tool,
    psychology_copy_tool,
    sales_forecast_tool,
    workflow_runner_tool,
    rl_feedback_tool,
    translation_tool,
    shopify_list_tool,
    shopify_create_tool,
    stripe_product_tool,
    stripe_payments_tool,
    stripe_checkout_tool,
    meta_status_tool,
    launch_ads_tool,
    profit_logger_tool
]

def get_all_tools():
    """Return all available tools"""
    return tools

def get_tool_names():
    """Return list of all tool names"""
    return [tool.name for tool in tools]

def get_tool_by_name(name: str):
    """Get a specific tool by name"""
    for tool in tools:
        if tool.name == name:
            return tool
    return None

# Test function
if __name__ == "__main__":
    print("🔧 Testing implemented tools...")

    # Test a few key functions
    print("\n1. Testing Google Trends...")
    result = fetch_google_trends("AI business")
    print(f"Result: {result}")

    print("\n2. Testing Amazon Products...")
    result = fetch_amazon_products("wireless earbuds")
    print(f"Result: {result}")

    print("\n3. Testing SEO Content...")
    result = generate_seo_content("AI productivity tools")
    print(f"Result: {result}")

    print(f"\n✅ Total tools available: {len(tools)}")
    print("Tool names:", [tool.name for tool in tools])