#!/usr/bin/env python3
import os
import sys
import subprocess
import time
import signal

def kill_existing_processes():
    """Kill any existing Streamlit or Flask processes"""
    try:
        subprocess.run(['pkill', '-f', 'streamlit'], check=False)
        subprocess.run(['pkill', '-f', 'flask'], check=False)
        subprocess.run(['pkill', '-f', 'app_saas'], check=False)
        time.sleep(2)
        print("✅ Cleaned up existing processes")
    except Exception as e:
        print(f"⚠️ Process cleanup: {e}")

def start_flask_app():
    """Start the Flask SaaS application"""
    try:
        print("🚀 Starting AI CEO SaaS Application...")

        # Set environment variables
        os.environ['FLASK_APP'] = 'app_saas.py'
        os.environ['FLASK_ENV'] = 'development'

        # Start Flask app
        process = subprocess.Popen([
            sys.executable, 'app_saas.py'
        ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

        print("🌐 Flask app starting on http://0.0.0.0:5000")
        print("📊 Dashboard available at: http://0.0.0.0:5000/dashboard")
        print("🔑 Login with: admin@example.com / test123")
        print("\n📡 Server output:")
        print("=" * 50)

        # Stream output
        for line in iter(process.stdout.readline, ''):
            if line.strip():
                # Filter out audio errors
                if not any(x in line.lower() for x in ['alsa', 'jack', 'sdl_audio', 'pulse']):
                    print(line.rstrip())

    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")
        process.terminate()
    except Exception as e:
        print(f"❌ Failed to start Flask app: {e}")

def main():
    """Main startup function"""
    print("🎯 AI CEO SaaS Platform Startup")
    print("=" * 40)

    # Kill existing processes
    kill_existing_processes()

    # Check if we should run Flask or Streamlit
    if len(sys.argv) > 1 and sys.argv[1] == 'streamlit':
        print("🔄 Starting in Streamlit mode...")
        try:
            subprocess.run([
                sys.executable, '-m', 'streamlit', 'run', 'main.py',
                '--server.address=0.0.0.0',
                '--server.port=5000',
                '--server.headless=true',
                '--browser.gatherUsageStats=false'
            ])
        except Exception as e:
            print(f"❌ Streamlit failed: {e}")
    else:
        # Default to Flask SaaS app
        start_flask_app()

if __name__ == "__main__":
    main()