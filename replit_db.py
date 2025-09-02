
import os
import json
import requests
from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid

class ReplitDB:
    """Replit Database integration for AI CEO platform"""
    
    def __init__(self):
        self.db_url = os.getenv('REPLIT_DB_URL', 'https://kv.replit.com/v0/placeholder')
        self.headers = {'Content-Type': 'application/json'}
    
    def set(self, key: str, value: Any) -> bool:
        """Set a value in Replit DB"""
        try:
            if isinstance(value, (dict, list)):
                value = json.dumps(value)
            
            response = requests.post(
                self.db_url,
                headers=self.headers,
                data={key: value}
            )
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Replit DB set error: {e}")
            return False
    
    def get(self, key: str) -> Any:
        """Get a value from Replit DB"""
        try:
            response = requests.get(f"{self.db_url}/{key}")
            if response.status_code == 200:
                try:
                    return json.loads(response.text)
                except json.JSONDecodeError:
                    return response.text
            return None
        except Exception as e:
            print(f"❌ Replit DB get error: {e}")
            return None
    
    def delete(self, key: str) -> bool:
        """Delete a key from Replit DB"""
        try:
            response = requests.delete(f"{self.db_url}/{key}")
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Replit DB delete error: {e}")
            return False
    
    def list_keys(self, prefix: str = "") -> List[str]:
        """List all keys with optional prefix"""
        try:
            response = requests.get(f"{self.db_url}?prefix={prefix}")
            if response.status_code == 200:
                return response.text.split('\n') if response.text else []
            return []
        except Exception as e:
            print(f"❌ Replit DB list error: {e}")
            return []

# Database Collections Manager
class ReplitDBManager:
    """Manage structured collections in Replit DB"""
    
    def __init__(self):
        self.db = ReplitDB()
    
    # USERS COLLECTION
    def create_user(self, email: str, password_hash: str, role: str = 'user') -> str:
        """Create a new user"""
        user_id = str(uuid.uuid4())
        user_data = {
            'id': user_id,
            'email': email.lower(),
            'password_hash': password_hash,
            'role': role,
            'status': 'active',
            'personality': 'professional',
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        if self.db.set(f"user:{user_id}", user_data):
            # Also store email->id mapping for quick lookup
            self.db.set(f"email:{email.lower()}", user_id)
            return user_id
        return None
    
    def get_user(self, user_id: str) -> Optional[Dict]:
        """Get user by ID"""
        return self.db.get(f"user:{user_id}")
    
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """Get user by email"""
        user_id = self.db.get(f"email:{email.lower()}")
        if user_id:
            return self.get_user(user_id)
        return None
    
    def update_user(self, user_id: str, updates: Dict) -> bool:
        """Update user data"""
        user = self.get_user(user_id)
        if user:
            user.update(updates)
            user['updated_at'] = datetime.now().isoformat()
            return self.db.set(f"user:{user_id}", user)
        return False
    
    # SUBSCRIPTIONS COLLECTION
    def create_subscription(self, user_id: str, stripe_subscription_id: str, tier: str) -> str:
        """Create a new subscription"""
        sub_id = str(uuid.uuid4())
        sub_data = {
            'id': sub_id,
            'user_id': user_id,
            'stripe_subscription_id': stripe_subscription_id,
            'tier': tier,  # starter/pro/enterprise
            'status': 'active',
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        if self.db.set(f"subscription:{sub_id}", sub_data):
            # Store user->subscription mapping
            self.db.set(f"user_subscription:{user_id}", sub_id)
            return sub_id
        return None
    
    def get_user_subscription(self, user_id: str) -> Optional[Dict]:
        """Get user's active subscription"""
        sub_id = self.db.get(f"user_subscription:{user_id}")
        if sub_id:
            return self.db.get(f"subscription:{sub_id}")
        return None
    
    def update_subscription(self, sub_id: str, updates: Dict) -> bool:
        """Update subscription data"""
        sub = self.db.get(f"subscription:{sub_id}")
        if sub:
            sub.update(updates)
            sub['updated_at'] = datetime.now().isoformat()
            return self.db.set(f"subscription:{sub_id}", sub)
        return False
    
    # PRODUCTS COLLECTION
    def create_product(self, seller_id: str, title: str, description: str, price: float, file_url: str = None) -> str:
        """Create a new product"""
        product_id = str(uuid.uuid4())
        product_data = {
            'id': product_id,
            'seller_id': seller_id,
            'title': title,
            'description': description,
            'file_url': file_url,
            'price': price,
            'status': 'active',
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        if self.db.set(f"product:{product_id}", product_data):
            # Add to seller's products list
            seller_products = self.db.get(f"seller_products:{seller_id}") or []
            seller_products.append(product_id)
            self.db.set(f"seller_products:{seller_id}", seller_products)
            return product_id
        return None
    
    def get_product(self, product_id: str) -> Optional[Dict]:
        """Get product by ID"""
        return self.db.get(f"product:{product_id}")
    
    def get_seller_products(self, seller_id: str) -> List[Dict]:
        """Get all products by seller"""
        product_ids = self.db.get(f"seller_products:{seller_id}") or []
        products = []
        for product_id in product_ids:
            product = self.get_product(product_id)
            if product:
                products.append(product)
        return products
    
    # ORDERS COLLECTION
    def create_order(self, buyer_id: str, product_id: str, amount: float, seller_id: str) -> str:
        """Create a new order"""
        order_id = str(uuid.uuid4())
        fee_taken = amount * 0.10  # 10% platform fee
        seller_payout = amount - fee_taken
        
        order_data = {
            'id': order_id,
            'buyer_id': buyer_id,
            'product_id': product_id,
            'seller_id': seller_id,
            'amount': amount,
            'fee_taken': fee_taken,
            'seller_payout': seller_payout,
            'status': 'pending',
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        if self.db.set(f"order:{order_id}", order_data):
            # Add to buyer's orders
            buyer_orders = self.db.get(f"buyer_orders:{buyer_id}") or []
            buyer_orders.append(order_id)
            self.db.set(f"buyer_orders:{buyer_id}", buyer_orders)
            
            # Add to seller's orders
            seller_orders = self.db.get(f"seller_orders:{seller_id}") or []
            seller_orders.append(order_id)
            self.db.set(f"seller_orders:{seller_id}", seller_orders)
            
            return order_id
        return None
    
    def update_order(self, order_id: str, updates: Dict) -> bool:
        """Update order data"""
        order = self.db.get(f"order:{order_id}")
        if order:
            order.update(updates)
            order['updated_at'] = datetime.now().isoformat()
            return self.db.set(f"order:{order_id}", order)
        return False
    
    # MEMORY COLLECTION
    def add_memory(self, user_id: str, memory_type: str, content: str) -> str:
        """Add AI memory for user"""
        memory_id = str(uuid.uuid4())
        memory_data = {
            'id': memory_id,
            'user_id': user_id,
            'type': memory_type,  # goal/note/action
            'content': content,
            'timestamp': datetime.now().isoformat()
        }
        
        if self.db.set(f"memory:{memory_id}", memory_data):
            # Add to user's memory list
            user_memories = self.db.get(f"user_memories:{user_id}") or []
            user_memories.append(memory_id)
            self.db.set(f"user_memories:{user_id}", user_memories)
            return memory_id
        return None
    
    def get_user_memories(self, user_id: str, memory_type: str = None) -> List[Dict]:
        """Get user's memories, optionally filtered by type"""
        memory_ids = self.db.get(f"user_memories:{user_id}") or []
        memories = []
        for memory_id in memory_ids:
            memory = self.db.get(f"memory:{memory_id}")
            if memory:
                if memory_type is None or memory.get('type') == memory_type:
                    memories.append(memory)
        return sorted(memories, key=lambda x: x['timestamp'], reverse=True)
    
    # ANALYTICS COLLECTION
    def log_analytics(self, metric_type: str, value: Any, user_id: str = None) -> str:
        """Log analytics event"""
        analytics_id = str(uuid.uuid4())
        analytics_data = {
            'id': analytics_id,
            'metric_type': metric_type,
            'value': value,
            'user_id': user_id,
            'timestamp': datetime.now().isoformat()
        }
        
        if self.db.set(f"analytics:{analytics_id}", analytics_data):
            # Add to daily analytics
            date_key = datetime.now().strftime('%Y-%m-%d')
            daily_analytics = self.db.get(f"daily_analytics:{date_key}") or []
            daily_analytics.append(analytics_id)
            self.db.set(f"daily_analytics:{date_key}", daily_analytics)
            return analytics_id
        return None
    
    def get_analytics(self, metric_type: str = None, days: int = 7) -> List[Dict]:
        """Get analytics data"""
        analytics = []
        for i in range(days):
            date = datetime.now() - timedelta(days=i)
            date_key = date.strftime('%Y-%m-%d')
            daily_ids = self.db.get(f"daily_analytics:{date_key}") or []
            
            for analytics_id in daily_ids:
                data = self.db.get(f"analytics:{analytics_id}")
                if data:
                    if metric_type is None or data.get('metric_type') == metric_type:
                        analytics.append(data)
        
        return sorted(analytics, key=lambda x: x['timestamp'], reverse=True)

# Global instance
replit_db_manager = ReplitDBManager()
