
import os
import json
from datetime import datetime, timedelta
from typing import Dict, List

class SocialMediaScheduler:
    def __init__(self):
        self.scheduled_posts = []
        self.posts_file = "scheduled_posts.json"
        self.load_scheduled_posts()
    
    def schedule_post(self, platform: str, content: str, schedule_time: datetime) -> Dict:
        """Schedule a social media post"""
        try:
            post = {
                "id": len(self.scheduled_posts) + 1,
                "platform": platform.lower(),
                "content": content,
                "schedule_time": schedule_time.isoformat(),
                "status": "scheduled",
                "created_at": datetime.now().isoformat()
            }
            
            self.scheduled_posts.append(post)
            self.save_scheduled_posts()
            
            return {"success": True, "post_id": post["id"], "message": f"Post scheduled for {platform}"}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def generate_social_content(self, product_info: Dict, platform: str) -> str:
        """Generate platform-specific content"""
        title = product_info.get('title', 'Digital Product')
        price = product_info.get('price', 29.99)
        
        templates = {
            "facebook": f"🚀 Just launched: {title}!\n\nPerfect for entrepreneurs who want real results.\n\n💰 Special price: ${price}\n🎯 Limited time offer\n\n#Business #Entrepreneur #Success",
            
            "instagram": f"✨ New launch alert! ✨\n\n{title} is here 🔥\n\nSwipe to see what's inside 👉\n\n💵 ${price} only\n⏰ Don't wait!\n\n#NewLaunch #Business #Success #Entrepreneur",
            
            "twitter": f"🚀 {title} is LIVE!\n\nEverything you need to succeed ⬇️\n💰 ${price}\n🔗 Link in bio\n\n#Launch #Business #Success",
            
            "linkedin": f"Excited to announce the launch of {title}!\n\nAfter months of development, we've created something truly valuable for business professionals.\n\nKey features:\n• Immediate implementation\n• Proven results\n• Expert support\n\nAvailable now for ${price}. What do you think?\n\n#Business #Innovation #Professional"
        }
        
        return templates.get(platform.lower(), templates["facebook"])
    
    def get_scheduled_posts(self, platform: str = None) -> List[Dict]:
        """Get scheduled posts, optionally filtered by platform"""
        if platform:
            return [post for post in self.scheduled_posts if post["platform"] == platform.lower()]
        return self.scheduled_posts
    
    def get_ready_posts(self) -> List[Dict]:
        """Get posts ready to be published"""
        now = datetime.now()
        ready_posts = []
        
        for post in self.scheduled_posts:
            if post["status"] == "scheduled":
                schedule_time = datetime.fromisoformat(post["schedule_time"])
                if schedule_time <= now:
                    ready_posts.append(post)
        
        return ready_posts
    
    def mark_published(self, post_id: int) -> Dict:
        """Mark a post as published"""
        for post in self.scheduled_posts:
            if post["id"] == post_id:
                post["status"] = "published"
                post["published_at"] = datetime.now().isoformat()
                self.save_scheduled_posts()
                return {"success": True, "message": "Post marked as published"}
        
        return {"success": False, "error": "Post not found"}
    
    def load_scheduled_posts(self):
        """Load scheduled posts from file"""
        try:
            if os.path.exists(self.posts_file):
                with open(self.posts_file, 'r') as f:
                    self.scheduled_posts = json.load(f)
            else:
                self.scheduled_posts = []
        except Exception:
            self.scheduled_posts = []
    
    def save_scheduled_posts(self):
        """Save scheduled posts to file"""
        try:
            with open(self.posts_file, 'w') as f:
                json.dump(self.scheduled_posts, f, indent=2)
        except Exception as e:
            print(f"Error saving scheduled posts: {e}")

# Helper functions
def schedule_product_launch_posts(product_info: Dict) -> Dict:
    """Schedule a complete social media campaign for a product launch"""
    scheduler = SocialMediaScheduler()
    now = datetime.now()
    scheduled_count = 0
    
    platforms = ["facebook", "instagram", "twitter", "linkedin"]
    
    for i, platform in enumerate(platforms):
        # Schedule posts at different times
        post_time = now + timedelta(hours=i+1)
        content = scheduler.generate_social_content(product_info, platform)
        
        result = scheduler.schedule_post(platform, content, post_time)
        if result["success"]:
            scheduled_count += 1
    
    return {
        "success": True,
        "scheduled_count": scheduled_count,
        "platforms": platforms,
        "message": f"Scheduled {scheduled_count} posts across {len(platforms)} platforms"
    }
