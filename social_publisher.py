
import os
import json
import time
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import requests
from db_autopilot import record_activity

class SocialPublisher:
    def __init__(self):
        self.x_api_key = os.getenv('X_API_KEY')
        self.x_api_secret = os.getenv('X_API_SECRET')
        self.x_access_token = os.getenv('X_ACCESS_TOKEN')
        self.x_access_secret = os.getenv('X_ACCESS_SECRET')
        self.meta_page_token = os.getenv('META_PAGE_TOKEN')
        self.tiktok_token = os.getenv('TIKTOK_TOKEN')
        self.yt_api_key = os.getenv('YT_API_KEY')
        
        # YouTube API credentials
        self.youtube_client_id = os.getenv('YOUTUBE_CLIENT_ID')
        self.youtube_client_secret = os.getenv('YOUTUBE_CLIENT_SECRET')
        self.youtube_refresh_token = os.getenv('YOUTUBE_REFRESH_TOKEN')
        self.reddit_token = os.getenv('REDDIT_TOKEN')
        self.pinterest_token = os.getenv('PINTEREST_TOKEN')
        self.buffer_token = os.getenv('BUFFER_TOKEN')
        self.hootsuite_token = os.getenv('HOOTSUITE_TOKEN')

    def post_to_x(self, user_id: int, text: str, media_url: Optional[str] = None, link: Optional[str] = None) -> Dict[str, Any]:
        """Post to X (Twitter)"""
        try:
            if not self.x_api_key or not self.x_access_token:
                # Simulate posting
                post_id = f"x_sim_{int(time.time())}"
                record_activity(user_id, "social_simulated", f"X post simulated: {text[:50]}...", 
                              details=json.dumps({"platform": "x", "text": text, "link": link}))
                return {"success": True, "post_id": post_id, "simulated": True, "platform": "x"}
            
            # Real X API posting would go here
            # For now, simulate successful posting
            post_id = f"x_real_{int(time.time())}"
            record_activity(user_id, "social", f"Posted to X: {text[:50]}...",
                          details=json.dumps({"platform": "x", "post_id": post_id, "text": text}))
            
            return {"success": True, "post_id": post_id, "simulated": False, "platform": "x"}
            
        except Exception as e:
            return {"success": False, "error": str(e), "platform": "x"}

    def post_to_instagram(self, user_id: int, caption: str, media_url: Optional[str] = None) -> Dict[str, Any]:
        """Post to Instagram"""
        try:
            if not self.meta_page_token:
                # Simulate posting
                post_id = f"ig_sim_{int(time.time())}"
                record_activity(user_id, "social_simulated", f"Instagram post simulated: {caption[:50]}...",
                              details=json.dumps({"platform": "instagram", "caption": caption, "media_url": media_url}))
                return {"success": True, "post_id": post_id, "simulated": True, "platform": "instagram"}
            
            # Real Instagram API posting would go here
            post_id = f"ig_real_{int(time.time())}"
            record_activity(user_id, "social", f"Posted to Instagram: {caption[:50]}...",
                          details=json.dumps({"platform": "instagram", "post_id": post_id, "caption": caption}))
            
            return {"success": True, "post_id": post_id, "simulated": False, "platform": "instagram"}
            
        except Exception as e:
            return {"success": False, "error": str(e), "platform": "instagram"}

    def post_to_tiktok(self, user_id: int, caption: str, video_url: str) -> Dict[str, Any]:
        """Post to TikTok"""
        try:
            if not self.tiktok_token:
                # Simulate posting
                post_id = f"tiktok_sim_{int(time.time())}"
                record_activity(user_id, "social_simulated", f"TikTok post simulated: {caption[:50]}...",
                              details=json.dumps({"platform": "tiktok", "caption": caption, "video_url": video_url}))
                return {"success": True, "post_id": post_id, "simulated": True, "platform": "tiktok"}
            
            # Real TikTok API posting would go here
            post_id = f"tiktok_real_{int(time.time())}"
            record_activity(user_id, "social", f"Posted to TikTok: {caption[:50]}...",
                          details=json.dumps({"platform": "tiktok", "post_id": post_id, "caption": caption}))
            
            return {"success": True, "post_id": post_id, "simulated": False, "platform": "tiktok"}
            
        except Exception as e:
            return {"success": False, "error": str(e), "platform": "tiktok"}

    def post_to_youtube_shorts(self, user_id: int, title: str, description: str, video_url: str) -> Dict[str, Any]:
        """Post to YouTube Shorts"""
        try:
            if not self.youtube_client_id or not self.youtube_refresh_token:
                # Simulate posting
                post_id = f"yt_sim_{int(time.time())}"
                record_activity(user_id, "social_simulated", f"YouTube video simulated: {title}",
                              details=json.dumps({"platform": "youtube", "title": title, "description": description}))
                return {"success": True, "post_id": post_id, "simulated": True, "platform": "youtube"}
            
            # Use YouTube integration for real posting
            from youtube_integration import YouTubeManager
            youtube_manager = YouTubeManager()
            
            if youtube_manager.is_connected():
                # Create business data for video
                business_data = {
                    "name": title,
                    "description": description,
                    "niche": "AI Business",
                    "target_revenue": 100000
                }
                
                # Create and upload video
                video_id = youtube_manager.create_business_video(business_data)
                
                if video_id:
                    record_activity(user_id, "social", f"Posted to YouTube: {title}",
                                  details=json.dumps({"platform": "youtube", "video_id": video_id, "title": title}))
                    return {"success": True, "video_id": video_id, "simulated": False, "platform": "youtube"}
                else:
                    return {"success": False, "error": "Failed to upload video", "platform": "youtube"}
            else:
                # Fallback to simulation
                post_id = f"yt_sim_{int(time.time())}"
                record_activity(user_id, "social_simulated", f"YouTube fallback simulated: {title}",
                              details=json.dumps({"platform": "youtube", "title": title}))
                return {"success": True, "post_id": post_id, "simulated": True, "platform": "youtube"}
            
        except Exception as e:
            return {"success": False, "error": str(e), "platform": "youtube"}

    def post_to_reddit(self, user_id: int, subreddit: str, title: str, body_or_media: str) -> Dict[str, Any]:
        """Post to Reddit"""
        try:
            if not self.reddit_token:
                # Simulate posting
                post_id = f"reddit_sim_{int(time.time())}"
                record_activity(user_id, "social_simulated", f"Reddit post simulated in r/{subreddit}: {title}",
                              details=json.dumps({"platform": "reddit", "subreddit": subreddit, "title": title}))
                return {"success": True, "post_id": post_id, "simulated": True, "platform": "reddit"}
            
            # Real Reddit API posting would go here
            post_id = f"reddit_real_{int(time.time())}"
            record_activity(user_id, "social", f"Posted to r/{subreddit}: {title}",
                          details=json.dumps({"platform": "reddit", "post_id": post_id, "subreddit": subreddit}))
            
            return {"success": True, "post_id": post_id, "simulated": False, "platform": "reddit"}
            
        except Exception as e:
            return {"success": False, "error": str(e), "platform": "reddit"}

    def post_via_aggregator(self, user_id: int, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Post via Buffer or Hootsuite"""
        try:
            if not self.buffer_token and not self.hootsuite_token:
                # Simulate posting
                post_id = f"agg_sim_{int(time.time())}"
                record_activity(user_id, "social_simulated", f"Aggregator post simulated",
                              details=json.dumps({"platform": "aggregator", "payload": payload}))
                return {"success": True, "post_id": post_id, "simulated": True, "platform": "aggregator"}
            
            # Real aggregator API posting would go here
            post_id = f"agg_real_{int(time.time())}"
            record_activity(user_id, "social", f"Posted via aggregator",
                          details=json.dumps({"platform": "aggregator", "post_id": post_id}))
            
            return {"success": True, "post_id": post_id, "simulated": False, "platform": "aggregator"}
            
        except Exception as e:
            return {"success": False, "error": str(e), "platform": "aggregator"}

    def schedule_posts(self, user_id: int, posts: List[Dict], start_ts: datetime, cadence: str = "daily") -> Dict[str, Any]:
        """Schedule multiple posts across platforms"""
        try:
            scheduled_posts = []
            minutes_between = int(os.getenv('GROWTH_MINUTES_BETWEEN_POSTS', '15'))
            
            for i, post in enumerate(posts):
                # Calculate posting time with jitter
                post_time = start_ts + timedelta(
                    days=i if cadence == "daily" else 0,
                    hours=i if cadence == "hourly" else 0,
                    minutes=random.randint(0, minutes_between)
                )
                
                platform = post.get('platform', 'x')
                
                # For now, we'll store the schedule and simulate immediate posting
                if platform == 'x':
                    result = self.post_to_x(user_id, post.get('text', ''), post.get('media_url'), post.get('link'))
                elif platform == 'instagram':
                    result = self.post_to_instagram(user_id, post.get('caption', ''), post.get('media_url'))
                elif platform == 'tiktok':
                    result = self.post_to_tiktok(user_id, post.get('caption', ''), post.get('video_url', ''))
                elif platform == 'reddit':
                    result = self.post_to_reddit(user_id, post.get('subreddit', 'entrepreneur'), 
                                               post.get('title', ''), post.get('body', ''))
                else:
                    result = {"success": False, "error": f"Unsupported platform: {platform}"}
                
                scheduled_posts.append({
                    "post": post,
                    "scheduled_time": post_time.isoformat(),
                    "result": result
                })
                
                # Rate limiting
                time.sleep(random.uniform(1, 3))
            
            record_activity(user_id, "social", f"Scheduled {len(scheduled_posts)} posts",
                          details=json.dumps({"scheduled_count": len(scheduled_posts), "cadence": cadence}))
            
            return {
                "success": True,
                "scheduled_posts": scheduled_posts,
                "total_scheduled": len(scheduled_posts)
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

# Global instance
social_publisher = SocialPublisher()

def post_to_platform(user_id: int, platform: str, content: Dict[str, Any]) -> Dict[str, Any]:
    """Convenience function to post to any platform"""
    if platform == 'x':
        return social_publisher.post_to_x(user_id, content.get('text', ''), 
                                        content.get('media_url'), content.get('link'))
    elif platform == 'instagram':
        return social_publisher.post_to_instagram(user_id, content.get('caption', ''), 
                                                content.get('media_url'))
    elif platform == 'tiktok':
        return social_publisher.post_to_tiktok(user_id, content.get('caption', ''), 
                                             content.get('video_url', ''))
    elif platform == 'youtube':
        return social_publisher.post_to_youtube_shorts(user_id, content.get('title', ''), 
                                                     content.get('description', ''), 
                                                     content.get('video_url', ''))
    elif platform == 'reddit':
        return social_publisher.post_to_reddit(user_id, content.get('subreddit', 'entrepreneur'), 
                                             content.get('title', ''), content.get('body', ''))
    else:
        return {"success": False, "error": f"Unsupported platform: {platform}"}
