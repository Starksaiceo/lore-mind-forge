
#!/usr/bin/env python3
"""Comprehensive Stripe Payment System Test"""

import os
import sys
import stripe
from config import STRIPE_SECRET_KEY, STRIPE_PUBLISHABLE_KEY
from payment_handler import test_stripe_connection, setup_stripe_payment, create_checkout_session, get_recent_payments
from payment_processor import StripeProcessor, get_real_stripe_revenue
from stripe_api import create_stripe_product, get_stripe_payments
import json

def test_stripe_configuration():
    """Test Stripe API key configuration"""
    print("🔧 Testing Stripe Configuration...")
    
    # Check if keys are loaded
    if STRIPE_SECRET_KEY:
        print(f"✅ STRIPE_SECRET_KEY loaded: {STRIPE_SECRET_KEY[:7]}...")
    else:
        print("❌ STRIPE_SECRET_KEY not found")
        return False
    
    if STRIPE_PUBLISHABLE_KEY:
        print(f"✅ STRIPE_PUBLISHABLE_KEY loaded: {STRIPE_PUBLISHABLE_KEY[:7]}...")
    else:
        print("❌ STRIPE_PUBLISHABLE_KEY not found")
    
    return True

def test_stripe_connection_direct():
    """Test direct Stripe API connection"""
    print("\n🌐 Testing Direct Stripe API Connection...")
    
    try:
        stripe.api_key = STRIPE_SECRET_KEY
        account = stripe.Account.retrieve()
        
        print(f"✅ Stripe API connected successfully!")
        print(f"   Account ID: {account.id}")
        print(f"   Country: {account.country}")
        print(f"   Business Type: {account.business_type}")
        
        return True
        
    except stripe.error.AuthenticationError as e:
        print(f"❌ Authentication failed: {e}")
        return False
    except stripe.error.APIConnectionError as e:
        print(f"❌ Connection failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_payment_handler_functions():
    """Test payment_handler.py functions"""
    print("\n🔧 Testing payment_handler.py functions...")
    
    # Test connection function
    connection_result = test_stripe_connection()
    print(f"   Connection test: {'✅' if connection_result else '❌'}")
    
    # Test product setup
    test_product = {
        "title": "Test Product",
        "description": "This is a test product for Stripe integration",
        "price": 29.99
    }
    
    try:
        setup_result = setup_stripe_payment(test_product)
        if setup_result.get("success"):
            print(f"✅ Product setup successful:")
            print(f"   Product ID: {setup_result.get('product_id')}")
            print(f"   Price ID: {setup_result.get('price_id')}")
            
            # Test checkout session creation
            checkout_result = create_checkout_session(
                setup_result.get('price_id'),
                "https://your-app.replit.dev/success",
                "https://your-app.replit.dev/cancel"
            )
            
            if checkout_result.get("success"):
                print(f"✅ Checkout session created:")
                print(f"   Session ID: {checkout_result.get('session_id')}")
                print(f"   Checkout URL: {checkout_result.get('checkout_url')[:50]}...")
            else:
                print(f"❌ Checkout session failed: {checkout_result.get('error')}")
                
        else:
            print(f"❌ Product setup failed: {setup_result.get('error')}")
            
    except Exception as e:
        print(f"❌ Payment handler test failed: {e}")

def test_payment_processor():
    """Test payment_processor.py StripeProcessor class"""
    print("\n💳 Testing StripeProcessor class...")
    
    try:
        processor = StripeProcessor()
        
        if processor.is_configured():
            print("✅ StripeProcessor configured correctly")
            
            # Test product creation
            test_product = {
                "title": "Processor Test Product",
                "description": "Test product via StripeProcessor",
                "price": 49.99
            }
            
            result = processor.create_product(test_product)
            if result.get("success"):
                print(f"✅ StripeProcessor product creation successful:")
                print(f"   Product ID: {result.get('product_id')}")
                print(f"   Price ID: {result.get('price_id')}")
                print(f"   URL: {result.get('url')}")
            else:
                print(f"❌ StripeProcessor product creation failed: {result.get('error')}")
                
            # Test revenue retrieval
            charges_result = processor.get_recent_charges()
            if charges_result.get("success"):
                print(f"✅ Revenue retrieval successful:")
                print(f"   Total charges: {len(charges_result.get('charges', []))}")
                print(f"   Total revenue: ${charges_result.get('total_revenue', 0):.2f}")
            else:
                print(f"❌ Revenue retrieval failed: {charges_result.get('error')}")
                
        else:
            print("❌ StripeProcessor not configured")
            
    except Exception as e:
        print(f"❌ StripeProcessor test failed: {e}")

def test_stripe_api_functions():
    """Test stripe_api.py functions"""
    print("\n🔌 Testing stripe_api.py functions...")
    
    try:
        # Test product creation
        result = create_stripe_product(
            "API Test Product",
            79.99,
            "Test product via stripe_api.py"
        )
        
        if result.get("success"):
            print(f"✅ stripe_api product creation successful:")
            print(f"   Product ID: {result.get('product_id')}")
            print(f"   Price ID: {result.get('price_id')}")
        else:
            print(f"❌ stripe_api product creation failed: {result.get('error')}")
            
        # Test payments retrieval
        payments = get_stripe_payments(5)
        print(f"✅ Retrieved {len(payments)} recent payments")
        
        if payments and len(payments) > 0 and not payments[0].get("error"):
            print("   Recent payments found:")
            for payment in payments[:3]:
                print(f"     ${payment.get('amount', 0):.2f} - {payment.get('id', 'N/A')}")
        else:
            print("   No payments found or error occurred")
            
    except Exception as e:
        print(f"❌ stripe_api test failed: {e}")

def test_real_revenue():
    """Test real revenue calculation"""
    print("\n💰 Testing Real Revenue Calculation...")
    
    try:
        revenue = get_real_stripe_revenue()
        print(f"✅ Real Stripe revenue: ${revenue:.2f}")
        
        # Test recent payments
        recent_payments = get_recent_payments(10)
        if recent_payments.get("success"):
            print(f"✅ Recent payments retrieved:")
            print(f"   Count: {recent_payments.get('count', 0)}")
            print(f"   Total revenue: ${recent_payments.get('total_revenue', 0):.2f}")
        else:
            print(f"❌ Recent payments failed: {recent_payments.get('error')}")
            
    except Exception as e:
        print(f"❌ Revenue calculation failed: {e}")

def test_live_api_calls():
    """Test live Stripe API calls"""
    print("\n🔴 Testing Live Stripe API Calls...")
    
    try:
        stripe.api_key = STRIPE_SECRET_KEY
        
        # Test listing products
        products = stripe.Product.list(limit=5)
        print(f"✅ Found {len(products.data)} products in Stripe")
        
        # Test listing prices
        prices = stripe.Price.list(limit=5)
        print(f"✅ Found {len(prices.data)} prices in Stripe")
        
        # Test listing charges
        charges = stripe.Charge.list(limit=5)
        print(f"✅ Found {len(charges.data)} charges in Stripe")
        
        total_revenue = sum(charge.amount for charge in charges.data if charge.paid) / 100
        print(f"✅ Total revenue from recent charges: ${total_revenue:.2f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Live API calls failed: {e}")
        return False

def main():
    """Run comprehensive Stripe system test"""
    print("🚀 Starting Comprehensive Stripe Payment System Test")
    print("=" * 60)
    
    # Test configuration
    config_ok = test_stripe_configuration()
    
    if not config_ok:
        print("\n❌ Configuration test failed. Please check your Stripe API keys.")
        return
    
    # Test direct connection
    connection_ok = test_stripe_connection_direct()
    
    if not connection_ok:
        print("\n❌ Direct connection test failed. Please check your Stripe configuration.")
        return
    
    # Test all modules
    test_payment_handler_functions()
    test_payment_processor()
    test_stripe_api_functions()
    test_real_revenue()
    
    # Test live API
    live_ok = test_live_api_calls()
    
    print("\n" + "=" * 60)
    if live_ok:
        print("🎉 STRIPE PAYMENT SYSTEM TEST COMPLETE - ALL SYSTEMS OPERATIONAL!")
    else:
        print("⚠️ STRIPE PAYMENT SYSTEM TEST COMPLETE - SOME ISSUES DETECTED")
    
    print("\n📊 Test Summary:")
    print(f"   Configuration: {'✅' if config_ok else '❌'}")
    print(f"   API Connection: {'✅' if connection_ok else '❌'}")
    print(f"   Live API Calls: {'✅' if live_ok else '❌'}")

if __name__ == "__main__":
    main()
