
import json
import sqlite3
from datetime import datetime
from typing import Dict, List, Any
import os

class AICEOMemorySystem:
    """Memory and learning system for the AI CEO agent"""
    
    def __init__(self, db_path="ai_ceo_memory.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the memory database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create memory tables
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS experiences (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    action_type TEXT NOT NULL,
                    context TEXT,
                    result TEXT,
                    success BOOLEAN,
                    revenue_generated REAL,
                    lessons_learned TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS successful_patterns (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pattern_type TEXT NOT NULL,
                    pattern_data TEXT,
                    success_rate REAL,
                    avg_revenue REAL,
                    usage_count INTEGER DEFAULT 1,
                    last_used DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS market_insights (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    niche TEXT NOT NULL,
                    trend_data TEXT,
                    performance_data TEXT,
                    optimal_pricing TEXT,
                    best_times TEXT,
                    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"Memory system init error: {e}")
    
    def record_experience(self, action_type: str, context: Dict, result: Dict) -> bool:
        """Record an experience for learning"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            lessons = self.extract_lessons(action_type, context, result)
            
            cursor.execute("""
                INSERT INTO experiences 
                (action_type, context, result, success, revenue_generated, lessons_learned)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                action_type,
                json.dumps(context),
                json.dumps(result),
                result.get("success", False),
                result.get("revenue_generated", 0.0),
                lessons
            ))
            
            conn.commit()
            conn.close()
            
            # Update patterns if successful
            if result.get("success"):
                self.update_successful_patterns(action_type, context, result)
            
            return True
            
        except Exception as e:
            print(f"Experience recording error: {e}")
            return False
    
    def extract_lessons(self, action_type: str, context: Dict, result: Dict) -> str:
        """Extract key lessons from an experience"""
        lessons = []
        
        if action_type == "product_creation":
            if result.get("success"):
                lessons.append(f"Successful product in {context.get('niche', 'unknown')} niche")
                lessons.append(f"Price point ${context.get('price', 0)} worked well")
            else:
                lessons.append(f"Product failed in {context.get('niche', 'unknown')} niche")
        
        elif action_type == "marketing_campaign":
            if result.get("success"):
                lessons.append(f"Effective ad copy style: {context.get('ad_style', 'unknown')}")
                lessons.append(f"Target audience: {context.get('target_audience', 'unknown')}")
        
        elif action_type == "trend_analysis":
            lessons.append(f"Trend '{context.get('keyword', 'unknown')}' had {result.get('interest_score', 0)} interest")
        
        return "; ".join(lessons)
    
    def update_successful_patterns(self, action_type: str, context: Dict, result: Dict):
        """Update successful patterns database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            pattern_data = {
                "niche": context.get("niche"),
                "price_range": context.get("price"),
                "keywords": context.get("keywords", []),
                "success_factors": result.get("success_factors", [])
            }
            
            # Check if pattern exists
            cursor.execute("""
                SELECT id, usage_count, success_rate, avg_revenue 
                FROM successful_patterns 
                WHERE pattern_type = ? AND pattern_data LIKE ?
            """, (action_type, f'%{context.get("niche", "")}%'))
            
            existing = cursor.fetchone()
            
            if existing:
                # Update existing pattern
                new_usage_count = existing[1] + 1
                new_success_rate = (existing[2] * existing[1] + 1) / new_usage_count
                new_avg_revenue = (existing[3] * existing[1] + result.get("revenue_generated", 0)) / new_usage_count
                
                cursor.execute("""
                    UPDATE successful_patterns 
                    SET usage_count = ?, success_rate = ?, avg_revenue = ?, last_used = CURRENT_TIMESTAMP
                    WHERE id = ?
                """, (new_usage_count, new_success_rate, new_avg_revenue, existing[0]))
            else:
                # Create new pattern
                cursor.execute("""
                    INSERT INTO successful_patterns 
                    (pattern_type, pattern_data, success_rate, avg_revenue)
                    VALUES (?, ?, ?, ?)
                """, (
                    action_type,
                    json.dumps(pattern_data),
                    1.0,
                    result.get("revenue_generated", 0.0)
                ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"Pattern update error: {e}")
    
    def get_successful_patterns(self, action_type: str = None) -> List[Dict]:
        """Get successful patterns for learning"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if action_type:
                cursor.execute("""
                    SELECT * FROM successful_patterns 
                    WHERE pattern_type = ? 
                    ORDER BY success_rate DESC, avg_revenue DESC
                """, (action_type,))
            else:
                cursor.execute("""
                    SELECT * FROM successful_patterns 
                    ORDER BY success_rate DESC, avg_revenue DESC
                """)
            
            patterns = []
            for row in cursor.fetchall():
                pattern = {
                    "id": row[0],
                    "pattern_type": row[1],
                    "pattern_data": json.loads(row[2]),
                    "success_rate": row[3],
                    "avg_revenue": row[4],
                    "usage_count": row[5],
                    "last_used": row[6]
                }
                patterns.append(pattern)
            
            conn.close()
            return patterns
            
        except Exception as e:
            print(f"Pattern retrieval error: {e}")
            return []
    
    def get_intelligence_insights(self) -> Dict:
        """Get AI intelligence insights for decision making"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get success rates by action type
            cursor.execute("""
                SELECT action_type, 
                       AVG(CASE WHEN success THEN 1.0 ELSE 0.0 END) as success_rate,
                       AVG(revenue_generated) as avg_revenue,
                       COUNT(*) as total_attempts
                FROM experiences 
                GROUP BY action_type
            """)
            
            action_performance = {}
            for row in cursor.fetchall():
                action_performance[row[0]] = {
                    "success_rate": row[1],
                    "avg_revenue": row[2],
                    "total_attempts": row[3]
                }
            
            # Get best performing niches
            cursor.execute("""
                SELECT json_extract(context, '$.niche') as niche,
                       AVG(CASE WHEN success THEN 1.0 ELSE 0.0 END) as success_rate,
                       AVG(revenue_generated) as avg_revenue
                FROM experiences 
                WHERE json_extract(context, '$.niche') IS NOT NULL
                GROUP BY niche
                ORDER BY success_rate DESC, avg_revenue DESC
                LIMIT 10
            """)
            
            top_niches = []
            for row in cursor.fetchall():
                if row[0]:  # Skip null niches
                    top_niches.append({
                        "niche": row[0],
                        "success_rate": row[1],
                        "avg_revenue": row[2]
                    })
            
            conn.close()
            
            return {
                "action_performance": action_performance,
                "top_niches": top_niches,
                "total_experiences": len(action_performance),
                "learning_status": "active"
            }
            
        except Exception as e:
            print(f"Intelligence insights error: {e}")
            return {"error": str(e)}
    
    def optimize_decision(self, action_type: str, context: Dict) -> Dict:
        """Use memory to optimize decisions"""
        try:
            patterns = self.get_successful_patterns(action_type)
            
            if not patterns:
                return {"recommendation": "no_data", "confidence": 0.0}
            
            # Find best matching pattern
            best_pattern = None
            best_score = 0.0
            
            for pattern in patterns:
                score = self.calculate_pattern_match(context, pattern["pattern_data"])
                if score > best_score:
                    best_score = score
                    best_pattern = pattern
            
            if best_pattern and best_score > 0.5:
                return {
                    "recommendation": "use_pattern",
                    "pattern": best_pattern,
                    "confidence": best_score,
                    "expected_success_rate": best_pattern["success_rate"],
                    "expected_revenue": best_pattern["avg_revenue"]
                }
            else:
                return {"recommendation": "explore_new", "confidence": 0.3}
                
        except Exception as e:
            return {"recommendation": "error", "error": str(e)}
    
    def calculate_pattern_match(self, context: Dict, pattern_data: Dict) -> float:
        """Calculate how well context matches a successful pattern"""
        score = 0.0
        total_factors = 0
        
        # Compare niche
        if context.get("niche") and pattern_data.get("niche"):
            if context["niche"].lower() == pattern_data["niche"].lower():
                score += 0.4
            total_factors += 0.4
        
        # Compare price range
        if context.get("price") and pattern_data.get("price_range"):
            price_diff = abs(context["price"] - pattern_data["price_range"]) / pattern_data["price_range"]
            if price_diff < 0.2:  # Within 20%
                score += 0.3
            total_factors += 0.3
        
        # Compare keywords
        if context.get("keywords") and pattern_data.get("keywords"):
            common_keywords = set(context["keywords"]) & set(pattern_data["keywords"])
            if common_keywords:
                score += 0.3 * (len(common_keywords) / len(pattern_data["keywords"]))
            total_factors += 0.3
        
        return score / total_factors if total_factors > 0 else 0.0

# Global memory system instance
memory_system = AICEOMemorySystem()

def record_ai_experience(action_type: str, context: Dict, result: Dict) -> bool:
    """Record an AI experience for learning"""
    return memory_system.record_experience(action_type, context, result)

def get_ai_recommendations(action_type: str, context: Dict) -> Dict:
    """Get AI recommendations based on memory"""
    return memory_system.optimize_decision(action_type, context)

def get_ai_intelligence() -> Dict:
    """Get current AI intelligence insights"""
    return memory_system.get_intelligence_insights()
