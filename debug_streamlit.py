
import streamlit as st
import sys
import os
import traceback

def main():
    st.title("🔧 Debug Dashboard")
    
    # Check Python and Streamlit
    st.subheader("System Info")
    st.write(f"Python: {sys.version}")
    st.write(f"Streamlit: {st.__version__}")
    
    # Check imports
    st.subheader("Import Check")
    
    modules_to_check = [
        'config', 'agent', 'profit_tracker', 'marketplace_uploader',
        'meta_api_safe', 'payment_processor', 'stripe_utils'
    ]
    
    for module in modules_to_check:
        try:
            __import__(module)
            st.success(f"✅ {module}")
        except Exception as e:
            st.error(f"❌ {module}: {str(e)}")
    
    # Check environment variables
    st.subheader("Environment Check")
    env_vars = [
        'OPENROUTER_API_KEY', 'STRIPE_SECRET_KEY', 'SHOPIFY_ACCESS_TOKEN'
    ]
    
    for var in env_vars:
        value = os.getenv(var)
        if value:
            masked = value[:8] + "..." if len(value) > 8 else "set"
            st.success(f"✅ {var}: {masked}")
        else:
            st.warning(f"⚠️ {var}: not set")
    
    # Check file syntax
    st.subheader("File Syntax Check")
    if st.button("Check profit_sprint.py"):
        try:
            import profit_sprint
            st.success("✅ profit_sprint.py imports successfully")
        except SyntaxError as e:
            st.error(f"❌ Syntax error: {e}")
        except Exception as e:
            st.error(f"❌ Import error: {e}")

if __name__ == "__main__":
    main()
