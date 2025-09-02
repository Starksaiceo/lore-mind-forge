
import time
import random
from datetime import datetime
from agent_session import create_user_session
from marketplace_uploader import upload_product_to_shopify
import requests
import os

def pick_products(niche, count=3):
    """Generate product ideas for a niche"""
    product_templates = {
        "fitness": [
            {"type": "ebook", "title": "30-Day Fitness Challenge Guide", "price": 29.99},
            {"type": "course", "title": "Home Workout Mastery", "price": 79.99},
            {"type": "template", "title": "Meal Planning Templates", "price": 19.99}
        ],
        "business": [
            {"type": "ebook", "title": "AI Business Automation Guide", "price": 49.99},
            {"type": "course", "title": "SaaS Launch Blueprint", "price": 199.99},
            {"type": "template", "title": "Business Plan Templates", "price": 39.99}
        ],
        "productivity": [
            {"type": "ebook", "title": "The Ultimate Productivity System", "price": 24.99},
            {"type": "course", "title": "Time Management Mastery", "price": 89.99},
            {"type": "template", "title": "Goal Setting Worksheets", "price": 14.99}
        ]
    }
    
    if niche.lower() in product_templates:
        return product_templates[niche.lower()][:count]
    
    # Generate custom products for any niche
    return [
        {"type": "ebook", "title": f"{niche.title()} Mastery Guide", "price": 39.99},
        {"type": "course", "title": f"Complete {niche.title()} Course", "price": 129.99},
        {"type": "template", "title": f"{niche.title()} Templates & Tools", "price": 24.99}
    ]

def generate_store_assets(niche):
    """Generate store assets like descriptions and marketing copy"""
    assets = {
        "store_name": f"{niche.title()} Pro",
        "tagline": f"Your ultimate destination for {niche} success",
        "about": f"We specialize in providing high-quality {niche} resources, courses, and tools to help you achieve your goals faster.",
        "logo_text": f"{niche.title()}Pro",
        "colors": {
            "primary": random.choice(["#3b82f6", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6"]),
            "secondary": "#f3f4f6"
        }
    }
    return assets

def write_ad_strategy(niche):
    """Generate ad strategy for the niche"""
    strategies = {
        "facebook": [
            f"Target {niche} enthusiasts aged 25-45",
            f"Use video content showcasing {niche} results",
            f"Retarget website visitors with {niche} testimonials",
            f"Create lookalike audiences from {niche} customers"
        ],
        "google": [
            f"Target '{niche} guide' and '{niche} course' keywords",
            f"Use ad extensions highlighting {niche} benefits",
            f"Create separate campaigns for beginner and advanced {niche}",
            f"Implement dynamic remarketing for {niche} products"
        ]
    }
    return strategies

def create_shopify_store(products, assets, user_id):
    """Create/update Shopify store with products"""
    session = create_user_session(user_id)
    results = []
    
    session.append_event("business_generation_started", {
        "niche": assets["store_name"],
        "product_count": len(products)
    })
    
    for product in products:
        # Enhanced product data
        product_data = {
            "title": product["title"],
            "description": f"Professional {product['type']} designed to help you master {assets['store_name'].lower()}. Includes step-by-step guidance, practical exercises, and proven strategies.",
            "price": product["price"],
            "body_html": f"""
            <h2>Transform Your {assets['store_name']} Journey</h2>
            <p>This comprehensive {product['type']} provides everything you need to succeed:</p>
            <ul>
                <li>✅ Step-by-step instructions</li>
                <li>✅ Real-world examples</li>
                <li>✅ Downloadable resources</li>
                <li>✅ 30-day money-back guarantee</li>
            </ul>
            <p><strong>Start your transformation today!</strong></p>
            """,
            "vendor": assets["store_name"],
            "product_type": product["type"].title(),
            "tags": f"{assets['store_name'].lower()}, {product['type']}, digital, instant download"
        }
        
        # Upload to Shopify
        upload_result = upload_product_to_shopify(product_data)
        results.append({
            "product": product,
            "upload_result": upload_result,
            "success": upload_result.get("success", False)
        })
        
        if upload_result.get("success"):
            session.append_event("product_created", {
                "title": product["title"],
                "price": product["price"],
                "platform": "shopify",
                "niche": assets["store_name"]
            })
        
        time.sleep(1)  # Rate limiting
    
    session.append_event("business_generation_completed", {
        "total_products": len(products),
        "successful_uploads": sum(1 for r in results if r["success"]),
        "store_assets": assets
    })
    
    return results

def run_one_click_generator(niche, user_id, pdf_content=None):
    """Main 1-click business generator function"""
    start_time = time.time()
    session = create_user_session(user_id)
    
    progress = []
    
    # Step 1: Generate products
    progress.append("🎯 Generating product ideas...")
    products = pick_products(niche)
    progress.append(f"✅ Generated {len(products)} products")
    
    # Step 2: Create store assets
    progress.append("🎨 Creating store assets...")
    assets = generate_store_assets(niche)
    progress.append("✅ Store branding created")
    
    # Step 3: Write marketing strategy
    progress.append("📢 Developing marketing strategy...")
    ad_strategy = write_ad_strategy(niche)
    progress.append("✅ Marketing strategy ready")
    
    # Step 4: Create Shopify store
    progress.append("🛒 Setting up Shopify store...")
    store_results = create_shopify_store(products, assets, user_id)
    successful_uploads = sum(1 for r in store_results if r["success"])
    progress.append(f"✅ Store created with {successful_uploads}/{len(products)} products")
    
    end_time = time.time()
    duration = end_time - start_time
    
    # Log final result
    session.append_event("one_click_business_generated", {
        "niche": niche,
        "duration_seconds": round(duration, 2),
        "products_created": successful_uploads,
        "total_products": len(products),
        "success_rate": round(successful_uploads / len(products) * 100, 1)
    })
    
    return {
        "success": True,
        "duration": round(duration, 2),
        "niche": niche,
        "products": products,
        "assets": assets,
        "ad_strategy": ad_strategy,
        "store_results": store_results,
        "successful_uploads": successful_uploads,
        "progress": progress,
        "summary": f"✅ Business created in {duration:.1f}s: {successful_uploads} products live on Shopify!"
    }

def generate_business_from_pdf(pdf_content, user_id):
    """Generate business from uploaded PDF content"""
    # Analyze PDF content to extract niche
    # This is a simplified version - you'd use AI to analyze the PDF
    
    keywords = ["fitness", "business", "productivity", "marketing", "health"]
    detected_niche = "business"  # Default
    
    for keyword in keywords:
        if keyword in pdf_content.lower():
            detected_niche = keyword
            break
    
    return run_one_click_generator(detected_niche, user_id, pdf_content)
