
#!/usr/bin/env python3
import subprocess
import sys
import time
import os

def main():
    print("🔧 Debug: Starting Streamlit with full logging...")
    
    # Set environment variables for better debugging
    os.environ['STREAMLIT_SERVER_HEADLESS'] = 'true'
    os.environ['STREAMLIT_BROWSER_GATHER_USAGE_STATS'] = 'false'
    os.environ['STREAMLIT_SERVER_ADDRESS'] = '0.0.0.0'
    os.environ['STREAMLIT_SERVER_PORT'] = '5000'
    
    print("🔧 Debug: Environment variables set")
    
    # Kill any existing streamlit processes
    try:
        subprocess.run(['pkill', '-f', 'streamlit'], check=False)
        print("🔧 Debug: Killed existing streamlit processes")
        time.sleep(2)
    except Exception as e:
        print(f"🔧 Debug: Error killing processes: {e}")
    
    # Check if main.py exists and has basic syntax
    if os.path.exists('main.py'):
        print("✅ main.py exists")
        try:
            with open('main.py', 'r') as f:
                content = f.read()
                if 'import streamlit as st' in content:
                    print("✅ main.py contains streamlit import")
                else:
                    print("❌ main.py missing streamlit import")
        except Exception as e:
            print(f"❌ Error reading main.py: {e}")
    else:
        print("❌ main.py not found")
    
    # Try to start streamlit with verbose output
    cmd = [
        sys.executable, '-m', 'streamlit', 'run', 'main.py',
        '--server.address=0.0.0.0',
        '--server.port=5000',
        '--server.headless=true',
        '--browser.gatherUsageStats=false',
        '--server.enableCORS=true',
        '--server.enableXsrfProtection=false',
        '--server.enableWebsocketCompression=false',
        '--logger.level=debug'
    ]
    
    print(f"🔧 Debug: Running command: {' '.join(cmd)}")
    
    try:
        # Run with real-time output
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        print("🔧 Debug: Streamlit process started, showing output:")
        print("=" * 50)
        
        for line in iter(process.stdout.readline, ''):
            print(line.rstrip())
            sys.stdout.flush()
            
    except KeyboardInterrupt:
        print("\n🔧 Debug: Interrupted by user")
        process.terminate()
    except Exception as e:
        print(f"❌ Error starting streamlit: {e}")

if __name__ == "__main__":
    main()
