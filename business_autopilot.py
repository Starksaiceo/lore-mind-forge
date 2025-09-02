
import os, json, asyncio, httpx
from typing import Dict, List
from datetime import datetime
from db_autopilot import record_activity, record_business, update_last_autopilot_run
from llm_autopilot import generate_business_ideas, validate_and_rank_ideas, create_product_copy
from agent_session import AgentSession

# Shopify integration
SHOPIFY_TOKEN = os.getenv("SHOPIFY_ACCESS_TOKEN")
SHOPIFY_DOMAIN = os.getenv("SHOPIFY_STORE_DOMAIN")  # e.g., myshop.myshopify.com

async def create_shopify_product(user_id: int, title: str, description: str, price: float = 19.0) -> Dict:
    """Create product on Shopify or simulate if no credentials"""
    if not (SHOPIFY_TOKEN and SHOPIFY_DOMAIN):
        # Simulate product creation
        simulated_id = f"sim_{int(datetime.now().timestamp())}"
        record_activity(user_id, "build", f"(Simulated) Created product: {title} @ ${price}", None, 
                       json.dumps({"title": title, "price": price, "simulated": True}))
        record_business(user_id, title, "shopify_simulated", simulated_id, 
                       json.dumps({"price": price, "simulated": True}))
        return {
            "success": True,
            "simulated": True, 
            "product_id": simulated_id,
            "title": title, 
            "price": price
        }

    # Real Shopify product creation
    url = f"https://{SHOPIFY_DOMAIN}/admin/api/2024-07/products.json"
    payload = {
        "product": {
            "title": title,
            "body_html": description,
            "variants": [{"price": str(price)}],
            "status": "active",
            "product_type": "Digital Product",
            "tags": "AI Generated, Autopilot"
        }
    }
    headers = {
        "X-Shopify-Access-Token": SHOPIFY_TOKEN, 
        "Content-Type": "application/json"
    }

    try:
        async with httpx.AsyncClient(timeout=90) as client:
            r = await client.post(url, headers=headers, json=payload)
            r.raise_for_status()
            data = r.json()
            
        product_id = str(data["product"]["id"])
        product_url = f"https://{SHOPIFY_DOMAIN.replace('.myshopify.com', '')}.myshopify.com/products/{data['product']['handle']}"
        
        record_activity(user_id, "build", f"Created Shopify product: {title} (ID: {product_id})", None, 
                       json.dumps({"product_id": product_id, "url": product_url}))
        record_business(user_id, title, "shopify", product_id, 
                       json.dumps({"price": price, "url": product_url}))
        
        return {
            "success": True,
            "product_id": product_id,
            "title": title,
            "url": product_url
        }
        
    except Exception as e:
        error_msg = f"Shopify API error: {str(e)}"
        record_activity(user_id, "error", error_msg)
        return {"success": False, "error": error_msg}

async def run_profit_cycle(user_id: int, user_email: str = "") -> Dict:
    """Run a complete profit cycle for user"""
    try:
        print(f"🤖 Starting profit cycle for user {user_id} ({user_email})")
        
        # Get user context from agent session
        try:
            session = AgentSession(user_id)
            user_context = f"User goals: {session.get_memory('goals', 'general business growth')}"
        except:
            user_context = ""
        
        # Step 1: Generate ideas
        print(f"💡 Generating business ideas for user {user_id}")
        ideas = await generate_business_ideas(user_context)
        if not ideas:
            record_activity(user_id, "error", "Failed to generate business ideas")
            return {"success": False, "error": "No ideas generated"}
        
        record_activity(user_id, "ideation", f"Generated {len(ideas)} business ideas", None,
                       json.dumps({"ideas": ideas}))
        
        # Step 2: Validate and select best idea
        print(f"🎯 Validating ideas for user {user_id}")
        validation = await validate_and_rank_ideas(ideas)
        best_idea = validation["best_idea"]
        
        record_activity(user_id, "validation", f"Selected: {best_idea}", None,
                       json.dumps(validation))
        
        # Step 3: Create product copy
        print(f"✍️ Creating product copy for user {user_id}")
        copy = await create_product_copy(best_idea, 19.0)
        
        record_activity(user_id, "copywriting", f"Created copy for: {copy['title']}")
        
        # Step 4: Build/publish product
        print(f"🚀 Creating product for user {user_id}")
        result = await create_shopify_product(user_id, copy["title"], copy["description"], copy["price"])
        
        if result["success"]:
            record_activity(user_id, "launch", f"Launched: {result['title']}", None,
                           json.dumps(result))
            print(f"✅ Successfully completed profit cycle for user {user_id}")
        else:
            record_activity(user_id, "error", f"Launch failed: {result.get('error', 'Unknown error')}")
            print(f"❌ Profit cycle failed for user {user_id}: {result.get('error')}")
        
        # Update last run timestamp
        update_last_autopilot_run(user_id)
        
        return {
            "success": result["success"],
            "idea": best_idea,
            "product": copy,
            "result": result
        }
        
    except Exception as e:
        error_msg = f"Profit cycle error: {str(e)}"
        record_activity(user_id, "error", error_msg)
        print(f"❌ Exception in profit cycle for user {user_id}: {e}")
        return {"success": False, "error": error_msg}

async def run_batch_cycles(user_list: List[Dict], max_concurrent: int = 3):
    """Run profit cycles for multiple users with concurrency control"""
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async def run_single_cycle(user_data):
        async with semaphore:
            return await run_profit_cycle(user_data["id"], user_data.get("email", ""))
    
    # Run cycles with controlled concurrency
    tasks = [run_single_cycle(user) for user in user_list]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    return results
