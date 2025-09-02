
import os
import requests
import json
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from replit_db import replit_db_manager
import logging

logger = logging.getLogger(__name__)

class ContentAutomation:
    """Automate content posting across multiple platforms"""
    
    def __init__(self):
        # Twitter/X API
        self.twitter_api_key = os.getenv('TWITTER_API_KEY')
        self.twitter_api_secret = os.getenv('TWITTER_API_SECRET')
        self.twitter_access_token = os.getenv('TWITTER_ACCESS_TOKEN')
        self.twitter_access_secret = os.getenv('TWITTER_ACCESS_SECRET')
        self.twitter_bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
        
        # YouTube API
        self.youtube_api_key = os.getenv('YOUTUBE_API_KEY')
        self.youtube_client_id = os.getenv('YOUTUBE_CLIENT_ID')
        self.youtube_client_secret = os.getenv('YOUTUBE_CLIENT_SECRET')
        self.youtube_refresh_token = os.getenv('YOUTUBE_REFRESH_TOKEN')
        
        # WordPress API
        self.wp_site_url = os.getenv('WP_SITE_URL')
        self.wp_username = os.getenv('WP_USERNAME')
        self.wp_password = os.getenv('WP_PASSWORD')
        self.wp_api_key = os.getenv('WP_API_KEY')
        
        # Substack API
        self.substack_api_key = os.getenv('SUBSTACK_API_KEY')
        
        # Telegram Bot
        self.telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')
    
    def post_tweet(self, user_id: str, content: str, media_urls: List[str] = None) -> Dict[str, Any]:
        """Post tweet to Twitter/X"""
        try:
            if not self.twitter_bearer_token:
                # Simulate posting
                result = {
                    'success': True,
                    'simulated': True,
                    'platform': 'twitter',
                    'post_id': f'sim_tweet_{int(datetime.now().timestamp())}',
                    'content': content[:280],  # Twitter limit
                    'posted_at': datetime.now().isoformat()
                }
                
                # Log to Replit DB
                replit_db_manager.log_analytics(
                    'content_posted',
                    {
                        'user_id': user_id,
                        'platform': 'twitter',
                        'simulated': True,
                        'content_length': len(content),
                        'has_media': bool(media_urls)
                    }
                )
                
                logger.info(f"🐦 Simulated tweet posted for user {user_id}")
                return result
            
            # Real Twitter API implementation would go here
            headers = {
                'Authorization': f'Bearer {self.twitter_bearer_token}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'text': content[:280]  # Twitter character limit
            }
            
            # Add media if provided
            if media_urls:
                # Would need to upload media first, then attach
                pass
            
            response = requests.post(
                'https://api.twitter.com/2/tweets',
                headers=headers,
                json=payload
            )
            
            if response.status_code == 201:
                tweet_data = response.json()
                result = {
                    'success': True,
                    'simulated': False,
                    'platform': 'twitter',
                    'post_id': tweet_data['data']['id'],
                    'content': content,
                    'posted_at': datetime.now().isoformat()
                }
                
                # Log to Replit DB
                replit_db_manager.log_analytics(
                    'content_posted',
                    {
                        'user_id': user_id,
                        'platform': 'twitter',
                        'simulated': False,
                        'post_id': result['post_id'],
                        'content_length': len(content)
                    }
                )
                
                return result
            else:
                return {
                    'success': False,
                    'error': f'Twitter API error: {response.status_code}',
                    'platform': 'twitter'
                }
                
        except Exception as e:
            logger.error(f"❌ Twitter posting error: {e}")
            return {
                'success': False,
                'error': str(e),
                'platform': 'twitter'
            }
    
    def upload_youtube_video(self, user_id: str, title: str, description: str, video_file_path: str, tags: List[str] = None) -> Dict[str, Any]:
        """Upload video to YouTube"""
        try:
            if not self.youtube_api_key:
                # Simulate upload
                result = {
                    'success': True,
                    'simulated': True,
                    'platform': 'youtube',
                    'video_id': f'sim_video_{int(datetime.now().timestamp())}',
                    'title': title,
                    'uploaded_at': datetime.now().isoformat()
                }
                
                # Log to Replit DB
                replit_db_manager.log_analytics(
                    'content_posted',
                    {
                        'user_id': user_id,
                        'platform': 'youtube',
                        'simulated': True,
                        'title': title,
                        'tags_count': len(tags) if tags else 0
                    }
                )
                
                logger.info(f"📺 Simulated YouTube upload for user {user_id}: {title}")
                return result
            
            # Real YouTube API implementation would go here
            # This requires OAuth 2.0 flow and Google API client
            return {
                'success': False,
                'error': 'YouTube API not implemented yet - requires OAuth setup',
                'platform': 'youtube'
            }
            
        except Exception as e:
            logger.error(f"❌ YouTube upload error: {e}")
            return {
                'success': False,
                'error': str(e),
                'platform': 'youtube'
            }
    
    def post_wordpress_article(self, user_id: str, title: str, content: str, tags: List[str] = None, status: str = 'publish') -> Dict[str, Any]:
        """Post article to WordPress"""
        try:
            if not self.wp_site_url or not self.wp_username:
                # Simulate posting
                result = {
                    'success': True,
                    'simulated': True,
                    'platform': 'wordpress',
                    'post_id': f'sim_wp_{int(datetime.now().timestamp())}',
                    'title': title,
                    'url': f'{self.wp_site_url or "https://example.com"}/sim-post-{int(datetime.now().timestamp())}',
                    'posted_at': datetime.now().isoformat()
                }
                
                # Log to Replit DB
                replit_db_manager.log_analytics(
                    'content_posted',
                    {
                        'user_id': user_id,
                        'platform': 'wordpress',
                        'simulated': True,
                        'title': title,
                        'content_length': len(content),
                        'tags_count': len(tags) if tags else 0
                    }
                )
                
                logger.info(f"📝 Simulated WordPress post for user {user_id}: {title}")
                return result
            
            # Real WordPress REST API implementation
            wp_api_url = f"{self.wp_site_url}/wp-json/wp/v2/posts"
            
            auth = (self.wp_username, self.wp_password or self.wp_api_key)
            
            payload = {
                'title': title,
                'content': content,
                'status': status,
                'tags': tags or []
            }
            
            response = requests.post(
                wp_api_url,
                auth=auth,
                json=payload
            )
            
            if response.status_code == 201:
                post_data = response.json()
                result = {
                    'success': True,
                    'simulated': False,
                    'platform': 'wordpress',
                    'post_id': post_data['id'],
                    'title': title,
                    'url': post_data['link'],
                    'posted_at': datetime.now().isoformat()
                }
                
                # Log to Replit DB
                replit_db_manager.log_analytics(
                    'content_posted',
                    {
                        'user_id': user_id,
                        'platform': 'wordpress',
                        'simulated': False,
                        'post_id': result['post_id'],
                        'url': result['url']
                    }
                )
                
                return result
            else:
                return {
                    'success': False,
                    'error': f'WordPress API error: {response.status_code}',
                    'platform': 'wordpress'
                }
                
        except Exception as e:
            logger.error(f"❌ WordPress posting error: {e}")
            return {
                'success': False,
                'error': str(e),
                'platform': 'wordpress'
            }
    
    def send_telegram_message(self, user_id: str, message: str, parse_mode: str = 'HTML') -> Dict[str, Any]:
        """Send message via Telegram Bot"""
        try:
            if not self.telegram_bot_token:
                # Simulate sending
                result = {
                    'success': True,
                    'simulated': True,
                    'platform': 'telegram',
                    'message_id': f'sim_tg_{int(datetime.now().timestamp())}',
                    'sent_at': datetime.now().isoformat()
                }
                
                # Log to Replit DB
                replit_db_manager.log_analytics(
                    'content_posted',
                    {
                        'user_id': user_id,
                        'platform': 'telegram',
                        'simulated': True,
                        'message_length': len(message)
                    }
                )
                
                logger.info(f"📱 Simulated Telegram message for user {user_id}")
                return result
            
            # Real Telegram Bot API implementation
            bot_api_url = f"https://api.telegram.org/bot{self.telegram_bot_token}/sendMessage"
            
            payload = {
                'chat_id': self.telegram_chat_id,
                'text': message,
                'parse_mode': parse_mode
            }
            
            response = requests.post(bot_api_url, json=payload)
            
            if response.status_code == 200:
                result_data = response.json()
                result = {
                    'success': True,
                    'simulated': False,
                    'platform': 'telegram',
                    'message_id': result_data['result']['message_id'],
                    'sent_at': datetime.now().isoformat()
                }
                
                # Log to Replit DB
                replit_db_manager.log_analytics(
                    'content_posted',
                    {
                        'user_id': user_id,
                        'platform': 'telegram',
                        'simulated': False,
                        'message_id': result['message_id']
                    }
                )
                
                return result
            else:
                return {
                    'success': False,
                    'error': f'Telegram API error: {response.status_code}',
                    'platform': 'telegram'
                }
                
        except Exception as e:
            logger.error(f"❌ Telegram sending error: {e}")
            return {
                'success': False,
                'error': str(e),
                'platform': 'telegram'
            }
    
    def create_substack_post(self, user_id: str, title: str, content: str, subtitle: str = None) -> Dict[str, Any]:
        """Create post on Substack"""
        try:
            if not self.substack_api_key:
                # Simulate posting
                result = {
                    'success': True,
                    'simulated': True,
                    'platform': 'substack',
                    'post_id': f'sim_sub_{int(datetime.now().timestamp())}',
                    'title': title,
                    'url': f'https://example.substack.com/p/sim-post-{int(datetime.now().timestamp())}',
                    'posted_at': datetime.now().isoformat()
                }
                
                # Log to Replit DB
                replit_db_manager.log_analytics(
                    'content_posted',
                    {
                        'user_id': user_id,
                        'platform': 'substack',
                        'simulated': True,
                        'title': title,
                        'content_length': len(content)
                    }
                )
                
                logger.info(f"📰 Simulated Substack post for user {user_id}: {title}")
                return result
            
            # Real Substack API implementation would go here
            # Note: Substack API is limited and may require manual setup
            return {
                'success': False,
                'error': 'Substack API not fully implemented - requires publication setup',
                'platform': 'substack'
            }
            
        except Exception as e:
            logger.error(f"❌ Substack posting error: {e}")
            return {
                'success': False,
                'error': str(e),
                'platform': 'substack'
            }

# Global instance
content_automation = ContentAutomation()

# Convenience functions
def post_to_all_platforms(user_id: str, content: Dict[str, str]) -> Dict[str, Any]:
    """Post content to all configured platforms"""
    results = {}
    
    # Twitter
    if content.get('tweet'):
        results['twitter'] = content_automation.post_tweet(
            user_id, 
            content['tweet']
        )
    
    # WordPress
    if content.get('article_title') and content.get('article_content'):
        results['wordpress'] = content_automation.post_wordpress_article(
            user_id,
            content['article_title'],
            content['article_content'],
            content.get('tags', [])
        )
    
    # Telegram
    if content.get('telegram_message'):
        results['telegram'] = content_automation.send_telegram_message(
            user_id,
            content['telegram_message']
        )
    
    # Substack
    if content.get('newsletter_title') and content.get('newsletter_content'):
        results['substack'] = content_automation.create_substack_post(
            user_id,
            content['newsletter_title'],
            content['newsletter_content'],
            content.get('newsletter_subtitle')
        )
    
    # Log overall campaign
    successful_platforms = [p for p, r in results.items() if r.get('success')]
    replit_db_manager.log_analytics(
        'multi_platform_campaign',
        {
            'user_id': user_id,
            'platforms_attempted': list(results.keys()),
            'platforms_successful': successful_platforms,
            'success_rate': len(successful_platforms) / len(results) if results else 0
        }
    )
    
    return {
        'success': len(successful_platforms) > 0,
        'results': results,
        'summary': {
            'attempted': len(results),
            'successful': len(successful_platforms),
            'failed': len(results) - len(successful_platforms)
        }
    }
