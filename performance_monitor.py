
#!/usr/bin/env python3
"""
Real-time performance monitoring for AI CEO SaaS Platform
Tracks user load, database performance, and system health
"""

import time
import threading
import logging
from datetime import datetime, timedelta
from collections import deque
from dataclasses import dataclass
from typing import Dict, List

logger = logging.getLogger(__name__)

@dataclass
class PerformanceMetric:
    timestamp: datetime
    active_users: int
    db_response_time: float
    memory_usage: float
    cpu_usage: float

class PerformanceMonitor:
    """Real-time performance monitoring"""
    
    def __init__(self, max_history=1000):
        self.metrics_history = deque(maxlen=max_history)
        self.active_sessions = set()
        self.request_times = deque(maxlen=100)
        self.db_query_times = deque(maxlen=100)
        self.monitoring = False
        self.monitor_thread = None
    
    def start_monitoring(self):
        """Start background monitoring"""
        if not self.monitoring:
            self.monitoring = True
            self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
            self.monitor_thread.start()
            logger.info("✅ Performance monitoring started")
    
    def stop_monitoring(self):
        """Stop background monitoring"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join()
        logger.info("🛑 Performance monitoring stopped")
    
    def record_request(self, user_id: str, duration: float):
        """Record a request completion"""
        self.active_sessions.add(user_id)
        self.request_times.append(duration)
        
        # Clean old sessions (5 minute timeout)
        current_time = time.time()
        if not hasattr(self, '_last_cleanup') or current_time - self._last_cleanup > 300:
            self._cleanup_sessions()
            self._last_cleanup = current_time
    
    def record_db_query(self, duration: float):
        """Record database query time"""
        self.db_query_times.append(duration)
    
    def get_current_metrics(self) -> Dict:
        """Get current performance metrics"""
        now = datetime.now()
        
        # Calculate averages
        avg_request_time = sum(self.request_times) / len(self.request_times) if self.request_times else 0
        avg_db_time = sum(self.db_query_times) / len(self.db_query_times) if self.db_query_times else 0
        
        # Get system metrics
        active_users = len(self.active_sessions)
        
        metrics = {
            'timestamp': now.isoformat(),
            'active_users': active_users,
            'avg_request_time': round(avg_request_time * 1000, 2),  # Convert to ms
            'avg_db_time': round(avg_db_time * 1000, 2),
            'requests_per_minute': len([t for t in self.request_times if time.time() - t < 60]),
            'performance_score': self._calculate_performance_score(),
            'capacity_utilization': min((active_users / 5000) * 100, 100),  # Percentage
            'status': self._get_system_status()
        }
        
        return metrics
    
    def get_capacity_analysis(self) -> Dict:
        """Analyze current capacity and scaling needs"""
        metrics = self.get_current_metrics()
        active_users = metrics['active_users']
        
        # Capacity thresholds
        if active_users < 50:
            status = "✅ Low Load - SQLite OK"
            recommendation = "Current setup sufficient"
        elif active_users < 200:
            status = "⚠️ Medium Load - Consider PostgreSQL"
            recommendation = "Upgrade to PostgreSQL soon"
        elif active_users < 1000:
            status = "🔶 High Load - PostgreSQL Required"
            recommendation = "Upgrade to PostgreSQL + Redis immediately"
        else:
            status = "🔴 Very High Load - Full Scaling Required"
            recommendation = "PostgreSQL + Redis + Horizontal Scaling"
        
        return {
            'current_users': active_users,
            'estimated_capacity': self._estimate_current_capacity(),
            'status': status,
            'recommendation': recommendation,
            'bottlenecks': self._identify_bottlenecks(metrics),
            'scaling_urgency': self._get_scaling_urgency(active_users)
        }
    
    def _monitor_loop(self):
        """Background monitoring loop"""
        while self.monitoring:
            try:
                metrics = self.get_current_metrics()
                
                # Store metric in history
                metric = PerformanceMetric(
                    timestamp=datetime.now(),
                    active_users=metrics['active_users'],
                    db_response_time=metrics['avg_db_time'],
                    memory_usage=0.0,  # Would need psutil for real memory monitoring
                    cpu_usage=0.0      # Would need psutil for real CPU monitoring
                )
                self.metrics_history.append(metric)
                
                # Log warnings for high load
                if metrics['active_users'] > 100:
                    logger.warning(f"High user load: {metrics['active_users']} active users")
                
                if metrics['avg_db_time'] > 1000:  # > 1 second
                    logger.warning(f"Slow database queries: {metrics['avg_db_time']}ms average")
                
            except Exception as e:
                logger.error(f"Monitoring error: {e}")
            
            time.sleep(30)  # Monitor every 30 seconds
    
    def _cleanup_sessions(self):
        """Remove old sessions"""
        # This is simplified - in reality you'd track last activity time
        if len(self.active_sessions) > 1000:
            # Keep only the most recent 500 sessions
            recent_sessions = list(self.active_sessions)[-500:]
            self.active_sessions = set(recent_sessions)
    
    def _calculate_performance_score(self) -> int:
        """Calculate overall performance score (0-100)"""
        score = 100
        
        # Penalize slow requests
        if self.request_times:
            avg_time = sum(self.request_times) / len(self.request_times)
            if avg_time > 2.0:  # > 2 seconds
                score -= 30
            elif avg_time > 1.0:  # > 1 second
                score -= 15
        
        # Penalize slow database
        if self.db_query_times:
            avg_db_time = sum(self.db_query_times) / len(self.db_query_times)
            if avg_db_time > 1.0:  # > 1 second
                score -= 25
            elif avg_db_time > 0.5:  # > 500ms
                score -= 10
        
        # Penalize high user load without proper scaling
        active_users = len(self.active_sessions)
        if active_users > 200:  # High load for SQLite
            score -= 20
        
        return max(score, 0)
    
    def _get_system_status(self) -> str:
        """Get overall system status"""
        score = self._calculate_performance_score()
        
        if score >= 80:
            return "✅ Excellent"
        elif score >= 60:
            return "⚠️ Good"
        elif score >= 40:
            return "🔶 Degraded"
        else:
            return "🔴 Critical"
    
    def _estimate_current_capacity(self) -> int:
        """Estimate maximum capacity with current setup"""
        # This is a simplified estimation
        avg_response_time = sum(self.request_times) / len(self.request_times) if self.request_times else 0.1
        
        # SQLite baseline capacity
        if avg_response_time < 0.5:
            return 200
        elif avg_response_time < 1.0:
            return 100
        else:
            return 50
    
    def _identify_bottlenecks(self, metrics: Dict) -> List[str]:
        """Identify system bottlenecks"""
        bottlenecks = []
        
        if metrics['avg_db_time'] > 500:
            bottlenecks.append("Database queries slow - consider PostgreSQL")
        
        if metrics['avg_request_time'] > 2000:
            bottlenecks.append("Overall response time slow - check app performance")
        
        if metrics['active_users'] > 100:
            bottlenecks.append("High user load for SQLite - upgrade database")
        
        return bottlenecks
    
    def _get_scaling_urgency(self, active_users: int) -> str:
        """Get scaling urgency level"""
        if active_users < 50:
            return "Low"
        elif active_users < 200:
            return "Medium"
        elif active_users < 500:
            return "High"
        else:
            return "Critical"

# Global monitor instance
monitor = PerformanceMonitor()

def start_monitoring():
    """Start performance monitoring"""
    monitor.start_monitoring()

def get_performance_report():
    """Get comprehensive performance report"""
    current_metrics = monitor.get_current_metrics()
    capacity_analysis = monitor.get_capacity_analysis()
    
    return {
        'current_performance': current_metrics,
        'capacity_analysis': capacity_analysis,
        'monitoring_active': monitor.monitoring,
        'total_metrics_collected': len(monitor.metrics_history)
    }

if __name__ == "__main__":
    print("📊 Performance Monitor Test")
    print("=" * 40)
    
    # Simulate some activity
    monitor.record_request("user1", 0.5)
    monitor.record_request("user2", 0.3)
    monitor.record_db_query(0.1)
    
    report = get_performance_report()
    print(f"Active Users: {report['current_performance']['active_users']}")
    print(f"Performance Score: {report['current_performance']['performance_score']}")
    print(f"System Status: {report['current_performance']['status']}")
    print(f"Capacity: {report['capacity_analysis']['estimated_capacity']} users")
