
import os, re, glob, json, time, importlib.util

PATCH_LOG = []

def ensure_os_import(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()
    if "import os" not in code:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("import os\n" + code)
        PATCH_LOG.append(f"✅ Added 'import os' to {file_path}")

def patch_all_files():
    py_files = glob.glob("**/*.py", recursive=True)
    for fp in py_files:
        if fp.endswith(("system_fix.py", "__init__.py")):
            continue
        with open(fp, "r", encoding="utf-8") as f:
            if "os.getenv" in f.read():
                ensure_os_import(fp)

def write_stripe_utils():
    code = '''
import stripe, os

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

def get_total_revenue(limit=25):
    """
    Return total PAID charges in USD.
    """
    try:
        charges = stripe.Charge.list(limit=limit)
        total = sum(c["amount"] for c in charges["data"] if c["paid"])
        return round(total / 100, 2)
    except Exception as e:
        print("❌ Stripe fetch failed:", e)
        return 0.0
'''
    with open("stripe_utils.py", "w", encoding="utf-8") as f:
        f.write(code)
    PATCH_LOG.append("✅ Created stripe_utils.py")

def stub_meta_ads():
    code = '''
def get_meta_token():
    print("⚠️  Meta Ads temporarily disabled — waiting for app approval.")
    return None
'''
    with open("meta_ads_stub.py", "w", encoding="utf-8") as f:
        f.write(code)
    PATCH_LOG.append("✅ Stubbed Meta Ads calls")

def write_streamlit_cfg():
    os.makedirs(".streamlit", exist_ok=True)
    cfg = "[server]\nenableCORS = true\nenableXsrfProtection = false\n"
    with open(".streamlit/config.toml", "w", encoding="utf-8") as f:
        f.write(cfg)
    PATCH_LOG.append("✅ Wrote .streamlit/config.toml")

def main():
    patch_all_files()
    write_stripe_utils()
    stub_meta_ads()
    write_streamlit_cfg()
    with open("patch_report.json", "w", encoding="utf-8") as f:
        json.dump({
            "timestamp": time.ctime(),
            "actions": PATCH_LOG
        }, f, indent=2)
    print("🔧 System patch complete. Actions:")
    for line in PATCH_LOG:
        print(" •", line)

if __name__ == "__main__":
    main()
