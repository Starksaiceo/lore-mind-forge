
import os
import requests
from config import get_openrouter_config

def generate_email_sequence(product_info, audience_type="entrepreneurs"):
    """Generate email sequence for product marketing"""
    try:
        config = get_openrouter_config()
        
        if not config.get("api_key"):
            # Fallback mode
            return generate_fallback_emails(product_info, audience_type)
        
        prompt = f"""
        Create a 3-email marketing sequence for this product:
        
        Product: {product_info.get('title', 'Digital Product')}
        Description: {product_info.get('description', 'Premium digital product')}
        Price: ${product_info.get('price', 29.99)}
        Audience: {audience_type}
        
        Generate:
        Email 1: Introduction & Value (subject + body)
        Email 2: Benefits & Social Proof (subject + body)  
        Email 3: Urgency & Final CTA (subject + body)
        
        Format as JSON with subjects and bodies.
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
            return {"success": True, "emails": content}
        else:
            return generate_fallback_emails(product_info, audience_type)
            
    except Exception as e:
        return generate_fallback_emails(product_info, audience_type)

def generate_fallback_emails(product_info, audience_type):
    """Fallback email templates when API unavailable"""
    title = product_info.get('title', 'Digital Product')
    price = product_info.get('price', 29.99)
    
    emails = {
        "email_1": {
            "subject": f"Introducing {title} - Game Changer for {audience_type.title()}",
            "body": f"""Hi there!

I wanted to personally introduce you to {title}.

This isn't just another product - it's specifically designed for {audience_type} who want real results.

What makes it different:
• Immediately actionable
• Proven by real users  
• Backed by our guarantee

Worth checking out: [PRODUCT_LINK]

Best,
AI CEO Team"""
        },
        "email_2": {
            "subject": f"Why {title} is Perfect for {audience_type.title()}",
            "body": f"""Quick question - are you still looking for a solution that actually works?

{title} has helped hundreds of {audience_type} achieve their goals:

✅ "Increased my productivity by 300%" - Sarah M.
✅ "Best investment I made this year" - Mike R.
✅ "Paid for itself in the first week" - Jennifer L.

For just ${price}, you get everything you need to succeed.

Ready to join them? [PRODUCT_LINK]

Talk soon,
AI CEO Team"""
        },
        "email_3": {
            "subject": f"Last chance: {title} (expires tonight)",
            "body": f"""This is it - last email about {title}.

Our special pricing ends tonight at midnight.

After that, the price goes up permanently.

Don't miss out on:
• Complete {title} system
• Bonus materials (worth $100+)
• 30-day money-back guarantee
• Lifetime updates

Secure your copy now: [PRODUCT_LINK]

This offer won't come again.

Final regards,
AI CEO Team"""
        }
    }
    
    return {"success": True, "emails": emails}
