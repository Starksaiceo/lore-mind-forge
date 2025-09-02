
#!/usr/bin/env python3
"""Console output diagnostic - run this to test if console is working"""

import sys
import time
import os

print("🔍 CONSOLE DIAGNOSTIC STARTING")
print("=" * 50)

# Test 1: Basic output
print("✅ Basic print() works")
sys.stdout.flush()

# Test 2: Environment check  
print(f"🔍 Python: {sys.version[:20]}")
print(f"🔍 Working dir: {os.getcwd()}")
print(f"🔍 Environment vars: {len(os.environ)}")
sys.stdout.flush()

# Test 3: Streamlit import
try:
    import streamlit as st
    print(f"✅ Streamlit {st.__version__} imports OK")
except Exception as e:
    print(f"❌ Streamlit import failed: {e}")

sys.stdout.flush()

# Test 4: Check main.py syntax
try:
    import py_compile
    py_compile.compile('main.py', doraise=True)
    print("✅ main.py syntax is valid")
except Exception as e:
    print(f"❌ main.py syntax error: {e}")

sys.stdout.flush()

# Test 5: Check problematic imports
modules_to_test = ['agent', 'profit_sprint', 'autopilot']
for module in modules_to_test:
    try:
        __import__(module)
        print(f"✅ {module} imports OK")
    except Exception as e:
        print(f"⚠️ {module} import issue: {e}")
    sys.stdout.flush()

print("=" * 50)
print("🎯 CONSOLE TEST COMPLETE")
print("🔍 If you see this message, your Console tab IS working!")
print("🔍 The issue may be with:")
print("   • Import errors blocking Streamlit startup")
print("   • 502 errors preventing server start")
print("   • Logger level suppressing output")
print("=" * 50)
