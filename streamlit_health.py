
import streamlit as st
import time
import os

def main():
    """Simple health check for Streamlit"""
    st.title("🏥 Streamlit Health Check")
    
    # Check environment
    st.subheader("Environment Check")
    st.write(f"**Port:** {os.environ.get('STREAMLIT_SERVER_PORT', '5000')}")
    st.write(f"**Address:** {os.environ.get('STREAMLIT_SERVER_ADDRESS', '0.0.0.0')}")
    st.write(f"**Headless:** {os.environ.get('STREAMLIT_SERVER_HEADLESS', 'true')}")
    
    # Check time
    st.subheader("Server Status")
    st.write(f"**Current Time:** {time.strftime('%Y-%m-%d %H:%M:%S')}")
    st.success("✅ Streamlit is running!")
    
    # Simple counter to verify updates
    if 'counter' not in st.session_state:
        st.session_state.counter = 0
    
    if st.button("Test Button"):
        st.session_state.counter += 1
    
    st.write(f"**Button clicks:** {st.session_state.counter}")

if __name__ == "__main__":
    main()
