import requests
import os
import stripe
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from config import get_stripe_config, XANO_BASE_URL
from shopify_uploader import upload_product_to_shopify

# Import rate limiter
try:
    from api_rate_limiter import rate_limited
except ImportError:
    # Fallback if rate limiter not available
    def rate_limited(api_name):
        def decorator(func):
            return func
        return decorator

# Initialize Stripe
stripe_config = get_stripe_config()
if stripe_config.get("secret_key"):
    stripe.api_key = stripe_config["secret_key"]

def get_real_stripe_revenue():
    """Get real revenue from Stripe API - FIXED IMPLEMENTATION"""
    try:
        if not stripe_config.get("secret_key"):
            print("⚠️ No Stripe secret key configured")
            return 0.0

        # Get charges from last 30 days
        thirty_days_ago = datetime.now() - timedelta(days=30)

        charges = stripe.Charge.list(
            limit=100,
            created={"gte": int(thirty_days_ago.timestamp())}
        )

        total_revenue = 0.0
        for charge in charges.data:
            if charge.paid and charge.status == "succeeded":
                total_revenue += charge.amount / 100  # Convert from cents

        print(f"✅ Stripe revenue: ${total_revenue:.2f}")
        return total_revenue

    except Exception as e:
        print(f"❌ Stripe revenue error: {e}")
        return 0.0

def calculate_total_real_revenue():
    """Calculate total real revenue from all sources"""
    stripe_revenue = get_real_stripe_revenue()
    # Add other revenue sources here when available (Shopify, etc.)
    return stripe_revenue

def get_total_revenue():
    """Alias for calculate_total_real_revenue for backward compatibility"""
    return calculate_total_real_revenue()

def get_total_profit_last_30_days():
    """Get profit from last 30 days"""
    # Based on the edited snippet, it seems the intention is to use Stripe revenue as a proxy for profit for digital products.
    # The original code fetched profit data from Xano.
    # For now, we'll return Stripe revenue as per the edited snippet's implied logic.
    return get_real_stripe_revenue()

@rate_limited('xano')
def post_profit(amount: float, source: str) -> bool:
    """Post profit to Xano API"""
    try:
        url = f"{XANO_BASE_URL}/profit"
        payload = {
            "amount": amount,
            "source": source,
            "timestamp": datetime.now().isoformat(),
            "created_at": int(datetime.now().timestamp())
        }

        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        print(f"✅ Profit logged: ${amount:.2f} from {source}")
        return True

    except Exception as e:
        print(f"❌ Error posting profit: {e}")
        return False

def log_profit(amount: float, source: str, ai_task_id: Optional[int] = None, ai_goal_id: Optional[int] = None) -> bool:
    """Enhanced profit logging with AI task tracking"""
    try:
        url = f"{XANO_BASE_URL}/profit"
        payload = {
            "amount": amount,
            "source": source,
            "timestamp": datetime.now().isoformat(),
            "created_at": int(datetime.now().timestamp()),
            "ai_task_id": ai_task_id,
            "ai_goal_id": ai_goal_id
        }

        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        print(f"✅ Enhanced profit logged: ${amount:.2f} from {source}")
        return True

    except Exception as e:
        print(f"❌ Error logging profit: {e}")
        return False

@rate_limited('xano')
def get_profit_data() -> List[Dict]:
    """Get all profit data from Xano"""
    try:
        url = f"{XANO_BASE_URL}/profit"
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()
        return data if isinstance(data, list) else []

    except Exception as e:
        print(f"❌ Error fetching profit data: {e}")
        return []

def get_all_profits() -> List[Dict]:
    """Alias for get_profit_data for backward compatibility"""
    return get_profit_data()

def calculate_total_profit() -> float:
    """Calculate total profit from Xano data"""
    try:
        profits = get_profit_data()
        total = sum(float(p.get('amount', 0)) for p in profits if p.get('amount'))
        return total
    except Exception as e:
        print(f"❌ Error calculating total profit: {e}")
        return 0.0

def get_profit_by_source() -> Dict[str, float]:
    """Get profit breakdown by source"""
    try:
        profits = get_profit_data()
        by_source = {}

        for profit in profits:
            source = profit.get('source', 'Unknown')
            amount = float(profit.get('amount', 0))
            by_source[source] = by_source.get(source, 0) + amount

        return by_source
    except Exception as e:
        print(f"❌ Error getting profit by source: {e}")
        return {}

# The following function was modified significantly.
# The original `get_total_profit_last_30_days` fetched from Xano, but the new implementation uses Stripe revenue.
# The edited snippet also provides a new `calculate_total_real_revenue` and `sync_real_revenue_to_xano`.

def sync_real_revenue_to_xano() -> float:
    """Sync real Stripe revenue to Xano database"""
    try:
        real_revenue = get_real_stripe_revenue()

        if real_revenue > 0:
            # Post to Xano
            data = {
                "amount": real_revenue,
                "source": "Stripe - Real Revenue Sync",
                "timestamp": datetime.now().isoformat(),
                "ai_task_id": 999  # Special ID for revenue sync
            }

            response = requests.post(
                f"{XANO_BASE_URL}/profit",
                json=data,
                timeout=10
            )

            if response.status_code == 200:
                print(f"✅ Synced ${real_revenue:.2f} to Xano")
                return real_revenue
            else:
                print(f"⚠️ Xano sync failed: {response.status_code}")
                return real_revenue
        else:
            return 0.0

    except Exception as e:
        print(f"❌ Revenue sync error: {e}")
        return 0.0

# The original `calculate_total_real_revenue` function is replaced by the new implementation.
# The Gumroad part has been removed.
# The original logic for fetching Stripe and Shopify revenue has been consolidated into the new implementation.
# The `stripe_utils` and `stripe_api` imports are no longer needed as Stripe is now handled directly.
# The `payment_processor` import for Shopify is retained due to `upload_product_to_shopify` being imported.
# However, `ShopifyProcessor.get_sales` is not called in the new `calculate_total_real_revenue`.