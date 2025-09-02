
#!/usr/bin/env python3
"""Real-time sprint monitoring with console streaming"""

import time
import json
from datetime import datetime

def monitor_sprint_real_time():
    """Monitor the profit sprint in real-time with console output"""
    print("🔍 Starting real-time sprint monitoring...")
    print("Press Ctrl+C to stop monitoring (sprint continues in background)")
    print("-" * 60)
    
    try:
        from profit_sprint import get_sprint_status
        
        while True:
            try:
                status = get_sprint_status()
                
                # Clear previous output (simple version)
                print(f"\n[{datetime.now().strftime('%H:%M:%S')}] SPRINT STATUS:")
                print(f"• Running: {'✅' if status.get('running') else '❌'}")
                print(f"• Products Verified: {status.get('products_verified', 0)}")
                print(f"• Real Earnings: {status.get('total_real_earnings', '$0.00')}")
                print(f"• Hours Remaining: {status.get('hours_remaining', 'N/A')}")
                
                # Show recent verified products
                verified = status.get('verified_products', [])
                if verified:
                    print(f"• Last Product: {verified[-1].get('title', 'Unknown')}")
                
                # Check for CSV exports
                try:
                    import os
                    export_files = [f for f in os.listdir('export') if f.startswith('products_')]
                    if export_files:
                        print(f"• CSV Exports: {len(export_files)} files ready")
                except:
                    pass
                
                print("-" * 40)
                
                # Wait 30 seconds before next update
                time.sleep(30)
                
            except KeyboardInterrupt:
                print("\n🛑 Monitoring stopped (sprint continues in background)")
                break
            except Exception as e:
                print(f"⚠️ Monitoring error: {e}")
                time.sleep(10)
                
    except Exception as e:
        print(f"❌ Monitor startup error: {e}")

if __name__ == "__main__":
    monitor_sprint_real_time()
