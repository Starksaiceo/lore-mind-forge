
import time
import schedule
from datetime import datetime
from reinvestment_agent import ReinvestmentAgent, run_agent

class AutonomousLoop:
    """Continuous autonomous reinvestment loop"""
    
    def __init__(self):
        self.agent = ReinvestmentAgent()
        self.loop_interval = 3600  # 1 hour
        self.running = False
        
    def run_continuous_loop(self, max_cycles: int = 24):
        """Run continuous reinvestment loop"""
        print("\n🤖 Starting continuous autonomous loop...")
        print(f"⏰ Will run for {max_cycles} cycles (every hour)")
        
        cycle_count = 0
        self.running = True
        
        while self.running and cycle_count < max_cycles:
            try:
                print(f"\n🔄 Cycle {cycle_count + 1}/{max_cycles}")
                print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                
                # Run reinvestment cycle
                config = {
                    "goal": "Autonomous reinvestment and scaling",
                    "autonomous": True,
                    "loop": True,
                    "track_profit": True,
                    "cycle_number": cycle_count + 1
                }
                
                result = run_agent(config)
                
                if result.get("result") == "success":
                    print(f"✅ Cycle {cycle_count + 1} completed successfully")
                    print(f"💰 Budget allocated: ${result.get('budget_allocated', 0):.2f}")
                elif result.get("result") == "waiting_for_profit":
                    print(f"⏳ Cycle {cycle_count + 1}: Waiting for sufficient profit")
                else:
                    print(f"⚠️ Cycle {cycle_count + 1}: {result.get('result', 'Unknown')}")
                
                cycle_count += 1
                
                # Wait for next cycle (unless it's the last one)
                if cycle_count < max_cycles and self.running:
                    print(f"😴 Sleeping for {self.loop_interval/60:.0f} minutes until next cycle...")
                    time.sleep(self.loop_interval)
                    
            except KeyboardInterrupt:
                print("\n⏹️ Loop stopped by user")
                self.running = False
                break
            except Exception as e:
                print(f"❌ Loop error: {e}")
                cycle_count += 1
                if cycle_count < max_cycles:
                    time.sleep(300)  # Wait 5 minutes on error
        
        print(f"\n🏁 Autonomous loop completed after {cycle_count} cycles")
        return {"cycles_completed": cycle_count, "final_status": "completed"}
    
    def stop_loop(self):
        """Stop the continuous loop"""
        self.running = False
        print("🛑 Stopping autonomous loop...")

if __name__ == "__main__":
    import sys
    
    max_cycles = int(sys.argv[1]) if len(sys.argv) > 1 else 24
    
    loop = AutonomousLoop()
    try:
        loop.run_continuous_loop(max_cycles)
    except KeyboardInterrupt:
        loop.stop_loop()
