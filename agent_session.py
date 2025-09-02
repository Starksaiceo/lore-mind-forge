
import sqlite3
import json
import os
from datetime import datetime
from typing import Optional, Dict, Any, List
from models import db, AgentMemory, AIEvent, User

class AgentSession:
    """Enhanced agent session manager with memory and event logging"""
    
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.session_start = datetime.utcnow()
        
    def get_memory(self, key: str, default: Any = None) -> Any:
        """Get value from agent memory"""
        try:
            memory = AgentMemory.query.filter_by(
                user_id=self.user_id, 
                key=key
            ).order_by(AgentMemory.id.desc()).first()
            
            if memory:
                try:
                    # Try to parse as JSON first
                    return json.loads(memory.value)
                except (json.JSONDecodeError, TypeError):
                    # Return as string if not JSON
                    return memory.value
            return default
            
        except Exception as e:
            print(f"❌ Memory get failed: {e}")
            return default

    def set_memory(self, key: str, value: Any) -> bool:
        """Set value in agent memory"""
        try:
            # Serialize value to JSON if it's not a string
            if isinstance(value, (dict, list, tuple)):
                json_value = json.dumps(value)
            else:
                json_value = str(value)
            
            # Create new memory entry
            memory = AgentMemory(
                user_id=self.user_id,
                key=key,
                value=json_value
            )
            db.session.add(memory)
            db.session.commit()
            
            return True
            
        except Exception as e:
            print(f"❌ Memory set failed: {e}")
            return False

    def log_event(self, event_type: str, data: Dict[str, Any], success: bool = True) -> Optional[int]:
        """Log an AI event for this user"""
        try:
            event = AIEvent(
                user_id=self.user_id,
                event_type=event_type,
                event_json=json.dumps(data, default=str),
                success=success,
                created_at=datetime.utcnow()
            )
            db.session.add(event)
            db.session.commit()
            
            status_icon = "✅" if success else "❌"
            print(f"📝 Event logged: {event_type} {status_icon}")
            return event.id
            
        except Exception as e:
            print(f"❌ Event logging failed: {e}")
            return None

    def get_events(self, event_type: Optional[str] = None, limit: int = 50) -> List[Dict]:
        """Get recent events for this user"""
        try:
            query = AIEvent.query.filter_by(user_id=self.user_id)
            
            if event_type:
                query = query.filter_by(event_type=event_type)
            
            events = query.order_by(AIEvent.created_at.desc()).limit(limit).all()
            
            return [{
                "id": event.id,
                "event_type": event.event_type,
                "data": json.loads(event.event_json) if event.event_json else {},
                "success": event.success,
                "created_at": event.created_at.isoformat()
            } for event in events]
            
        except Exception as e:
            print(f"❌ Get events failed: {e}")
            return []

    def get_session_summary(self) -> Dict[str, Any]:
        """Get summary of current session"""
        try:
            session_duration = (datetime.utcnow() - self.session_start).total_seconds()
            
            recent_events = self.get_events(limit=10)
            success_count = sum(1 for event in recent_events if event["success"])
            
            return {
                "user_id": self.user_id,
                "session_duration_seconds": session_duration,
                "recent_events_count": len(recent_events),
                "success_rate": success_count / len(recent_events) if recent_events else 0,
                "last_activity": recent_events[0]["created_at"] if recent_events else None
            }
            
        except Exception as e:
            print(f"❌ Session summary failed: {e}")
            return {"error": str(e)}

    def clear_memory(self, key_pattern: Optional[str] = None) -> bool:
        """Clear agent memory (optionally by key pattern)"""
        try:
            if key_pattern:
                AgentMemory.query.filter(
                    AgentMemory.user_id == self.user_id,
                    AgentMemory.key.like(f"%{key_pattern}%")
                ).delete(synchronize_session=False)
            else:
                AgentMemory.query.filter_by(user_id=self.user_id).delete()
            
            db.session.commit()
            print(f"🧹 Memory cleared for user {self.user_id}")
            return True
            
        except Exception as e:
            print(f"❌ Memory clear failed: {e}")
            return False

    def increment_counter(self, key: str, amount: int = 1) -> int:
        """Increment a counter in memory"""
        current = self.get_memory(key, 0)
        if isinstance(current, (int, float)):
            new_value = current + amount
        else:
            new_value = amount
        
        self.set_memory(key, new_value)
        return new_value

    def append_to_list(self, key: str, item: Any) -> List:
        """Append item to a list in memory"""
        current = self.get_memory(key, [])
        if not isinstance(current, list):
            current = []
        
        current.append(item)
        self.set_memory(key, current)
        return current

    def get_preferred_name(self, fallback_name: str = "there") -> str:
        """Get user's preferred name for greetings"""
        preferred_name = self.get_memory('preferred_name')
        return preferred_name if preferred_name else fallback_name

    def learn_name_from_text(self, text: str) -> Optional[str]:
        """Extract and learn name from user input text"""
        import re
        
        # Common patterns for name introduction
        patterns = [
            r"my name is (\w+)",
            r"i'm (\w+)",
            r"call me (\w+)",
            r"i am (\w+)",
        ]
        
        text_lower = text.lower()
        for pattern in patterns:
            match = re.search(pattern, text_lower)
            if match:
                name = match.group(1).title()
                self.set_memory('preferred_name', name)
                self.log_event('name_learned', {
                    'preferred_name': name,
                    'learned_from': 'conversation',
                    'source_text': text
                })
                return name
        
        return None

# Helper functions for backwards compatibility
def create_agent_session(user_id: int) -> AgentSession:
    """Create a new agent session"""
    return AgentSession(user_id)

def log_agent_event(user_id: int, event_type: str, data: Dict, success: bool = True) -> Optional[int]:
    """Quick event logging without session"""
    session = AgentSession(user_id)
    return session.log_event(event_type, data, success)

# Export for use in other modules
__all__ = ['AgentSession', 'create_agent_session', 'log_agent_event']
