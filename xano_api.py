
import os
import requests
import json
from typing import Dict, List, Optional
from datetime import datetime
from config import XANO_BASE_URL, XANO_PROFIT_ENDPOINT

class XanoAPI:
    """Xano API service for data management and profit tracking"""
    
    def __init__(self):
        self.base_url = XANO_BASE_URL
        self.profit_endpoint = XANO_PROFIT_ENDPOINT
        
    def is_configured(self) -> bool:
        """Check if Xano is properly configured"""
        return bool(self.base_url)
    
    def log_profit(self, amount: float, source: str, ai_task_id: Optional[int] = None, ai_goal_id: Optional[int] = None) -> Dict:
        """Log profit entry to Xano"""
        try:
            if not self.is_configured():
                return {"success": False, "error": "Xano not configured"}
            
            data = {
                "amount": float(amount),
                "source": str(source),
                "timestamp": datetime.now().isoformat(),
                "created_at": int(datetime.now().timestamp())
            }
            
            if ai_task_id:
                data["ai_task_id"] = ai_task_id
            if ai_goal_id:
                data["ai_goal_id"] = ai_goal_id
            
            response = requests.post(
                f"{self.base_url}/profit",
                json=data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            response.raise_for_status()
            
            result = response.json()
            return {
                "success": True,
                "profit_id": result.get("id"),
                "amount": amount,
                "source": source,
                "data": result
            }
            
        except Exception as e:
            return {"success": False, "error": f"Xano profit logging error: {str(e)}"}
    
    def get_profits(self, limit: Optional[int] = None) -> List[Dict]:
        """Get profit entries from Xano"""
        try:
            if not self.is_configured():
                return []
            
            url = f"{self.base_url}/profit"
            params = {}
            if limit:
                params["limit"] = limit
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            if isinstance(data, list):
                return data
            return []
            
        except Exception as e:
            print(f"Error fetching Xano profits: {e}")
            return []
    
    def get_goals(self) -> List[Dict]:
        """Get AI goals from Xano"""
        try:
            if not self.is_configured():
                return []
            
            response = requests.get(f"{self.base_url}/ai_goal", timeout=10)
            response.raise_for_status()
            
            data = response.json()
            if isinstance(data, list):
                return data
            elif isinstance(data, dict) and 'result1' in data:
                return data['result1']
            return []
            
        except Exception as e:
            print(f"Error fetching Xano goals: {e}")
            return []
    
    def create_goal(self, goal_data: Dict) -> Dict:
        """Create a new AI goal in Xano"""
        try:
            if not self.is_configured():
                return {"success": False, "error": "Xano not configured"}
            
            data = {
                "description": goal_data.get("description", ""),
                "priority": goal_data.get("priority", 1),
                "status": goal_data.get("status", "pending"),
                "created_at": int(datetime.now().timestamp())
            }
            
            response = requests.post(
                f"{self.base_url}/ai_goal",
                json=data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            response.raise_for_status()
            
            result = response.json()
            return {
                "success": True,
                "goal_id": result.get("id"),
                "data": result
            }
            
        except Exception as e:
            return {"success": False, "error": f"Xano goal creation error: {str(e)}"}
    
    def store_ai_memory(self, command: str, response: str) -> Dict:
        """Store AI command and response as memory"""
        try:
            if not self.is_configured():
                return {"success": False, "error": "Xano not configured"}
            
            data = {
                "command": command,
                "response": response,
                "created_at": int(datetime.now().timestamp())
            }
            
            response = requests.post(
                f"{self.base_url}/ai_memory",
                json=data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            response.raise_for_status()
            
            result = response.json()
            return {"success": True, "memory_id": result.get("id")}
            
        except Exception as e:
            return {"success": False, "error": f"Xano memory storage error: {str(e)}"}

# Global instance
xano_api = XanoAPI()

# Convenience functions
def log_profit_to_xano(amount: float, source: str, ai_task_id: Optional[int] = None, ai_goal_id: Optional[int] = None) -> Dict:
    """Log profit to Xano"""
    return xano_api.log_profit(amount, source, ai_task_id, ai_goal_id)

def get_xano_profits(limit: Optional[int] = None) -> List[Dict]:
    """Get profits from Xano"""
    return xano_api.get_profits(limit)

def get_xano_goals() -> List[Dict]:
    """Get goals from Xano"""
    return xano_api.get_goals()

def create_xano_goal(goal_data: Dict) -> Dict:
    """Create goal in Xano"""
    return xano_api.create_goal(goal_data)
