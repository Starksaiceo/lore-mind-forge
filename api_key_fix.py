
import os
from dotenv import load_dotenv

def validate_and_fix_api_keys():
    """Validate API keys and provide fallbacks"""
    load_dotenv()
    
    # Check OpenRouter API key
    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    if not openrouter_key or "sk-" not in openrouter_key:
        print("⚠️ OpenRouter API key missing or invalid")
        print("💡 Add your OpenRouter API key to Replit Secrets:")
        print("   1. Go to Tools > Secrets")
        print("   2. Add key: OPENROUTER_API_KEY")
        print("   3. Add your sk-or-... key as value")
        return False
    
    print("✅ OpenRouter API key validated")
    return True

def enable_zero_cost_mode():
    """Enable zero-cost fallback mode"""
    os.environ["ZERO_COST_MODE"] = "true"
    print("🆓 Zero-cost mode enabled - using local templates")

if __name__ == "__main__":
    if not validate_and_fix_api_keys():
        enable_zero_cost_mode()
