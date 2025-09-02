
# simplified_main.py

import agent_logic
import workflow_controller  
import profit_tracker
import self_improvement
import time
from datetime import datetime

def main():
    """Main entry point for the AI CEO workflow system"""
    print("🧠 AI CEO Starting Full Workflow...")
    print(f"🕐 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Option 1: Run single cycle
        print("\n🔄 Running single workflow cycle...")
        success = workflow_controller.run_full_system()
        
        if success:
            print("✅ Single cycle completed successfully!")
            
            # Ask user if they want continuous mode
            print("\n💡 Single cycle complete. The system can also run continuously.")
            print("   To start continuous mode, run: python workflow_controller.py")
            
        else:
            print("⚠️ Single cycle had issues. Check logs above.")
            
    except KeyboardInterrupt:
        print("\n🛑 Workflow stopped by user")
    except Exception as e:
        print(f"\n❌ Main workflow error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
