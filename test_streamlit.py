
import streamlit as st
import os

st.title("🏥 Streamlit Health Check")
st.write("If you can see this, Streamlit is working!")

# Show environment variables
st.subheader("Environment Check")
st.write(f"Port: {os.environ.get('STREAMLIT_SERVER_PORT', '5000')}")
st.write(f"Address: {os.environ.get('STREAMLIT_SERVER_ADDRESS', '0.0.0.0')}")

# Simple button test
if st.button("Test Button"):
    st.success("✅ Button works!")

st.info("Basic Streamlit test complete")
