import agent_logic
import auto_product_builder
import profit_tracker
import time
import json
from datetime import datetime
from marketplace_uploader import upload_to_shopify

# System Configuration
MAX_RETRIES = 3
TASK_BUDGET = 25.00
CYCLE_DELAY = 1800  # 30 minutes between cycles

class WorkflowMetrics:
    def __init__(self):
        self.cycles_completed = 0
        self.total_revenue = 0.0
        self.successful_uploads = 0
        self.failed_steps = []
        self.start_time = datetime.now()

    def log_success(self, step_name, revenue=0.0):
        if step_name == "Upload to Shopify":
            self.successful_uploads += 1
        if revenue > 0:
            self.total_revenue += revenue

    def log_failure(self, step_name, error):
        self.failed_steps.append({
            "step": step_name,
            "error": str(error),
            "timestamp": datetime.now().isoformat()
        })

    def get_performance_summary(self):
        runtime = (datetime.now() - self.start_time).total_seconds() / 3600
        return {
            "cycles": self.cycles_completed,
            "revenue": round(self.total_revenue, 2),
            "uploads": self.successful_uploads,
            "runtime_hours": round(runtime, 2),
            "revenue_per_hour": round(self.total_revenue / runtime, 2) if runtime > 0 else 0,
            "success_rate": round((self.cycles_completed - len(self.failed_steps)) / max(self.cycles_completed, 1) * 100, 1),
            "platform": "Shopify (Gumroad disabled)"
        }

metrics = WorkflowMetrics()

def safe_step(step_func, *args, max_retries=MAX_RETRIES, step_name="Step", critical=False):
    """Enhanced step execution with better error handling and metrics"""
    attempt = 0
    last_error = None

    while attempt <= max_retries:
        try:
            print(f"🔄 {step_name} (Attempt {attempt + 1}/{max_retries + 1})...")

            start_time = time.time()
            result = step_func(*args)
            execution_time = time.time() - start_time

            if result is not False and result is not None:
                print(f"✅ {step_name} completed in {execution_time:.1f}s")

                # Extract revenue if returned
                revenue = 0.0
                if isinstance(result, dict) and "revenue" in result:
                    revenue = result["revenue"]
                elif isinstance(result, dict) and "price" in result:
                    revenue = result["price"]

                metrics.log_success(step_name, revenue)
                return result
            else:
                print(f"⚠️ {step_name} returned empty/false result")

        except Exception as e:
            last_error = e
            print(f"❌ {step_name} error: {str(e)}")
            if attempt < max_retries:
                print(f"🔄 Retrying in 5 seconds...")
                time.sleep(5)

        attempt += 1

    # All attempts failed
    metrics.log_failure(step_name, last_error or "Unknown failure")

    if critical:
        print(f"🚫 CRITICAL: {step_name} failed completely. Aborting cycle.")
        return None
    else:
        print(f"⚠️ {step_name} failed but continuing workflow...")
        return False

def run_full_system():
    """Enhanced main workflow with Shopify focus"""
    cycle_start = time.time()
    cycle_num = metrics.cycles_completed + 1
    print(f"\n🚀 === AI CEO Cycle #{cycle_num} Starting (Shopify-Powered) ===")
    print(f"⏰ Cycle started at: {datetime.now().strftime('%H:%M:%S')}")
    print(f"💰 Available Budget: ${TASK_BUDGET}")

    if TASK_BUDGET <= 0:
        print("⛔ Budget exhausted. Switching to revenue optimization mode...")
        safe_step(profit_tracker.optimize_existing_products, step_name="Optimize Existing")
        return

    # STEP 1: Market Research & Product Generation (CRITICAL)
    print("\n📈 Phase 1: Market Research & Product Development")
    product = safe_step(
        agent_logic.generate_product, 
        step_name="Generate High-Value Product", 
        critical=True
    )

    if not product:
        print("🚫 Cannot proceed without product. Aborting cycle.")
        return

    print(f"🎯 Generated: {product.get('title', 'Unknown Product')} - ${product.get('price', 0)}")

    # STEP 2: Shopify Upload (REPLACES GUMROAD)
    print("\n🛒 Phase 2: Shopify Store Upload")
    shopify_result = safe_step(
        upload_to_shopify, 
        product, 
        step_name="Upload to Shopify",
        critical=True
    )

    if not shopify_result or not shopify_result.get("success"):
        print("⚠️ Shopify upload failed. Skipping promotion.")
        return
    else:
        print(f"✅ Shopify Upload Success: {shopify_result.get('url')}")

        # STEP 3: Social Media Promotion
        print("\n📢 Phase 3: Marketing & Promotion")
        safe_step(
            agent_logic.promote_on_social, 
            product, 
            step_name="Social Media Promotion"
        )

    # STEP 4: Revenue Tracking & Analytics
    print("\n📊 Phase 4: Performance Analysis")
    revenue_data = safe_step(
        profit_tracker.track_revenue, 
        step_name="Track Revenue"
    )

    # Log to external analytics
    safe_step(
        profit_tracker.log_profit,
        product.get("price", 0), 
        f"Shopify Product: {product.get('title', 'Unknown')}", 
        f"ai_ceo_shopify_{int(time.time())}", 
        step_name="Log Performance Data"
    )

    # Cycle completion
    metrics.cycles_completed += 1
    cycle_duration = time.time() - cycle_start

    print(f"\n✅ === Cycle #{metrics.cycles_completed} Complete ===")
    print(f"⏱️ Duration: {cycle_duration:.1f} seconds")
    print(f"🛒 Platform: Shopify (Gumroad disabled)")
    print(f"⏰ Completed at: {datetime.now().strftime('%H:%M:%S')}")

    # Show performance summary every 3 cycles
    if metrics.cycles_completed % 3 == 0:
        print(f"📈 Performance Summary: {metrics.get_performance_summary()}")

    print(f"⏳ Next cycle in {CYCLE_DELAY/60:.0f} minutes...")
    return True

def cron_loop(hours=0.5):
    """Optimized auto-loop with Shopify integration"""
    print(f"🕒 Starting Enhanced Auto-Loop (Shopify-powered)")
    print("🎯 Goal: Maximum revenue generation via Shopify store")

    while True:
        try:
            run_full_system()

            # Dynamic sleep based on performance
            performance = metrics.get_performance_summary()
            if performance["success_rate"] > 80:
                sleep_time = CYCLE_DELAY * 0.75
            elif performance["success_rate"] < 50:
                sleep_time = CYCLE_DELAY * 1.5
            else:
                sleep_time = CYCLE_DELAY

            print(f"😴 Sleeping {sleep_time/60:.1f} minutes before next cycle...")
            time.sleep(sleep_time)

        except KeyboardInterrupt:
            print("\n🛑 Auto-loop stopped by user")
            print(f"📊 Final Performance: {metrics.get_performance_summary()}")
            break
        except Exception as e:
            print(f"🚨 Critical loop error: {e}")
            print("🔄 Restarting in 5 minutes...")
            time.sleep(300)

if __name__ == "__main__":
    print("🧠 AI CEO 2.0 Workflow Controller (Shopify Edition)")
    print("🛒 Gumroad disabled - All uploads go to Shopify")
    print("\nChoose mode:")
    print("1. Single cycle test")
    print("2. Auto-loop (recommended)")

    choice = input("Enter choice (1-2): ").strip()

    if choice == "1":
        run_full_system()
    else:
        cron_loop()