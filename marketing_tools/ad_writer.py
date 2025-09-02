import os
import json
from typing import Dict, Any, List
from datetime import datetime
import requests
from config import OPENROUTER_API_KEY

def generate_ad_copy(product_info: Dict[str, Any], platform: str = "facebook") -> Dict[str, Any]:
    """Generate ad copy for specific platform"""
    try:
        # Ensure product_info is a proper dictionary
        if not isinstance(product_info, dict):
            product_info = {}

        platform_specs = get_platform_specs(platform)

        # Check if API key is available
        if not OPENROUTER_API_KEY:
            print("⚠️ No API key available, using fallback ads")
            return create_fallback_ads(product_info, platform)

        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }

        # Safely extract product information
        title = str(product_info.get('title', 'Digital Product'))
        description = str(product_info.get('description', 'High-value digital product'))
        price = product_info.get('price', 97)
        audience = str(product_info.get('audience', 'entrepreneurs and business owners'))

        prompt = f"""Create high-converting ad copy for {platform.title()} for this product:

Product: {title}
Description: {description}
Price: ${price}
Target Audience: {audience}

Platform Requirements:
- Headline: {platform_specs['headline_limit']} characters max
- Body Text: {platform_specs['body_limit']} characters max
- CTA: {platform_specs['cta_limit']} characters max
- Style: {platform_specs['style']}

Create 3 variations of ad copy that:
1. Focus on benefits over features
2. Include social proof elements
3. Create urgency/scarcity
4. Have clear call-to-action
5. Match {platform} best practices

Format as JSON with headline, body, cta, and variation_name for each."""

        payload = {
            "model": "openai/gpt-3.5-turbo",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 1500,
            "temperature": 0.8
        }

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )

        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']

            try:
                # Extract JSON from response
                start_idx = content.find('[')
                end_idx = content.rfind(']') + 1
                if start_idx != -1 and end_idx != -1:
                    json_str = content[start_idx:end_idx]
                    ad_variations = json.loads(json_str)

                    # Ensure we have a list of properly formatted ads
                    if isinstance(ad_variations, list) and len(ad_variations) > 0:
                        # Take only first 3 variations
                        final_variations = ad_variations[:3]
                    else:
                        final_variations = create_fallback_ads(product_info, platform)["variations"]
                else:
                    final_variations = create_fallback_ads(product_info, platform)["variations"]

                return {
                    "platform": platform,
                    "product": title,
                    "variations": final_variations,
                    "platform_specs": platform_specs,
                    "created_at": datetime.now().isoformat()
                }

            except (json.JSONDecodeError, KeyError, TypeError) as e:
                print(f"⚠️ JSON parsing error: {e}, using fallback")
                return create_fallback_ads(product_info, platform)

        else:
            print(f"❌ Ad generation failed: {response.status_code}")
            return create_fallback_ads(product_info, platform)

    except Exception as e:
        print(f"❌ Ad copy generation error: {e}")
        return create_fallback_ads(product_info, platform)

def get_platform_specs(platform: str) -> Dict[str, Any]:
    """Get platform-specific requirements"""
    specs = {
        "facebook": {
            "headline_limit": 40,
            "body_limit": 125,
            "cta_limit": 20,
            "style": "conversational, benefit-focused",
            "image_ratio": "1:1 or 16:9"
        },
        "instagram": {
            "headline_limit": 40,
            "body_limit": 125,
            "cta_limit": 20,
            "style": "visual, lifestyle-focused",
            "image_ratio": "1:1 or 4:5"
        },
        "google": {
            "headline_limit": 30,
            "body_limit": 90,
            "cta_limit": 15,
            "style": "direct, search-intent focused",
            "image_ratio": "1.91:1"
        },
        "linkedin": {
            "headline_limit": 50,
            "body_limit": 150,
            "cta_limit": 25,
            "style": "professional, B2B focused",
            "image_ratio": "1.91:1"
        },
        "twitter": {
            "headline_limit": 280,
            "body_limit": 280,
            "cta_limit": 20,
            "style": "concise, trending hashtags",
            "image_ratio": "16:9"
        }
    }

    return specs.get(platform.lower(), specs["facebook"])

def create_fallback_ads(product_info: Dict[str, Any], platform: str) -> Dict[str, Any]:
    """Create fallback ad copy when AI fails"""
    # Safely handle product_info
    if not isinstance(product_info, dict):
        product_info = {}

    title = str(product_info.get('title', 'Digital Product'))
    price = product_info.get('price', 97)
    platform_specs = get_platform_specs(platform)

    # Truncate title if too long for headlines
    short_title = title[:20] + "..." if len(title) > 23 else title

    variations = [
        {
            "variation_name": "Benefit-Focused",
            "headline": f"Transform Your Business with {short_title}",
            "body": f"Discover the proven system that's helping thousands achieve breakthrough results. Get started for just ${price}.",
            "cta": "Get Started Now"
        },
        {
            "variation_name": "Social Proof",
            "headline": f"Join 10,000+ Success Stories",
            "body": f"See why customers love {short_title}. Real results, real testimonials, real transformation. Limited time offer.",
            "cta": "Join Today"
        },
        {
            "variation_name": "Urgency",
            "headline": f"Last Chance: {short_title} Special Price",
            "body": f"Don't miss out! Special pricing ends soon. Get everything you need to succeed for just ${price}.",
            "cta": "Claim Offer"
        }
    ]

    return {
        "platform": platform,
        "product": title,
        "variations": variations,
        "platform_specs": platform_specs,
        "created_at": datetime.now().isoformat()
    }

def get_supported_platforms() -> List[Dict[str, Any]]:
    """Get list of supported advertising platforms"""
    return [
        {"name": "Facebook", "id": "facebook", "description": "Facebook News Feed ads"},
        {"name": "Instagram", "id": "instagram", "description": "Instagram feed and stories"},
        {"name": "Google Ads", "id": "google", "description": "Google Search and Display"},
        {"name": "LinkedIn", "id": "linkedin", "description": "LinkedIn professional network"},
        {"name": "Twitter", "id": "twitter", "description": "Twitter promoted tweets"}
    ]

def save_ad_copy(user_id: int, ad_data: Dict, product_name: str) -> str:
    """Save ad copy to file"""
    try:
        os.makedirs("content_ready_to_post", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        filename = f"content_ready_to_post/ads_{product_name}_{ad_data['platform']}_{timestamp}.json"

        with open(filename, 'w') as f:
            json.dump({
                "user_id": user_id,
                "product_name": product_name,
                "created_at": datetime.now().isoformat(),
                "ad_data": ad_data
            }, f, indent=2)

        print(f"📱 Ad copy saved: {filename}")
        return filename

    except Exception as e:
        print(f"❌ Ad copy save failed: {e}")
        return ""

def generate_multi_platform_ads(product_info: Dict[str, Any]) -> Dict[str, Any]:
    """Generate ad copy for multiple platforms"""
    platforms = ["facebook", "instagram", "google", "linkedin"]
    results = {}

    for platform in platforms:
        print(f"🎯 Generating {platform} ads...")
        results[platform] = generate_ad_copy(product_info, platform)

    return {
        "product": product_info.get('title', 'Product'),
        "platforms": results,
        "created_at": datetime.now().isoformat(),
        "total_variations": sum(len(data.get('variations', [])) for data in results.values())
    }

# Export functions
__all__ = ['generate_ad_copy', 'get_supported_platforms', 'save_ad_copy', 'generate_multi_platform_ads']