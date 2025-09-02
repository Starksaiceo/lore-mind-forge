import os, asyncio, json, random
from datetime import datetime, timedelta
from db_autopilot import init_autopilot_tables, get_autopilot_users, record_activity
from business_autopilot import run_batch_cycles, run_profit_cycle
from replit_db import replit_db_manager
from content_automation import content_automation, post_to_all_platforms
from ads_automation import ads_automation, launch_multi_platform_campaign

AUTOPILOT_ENABLED = os.getenv("AUTOPILOT_ENABLED", "true").lower() == "true"
INTERVAL_MINUTES = int(os.getenv("AUTOPILOT_INTERVAL_MINUTES", "30"))

class AutopilotManager:
    def __init__(self):
        self.running = False
        self.task = None

    async def start(self):
        """Start the autopilot background loop"""
        if not AUTOPILOT_ENABLED:
            print("⚠️ Autopilot disabled by environment variable")
            return

        if self.running:
            print("⚠️ Autopilot already running")
            return

        print(f"🚀 Starting autopilot manager (interval: {INTERVAL_MINUTES} minutes)")

        # Initialize autopilot tables
        init_autopilot_tables()

        self.running = True
        self.task = asyncio.create_task(self._autopilot_loop())

    async def stop(self):
        """Stop the autopilot background loop"""
        if self.task:
            self.running = False
            self.task.cancel()
            try:
                await self.task
            except asyncio.CancelledError:
                pass
            print("🛑 Autopilot manager stopped")

    async def _autopilot_loop(self):
        """Main autopilot loop"""
        while self.running:
            try:
                await self._run_autopilot_cycle()
                await asyncio.sleep(INTERVAL_MINUTES * 60)
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"❌ Autopilot loop error: {e}")
                await asyncio.sleep(60)  # Wait 1 minute on error

    async def _run_autopilot_cycle(self):
        """Run one autopilot cycle for all eligible users"""
        try:
            users = get_autopilot_users()
            if not users:
                print("📭 No users with autopilot enabled")
                return

            print(f"🤖 Running autopilot cycle for {len(users)} users")

            # Run cycles in batches to avoid overwhelming the system
            batch_size = 5
            for i in range(0, len(users), batch_size):
                batch = users[i:i + batch_size]
                print(f"🔄 Processing batch {i//batch_size + 1}: {len(batch)} users")

                results = await run_batch_cycles(batch, max_concurrent=3)

                # Log results
                successful = sum(1 for r in results if isinstance(r, dict) and r.get("success"))
                print(f"✅ Batch complete: {successful}/{len(batch)} successful cycles")

                # Brief pause between batches
                if i + batch_size < len(users):
                    await asyncio.sleep(5)

            print(f"🎉 Autopilot cycle complete for all {len(users)} users")

        except Exception as e:
            print(f"❌ Autopilot cycle error: {e}")

# Global autopilot manager instance
autopilot_manager = AutopilotManager()

async def start_autopilot():
    """Start autopilot (called from app startup)"""
    await autopilot_manager.start()

async def stop_autopilot():
    """Stop autopilot (called from app shutdown)"""
    await autopilot_manager.stop()

async def get_trending_topics():
    """Placeholder for getting trending topics"""
    # In a real scenario, this would fetch trending topics from an external API or service
    return [{"topic": "AI in Business", "source": "news"}, {"topic": "Remote Work Trends", "source": "social"}]

async def run_manual_cycle(user_id: int):
    """Run a manual autopilot cycle for a specific user"""
    try:
        print(f"🔄 Running manual cycle for user {user_id}")

        # Get trending topics for ideas
        trends = await get_trending_topics()

        # Run the profit cycle
        result = await run_profit_cycle(user_id)

        # Growth Engine integration
        growth_enabled = os.getenv('GROWTH_ENABLED', 'true').lower() == 'true'
        growth_result = {"enabled": growth_enabled}

        if growth_enabled:
            try:
                # Generate and post content
                growth_result.update(await run_growth_cycle(user_id, result))
            except Exception as e:
                print(f"⚠️ Growth Engine error: {e}")
                growth_result["error"] = str(e)

        record_activity(user_id, "manual_cycle", "Manual autopilot cycle completed", 
                       0.0, json.dumps({**result, "growth": growth_result}))

        return {
            "success": True,
            "result": result,
            "growth": growth_result,
            "trends_analyzed": len(trends)
        }

    except Exception as e:
        error_msg = f"Manual cycle error: {str(e)}"
        record_activity(user_id, "error", error_msg, 0.0)
        print(f"❌ {error_msg}")
        return {"success": False, "error": error_msg}

async def run_growth_cycle(user_id: int, profit_result: dict) -> dict:
    """Run Growth Engine cycle"""
    try:
        from content_engine import generate_social_calendar, write_social_post
        from social_publisher import social_publisher
        from ad_manager import ad_manager

        growth_results = {"posts": [], "ads": [], "simulated": True}

        # Check if we have a new product to promote
        new_product = profit_result.get("product")
        if new_product:
            # Launch ads for new product
            budget_daily = float(os.getenv('GROWTH_DAILY_AD_BUDGET', '10.0'))
            if budget_daily > 0:
                ad_result = ad_manager.launch_ads(user_id, new_product, "traffic", budget_daily)
                growth_results["ads"].append(ad_result)
                print(f"📢 Launched ads for {new_product.get('title', 'product')}")

        # Generate daily content
        daily_posts = int(os.getenv('GROWTH_DAILY_POSTS', '1'))
        if daily_posts > 0:
            # Generate content calendar
            niches = ["business", "ai", "productivity", "entrepreneurship"]
            calendar_result = generate_social_calendar(user_id, niches, "daily")

            if calendar_result["success"]:
                # Get today's content ideas
                today_posts = calendar_result["calendar"]["calendar"][0]["posts"][:daily_posts]

                for post_idea in today_posts:
                    # Write social post
                    post_result = write_social_post(user_id, post_idea, "instagram")

                    if post_result["success"]:
                        # Post to multiple platforms
                        platforms = post_idea.get("platforms", ["instagram", "x"])

                        for platform in platforms[:2]:  # Limit to 2 platforms per post
                            try:
                                if platform == "instagram":
                                    publish_result = social_publisher.post_to_instagram(
                                        user_id, 
                                        post_result["post"]["copy"]
                                    )
                                elif platform == "x":
                                    publish_result = social_publisher.post_to_x(
                                        user_id, 
                                        post_result["post"]["copy"][:280]  # Twitter character limit
                                    )
                                else:
                                    continue

                                growth_results["posts"].append(publish_result)
                                print(f"📱 Posted to {platform}: {post_result['post']['copy'][:50]}...")

                                # Rate limiting
                                await asyncio.sleep(random.uniform(2, 5))

                            except Exception as e:
                                print(f"⚠️ Platform {platform} posting error: {e}")

        # Record growth activity
        record_activity(user_id, "growth", f"Growth cycle: {len(growth_results['posts'])} posts, {len(growth_results['ads'])} ads",
                       0.0, json.dumps(growth_results))

        return growth_results

    except Exception as e:
        print(f"❌ Growth cycle error: {e}")
        return {"error": str(e)}

async def run_content_only_cycle(user_id: int):
    """Run content-only cycle when no new products exist"""
    try:
        from content_engine import make_caption_pack
        from social_publisher import social_publisher

        # Generate funny/engaging captions
        caption_result = make_caption_pack(user_id, "funny")

        if caption_result["success"]:
            # Post one random caption
            import random
            caption = random.choice(caption_result["captions"])

            # Post to Instagram
            result = social_publisher.post_to_instagram(user_id, caption["text"])

            record_activity(user_id, "content", f"Posted content-only update: {caption['text'][:50]}...",
                           0.0, json.dumps(result))

            return {"success": True, "posted": result}

        return {"success": False, "error": "Caption generation failed"}

    except Exception as e:
        return {"success": False, "error": str(e)}