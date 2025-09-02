
import os
import requests
from config import get_openrouter_config

def generate_ad_copy(product_info, platform="facebook"):
    """Generate ad copy for different platforms"""
    try:
        config = get_openrouter_config()
        
        if not config.get("api_key"):
            return generate_fallback_ads(product_info, platform)
        
        prompt = f"""
        Create {platform} ad copy for this product:
        
        Product: {product_info.get('title', 'Digital Product')}
        Description: {product_info.get('description', 'Premium digital product')}
        Price: ${product_info.get('price', 29.99)}
        Platform: {platform}
        
        Generate:
        - Headline (attention-grabbing)
        - Body text (benefits-focused)
        - Call to action (action-oriented)
        
        Optimize for {platform} best practices.
        """
        
        headers = {
            "Authorization": f"Bearer {config['api_key']}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": config.get("model", "anthropic/claude-3-opus"),
            "messages": [{"role": "user", "content": prompt}]
        }
        
        response = requests.post(f"{config['base_url']}/chat/completions", 
                               headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            return {"success": True, "ad_copy": content}
        else:
            return generate_fallback_ads(product_info, platform)
            
    except Exception as e:
        return generate_fallback_ads(product_info, platform)

def generate_fallback_ads(product_info, platform):
    """Fallback ad templates when API unavailable"""
    title = product_info.get('title', 'Digital Product')
    price = product_info.get('price', 29.99)
    
    if platform.lower() == "facebook":
        return {
            "success": True,
            "ad_copy": {
                "headline": f"🚀 {title} - Transform Your Business Today",
                "body": f"Stop struggling with outdated methods. {title} gives you everything you need to succeed. Join thousands of satisfied customers. Limited time: only ${price}!",
                "cta": "Get Instant Access"
            }
        }
    elif platform.lower() == "google":
        return {
            "success": True,
            "ad_copy": {
                "headline": f"{title} | Official Site",
                "body": f"Get {title} now. Proven results. 30-day guarantee. Starting at ${price}.",
                "cta": "Shop Now"
            }
        }
    else:
        return {
            "success": True,
            "ad_copy": {
                "headline": f"Discover {title}",
                "body": f"Revolutionary {title} - perfect for ambitious professionals. Only ${price}.",
                "cta": "Learn More"
            }
        }
