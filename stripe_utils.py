import stripe
import os
from config import STRIPE_SECRET_KEY

def get_stripe_revenue():
    """Get real revenue from Stripe"""
    if not STRIPE_SECRET_KEY:
        print("⚠️ No Stripe key configured")
        return 0.0

    try:
        stripe.api_key = STRIPE_SECRET_KEY
        charges = stripe.Charge.list(limit=10)

        if not charges.data:
            print("💡 No Stripe charges found - create a test charge in Stripe dashboard")
            return 0.0

        total = sum([charge.amount for charge in charges.data if charge.status == 'succeeded']) / 100
        print(f"✅ Stripe Charges: {len(charges.data)} found")
        print(f"💳 Real Stripe Revenue: ${total:.2f}")
        return total
    except Exception as e:
        print(f"❌ Stripe API error: {str(e)}")
        return 0.0

def create_test_stripe_payment():
    """Create a test payment for development"""
    try:
        if not STRIPE_SECRET_KEY:
            return False

        stripe.api_key = STRIPE_SECRET_KEY

        # Create a test payment intent
        payment_intent = stripe.PaymentIntent.create(
            amount=2000,  # $20.00
            currency='usd',
            description='Test payment for AI CEO development',
        )

        print(f"✅ Test payment created: {payment_intent.id}")
        return True

    except Exception as e:
        print(f"❌ Test payment failed: {e}")
        return False