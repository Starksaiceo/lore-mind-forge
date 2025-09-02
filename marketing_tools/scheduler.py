
import os
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MarketingScheduler:
    """Marketing content scheduler using APScheduler"""
    
    def __init__(self, db_url: str = "sqlite:///marketing_jobs.db"):
        self.jobstore = SQLAlchemyJobStore(url=db_url)
        self.scheduler = BackgroundScheduler(
            jobstores={'default': self.jobstore},
            job_defaults={'coalesce': False, 'max_instances': 3}
        )
        self.scheduler.start()
        logger.info("✅ Marketing scheduler started")

    def schedule_social_post(self, platform: str, content: Dict[str, Any], run_at: datetime, user_id: int) -> str:
        """Schedule a social media post"""
        try:
            job_id = f"social_{platform}_{user_id}_{int(run_at.timestamp())}"
            
            self.scheduler.add_job(
                func=self._execute_social_post,
                trigger=DateTrigger(run_date=run_at),
                args=[platform, content, user_id],
                id=job_id,
                name=f"Social post to {platform}",
                replace_existing=True
            )
            
            logger.info(f"📅 Scheduled {platform} post for {run_at}")
            return job_id
            
        except Exception as e:
            logger.error(f"❌ Schedule social post failed: {e}")
            return ""

    def schedule_email_campaign(self, email_data: Dict[str, Any], send_at: datetime, user_id: int) -> str:
        """Schedule an email campaign"""
        try:
            job_id = f"email_{user_id}_{int(send_at.timestamp())}"
            
            self.scheduler.add_job(
                func=self._execute_email_send,
                trigger=DateTrigger(run_date=send_at),
                args=[email_data, user_id],
                id=job_id,
                name=f"Email campaign: {email_data.get('subject', 'Untitled')}",
                replace_existing=True
            )
            
            logger.info(f"📧 Scheduled email for {send_at}")
            return job_id
            
        except Exception as e:
            logger.error(f"❌ Schedule email failed: {e}")
            return ""

    def schedule_ad_campaign(self, ad_data: Dict[str, Any], start_at: datetime, user_id: int) -> str:
        """Schedule an ad campaign launch"""
        try:
            job_id = f"ad_{ad_data.get('platform', 'unknown')}_{user_id}_{int(start_at.timestamp())}"
            
            self.scheduler.add_job(
                func=self._execute_ad_launch,
                trigger=DateTrigger(run_date=start_at),
                args=[ad_data, user_id],
                id=job_id,
                name=f"Ad campaign: {ad_data.get('headline', 'Untitled')}",
                replace_existing=True
            )
            
            logger.info(f"🎯 Scheduled ad campaign for {start_at}")
            return job_id
            
        except Exception as e:
            logger.error(f"❌ Schedule ad campaign failed: {e}")
            return ""

    def _execute_social_post(self, platform: str, content: Dict[str, Any], user_id: int):
        """Execute scheduled social media post"""
        try:
            # Save to content_ready_to_post for manual posting
            os.makedirs("content_ready_to_post", exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M")
            filename = f"content_ready_to_post/{platform}_post_{timestamp}.json"
            
            post_data = {
                "platform": platform,
                "user_id": user_id,
                "content": content,
                "scheduled_at": datetime.now().isoformat(),
                "status": "ready_to_post"
            }
            
            with open(filename, 'w') as f:
                json.dump(post_data, f, indent=2)
            
            logger.info(f"📱 {platform} post ready: {filename}")
            
            # In a real implementation, you would integrate with platform APIs here
            # For now, we save to file for manual posting
            
        except Exception as e:
            logger.error(f"❌ Social post execution failed: {e}")

    def _execute_email_send(self, email_data: Dict[str, Any], user_id: int):
        """Execute scheduled email send"""
        try:
            # Save to content_ready_to_post for manual sending
            os.makedirs("content_ready_to_post", exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M")
            filename = f"content_ready_to_post/email_campaign_{timestamp}.json"
            
            campaign_data = {
                "user_id": user_id,
                "email_data": email_data,
                "scheduled_at": datetime.now().isoformat(),
                "status": "ready_to_send"
            }
            
            with open(filename, 'w') as f:
                json.dump(campaign_data, f, indent=2)
            
            logger.info(f"📧 Email campaign ready: {filename}")
            
            # In a real implementation, you would integrate with email service here
            
        except Exception as e:
            logger.error(f"❌ Email execution failed: {e}")

    def _execute_ad_launch(self, ad_data: Dict[str, Any], user_id: int):
        """Execute scheduled ad campaign launch"""
        try:
            # Save to content_ready_to_post for manual launch
            os.makedirs("content_ready_to_post", exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M")
            filename = f"content_ready_to_post/ad_campaign_{timestamp}.json"
            
            campaign_data = {
                "user_id": user_id,
                "ad_data": ad_data,
                "scheduled_at": datetime.now().isoformat(),
                "status": "ready_to_launch"
            }
            
            with open(filename, 'w') as f:
                json.dump(campaign_data, f, indent=2)
            
            logger.info(f"🎯 Ad campaign ready: {filename}")
            
            # In a real implementation, you would integrate with ad platform APIs here
            
        except Exception as e:
            logger.error(f"❌ Ad execution failed: {e}")

    def get_scheduled_jobs(self, user_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get list of scheduled jobs"""
        try:
            jobs = []
            for job in self.scheduler.get_jobs():
                job_info = {
                    "id": job.id,
                    "name": job.name,
                    "next_run": job.next_run_time.isoformat() if job.next_run_time else None,
                    "args": job.args
                }
                
                # Filter by user_id if provided
                if user_id is None or (len(job.args) > 2 and job.args[2] == user_id):
                    jobs.append(job_info)
            
            return jobs
            
        except Exception as e:
            logger.error(f"❌ Get scheduled jobs failed: {e}")
            return []

    def cancel_job(self, job_id: str) -> bool:
        """Cancel a scheduled job"""
        try:
            self.scheduler.remove_job(job_id)
            logger.info(f"🗑️ Cancelled job: {job_id}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Cancel job failed: {e}")
            return False

    def schedule_content_series(self, content_list: List[Dict], start_date: datetime, interval_hours: int, user_id: int) -> List[str]:
        """Schedule a series of content posts"""
        job_ids = []
        current_date = start_date
        
        for i, content in enumerate(content_list):
            if content.get('type') == 'social':
                job_id = self.schedule_social_post(
                    content.get('platform', 'facebook'),
                    content,
                    current_date,
                    user_id
                )
            elif content.get('type') == 'email':
                job_id = self.schedule_email_campaign(
                    content,
                    current_date,
                    user_id
                )
            else:
                continue
            
            if job_id:
                job_ids.append(job_id)
            
            current_date += timedelta(hours=interval_hours)
        
        logger.info(f"📅 Scheduled {len(job_ids)} content pieces")
        return job_ids

    def get_marketing_calendar(self, user_id: int, days: int = 30) -> Dict[str, List]:
        """Get marketing calendar for user"""
        try:
            calendar = {}
            jobs = self.get_scheduled_jobs(user_id)
            
            for job in jobs:
                if job['next_run']:
                    date_key = job['next_run'][:10]  # YYYY-MM-DD
                    if date_key not in calendar:
                        calendar[date_key] = []
                    calendar[date_key].append(job)
            
            return calendar
            
        except Exception as e:
            logger.error(f"❌ Get marketing calendar failed: {e}")
            return {}

    def shutdown(self):
        """Shutdown the scheduler"""
        self.scheduler.shutdown()
        logger.info("🛑 Marketing scheduler stopped")

# Global scheduler instance
marketing_scheduler = MarketingScheduler()

# Helper functions
def schedule_social_post(platform: str, content: Dict, run_at: datetime, user_id: int) -> str:
    return marketing_scheduler.schedule_social_post(platform, content, run_at, user_id)

def schedule_email_campaign(email_data: Dict, send_at: datetime, user_id: int) -> str:
    return marketing_scheduler.schedule_email_campaign(email_data, send_at, user_id)

def get_scheduled_jobs(user_id: int) -> List[Dict]:
    return marketing_scheduler.get_scheduled_jobs(user_id)

def cancel_job(job_id: str) -> bool:
    return marketing_scheduler.cancel_job(job_id)

# Export for use in other modules
__all__ = ['MarketingScheduler', 'marketing_scheduler', 'schedule_social_post', 'schedule_email_campaign', 'get_scheduled_jobs', 'cancel_job']
