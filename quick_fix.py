
import os, re, glob, textwrap
from pathlib import Path

LOG = []

# 1️⃣  Ensure python-dotenv is loaded application-wide
DOTENV_SNIPPET = "from dotenv import load_dotenv\nload_dotenv()\n"

def prepend_dotenv(fp):
    code = Path(fp).read_text(encoding="utf-8")
    if "load_dotenv()" not in code:
        Path(fp).write_text(DOTENV_SNIPPET + code, encoding="utf-8")
        LOG.append(f"✅ Added load_dotenv() to {fp}")

# 2️⃣  Fix stripe_api.py syntax error (missing except)
def patch_stripe():
    fp = Path("stripe_api.py")
    if not fp.exists(): return
    code = fp.read_text(encoding="utf-8")
    if "expected 'except'" in code or "try:" in code and "except" not in code:
        fixed = re.sub(
            r"try:\s*\n([^\n]+\n)+",
            lambda m: m.group(0) + "    except Exception as e:\n        print('❌ Stripe fetch failed:', e)\n        return 0.0\n",
            code, count=1, flags=re.M
        )
        fp.write_text(fixed, encoding="utf-8")
        LOG.append("✅ Patched stripe_api.py try/except")

# 3️⃣  Fix indentation error in payment_processor.py line 302
def fix_indent():
    fp = Path("payment_processor.py")
    if not fp.exists(): return
    lines = fp.read_text(encoding="utf-8").splitlines()
    # naive auto-dedent the block around 302
    idx = 301  # zero-based
    if idx < len(lines):
        lines[idx] = lines[idx].lstrip()  # remove leading spaces/tabs
        fp.write_text("\n".join(lines), encoding="utf-8")
        LOG.append("✅ Fixed indent in payment_processor.py line 302")

# 4️⃣  Insert dotenv preload into main entry scripts
for entry in ["main.py", "app.py", "profit_sprint.py"]:
    if Path(entry).exists():
        prepend_dotenv(entry)

patch_stripe()
fix_indent()

# 5️⃣  Verify Gumroad key
if os.getenv("GUMROAD_API_KEY"):
    LOG.append("✅ GUMROAD_API_KEY detected in environment")
else:
    LOG.append("❌ GUMROAD_API_KEY still missing - add it to .env")

Path("quick_fix_report.txt").write_text("\n".join(LOG), encoding="utf-8")
print("🔧 Quick fix complete:\n" + "\n".join(LOG))
