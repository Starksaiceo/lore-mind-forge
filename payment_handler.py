
import stripe
import os
from typing import Dict, Any

# Initialize Stripe with secret key from Replit Secrets
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
stripe.api_key = STRIPE_SECRET_KEY

if not STRIPE_SECRET_KEY:
    print("❌ STRIPE_SECRET_KEY not found in Replit Secrets")
    print("💡 Please add STRIPE_SECRET_KEY to your Replit Secrets")
else:
    print("✅ STRIPE_SECRET_KEY loaded from Secrets")

print(f"🔐 Stripe API Key configured: {'✅' if stripe.api_key else '❌'}")

def setup_stripe_payment(product: Dict[str, Any]) -> Dict[str, Any]:
    """
    Set up Stripe product and price for a given product
    
    Args:
        product: Dictionary containing title, description, and price
        
    Returns:
        Dictionary with success status and product/price IDs
    """
    try:
        # Create Stripe product
        product_data = stripe.Product.create(
            name=product["title"],
            description=product.get("description", "AI-generated digital product")
        )
        
        # Create price for the product
        price_data = stripe.Price.create(
            unit_amount=int(product["price"] * 100),  # Convert to cents
            currency="usd",
            product=product_data.id
        )
        
        print(f"[STRIPE] Product created with ID: {product_data.id}")
        print(f"[STRIPE] Price ID: {price_data.id}")
        
        return {
            "success": True,
            "product_id": product_data.id,
            "price_id": price_data.id,
            "product_name": product["title"],
            "price": product["price"]
        }
        
    except stripe.error.StripeError as e:
        print(f"[STRIPE ERROR] Stripe API Error: {e}")
        return {
            "success": False,
            "error": f"Stripe API Error: {str(e)}"
        }
    except Exception as e:
        print(f"[STRIPE ERROR] General Error: {e}")
        return {
            "success": False,
            "error": f"General Error: {str(e)}"
        }

def create_checkout_session(price_id: str, success_url: str = None, cancel_url: str = None) -> Dict[str, Any]:
    """
    Create a Stripe checkout session for a given price
    
    Args:
        price_id: Stripe price ID
        success_url: URL to redirect after successful payment
        cancel_url: URL to redirect after cancelled payment
        
    Returns:
        Dictionary with checkout session URL and ID
    """
    try:
        # Default URLs if not provided
        if not success_url:
            success_url = "https://your-app.replit.dev/success"
        if not cancel_url:
            cancel_url = "https://your-app.replit.dev/cancel"
            
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': price_id,
                'quantity': 1,
            }],
            mode='payment',
            success_url=success_url,
            cancel_url=cancel_url,
        )
        
        print(f"[STRIPE] Checkout session created: {session.id}")
        
        return {
            "success": True,
            "session_id": session.id,
            "checkout_url": session.url
        }
        
    except stripe.error.StripeError as e:
        print(f"[STRIPE ERROR] Checkout session failed: {e}")
        return {
            "success": False,
            "error": f"Checkout session error: {str(e)}"
        }

def get_recent_payments(limit: int = 10) -> Dict[str, Any]:
    """
    Get recent successful payments from Stripe
    
    Args:
        limit: Number of recent payments to fetch
        
    Returns:
        Dictionary with payment data
    """
    try:
        charges = stripe.Charge.list(limit=limit)
        
        payments = []
        total_revenue = 0
        
        for charge in charges.data:
            if charge.status == 'succeeded':
                amount = charge.amount / 100  # Convert from cents
                payments.append({
                    "id": charge.id,
                    "amount": amount,
                    "currency": charge.currency,
                    "created": charge.created,
                    "description": charge.description
                })
                total_revenue += amount
        
        print(f"[STRIPE] Retrieved {len(payments)} successful payments, total: ${total_revenue:.2f}")
        
        return {
            "success": True,
            "payments": payments,
            "total_revenue": total_revenue,
            "count": len(payments)
        }
        
    except stripe.error.StripeError as e:
        print(f"[STRIPE ERROR] Failed to retrieve payments: {e}")
        return {
            "success": False,
            "error": f"Payment retrieval error: {str(e)}"
        }

# Test function to verify Stripe connection
def test_stripe_connection() -> bool:
    """Test if Stripe API connection is working"""
    try:
        if not stripe.api_key:
            print("[STRIPE ERROR] No API key configured")
            return False
            
        # Try to retrieve account info
        account = stripe.Account.retrieve()
        print(f"[STRIPE] Connection successful! Account ID: {account.id}")
        return True
    except stripe.error.AuthenticationError as e:
        print(f"[STRIPE ERROR] Authentication failed - check your API key: {e}")
        return False
    except stripe.error.APIConnectionError as e:
        print(f"[STRIPE ERROR] Network connection failed: {e}")
        return False
    except Exception as e:
        print(f"[STRIPE ERROR] Connection failed: {e}")
        return False

if __name__ == "__main__":
    # Test the connection when run directly
    print("Testing Stripe connection...")
    if test_stripe_connection():
        print("✅ Stripe integration ready!")
    else:
        print("❌ Stripe integration failed. Check your API keys.")
