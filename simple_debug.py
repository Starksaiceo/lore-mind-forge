
#!/usr/bin/env python3
import sys
import os

print("🔍 SIMPLE DIAGNOSTIC STARTING")
print(f"Python version: {sys.version}")
print(f"Working directory: {os.getcwd()}")

# Test 1: Basic Streamlit import
try:
    import streamlit as st
    print("✅ Streamlit imports successfully")
    print(f"Streamlit version: {st.__version__}")
except Exception as e:
    print(f"❌ Streamlit import failed: {e}")
    sys.exit(1)

# Test 2: Check main.py syntax
try:
    import py_compile
    py_compile.compile('main.py', doraise=True)
    print("✅ main.py compiles without syntax errors")
except Exception as e:
    print(f"❌ main.py has syntax errors: {e}")
    sys.exit(1)

# Test 3: Test problematic imports
problematic_modules = ['profit_sprint', 'agent', 'autopilot']
for module in problematic_modules:
    try:
        __import__(module)
        print(f"✅ {module} imports successfully")
    except Exception as e:
        print(f"⚠️ {module} import issue: {e}")

# Test 4: Run minimal Streamlit
print("\n🚀 Starting minimal Streamlit test...")
print("If this works, the issue is in main.py imports")

try:
    # Create minimal test content
    with open('temp_test.py', 'w') as f:
        f.write("""
import streamlit as st
print("🎯 Minimal test running in console!")
st.write("📊 Minimal test running in app!")
st.success("✅ Basic Streamlit works!")
""")
    
    print("✅ Created temp_test.py")
    print("Run: streamlit run temp_test.py --server.address=0.0.0.0 --server.port=5000")
    
except Exception as e:
    print(f"❌ Error creating test file: {e}")

print("\n" + "="*50)
print("🔍 DIAGNOSTIC COMPLETE")
