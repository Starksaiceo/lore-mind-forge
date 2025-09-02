
import time
import functools
from datetime import datetime, timedelta
from collections import defaultdict
import requests

class APIRateLimiter:
    def __init__(self):
        self.call_counts = defaultdict(list)
        self.limits = {
            'xano': {'calls': 30, 'window': 60},  # 30 calls per minute
            'stripe': {'calls': 100, 'window': 60},  # 100 calls per minute
            'gumroad': {'calls': 20, 'window': 60},  # 20 calls per minute
            'default': {'calls': 10, 'window': 60}   # Conservative default
        }
    
    def is_within_limit(self, api_name):
        """Check if we're within rate limits for the API"""
        now = datetime.now()
        limit_info = self.limits.get(api_name, self.limits['default'])
        
        # Clean old calls outside the window
        cutoff = now - timedelta(seconds=limit_info['window'])
        self.call_counts[api_name] = [
            call_time for call_time in self.call_counts[api_name] 
            if call_time > cutoff
        ]
        
        return len(self.call_counts[api_name]) < limit_info['calls']
    
    def wait_if_needed(self, api_name):
        """Wait if we're approaching rate limits"""
        if not self.is_within_limit(api_name):
            wait_time = 5  # Wait 5 seconds if at limit
            print(f"⏳ Rate limiting {api_name}: waiting {wait_time}s...")
            time.sleep(wait_time)
    
    def record_call(self, api_name):
        """Record that we made an API call"""
        self.call_counts[api_name].append(datetime.now())

# Global rate limiter instance
rate_limiter = APIRateLimiter()

def rate_limited(api_name):
    """Decorator to add rate limiting to API functions"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            rate_limiter.wait_if_needed(api_name)
            rate_limiter.record_call(api_name)
            
            try:
                return func(*args, **kwargs)
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 429:
                    print(f"🚫 {api_name} rate limited: {e}")
                    time.sleep(10)  # Wait longer for 429 errors
                    return None
                raise e
        return wrapper
    return decorator
