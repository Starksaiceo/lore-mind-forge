"""
YouTube Integration for AI CEO Platform
Handles automated YouTube video creation and posting
"""

import os
import logging
import json
import tempfile
from typing import Dict, List, Optional, Any
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import requests

logger = logging.getLogger(__name__)

class YouTubeManager:
    """Manages YouTube video creation and posting for AI CEO platform"""
    
    def __init__(self):
        """Initialize YouTube manager with OAuth credentials"""
        self.config = {
            "client_id": os.getenv("YOUTUBE_CLIENT_ID"),
            "client_secret": os.getenv("YOUTUBE_CLIENT_SECRET"), 
            "refresh_token": os.getenv("YOUTUBE_REFRESH_TOKEN"),
            "api_key": os.getenv("YOUTUBE_API_KEY")
        }
        
        self.youtube_service = None
        self.connected = False
        
        # Initialize YouTube API service
        if self._has_oauth_credentials():
            try:
                self._initialize_service()
                self.connected = True
                logger.info("✅ YouTube API client initialized successfully")
            except Exception as e:
                logger.error(f"❌ Failed to initialize YouTube client: {e}")
                self.connected = False
        else:
            logger.warning("⚠️ YouTube OAuth credentials not configured - running in simulation mode")
            self.connected = False
    
    def _has_oauth_credentials(self) -> bool:
        """Check if all required OAuth credentials are available"""
        required = ["client_id", "client_secret", "refresh_token"]
        return all(self.config.get(key) for key in required)
    
    def _initialize_service(self):
        """Initialize YouTube API service with OAuth credentials"""
        credentials = Credentials(
            None,
            refresh_token=self.config["refresh_token"],
            token_uri="https://oauth2.googleapis.com/token",
            client_id=self.config["client_id"],
            client_secret=self.config["client_secret"],
            scopes=["https://www.googleapis.com/auth/youtube.upload"]
        )
        
        # Refresh the access token
        credentials.refresh(Request())
        
        # Build YouTube service
        self.youtube_service = build("youtube", "v3", credentials=credentials)
    
    def is_connected(self) -> bool:
        """Check if YouTube is properly connected"""
        return self.connected
    
    def get_channel_info(self) -> Optional[Dict[str, Any]]:
        """Get information about the authenticated YouTube channel"""
        if not self.connected:
            return None
            
        try:
            request = self.youtube_service.channels().list(
                part="snippet,statistics",
                mine=True
            )
            response = request.execute()
            
            if response.get("items"):
                channel = response["items"][0]
                return {
                    "id": channel["id"],
                    "title": channel["snippet"]["title"],
                    "description": channel["snippet"]["description"],
                    "subscriber_count": channel["statistics"].get("subscriberCount", "0"),
                    "video_count": channel["statistics"].get("videoCount", "0"),
                    "view_count": channel["statistics"].get("viewCount", "0")
                }
            else:
                logger.warning("⚠️ No YouTube channel found for authenticated account")
                return None
                
        except HttpError as e:
            logger.error(f"❌ Failed to get channel info: {e}")
            return None
    
    def create_video_content(self, business_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate video content based on business data"""
        try:
            # Create video title and description based on business
            title = self._generate_video_title(business_data)
            description = self._generate_video_description(business_data)
            tags = self._generate_video_tags(business_data)
            
            # Generate video script
            script = self._generate_video_script(business_data)
            
            return {
                "title": title,
                "description": description,
                "tags": tags,
                "script": script,
                "category_id": "27",  # Education category
                "privacy_status": "public"
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to create video content: {e}")
            return {}
    
    def _generate_video_title(self, business_data: Dict[str, Any]) -> str:
        """Generate compelling YouTube video title"""
        business_name = business_data.get("name", "Your Business")
        niche = business_data.get("niche", "business")
        
        titles = [
            f"How I Built a ${business_data.get('target_revenue', 100000)} {niche} Business with AI",
            f"The AI Secret Behind {business_name}'s Success Story",
            f"Building {business_name}: AI-Powered {niche} Revolution",
            f"From Zero to ${business_data.get('target_revenue', 100000)}: {business_name} Journey",
            f"The Future of {niche}: {business_name} AI Breakthrough"
        ]
        
        # Choose title based on business type
        return titles[0]  # Can be made more intelligent based on niche
    
    def _generate_video_description(self, business_data: Dict[str, Any]) -> str:
        """Generate YouTube video description with SEO optimization"""
        business_name = business_data.get("name", "Your Business")
        description = business_data.get("description", "AI-powered business automation")
        
        return f"""🚀 Discover how {business_name} is revolutionizing business automation with AI!

{description}

In this video, you'll learn:
✅ How AI is transforming business operations
✅ The secrets behind automated revenue generation
✅ Real strategies for scaling with artificial intelligence
✅ Step-by-step business automation techniques

🔥 Want to start your own AI-powered business? 
👉 Visit our platform: [Your Platform URL]

📊 Business Highlights:
• Target Revenue: ${business_data.get('target_revenue', 100000)}
• Industry: {business_data.get('niche', 'Technology')}
• Automation Level: 95%+ autonomous

💡 Timestamps:
00:00 Introduction
01:30 AI Business Overview
03:00 Automation Strategies
05:00 Revenue Generation
07:00 Scaling Techniques
09:00 Next Steps

🏷️ Tags: #AI #Business #Automation #Entrepreneur #Technology #Revenue #Scaling

Subscribe for more AI business insights! 🔔
"""
    
    def _generate_video_tags(self, business_data: Dict[str, Any]) -> List[str]:
        """Generate relevant YouTube tags for SEO"""
        base_tags = [
            "AI", "artificial intelligence", "business automation",
            "entrepreneur", "startup", "revenue generation",
            "passive income", "online business", "technology"
        ]
        
        # Add niche-specific tags
        niche = business_data.get("niche", "").lower()
        if "saas" in niche:
            base_tags.extend(["SaaS", "software", "subscription"])
        elif "ecommerce" in niche:
            base_tags.extend(["ecommerce", "online store", "selling"])
        elif "content" in niche:
            base_tags.extend(["content creation", "digital products", "media"])
        
        return base_tags[:15]  # YouTube allows max 15 tags
    
    def _generate_video_script(self, business_data: Dict[str, Any]) -> str:
        """Generate video script for AI narration"""
        business_name = business_data.get("name", "Your Business")
        niche = business_data.get("niche", "business")
        target_revenue = business_data.get("target_revenue", 100000)
        
        return f"""
[INTRO MUSIC - 5 seconds]

Hi everyone! Welcome back to the channel. Today, I'm excited to share an incredible AI business story about {business_name}.

[PAUSE]

Have you ever wondered what it would be like if artificial intelligence could run an entire business for you? Well, that's exactly what happened with {business_name}.

[TRANSITION]

{business_name} is a {niche} business that was created and is managed almost entirely by AI. The goal? Generate ${target_revenue} in revenue through complete automation.

[MAIN CONTENT]

Here's what makes this so amazing:

First, the AI handles all content creation. Every blog post, social media update, and marketing campaign is generated automatically based on market trends and customer behavior.

Second, it manages the entire sales process. From lead generation to customer support, the AI takes care of everything.

Third, and this is the really cool part - it continuously optimizes itself. The AI analyzes performance data and adjusts strategies in real-time.

[RESULTS]

The results speak for themselves. {business_name} has achieved impressive growth through pure automation, proving that AI can truly run a business independently.

[CALL TO ACTION]

If you're interested in starting your own AI-powered business, check out the link in the description. The platform I used is available for anyone to try.

Thanks for watching! Don't forget to subscribe for more AI business content, and I'll see you in the next video!

[OUTRO MUSIC - 3 seconds]
"""
    
    def upload_video(self, video_file_path: str, video_data: Dict[str, Any]) -> Optional[str]:
        """Upload video to YouTube and return video ID"""
        if not self.connected:
            logger.warning("⚠️ YouTube not connected - simulating video upload")
            return f"sim_video_{hash(video_data.get('title', 'video'))}"
        
        try:
            # Prepare video metadata
            body = {
                "snippet": {
                    "title": video_data.get("title", "AI Business Video"),
                    "description": video_data.get("description", ""),
                    "tags": video_data.get("tags", []),
                    "categoryId": video_data.get("category_id", "27")
                },
                "status": {
                    "privacyStatus": video_data.get("privacy_status", "public"),
                    "embeddable": True,
                    "license": "youtube"
                }
            }
            
            # Upload video file
            media = MediaFileUpload(
                video_file_path,
                chunksize=-1,
                resumable=True,
                mimetype="video/mp4"
            )
            
            # Execute upload
            insert_request = self.youtube_service.videos().insert(
                part=",".join(body.keys()),
                body=body,
                media_body=media
            )
            
            response = insert_request.execute()
            video_id = response.get("id")
            
            if video_id:
                logger.info(f"✅ Video uploaded successfully: {video_id}")
                return video_id
            else:
                logger.error("❌ Video upload failed - no video ID returned")
                return None
                
        except HttpError as e:
            logger.error(f"❌ YouTube upload failed: {e}")
            return None
        except Exception as e:
            logger.error(f"❌ Video upload exception: {e}")
            return None
    
    def create_business_video(self, business_data: Dict[str, Any]) -> Optional[str]:
        """Create and upload a complete business showcase video"""
        try:
            # Generate video content
            video_content = self.create_video_content(business_data)
            
            if not video_content:
                logger.error("❌ Failed to generate video content")
                return None
            
            # Create video file (for now, generate a simple text-to-video)
            video_file = self._create_video_file(video_content, business_data)
            
            if not video_file:
                logger.error("❌ Failed to create video file")
                return None
            
            # Upload to YouTube
            video_id = self.upload_video(video_file, video_content)
            
            # Clean up temporary file
            if os.path.exists(video_file):
                os.remove(video_file)
            
            return video_id
            
        except Exception as e:
            logger.error(f"❌ Failed to create business video: {e}")
            return None
    
    def _create_video_file(self, video_content: Dict[str, Any], business_data: Dict[str, Any]) -> Optional[str]:
        """Create video file from content data"""
        try:
            try:
                import moviepy.editor as mp
                from PIL import Image, ImageDraw, ImageFont
                import numpy as np
            except ImportError:
                logger.warning("⚠️ Video creation libraries not available - generating text-based content")
                return None
            
            # Create temporary file
            temp_video = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
            temp_video.close()
            
            # Video settings
            width, height = 1920, 1080
            fps = 30
            duration = 30  # 30-second video
            
            # Create frames
            frames = []
            for i in range(fps * duration):
                # Create frame with business info
                img = Image.new('RGB', (width, height), color='#1a1a1a')
                draw = ImageDraw.Draw(img)
                
                # Try to load font, fallback to default
                try:
                    font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 72)
                    font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 48)
                except:
                    font_large = ImageFont.load_default()
                    font_medium = ImageFont.load_default()
                
                # Draw business name
                business_name = business_data.get("name", "AI Business")
                text_bbox = draw.textbbox((0, 0), business_name, font=font_large)
                text_width = text_bbox[2] - text_bbox[0]
                text_x = (width - text_width) // 2
                
                draw.text((text_x, height//3), business_name, fill='#ffffff', font=font_large)
                
                # Draw description
                description = business_data.get("description", "AI-Powered Business Automation")
                desc_bbox = draw.textbbox((0, 0), description, font=font_medium)
                desc_width = desc_bbox[2] - desc_bbox[0]
                desc_x = (width - desc_width) // 2
                
                draw.text((desc_x, height//2), description, fill='#cccccc', font=font_medium)
                
                # Draw revenue target
                revenue_text = f"Target Revenue: ${business_data.get('target_revenue', 100000):,}"
                rev_bbox = draw.textbbox((0, 0), revenue_text, font=font_medium)
                rev_width = rev_bbox[2] - rev_bbox[0]
                rev_x = (width - rev_width) // 2
                
                draw.text((rev_x, height*2//3), revenue_text, fill='#00ff88', font=font_medium)
                
                # Convert PIL image to numpy array
                frame = np.array(img)
                frames.append(frame)
            
            # Create video from frames
            clip = mp.ImageSequenceClip(frames, fps=fps)
            
            # Add audio (optional - could add narration here)
            # For now, just export silent video
            clip.write_videofile(temp_video.name, codec='libx264', audio_codec='aac')
            
            logger.info(f"✅ Video file created: {temp_video.name}")
            return temp_video.name
            
        except Exception as e:
            logger.error(f"❌ Failed to create video file: {e}")
            return None
    
    def launch_youtube_campaign(self, business_data: Dict[str, Any]) -> Dict[str, Any]:
        """Launch complete YouTube marketing campaign for business"""
        try:
            if not self.connected:
                logger.warning("⚠️ YouTube running in simulation mode")
                return {
                    "success": True,
                    "simulation": True,
                    "video_id": f"sim_yt_{hash(str(business_data))}",
                    "message": "YouTube campaign simulated successfully",
                    "next_steps": "Connect YouTube account via OAuth for real uploads"
                }
            
            # Create and upload business video
            video_id = self.create_business_video(business_data)
            
            if video_id:
                video_url = f"https://www.youtube.com/watch?v={video_id}"
                logger.info(f"✅ YouTube campaign launched: {video_url}")
                
                return {
                    "success": True,
                    "video_id": video_id,
                    "video_url": video_url,
                    "message": f"Video uploaded successfully to YouTube",
                    "analytics": {
                        "platform": "YouTube",
                        "content_type": "business_showcase",
                        "estimated_reach": "1000-5000 views"
                    }
                }
            else:
                return {
                    "success": False,
                    "error": "Failed to upload video to YouTube",
                    "next_steps": "Check YouTube channel permissions and quota limits"
                }
                
        except Exception as e:
            logger.error(f"❌ YouTube campaign failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "next_steps": "Review YouTube API credentials and permissions"
            }
    
    def get_video_analytics(self, video_id: str) -> Dict[str, Any]:
        """Get analytics for uploaded video"""
        if not self.connected:
            return {
                "views": 0,
                "likes": 0,
                "comments": 0,
                "watch_time": 0,
                "simulation": True
            }
        
        try:
            request = self.youtube_service.videos().list(
                part="statistics",
                id=video_id
            )
            response = request.execute()
            
            if response.get("items"):
                stats = response["items"][0]["statistics"]
                return {
                    "views": int(stats.get("viewCount", 0)),
                    "likes": int(stats.get("likeCount", 0)),
                    "comments": int(stats.get("commentCount", 0)),
                    "dislikes": int(stats.get("dislikeCount", 0))
                }
            else:
                return {"error": "Video not found"}
                
        except HttpError as e:
            logger.error(f"❌ Failed to get video analytics: {e}")
            return {"error": str(e)}