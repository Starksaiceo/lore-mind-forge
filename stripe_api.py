import os
import stripe
from typing import Dict, List, Optional
from config import STRIPE_SECRET_KEY, STRIPE_PUBLISHABLE_KEY

# Configure Stripe
if STRIPE_SECRET_KEY:
    stripe.api_key = STRIPE_SECRET_KEY

class StripeAPI:
    """Stripe API service for payment processing and product management"""

    def __init__(self):
        self.secret_key = STRIPE_SECRET_KEY
        self.publishable_key = STRIPE_PUBLISHABLE_KEY

    def is_configured(self) -> bool:
        """Check if Stripe is properly configured"""
        return bool(self.secret_key)

    def create_product(self, product_data: Dict) -> Dict:
        """Create a product and price in Stripe"""
        try:
            if not self.is_configured():
                return {"success": False, "error": "Stripe not configured"}

            # Create product
            product = stripe.Product.create(
                name=product_data.get("title", "AI Generated Product"),
                description=product_data.get("description", "Digital product created by AI"),
                type="service"
            )

            # Create price
            price = stripe.Price.create(
                product=product.id,
                unit_amount=int(product_data.get("price", 97) * 100),  # Convert to cents
                currency="usd"
            )

            return {
                "success": True,
                "product_id": product.id,
                "price_id": price.id,
                "product_url": f"https://buy.stripe.com/{price.id}",
                "data": {"product": product, "price": price}
            }

        except Exception as e:
            return {"success": False, "error": f"Stripe product creation error: {str(e)}"}

    def get_payments(self, limit: int = 10) -> List[Dict]:
        """Get recent payments from Stripe"""
        try:
            if not self.is_configured():
                return []

            payments = stripe.PaymentIntent.list(limit=limit)

            return [{
                "id": payment.id,
                "amount": payment.amount / 100,  # Convert from cents
                "currency": payment.currency,
                "status": payment.status,
                "created": payment.created,
                "description": payment.description
            } for payment in payments.data]

        except Exception as e:
            print(f"Error fetching Stripe payments: {e}")
            return []

    def create_checkout_session(self, price_id: str, success_url: str, cancel_url: str) -> Dict:
        """Create a Stripe checkout session"""
        try:
            if not self.is_configured():
                return {"success": False, "error": "Stripe not configured"}

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

            return {
                "success": True,
                "checkout_url": session.url,
                "session_id": session.id
            }

        except Exception as e:
            return {"success": False, "error": f"Checkout session error: {str(e)}"}

# Global instance
stripe_api = StripeAPI()

# Convenience functions
def create_stripe_product(product_data: Dict) -> Dict:
    """Create product in Stripe"""
    return stripe_api.create_product(product_data)

def get_stripe_payments(limit=10):
    """Get recent Stripe payments"""
    try:
        import os
        stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

        if not stripe.api_key:
            return [{"error": "Stripe API key not configured"}]

        stripe_key = os.environ.get('STRIPE_SECRET_KEY')

        try:
            stripe.api_key = stripe_key
            recent_charges = stripe.Charge.list(limit=limit)

            payments = []
            for charge in recent_charges.data:
                payments.append({
                    "id": charge.id,
                    "amount": charge.amount / 100,  # Convert cents to dollars
                    "currency": charge.currency,
                    "status": charge.status,
                    "created": charge.created,
                    "description": charge.description
                })

            return payments
        except Exception as e:
            print(f'❌ Stripe fetch failed: {e}')
            return []
    except Exception as e:
        print(f'❌ Stripe payments retrieval failed: {e}')
        return []
import stripe
import os
from typing import List, Dict, Optional
from config import STRIPE_SECRET_KEY

# Initialize Stripe
if STRIPE_SECRET_KEY:
    stripe.api_key = STRIPE_SECRET_KEY

def get_stripe_payments(limit: int = 10) -> List[Dict]:
    """Get recent Stripe charges/payments"""
    try:
        if not STRIPE_SECRET_KEY:
            return []
        
        charges = stripe.Charge.list(limit=limit)
        payments = []
        
        for charge in charges.data:
            if charge.status == 'succeeded':
                payments.append({
                    "amount": charge.amount / 100,  # Convert from cents
                    "currency": charge.currency,
                    "id": charge.id,
                    "created": charge.created,
                    "description": charge.description
                })
        
        return payments
    
    except Exception as e:
        print(f"Stripe API error: {e}")
        return [{"error": str(e)}]

def create_stripe_product(name: str, price: float, description: str = "") -> Dict:
    """Create a Stripe product and price"""
    try:
        if not STRIPE_SECRET_KEY:
            return {"success": False, "error": "Stripe not configured"}

        # Create product
        product = stripe.Product.create(
            name=name,
            description=description,
            type='service'  # Use 'service' for digital products
        )

        # Create price
        price_obj = stripe.Price.create(
            unit_amount=int(price * 100),  # Convert to cents
            currency='usd',
            product=product.id,
        )

        return {
            "success": True,
            "product_id": product.id,
            "price_id": price_obj.id,
            "payment_link": f"https://buy.stripe.com/test_{price_obj.id}"  # Example link
        }

    except Exception as e:
        return {"success": False, "error": str(e)}

def get_total_stripe_revenue() -> float:
    """Get total revenue from Stripe"""
    try:
        if not STRIPE_SECRET_KEY:
            return 0.0
        
        charges = stripe.Charge.list(limit=100)
        total = 0.0
        
        for charge in charges.data:
            if charge.status == 'succeeded':
                total += charge.amount / 100  # Convert from cents
        
        return total
    
    except Exception as e:
        print(f"Stripe revenue calculation error: {e}")
        return 0.0
