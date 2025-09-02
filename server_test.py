
#!/usr/bin/env python3
"""Minimal server test to isolate Streamlit startup issues"""

import streamlit as st
import sys
import os

print("🔍 MINIMAL SERVER TEST STARTING")
print("=" * 50)

# Force output flushing
sys.stdout.flush()
sys.stderr.flush()

# Basic Streamlit setup
st.set_page_config(page_title="Server Test", layout="wide")

# Configure environment for Replit
os.environ['STREAMLIT_SERVER_HEADLESS'] = 'true'
os.environ['STREAMLIT_SERVER_ADDRESS'] = '0.0.0.0'
os.environ['STREAMLIT_SERVER_PORT'] = '5000'

print("✅ Environment configured")
sys.stdout.flush()

# Simple content
st.title("🚀 Server Test Success!")
st.write("If you can see this page, the Streamlit server is working properly.")
st.success("✅ Basic Streamlit functionality confirmed!")

# Simple interaction test
if st.button("Test Button"):
    st.balloons()
    st.success("Button interaction works!")
    print("✅ Button clicked successfully!")

st.info("Server test completed - main.py should work now")

print("✅ Streamlit server test completed successfully")
sys.stdout.flush()
