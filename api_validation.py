
import os
from config import validate_api_keys
from stripe_api import stripe_api
from xano_api import xano_api
from meta_api import meta_api

def validate_all_services():
    """Validate all API services and return status"""
    validation_results = {
        "timestamp": __import__('datetime').datetime.now().isoformat(),
        "services": {}
    }
    
    # Validate API keys
    key_validation = validate_api_keys()
    validation_results["api_keys"] = key_validation
    
    # Test Stripe
    validation_results["services"]["stripe"] = {
        "configured": stripe_api.is_configured(),
        "status": "configured" if stripe_api.is_configured() else "missing_keys"
    }
    
    if stripe_api.is_configured():
        try:
            payments = stripe_api.get_payments(1)
            validation_results["services"]["stripe"]["api_test"] = "success"
            validation_results["services"]["stripe"]["recent_payments"] = len(payments)
        except Exception as e:
            validation_results["services"]["stripe"]["api_test"] = f"error: {str(e)}"
    
    # Test Shopify
    validation_results["services"]["shopify"] = {
        "configured": True,
        "status": "configured"
    }
    
    try:
        from marketplace_uploader import check_shopify_connection
        shopify_status = check_shopify_connection()
        validation_results["services"]["shopify"]["api_test"] = "success" if shopify_status.get("connected") else "failed"
        validation_results["services"]["shopify"]["products_count"] = shopify_status.get("products_count", 0)
    except Exception as e:
        validation_results["services"]["shopify"]["api_test"] = f"error: {str(e)}"
    
    # Test Xano
    validation_results["services"]["xano"] = {
        "configured": xano_api.is_configured(),
        "status": "configured" if xano_api.is_configured() else "missing_url"
    }
    
    if xano_api.is_configured():
        try:
            profits = xano_api.get_profits(1)
            validation_results["services"]["xano"]["api_test"] = "success"
            validation_results["services"]["xano"]["profit_entries"] = len(profits)
        except Exception as e:
            validation_results["services"]["xano"]["api_test"] = f"error: {str(e)}"
    
    # Test Meta
    validation_results["services"]["meta"] = {
        "configured": meta_api.is_configured(),
        "status": "configured" if meta_api.is_configured() else "missing_keys"
    }
    
    if meta_api.is_configured():
        try:
            app_status = meta_api.check_app_status()
            validation_results["services"]["meta"]["api_test"] = "success"
            validation_results["services"]["meta"]["app_status"] = app_status
        except Exception as e:
            validation_results["services"]["meta"]["api_test"] = f"error: {str(e)}"
    
    return validation_results

def print_validation_summary():
    """Print a human-readable validation summary"""
    results = validate_all_services()
    
    print("🔐 API VALIDATION SUMMARY")
    print("=" * 50)
    
    # API Keys status
    if results["api_keys"]["all_required_present"]:
        print("✅ Required API keys: CONFIGURED")
    else:
        print("❌ Missing required keys:", results["api_keys"]["missing_required"])
    
    # Service status
    for service_name, service_data in results["services"].items():
        status_icon = "✅" if service_data.get("configured") else "❌"
        print(f"{status_icon} {service_name.title()}: {service_data.get('status', 'unknown')}")
        
        if service_data.get("api_test") == "success":
            print(f"   🔗 API connection: working")
        elif service_data.get("api_test"):
            print(f"   ⚠️  API test: {service_data['api_test']}")
    
    print("=" * 50)
    
    return results

if __name__ == "__main__":
    print_validation_summary()
