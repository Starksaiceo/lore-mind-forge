
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import re
from llm_helper import get_llm_client

def generate_social_calendar(user_id: int, niches: List[str], cadence: str = "daily") -> Dict[str, Any]:
    """Generate a 14-day social media content calendar"""
    try:
        llm = get_llm_client()
        
        # Calculate days needed
        days = 14 if cadence == "daily" else 7
        
        prompt = f"""Create a {days}-day social media content calendar for these niches: {', '.join(niches)}.

Return JSON format:
{{
  "calendar": [
    {{
      "day": 1,
      "date": "2025-01-01",
      "posts": [
        {{
          "hook": "Mind-blowing tip",
          "angle": "Educational",
          "cta": "Save this post",
          "topic": "Specific topic",
          "platforms": ["instagram", "tiktok", "x"]
        }}
      ]
    }}
  ]
}}

Focus on engaging, shareable content that drives traffic to products. Include educational, entertaining, and promotional mix."""

        response = llm.complete(prompt, task_hint="content generation", complexity="medium")
        
        try:
            calendar_data = json.loads(response)
        except json.JSONDecodeError:
            # Fallback structure
            calendar_data = {
                "calendar": [
                    {
                        "day": i+1,
                        "date": (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d"),
                        "posts": [{
                            "hook": f"Day {i+1} insight",
                            "angle": "Educational",
                            "cta": "Learn more",
                            "topic": niches[0] if niches else "business",
                            "platforms": ["instagram", "x", "tiktok"]
                        }]
                    } for i in range(days)
                ]
            }
        
        return {
            "success": True,
            "calendar": calendar_data,
            "user_id": user_id,
            "generated_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}

def write_social_post(user_id: int, idea: Dict[str, Any], format: str) -> Dict[str, Any]:
    """Write social media post based on idea and format"""
    try:
        llm = get_llm_client()
        
        prompt = f"""Write a {format} social media post based on this idea:
Hook: {idea.get('hook', 'Unknown')}
Angle: {idea.get('angle', 'Unknown')}
Topic: {idea.get('topic', 'Unknown')}
CTA: {idea.get('cta', 'Unknown')}

Format requirements:
- Instagram: 1-2 paragraphs, engaging, visual-focused
- TikTok: Short, punchy, trend-aware
- X (Twitter): Concise, thread-worthy, engaging
- LinkedIn: Professional, value-driven

Return JSON:
{{
  "copy": "Main post text",
  "title": "Optional title/headline",
  "hashtags": ["#relevant", "#hashtags"],
  "cta": "Clear call to action",
  "link_placeholder": "{{PRODUCT_LINK}}"
}}

Keep content brand-safe and engaging."""

        response = llm.complete(prompt, task_hint="content generation", complexity="medium")
        
        try:
            post_data = json.loads(response)
        except json.JSONDecodeError:
            # Fallback
            post_data = {
                "copy": f"Exciting {format} content about {idea.get('topic', 'business')}",
                "title": idea.get('hook', 'Great insight'),
                "hashtags": ["#business", "#ai", "#productivity"],
                "cta": idea.get('cta', 'Learn more'),
                "link_placeholder": "{PRODUCT_LINK}"
            }
        
        # Apply safety filter
        post_data["copy"] = safety_filter(post_data["copy"])
        
        return {
            "success": True,
            "post": post_data,
            "format": format,
            "user_id": user_id
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}

def make_variations(user_id: int, base_post: Dict[str, Any], n: int = 5) -> Dict[str, Any]:
    """Generate A/B test variations of a post"""
    try:
        llm = get_llm_client()
        
        prompt = f"""Create {n} variations of this social media post:
Original: {base_post.get('copy', '')}

Generate variations with different:
- Lengths (short, medium, long)
- Tones (professional, casual, humorous, urgent)
- Hooks (question, statement, story, statistic)

Return JSON:
{{
  "variations": [
    {{
      "copy": "Variation text",
      "tone": "humorous",
      "length": "short",
      "hook_type": "question"
    }}
  ]
}}"""

        response = llm.complete(prompt, task_hint="content generation", complexity="medium")
        
        try:
            variations_data = json.loads(response)
        except json.JSONDecodeError:
            # Fallback variations
            variations_data = {
                "variations": [
                    {"copy": f"Variation {i+1}: " + base_post.get('copy', '')[:100], 
                     "tone": ["professional", "casual", "humorous"][i % 3],
                     "length": ["short", "medium", "long"][i % 3],
                     "hook_type": ["question", "statement", "story"][i % 3]}
                    for i in range(n)
                ]
            }
        
        # Apply safety filter to all variations
        for var in variations_data["variations"]:
            var["copy"] = safety_filter(var["copy"])
        
        return {
            "success": True,
            "variations": variations_data["variations"],
            "user_id": user_id
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}

def write_ad_copy(user_id: int, product: Dict[str, Any], objective: str) -> Dict[str, Any]:
    """Generate advertising copy for a product"""
    try:
        llm = get_llm_client()
        
        prompt = f"""Create advertising copy for this product:
Product: {product.get('title', 'Unknown')}
Description: {product.get('description', 'No description')}
Price: ${product.get('price', 0)}
Objective: {objective}

Return JSON:
{{
  "headline": "Main headline",
  "primary_text": "Primary ad text",
  "cta": "Call to action button text",
  "descriptions": ["Short description 1", "Short description 2"],
  "hooks": [
    "Hook 1 - attention grabbing",
    "Hook 2 - benefit focused",
    "Hook 3 - urgency",
    "Hook 4 - social proof",
    "Hook 5 - curiosity"
  ]
}}

Focus on benefits, urgency, and clear value proposition."""

        response = llm.complete(prompt, task_hint="content generation", complexity="medium")
        
        try:
            ad_data = json.loads(response)
        except json.JSONDecodeError:
            # Fallback ad copy
            ad_data = {
                "headline": f"Transform Your {product.get('title', 'Business')}",
                "primary_text": f"Discover {product.get('title', 'this amazing product')} - {product.get('description', 'the solution you need')}",
                "cta": "Get Started Now",
                "descriptions": [
                    f"Get {product.get('title', 'this product')} today",
                    f"Transform your results with {product.get('title', 'our solution')}"
                ],
                "hooks": [
                    "Ready to transform your business?",
                    "Stop struggling with manual processes",
                    "Limited time offer",
                    "Join thousands of satisfied customers",
                    "What if you could automate everything?"
                ]
            }
        
        # Apply safety filter
        for key in ["headline", "primary_text", "cta"]:
            if key in ad_data:
                ad_data[key] = safety_filter(ad_data[key])
        
        return {
            "success": True,
            "ad_copy": ad_data,
            "product_id": product.get('id'),
            "user_id": user_id
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}

def make_caption_pack(user_id: int, tone: str = "funny") -> Dict[str, Any]:
    """Generate a pack of captions with specific tone"""
    try:
        llm = get_llm_client()
        
        prompt = f"""Generate 10 social media captions with a {tone} tone.

Captions should be:
- Platform-safe and brand-friendly
- Engaging and shareable
- Include relevant hashtags
- Have clear CTAs

Return JSON:
{{
  "captions": [
    {{
      "text": "Caption text here",
      "hashtags": ["#relevant", "#hashtags"],
      "cta": "Specific call to action",
      "best_for": "instagram|tiktok|x"
    }}
  ]
}}

Tone guidelines:
- Funny: Witty, relatable, light-hearted
- Informative: Educational, valuable, clear
- Luxury: Sophisticated, premium, aspirational"""

        response = llm.complete(prompt, task_hint="content generation", complexity="medium")
        
        try:
            caption_data = json.loads(response)
        except json.JSONDecodeError:
            # Fallback captions
            caption_data = {
                "captions": [
                    {
                        "text": f"{tone.title()} caption {i+1} about business automation",
                        "hashtags": ["#business", "#ai", "#automation"],
                        "cta": "Learn more in bio",
                        "best_for": ["instagram", "tiktok", "x"][i % 3]
                    } for i in range(10)
                ]
            }
        
        # Apply safety filter
        for caption in caption_data["captions"]:
            caption["text"] = safety_filter(caption["text"])
        
        return {
            "success": True,
            "captions": caption_data["captions"],
            "tone": tone,
            "user_id": user_id
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}

def safety_filter(text: str) -> str:
    """Filter content to ensure brand-safe, platform-safe output"""
    if not text:
        return text
    
    # Remove potential profanity and harmful content
    unsafe_patterns = [
        r'\b(damn|hell|shit|fuck|bitch|ass|crap)\b',
        r'\b(guarantee|guaranteed)\b',  # Avoid guarantee claims
        r'\b(cure|treatment|medical)\b',  # Avoid medical claims
        r'\b(get rich quick|make money fast)\b',  # Avoid scam-like language
    ]
    
    filtered_text = text
    for pattern in unsafe_patterns:
        filtered_text = re.sub(pattern, '[filtered]', filtered_text, flags=re.IGNORECASE)
    
    # Remove excessive punctuation
    filtered_text = re.sub(r'[!]{3,}', '!!', filtered_text)
    filtered_text = re.sub(r'[?]{3,}', '??', filtered_text)
    
    return filtered_text.strip()
