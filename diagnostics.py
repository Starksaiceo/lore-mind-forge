
# === ENV & CONNECTIVITY DIAGNOSTICS ===
import os, json, stripe, requests, py_compile, traceback
from dotenv import load_dotenv
load_dotenv()   # ensures .env + Replit secrets are in os.environ

def mask(val):
    if not val: return None
    return val[:6] + "…" + val[-4:]

report = {"env": {}, "stripe": {}, "gumroad": {}, "syntax": {}}

# 1️⃣  capture env - Shopify + Stripe only
for k in ["STRIPE_SECRET_KEY", "STRIPE_PUBLISHABLE_KEY", "SHOPIFY_ACCESS_TOKEN"]:
    report["env"][k] = mask(os.getenv(k))

# 2️⃣  Stripe test
try:
    stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
    acct = stripe.Account.retrieve()
    report["stripe"]["success"] = True
    report["stripe"]["id"] = acct["id"]
except Exception as e:
    report["stripe"]["success"] = False
    report["stripe"]["error"] = str(e)

# 3️⃣ Shopify test - check connection
try:
    from marketplace_uploader import check_shopify_connection
    result = check_shopify_connection()
    report["shopify"]["success"] = result.get("connected", False)
    report["shopify"]["store_name"] = result.get("store_name", "Unknown")
    report["shopify"]["products_count"] = result.get("products_count", 0)
except Exception as e:
    report["shopify"]["success"] = False
    report["shopify"]["error"] = str(e)

print(json.dumps(report, indent=2))mps(report, indent=2))
