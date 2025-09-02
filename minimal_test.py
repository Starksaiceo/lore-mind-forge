
import streamlit as st
import sys

st.title("🧪 Minimal Test")
st.write("This is a minimal Streamlit app")
st.write(f"Python version: {sys.version}")

if st.button("Test Button"):
    st.success("Button works!")
    
st.write("If you see this, Streamlit is working!")
