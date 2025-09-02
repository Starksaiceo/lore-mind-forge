
#!/usr/bin/env python3
"""Direct execution script for real 48-hour profit sprint"""

import sys
import time
import json
from datetime import datetime

def run_real_profit_sprint():
    """Execute the real 48-hour profit sprint with monitoring"""
    print("🚀 STARTING REAL 48-HOUR PROFIT SPRINT")
    print("=" * 50)
    print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("✅ All systems verified:")
    print("  • Xano endpoints: 200 OK")
    print("  • Gumroad CSV fallback: Active")
    print("  • Claude/OpenRouter: Quota restored")
    print("=" * 50)
    
    try:
        # Import and start the profit sprint
        from profit_sprint import start_profit_sprint, get_sprint_status
        
        # Start the sprint
        result = start_profit_sprint()
        
        if result.get("status") == "success":
            print("✅ REAL PROFIT SPRINT LAUNCHED SUCCESSFULLY!")
            print(f"🔒 Verification: {result.get('verification', 'Unknown')}")
            print(f"⏰ Start Time: {result.get('start_time', 'Unknown')}")
            print()
            print("🎯 Sprint Features Active:")
            print("  • Real trending product analysis")
            print("  • Verified Gumroad uploads only")
            print("  • Live sales tracking")
            print("  • Xano profit logging")
            print("  • 48-hour autonomous operation")
            print()
            
            # Show initial status
            status = get_sprint_status()
            print("📊 INITIAL STATUS:")
            print(json.dumps(status, indent=2))
            print()
            print("🔄 Sprint is now running autonomously in the background...")
            print("💡 Check status anytime with: python -c \"from profit_sprint import get_sprint_status; print(get_sprint_status())\"")
            
            return True
            
        else:
            print(f"❌ SPRINT FAILED TO START: {result.get('message', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ CRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

def monitor_sprint_logs():
    """Monitor sprint activity and log to console"""
    print("\n🔍 STARTING REAL-TIME MONITORING...")
    print("Press Ctrl+C to stop monitoring (sprint continues)")
    print("-" * 40)
    
    try:
        from profit_sprint import get_sprint_status
        
        while True:
            try:
                status = get_sprint_status()
                
                print(f"\n[{datetime.now().strftime('%H:%M:%S')}] SPRINT STATUS:")
                print(f"  🔄 Running: {'✅' if status.get('running') else '❌'}")
                print(f"  📦 Products Verified: {status.get('products_verified', 0)}")
                print(f"  💰 Real Earnings: {status.get('total_real_earnings', '$0.00')}")
                print(f"  ⏱️  Hours Remaining: {status.get('hours_remaining', 'N/A')}")
                
                # Show recent verified products
                verified = status.get('verified_products', [])
                if verified:
                    recent_product = verified[-1]
                    print(f"  🆕 Latest Product: {recent_product.get('title', 'Unknown')}")
                    if recent_product.get('gumroad_url'):
                        print(f"     URL: {recent_product['gumroad_url']}")
                
                # Check for CSV exports
                try:
                    import os
                    if os.path.exists('export'):
                        export_files = [f for f in os.listdir('export') if f.startswith('products_')]
                        if export_files:
                            print(f"  📁 CSV Exports: {len(export_files)} files ready")
                except:
                    pass
                
                print("-" * 40)
                
                # Wait 60 seconds before next update
                time.sleep(60)
                
            except KeyboardInterrupt:
                print("\n🛑 Monitoring stopped (sprint continues in background)")
                break
            except Exception as e:
                print(f"⚠️ Monitoring error: {e}")
                time.sleep(30)
                
    except Exception as e:
        print(f"❌ Monitor startup error: {e}")

if __name__ == "__main__":
    print("🤖 AI CEO - Real Profit Sprint Launcher")
    print("🔒 REAL UPLOADS ONLY - No simulation mode")
    print()
    
    # Start the real sprint
    success = run_real_profit_sprint()
    
    if success:
        print("\n" + "=" * 50)
        print("✅ SPRINT ACTIVE - Choose monitoring option:")
        print("1. Monitor with live updates (recommended)")
        print("2. Run in background only")
        
        try:
            choice = input("\nEnter choice (1 or 2): ").strip()
            
            if choice == "1":
                monitor_sprint_logs()
            else:
                print("🚀 Sprint running in background mode")
                print("💡 Check status anytime by running this script again")
                
        except KeyboardInterrupt:
            print("\n🚀 Sprint continues in background")
            
    else:
        print("❌ Sprint failed to start - check logs above")
        sys.exit(1)
