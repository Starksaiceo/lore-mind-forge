
import streamlit as st
import os

# Add immediate console debugging
print("🚀 MINIMAL STREAMLIT TEST STARTING")
print("=" * 50)

st.title("🏥 Streamlit Health Check")

# Show basic info
st.write("✅ Streamlit is working!")
st.write(f"Python path: {os.getcwd()}")

# Simple button test
if st.button("Test Button"):
    st.success("✅ Button interaction works!")
    print("✅ Button clicked successfully!")

# Show session state
if 'counter' not in st.session_state:
    st.session_state.counter = 0

if st.button("Counter Test"):
    st.session_state.counter += 1
    print(f"✅ Counter: {st.session_state.counter}")

st.write(f"Counter: {st.session_state.counter}")

st.info("If you see this page, Streamlit basic functionality works!")
print("✅ Minimal Streamlit app loaded successfully!")
