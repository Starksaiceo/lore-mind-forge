
import os
import json
from typing import List, Dict, Any
from datetime import datetime
import requests
from config import OPENROUTER_API_KEY

def generate_email_sequence(product_info: Dict[str, Any], audience: str = "general", sequence_length: int = 5) -> List[Dict[str, Any]]:
    """Generate email marketing sequence for a product"""
    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        
        prompt = f"""Create a {sequence_length}-email marketing sequence for this product:

Product: {product_info.get('title', 'Digital Product')}
Description: {product_info.get('description', 'High-value digital product')}
Price: ${product_info.get('price', 97)}
Target Audience: {audience}

Create emails that follow this sequence:
1. Welcome & Value Introduction
2. Problem Agitation & Solution Preview
3. Social Proof & Case Studies
4. Urgency & Scarcity
5. Final Call to Action

For each email, provide:
- Subject line (compelling, under 50 chars)
- Body content (conversational, benefit-focused)
- Call-to-action button text
- Send timing (days after signup)

Format as JSON array of email objects."""

        payload = {
            "model": "openai/gpt-3.5-turbo",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 2000,
            "temperature": 0.7
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
            
            # Try to extract JSON from response
            try:
                # Find JSON in response
                start_idx = content.find('[')
                end_idx = content.rfind(']') + 1
                if start_idx != -1 and end_idx != -1:
                    json_str = content[start_idx:end_idx]
                    emails = json.loads(json_str)
                else:
                    # Fallback: create structured emails
                    emails = create_fallback_sequence(product_info, audience, sequence_length)
                
                # Ensure all emails have required fields
                for i, email in enumerate(emails):
                    email.setdefault('id', i + 1)
                    email.setdefault('subject', f"Email #{i + 1}")
                    email.setdefault('body', "Email content here...")
                    email.setdefault('cta_text', "Learn More")
                    email.setdefault('send_day', i + 1)
                
                return emails[:sequence_length]
                
            except json.JSONDecodeError:
                return create_fallback_sequence(product_info, audience, sequence_length)
        
        else:
            print(f"❌ Email generation failed: {response.status_code}")
            return create_fallback_sequence(product_info, audience, sequence_length)
            
    except Exception as e:
        print(f"❌ Email sequence generation error: {e}")
        return create_fallback_sequence(product_info, audience, sequence_length)

def create_fallback_sequence(product_info: Dict[str, Any], audience: str, sequence_length: int) -> List[Dict[str, Any]]:
    """Create fallback email sequence when AI fails"""
    title = product_info.get('title', 'Digital Product')
    price = product_info.get('price', 97)
    
    templates = [
        {
            "id": 1,
            "subject": f"Welcome! Your {title} journey begins",
            "body": f"Hi there!\n\nWelcome to an exciting journey with {title}. You're about to discover how this can transform your business and help you achieve your goals.\n\nIn the coming days, I'll share valuable insights and show you exactly how {title} can help you succeed.\n\nStay tuned for exclusive tips!",
            "cta_text": "Get Started Now",
            "send_day": 1
        },
        {
            "id": 2,
            "subject": "The #1 mistake everyone makes",
            "body": f"Yesterday I mentioned {title}, and I want to share something important...\n\nMost people struggle because they're missing one crucial element. This mistake costs them time, money, and results.\n\n{title} was designed specifically to solve this problem. Tomorrow, I'll show you proof it works.",
            "cta_text": "See The Solution",
            "send_day": 2
        },
        {
            "id": 3,
            "subject": "PROOF: Real results from real people",
            "body": f"I promised you proof, so here it is...\n\nOur customers have achieved incredible results with {title}:\n• Increased productivity by 300%\n• Saved 10+ hours per week\n• Generated additional income\n\nThese aren't just claims - these are real results from real people like you.",
            "cta_text": "Join Them Now",
            "send_day": 3
        },
        {
            "id": 4,
            "subject": "Only 48 hours left...",
            "body": f"Time is running out!\n\nThe special pricing for {title} ends in just 48 hours. After that, the price goes up to the regular ${price + 50}.\n\nDon't miss this opportunity to get everything at the current price of just ${price}.\n\nThis could be the decision that changes everything for you.",
            "cta_text": "Secure Your Copy",
            "send_day": 4
        },
        {
            "id": 5,
            "subject": "FINAL HOURS - Don't miss out",
            "body": f"This is it - your final chance!\n\nThe special offer for {title} ends tonight at midnight. After that, this opportunity is gone.\n\nDon't let this slip away. Take action now and start your transformation today.\n\nClick below to secure your copy before it's too late:",
            "cta_text": "Get It Now",
            "send_day": 5
        }
    ]
    
    return templates[:sequence_length]

def get_email_templates() -> List[Dict[str, Any]]:
    """Get available email templates"""
    return [
        {
            "name": "Product Launch",
            "description": "5-email sequence for new product launches",
            "emails": 5,
            "use_case": "New product introduction"
        },
        {
            "name": "Re-engagement",
            "description": "3-email sequence to re-engage inactive subscribers",
            "emails": 3,
            "use_case": "Win back customers"
        },
        {
            "name": "Webinar Funnel",
            "description": "7-email sequence for webinar promotion",
            "emails": 7,
            "use_case": "Event promotion"
        }
    ]

def save_email_sequence(user_id: int, sequence: List[Dict], product_name: str) -> str:
    """Save email sequence to file"""
    try:
        os.makedirs("content_ready_to_post", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        filename = f"content_ready_to_post/email_sequence_{product_name}_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump({
                "user_id": user_id,
                "product_name": product_name,
                "created_at": datetime.now().isoformat(),
                "emails": sequence
            }, f, indent=2)
        
        print(f"📧 Email sequence saved: {filename}")
        return filename
        
    except Exception as e:
        print(f"❌ Email sequence save failed: {e}")
        return ""

# Export functions
__all__ = ['generate_email_sequence', 'get_email_templates', 'save_email_sequence']
