"""
🧠 Memory Analyzer - AI CEO Multi-Agent Intelligence
Analyzes historical performance data to identify best strategies and patterns
"""

import logging
from datetime import datetime, timedelta
from models import db, AgentMemory, ProductStore
from sqlalchemy import func, desc
import json
from typing import Dict, List, Optional
from collections import defaultdict, Counter
import statistics

logger = logging.getLogger(__name__)

class MemoryAnalyzer:
    """Analyzes AI memory to identify patterns and optimal strategies"""
    
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.analysis_period_days = 30  # Analyze last 30 days
    
    def get_all_memories(self, memory_type: str = None) -> List[Dict]:
        """Retrieve all relevant memories for analysis"""
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=self.analysis_period_days)
            
            query = db.session.query(AgentMemory).filter(
                AgentMemory.user_id == self.user_id,
                AgentMemory.created_at >= cutoff_date
            )
            
            if memory_type:
                query = query.filter(AgentMemory.key == memory_type)
            
            memories = query.order_by(desc(AgentMemory.created_at)).all()
            
            parsed_memories = []
            for memory in memories:
                try:
                    parsed_data = {
                        "id": memory.id,
                        "key": memory.key,
                        "created_at": memory.created_at,
                        "data": json.loads(memory.value) if memory.value else {}
                    }
                    parsed_memories.append(parsed_data)
                except json.JSONDecodeError:
                    # Handle non-JSON memories
                    parsed_memories.append({
                        "id": memory.id,
                        "key": memory.key,
                        "created_at": memory.created_at,
                        "data": {"raw_value": memory.value}
                    })
            
            return parsed_memories
            
        except Exception as e:
            logger.error(f"Error retrieving memories: {e}")
            return []
    
    def analyze_strategy_performance(self) -> Dict:
        """Analyze which strategies have been most profitable"""
        try:
            strategy_memories = self.get_all_memories("strategy_result")
            flip_memories = self.get_all_memories("flip_result")
            
            all_strategy_data = strategy_memories + flip_memories
            
            if not all_strategy_data:
                return {"error": "No strategy data available for analysis"}
            
            # Group by strategy type
            strategy_performance = defaultdict(list)
            
            for memory in all_strategy_data:
                data = memory.get("data", {})
                strategy = data.get("strategy", "unknown")
                profit = data.get("profit", 0)
                
                if isinstance(profit, (int, float)) and profit > 0:
                    strategy_performance[strategy].append({
                        "profit": profit,
                        "date": memory["created_at"],
                        "data": data
                    })
            
            # Calculate performance metrics
            strategy_stats = {}
            for strategy, results in strategy_performance.items():
                profits = [r["profit"] for r in results]
                strategy_stats[strategy] = {
                    "total_attempts": len(results),
                    "total_profit": sum(profits),
                    "avg_profit": statistics.mean(profits) if profits else 0,
                    "success_rate": len([p for p in profits if p > 0]) / len(profits) if profits else 0,
                    "best_result": max(profits) if profits else 0,
                    "consistency": 1 - (statistics.stdev(profits) / statistics.mean(profits)) if len(profits) > 1 and statistics.mean(profits) > 0 else 0
                }
            
            # Rank strategies by performance
            ranked_strategies = sorted(
                strategy_stats.items(),
                key=lambda x: x[1]["total_profit"] * x[1]["success_rate"],
                reverse=True
            )
            
            return {
                "analysis_period_days": self.analysis_period_days,
                "total_strategies_analyzed": len(strategy_stats),
                "strategy_performance": dict(strategy_stats),
                "top_strategies": ranked_strategies[:5],
                "recommendations": self._generate_strategy_recommendations(ranked_strategies)
            }
            
        except Exception as e:
            logger.error(f"Strategy analysis error: {e}")
            return {"error": str(e)}
    
    def analyze_product_patterns(self) -> Dict:
        """Analyze which types of products perform best"""
        try:
            # Get products from database
            cutoff_date = datetime.utcnow() - timedelta(days=self.analysis_period_days)
            products = db.session.query(ProductStore).filter(
                ProductStore.user_id == self.user_id,
                ProductStore.created_at >= cutoff_date
            ).all()
            
            if not products:
                return {"error": "No recent products for analysis"}
            
            # Group by category
            category_performance = defaultdict(list)
            price_ranges = {"low": [], "medium": [], "high": []}
            
            for product in products:
                category = product.category or "unknown"
                revenue = product.revenue or 0
                price = product.price or 0
                
                category_performance[category].append({
                    "revenue": revenue,
                    "price": price,
                    "title": product.title,
                    "profit_margin": (revenue - price * 0.3) / revenue if revenue > 0 else 0  # Assume 30% cost
                })
                
                # Price range analysis
                if price < 10:
                    price_ranges["low"].append(revenue)
                elif price < 50:
                    price_ranges["medium"].append(revenue)
                else:
                    price_ranges["high"].append(revenue)
            
            # Calculate category stats
            category_stats = {}
            for category, products_data in category_performance.items():
                revenues = [p["revenue"] for p in products_data]
                prices = [p["price"] for p in products_data]
                
                category_stats[category] = {
                    "product_count": len(products_data),
                    "total_revenue": sum(revenues),
                    "avg_revenue": statistics.mean(revenues) if revenues else 0,
                    "avg_price": statistics.mean(prices) if prices else 0,
                    "conversion_rate": len([r for r in revenues if r > 0]) / len(revenues) if revenues else 0,
                    "best_performer": max(products_data, key=lambda x: x["revenue"])["title"] if products_data else "None"
                }
            
            # Price range analysis
            price_analysis = {}
            for range_name, revenues in price_ranges.items():
                if revenues:
                    price_analysis[range_name] = {
                        "product_count": len(revenues),
                        "avg_revenue": statistics.mean(revenues),
                        "total_revenue": sum(revenues)
                    }
            
            return {
                "total_products": len(products),
                "category_performance": dict(category_stats),
                "price_range_analysis": price_analysis,
                "top_categories": sorted(category_stats.items(), key=lambda x: x[1]["total_revenue"], reverse=True)[:3],
                "insights": self._generate_product_insights(category_stats, price_analysis)
            }
            
        except Exception as e:
            logger.error(f"Product analysis error: {e}")
            return {"error": str(e)}
    
    def analyze_timing_patterns(self) -> Dict:
        """Analyze when strategies/products perform best"""
        try:
            all_memories = self.get_all_memories()
            
            if not all_memories:
                return {"error": "No timing data available"}
            
            # Group by day of week and hour
            day_performance = defaultdict(list)
            hour_performance = defaultdict(list)
            monthly_trends = defaultdict(list)
            
            for memory in all_memories:
                created_at = memory["created_at"]
                data = memory.get("data", {})
                profit = data.get("profit", 0) if isinstance(data.get("profit"), (int, float)) else 0
                
                # Day of week (0=Monday, 6=Sunday)
                day_of_week = created_at.weekday()
                day_performance[day_of_week].append(profit)
                
                # Hour of day
                hour = created_at.hour
                hour_performance[hour].append(profit)
                
                # Month
                month = created_at.month
                monthly_trends[month].append(profit)
            
            # Calculate averages
            day_stats = {}
            day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            for day_num, profits in day_performance.items():
                if profits:
                    day_stats[day_names[day_num]] = {
                        "avg_profit": statistics.mean(profits),
                        "total_activities": len(profits)
                    }
            
            hour_stats = {}
            for hour, profits in hour_performance.items():
                if profits:
                    hour_stats[f"{hour:02d}:00"] = {
                        "avg_profit": statistics.mean(profits),
                        "total_activities": len(profits)
                    }
            
            # Find best times
            best_day = max(day_stats.items(), key=lambda x: x[1]["avg_profit"]) if day_stats else None
            best_hour = max(hour_stats.items(), key=lambda x: x[1]["avg_profit"]) if hour_stats else None
            
            return {
                "day_performance": day_stats,
                "hour_performance": hour_stats,
                "best_day": best_day[0] if best_day else "Unknown",
                "best_hour": best_hour[0] if best_hour else "Unknown",
                "timing_insights": self._generate_timing_insights(day_stats, hour_stats)
            }
            
        except Exception as e:
            logger.error(f"Timing analysis error: {e}")
            return {"error": str(e)}
    
    def calculate_win_loss_ratios(self) -> Dict:
        """Calculate success/failure ratios across different activities"""
        try:
            all_memories = self.get_all_memories()
            
            activity_results = defaultdict({"wins": 0, "losses": 0, "neutral": 0})
            
            for memory in all_memories:
                key = memory["key"]
                data = memory.get("data", {})
                
                # Determine win/loss based on profit or success indicators
                profit = data.get("profit", 0)
                success = data.get("success", None)
                
                if isinstance(profit, (int, float)):
                    if profit > 0:
                        activity_results[key]["wins"] += 1
                    elif profit < 0:
                        activity_results[key]["losses"] += 1
                    else:
                        activity_results[key]["neutral"] += 1
                elif success is True:
                    activity_results[key]["wins"] += 1
                elif success is False:
                    activity_results[key]["losses"] += 1
                else:
                    activity_results[key]["neutral"] += 1
            
            # Calculate ratios
            ratios = {}
            for activity, results in activity_results.items():
                total = results["wins"] + results["losses"] + results["neutral"]
                if total > 0:
                    ratios[activity] = {
                        "win_rate": results["wins"] / total,
                        "loss_rate": results["losses"] / total,
                        "neutral_rate": results["neutral"] / total,
                        "total_attempts": total,
                        "wins": results["wins"],
                        "losses": results["losses"]
                    }
            
            # Overall performance
            total_wins = sum(r["wins"] for r in ratios.values())
            total_attempts = sum(r["total_attempts"] for r in ratios.values())
            overall_win_rate = total_wins / total_attempts if total_attempts > 0 else 0
            
            return {
                "activity_ratios": dict(ratios),
                "overall_win_rate": overall_win_rate,
                "total_activities": total_attempts,
                "best_performing_activity": max(ratios.items(), key=lambda x: x[1]["win_rate"]) if ratios else None,
                "needs_improvement": [k for k, v in ratios.items() if v["win_rate"] < 0.3]
            }
            
        except Exception as e:
            logger.error(f"Win/loss analysis error: {e}")
            return {"error": str(e)}
    
    def generate_comprehensive_analysis(self) -> Dict:
        """Generate complete memory analysis report"""
        try:
            strategy_analysis = self.analyze_strategy_performance()
            product_analysis = self.analyze_product_patterns()
            timing_analysis = self.analyze_timing_patterns()
            winloss_analysis = self.calculate_win_loss_ratios()
            
            # Generate overall recommendations
            overall_recommendations = []
            
            # Strategy recommendations
            if "top_strategies" in strategy_analysis:
                top_strategy = strategy_analysis["top_strategies"][0] if strategy_analysis["top_strategies"] else None
                if top_strategy:
                    overall_recommendations.append(f"Focus on '{top_strategy[0]}' strategy - highest total profit")
            
            # Product recommendations
            if "top_categories" in product_analysis:
                top_category = product_analysis["top_categories"][0] if product_analysis["top_categories"] else None
                if top_category:
                    overall_recommendations.append(f"Create more {top_category[0]} products - best performing category")
            
            # Timing recommendations
            if "best_day" in timing_analysis and "best_hour" in timing_analysis:
                overall_recommendations.append(f"Schedule important activities on {timing_analysis['best_day']} at {timing_analysis['best_hour']}")
            
            # Performance recommendations
            if "overall_win_rate" in winloss_analysis:
                win_rate = winloss_analysis["overall_win_rate"]
                if win_rate < 0.5:
                    overall_recommendations.append("Focus on improving strategy execution - current success rate is below 50%")
                elif win_rate > 0.7:
                    overall_recommendations.append("Excellent performance! Scale successful strategies")
            
            comprehensive_report = {
                "analysis_date": datetime.utcnow().isoformat(),
                "user_id": self.user_id,
                "period_analyzed_days": self.analysis_period_days,
                "strategy_analysis": strategy_analysis,
                "product_analysis": product_analysis,
                "timing_analysis": timing_analysis,
                "performance_analysis": winloss_analysis,
                "overall_recommendations": overall_recommendations[:5],  # Top 5 recommendations
                "next_analysis_date": (datetime.utcnow() + timedelta(days=7)).isoformat()
            }
            
            return comprehensive_report
            
        except Exception as e:
            logger.error(f"Comprehensive analysis error: {e}")
            return {
                "error": str(e),
                "analysis_date": datetime.utcnow().isoformat(),
                "user_id": self.user_id
            }
    
    def _generate_strategy_recommendations(self, ranked_strategies: List) -> List[str]:
        """Generate specific strategy recommendations"""
        recommendations = []
        
        if not ranked_strategies:
            return ["No strategy data available for recommendations"]
        
        top_strategy = ranked_strategies[0]
        recommendations.append(f"Prioritize '{top_strategy[0]}' - your most profitable strategy")
        
        if len(ranked_strategies) > 1:
            second_strategy = ranked_strategies[1]
            recommendations.append(f"Also consider '{second_strategy[0]}' as backup strategy")
        
        # Look for consistency patterns
        consistent_strategies = [s for s in ranked_strategies if s[1]["consistency"] > 0.7]
        if consistent_strategies:
            recommendations.append(f"'{consistent_strategies[0][0]}' shows high consistency - reliable choice")
        
        return recommendations[:3]
    
    def _generate_product_insights(self, category_stats: Dict, price_analysis: Dict) -> List[str]:
        """Generate product-specific insights"""
        insights = []
        
        if category_stats:
            best_category = max(category_stats.items(), key=lambda x: x[1]["avg_revenue"])
            insights.append(f"{best_category[0]} category generates highest average revenue")
        
        if price_analysis:
            best_price_range = max(price_analysis.items(), key=lambda x: x[1]["avg_revenue"])
            insights.append(f"{best_price_range[0]} price range performs best")
        
        return insights
    
    def _generate_timing_insights(self, day_stats: Dict, hour_stats: Dict) -> List[str]:
        """Generate timing-specific insights"""
        insights = []
        
        if day_stats:
            weekend_days = ["Saturday", "Sunday"]
            weekend_performance = [v["avg_profit"] for k, v in day_stats.items() if k in weekend_days]
            weekday_performance = [v["avg_profit"] for k, v in day_stats.items() if k not in weekend_days]
            
            if weekend_performance and weekday_performance:
                avg_weekend = statistics.mean(weekend_performance)
                avg_weekday = statistics.mean(weekday_performance)
                
                if avg_weekend > avg_weekday:
                    insights.append("Weekend activities tend to be more profitable")
                else:
                    insights.append("Weekday activities show better performance")
        
        return insights

def analyze_user_memory(user_id: int) -> Dict:
    """Convenience function to analyze user memory"""
    analyzer = MemoryAnalyzer(user_id)
    return analyzer.generate_comprehensive_analysis()

if __name__ == "__main__":
    # Test the memory analyzer
    print("🧠 Testing Memory Analyzer...")
    analysis = analyze_user_memory(1)
    print(f"Strategies analyzed: {len(analysis.get('strategy_analysis', {}).get('strategy_performance', {}))}")
    print(f"Recommendations: {len(analysis.get('overall_recommendations', []))}")