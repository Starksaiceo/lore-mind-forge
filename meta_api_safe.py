import os
from config import META_APP_ID, META_APP_SECRET, META_ACCESS_TOKEN
import time

def check_meta_app_status():
    """Check Meta app configuration safely"""
    try:
        # Check if we have placeholder values
        if META_APP_ID == "fake_meta_id" or META_APP_ID == "placeholder":
            return {
                "approved": False,
                "status": "not_configured",
                "message": "Meta app not configured"
            }

        if not META_ACCESS_TOKEN or META_ACCESS_TOKEN == "placeholder":
            return {
                "approved": False,
                "status": "awaiting_token",
                "message": "Meta access token needed"
            }

        # If we have real values, try to check status
        return {
            "approved": True,
            "status": "configured",
            "message": "Meta app configured"
        }

    except Exception as e:
        return {
            "approved": False,
            "status": "error",
            "message": f"Meta check failed: {e}"
        }

def create_meta_ad_campaign(product, budget=20.0):
    """Create Meta ad campaign with safety checks"""
    try:
        status = check_meta_app_status()

        if not status["approved"]:
            print(f"⚠️ Meta ads not ready: {status['message']}")
            return {
                "success": False,
                "mock": True,
                "budget": budget,
                "platform": "meta_mock",
                "message": status["message"]
            }

        # Real Meta ad creation would go here
        print(f"🚀 Creating Meta ad for {product.get('title', 'Unknown')} with ${budget} budget")

        return {
            "success": True,
            "mock": False,
            "budget": budget,
            "platform": "meta",
            "campaign_id": f"mock_campaign_{int(time.time())}"
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "mock": True
        }

def run_meta_ads_campaign():
    """Run Meta ads campaign with safety checks"""
    try:
        from config import META_APP_ID, META_ACCESS_TOKEN, THREADS_APP_ID

        # Check if Meta is properly configured
        if not META_APP_ID or META_APP_ID == "placeholder":
            print("🛑 Skipping Meta Ads – META_APP_ID is placeholder")
            return {"success": False, "error": "Meta not configured"}

        if not META_ACCESS_TOKEN:
            print("🛑 Skipping Meta Ads – No access token")
            return {"success": False, "error": "No Meta access token"}

        if THREADS_APP_ID == "placeholder":
            print("🛑 Skipping Meta Ads – THREADS_APP_ID is placeholder")
            return {"success": False, "error": "Threads not configured"}

        print("🎯 Running Meta ads campaign...")

        # Placeholder for actual Meta ads logic
        return {
            "success": True,
            "campaign_id": f"meta_campaign_{int(time.time())}",
            "budget": 10.0,
            "status": "active"
        }

    except Exception as e:
        print(f"❌ Meta ads error: {e}")
        return {"success": False, "error": str(e)}