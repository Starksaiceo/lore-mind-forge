"""
🔄 Reflect and Adapt - AI CEO Multi-Agent Intelligence
Daily self-improvement system that learns from results and adapts strategies
"""

import logging
from datetime import datetime, timedelta
from models import db, AgentMemory
from memory_analyzer import MemoryAnalyzer
from config import OPENROUTER_API_KEY
import requests
import json
import os
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class ReflectionAgent:
    """AI agent that reflects on performance and adapts strategies"""
    
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.memory_analyzer = MemoryAnalyzer(user_id)
    
    def perform_daily_reflection(self) -> Dict:
        """Perform daily reflection on AI performance and results"""
        try:
            # Get comprehensive memory analysis
            analysis = self.memory_analyzer.generate_comprehensive_analysis()
            
            if "error" in analysis:
                logger.error(f"Memory analysis failed: {analysis['error']}")
                return {"error": "Memory analysis failed", "reflection_date": datetime.utcnow().isoformat()}
            
            # Extract key insights for reflection
            reflection_data = {
                "reflection_date": datetime.utcnow().isoformat(),
                "user_id": self.user_id,
                "performance_summary": self._summarize_performance(analysis),
                "learning_points": self._extract_learning_points(analysis),
                "adaptation_needed": self._identify_adaptation_needs(analysis),
                "success_patterns": self._identify_success_patterns(analysis),
                "failure_patterns": self._identify_failure_patterns(analysis)
            }
            
            # Generate AI-powered insights
            ai_insights = self._generate_ai_insights(reflection_data)
            reflection_data["ai_insights"] = ai_insights
            
            # Save reflection to memory
            self._save_reflection(reflection_data)
            
            logger.info(f"Daily reflection completed for user {self.user_id}")
            return reflection_data
            
        except Exception as e:
            logger.error(f"Daily reflection error: {e}")
            return {
                "error": str(e),
                "reflection_date": datetime.utcnow().isoformat(),
                "user_id": self.user_id
            }
    
    def _summarize_performance(self, analysis: Dict) -> Dict:
        """Summarize overall performance from analysis"""
        performance_summary = {
            "period_analyzed": analysis.get("period_analyzed_days", 30),
            "total_strategies_tested": 0,
            "overall_success_rate": 0,
            "revenue_trend": "stable"
        }
        
        # Extract performance metrics
        if "performance_analysis" in analysis:
            perf_data = analysis["performance_analysis"]
            performance_summary["overall_success_rate"] = perf_data.get("overall_win_rate", 0)
            performance_summary["total_activities"] = perf_data.get("total_activities", 0)
        
        if "strategy_analysis" in analysis:
            strat_data = analysis["strategy_analysis"]
            performance_summary["total_strategies_tested"] = strat_data.get("total_strategies_analyzed", 0)
        
        return performance_summary
    
    def _extract_learning_points(self, analysis: Dict) -> List[str]:
        """Extract key learning points from performance analysis"""
        learning_points = []
        
        # Strategy learnings
        if "strategy_analysis" in analysis and "top_strategies" in analysis["strategy_analysis"]:
            top_strategies = analysis["strategy_analysis"]["top_strategies"]
            if top_strategies:
                learning_points.append(f"Most profitable strategy: {top_strategies[0][0]}")
        
        # Product learnings
        if "product_analysis" in analysis and "top_categories" in analysis["product_analysis"]:
            top_categories = analysis["product_analysis"]["top_categories"]
            if top_categories:
                learning_points.append(f"Best performing product category: {top_categories[0][0]}")
        
        # Timing learnings
        if "timing_analysis" in analysis:
            timing_data = analysis["timing_analysis"]
            best_day = timing_data.get("best_day", "Unknown")
            best_hour = timing_data.get("best_hour", "Unknown")
            if best_day != "Unknown" and best_hour != "Unknown":
                learning_points.append(f"Optimal timing: {best_day} at {best_hour}")
        
        # Performance learnings
        if "performance_analysis" in analysis:
            perf_data = analysis["performance_analysis"]
            win_rate = perf_data.get("overall_win_rate", 0)
            if win_rate > 0.7:
                learning_points.append("High success rate indicates effective strategies")
            elif win_rate < 0.3:
                learning_points.append("Low success rate suggests need for strategy revision")
        
        return learning_points[:5]  # Top 5 learning points
    
    def _identify_adaptation_needs(self, analysis: Dict) -> List[Dict]:
        """Identify what needs to be adapted based on performance"""
        adaptations = []
        
        # Check win/loss ratios
        if "performance_analysis" in analysis:
            perf_data = analysis["performance_analysis"]
            needs_improvement = perf_data.get("needs_improvement", [])
            
            for activity in needs_improvement:
                adaptations.append({
                    "area": activity,
                    "issue": "Low success rate",
                    "priority": "high",
                    "suggested_action": f"Revise {activity} strategy or approach"
                })
        
        # Check strategy performance
        if "strategy_analysis" in analysis:
            strat_data = analysis["strategy_analysis"]
            strategy_perf = strat_data.get("strategy_performance", {})
            
            for strategy, metrics in strategy_perf.items():
                if metrics.get("success_rate", 0) < 0.4:
                    adaptations.append({
                        "area": f"strategy_{strategy}",
                        "issue": "Poor conversion rate",
                        "priority": "medium",
                        "suggested_action": f"Optimize {strategy} execution or replace"
                    })
        
        # Check product performance
        if "product_analysis" in analysis:
            prod_data = analysis["product_analysis"]
            category_perf = prod_data.get("category_performance", {})
            
            for category, metrics in category_perf.items():
                if metrics.get("conversion_rate", 0) < 0.2:
                    adaptations.append({
                        "area": f"product_{category}",
                        "issue": "Low conversion rate",
                        "priority": "medium",
                        "suggested_action": f"Improve {category} product quality or pricing"
                    })
        
        # Sort by priority
        priority_order = {"high": 3, "medium": 2, "low": 1}
        adaptations.sort(key=lambda x: priority_order.get(x["priority"], 0), reverse=True)
        
        return adaptations[:3]  # Top 3 adaptations needed
    
    def _identify_success_patterns(self, analysis: Dict) -> List[Dict]:
        """Identify patterns that lead to success"""
        success_patterns = []
        
        # Top performing strategies
        if "strategy_analysis" in analysis and "top_strategies" in analysis["strategy_analysis"]:
            top_strategies = analysis["strategy_analysis"]["top_strategies"]
            for i, (strategy, metrics) in enumerate(top_strategies[:3]):
                success_patterns.append({
                    "pattern_type": "strategy",
                    "pattern": strategy,
                    "success_metric": metrics.get("total_profit", 0),
                    "consistency": metrics.get("consistency", 0),
                    "rank": i + 1
                })
        
        # Best product categories
        if "product_analysis" in analysis and "top_categories" in analysis["product_analysis"]:
            top_categories = analysis["product_analysis"]["top_categories"]
            for i, (category, metrics) in enumerate(top_categories[:2]):
                success_patterns.append({
                    "pattern_type": "product_category",
                    "pattern": category,
                    "success_metric": metrics.get("total_revenue", 0),
                    "conversion_rate": metrics.get("conversion_rate", 0),
                    "rank": i + 1
                })
        
        # Best timing patterns
        if "timing_analysis" in analysis:
            timing_data = analysis["timing_analysis"]
            best_day = timing_data.get("best_day", "Unknown")
            best_hour = timing_data.get("best_hour", "Unknown")
            
            if best_day != "Unknown":
                success_patterns.append({
                    "pattern_type": "timing",
                    "pattern": f"{best_day} at {best_hour}",
                    "success_metric": "optimal_timing",
                    "rank": 1
                })
        
        return success_patterns
    
    def _identify_failure_patterns(self, analysis: Dict) -> List[Dict]:
        """Identify patterns that lead to failure"""
        failure_patterns = []
        
        # Poor performing strategies
        if "strategy_analysis" in analysis:
            strat_data = analysis["strategy_analysis"]
            strategy_perf = strat_data.get("strategy_performance", {})
            
            poor_strategies = [
                (strategy, metrics) for strategy, metrics in strategy_perf.items()
                if metrics.get("success_rate", 0) < 0.3
            ]
            
            for strategy, metrics in poor_strategies[:3]:
                failure_patterns.append({
                    "pattern_type": "strategy",
                    "pattern": strategy,
                    "failure_rate": 1 - metrics.get("success_rate", 0),
                    "total_attempts": metrics.get("total_attempts", 0)
                })
        
        # Underperforming product categories
        if "product_analysis" in analysis:
            prod_data = analysis["product_analysis"]
            category_perf = prod_data.get("category_performance", {})
            
            poor_categories = [
                (category, metrics) for category, metrics in category_perf.items()
                if metrics.get("conversion_rate", 0) < 0.2
            ]
            
            for category, metrics in poor_categories[:2]:
                failure_patterns.append({
                    "pattern_type": "product_category",
                    "pattern": category,
                    "failure_rate": 1 - metrics.get("conversion_rate", 0),
                    "avg_revenue": metrics.get("avg_revenue", 0)
                })
        
        return failure_patterns
    
    def _generate_ai_insights(self, reflection_data: Dict) -> Dict:
        """Generate AI-powered insights from reflection data"""
        try:
            prompt = f\"\"\"
            As an AI business advisor, analyze this performance reflection and provide strategic insights:
            
            Performance Summary:
            - Success Rate: {reflection_data['performance_summary'].get('overall_success_rate', 0):.2%}
            - Strategies Tested: {reflection_data['performance_summary'].get('total_strategies_tested', 0)}
            
            Learning Points:
            {chr(10).join(f"- {point}" for point in reflection_data.get('learning_points', []))}
            
            Success Patterns:
            {chr(10).join(f"- {p['pattern']} ({p['pattern_type']})" for p in reflection_data.get('success_patterns', []))}
            
            Areas Needing Improvement:
            {chr(10).join(f"- {a['area']}: {a['issue']}" for a in reflection_data.get('adaptation_needed', []))}
            
            Provide:
            1. Key insight about performance trends
            2. Top strategic recommendation for next period
            3. One specific tactic to improve results
            
            Format as JSON:
            {{
                "key_insight": "Your main insight",
                "strategic_recommendation": "Your recommendation", 
                "tactical_improvement": "Your specific tactic"
            }}
            \"\"\"
            
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "anthropic/claude-3-haiku",
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 300
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content'].strip()
                
                try:
                    ai_insights = json.loads(content)
                    return ai_insights
                except json.JSONDecodeError:
                    return self._fallback_insights(reflection_data)
            else:
                return self._fallback_insights(reflection_data)
                
        except Exception as e:
            logger.error(f"AI insights generation error: {e}")
            return self._fallback_insights(reflection_data)
    
    def _fallback_insights(self, reflection_data: Dict) -> Dict:
        """Generate fallback insights when AI fails"""
        success_rate = reflection_data['performance_summary'].get('overall_success_rate', 0)
        
        if success_rate > 0.7:
            key_insight = "Strong performance indicates effective strategy execution"
            recommendation = "Scale successful strategies and increase activity frequency"
        elif success_rate > 0.4:
            key_insight = "Moderate performance with room for optimization"
            recommendation = "Focus on improving conversion rates and strategy consistency"
        else:
            key_insight = "Performance below optimal - significant improvement needed"
            recommendation = "Analyze and replace underperforming strategies immediately"
        
        return {
            "key_insight": key_insight,
            "strategic_recommendation": recommendation,
            "tactical_improvement": "Focus on data-driven decision making and A/B testing"
        }
    
    def _save_reflection(self, reflection_data: Dict):
        """Save reflection results to memory"""
        try:
            memory = AgentMemory(
                user_id=self.user_id,
                key="daily_reflection",
                value=json.dumps(reflection_data)
            )
            db.session.add(memory)
            db.session.commit()
            
            logger.info(f"Reflection saved for user {self.user_id}")
            
        except Exception as e:
            logger.error(f"Reflection save error: {e}")
    
    def create_next_strategy_file(self, reflection_data: Dict) -> bool:
        """Create next_strategy.txt file for strategist to use"""
        try:
            # Extract key recommendations
            ai_insights = reflection_data.get("ai_insights", {})
            success_patterns = reflection_data.get("success_patterns", [])
            adaptation_needed = reflection_data.get("adaptation_needed", [])
            
            # Create strategy guidance content
            strategy_content = f\"\"\"# Next Strategy Guidance - {datetime.utcnow().strftime('%Y-%m-%d')}

## AI Insights
**Key Insight:** {ai_insights.get('key_insight', 'Focus on proven successful patterns')}

**Strategic Recommendation:** {ai_insights.get('strategic_recommendation', 'Continue with best performing strategies')}

**Tactical Improvement:** {ai_insights.get('tactical_improvement', 'Optimize execution and measurement')}

## Success Patterns to Replicate
\"\"\"
            
            for i, pattern in enumerate(success_patterns[:3], 1):
                strategy_content += f\"{i}. {pattern['pattern']} ({pattern['pattern_type']}) - Rank #{pattern['rank']}\\n\"
            
            strategy_content += \"\\n## Areas Requiring Adaptation\\n\"
            for i, adaptation in enumerate(adaptation_needed[:3], 1):
                strategy_content += f\"{i}. {adaptation['area']}: {adaptation['suggested_action']}\\n\"
            
            strategy_content += f\"\\n## Performance Summary\\n\"
            strategy_content += f\"- Success Rate: {reflection_data['performance_summary'].get('overall_success_rate', 0):.2%}\\n\"
            strategy_content += f\"- Total Strategies Tested: {reflection_data['performance_summary'].get('total_strategies_tested', 0)}\\n\"
            strategy_content += f\"- Reflection Date: {reflection_data['reflection_date']}\\n\"
            
            strategy_content += \"\\n---\\n*This guidance is automatically generated from AI performance analysis*\"
            
            # Write to file
            with open("next_strategy.txt", "w", encoding="utf-8") as f:
                f.write(strategy_content)
            
            logger.info("next_strategy.txt file created successfully")
            return True
            
        except Exception as e:
            logger.error(f"Strategy file creation error: {e}")
            return False
    
    def run_daily_reflection_cycle(self) -> Dict:
        """Main method: Run complete daily reflection and adaptation cycle"""
        try:
            # Perform reflection
            reflection_result = self.perform_daily_reflection()
            
            if "error" in reflection_result:
                return reflection_result
            
            # Create strategy guidance file
            file_created = self.create_next_strategy_file(reflection_result)
            reflection_result["strategy_file_created"] = file_created
            
            # Schedule next reflection (save reminder)
            next_reflection_time = datetime.utcnow() + timedelta(days=1)
            reflection_result["next_reflection_scheduled"] = next_reflection_time.isoformat()
            
            logger.info(f"Daily reflection cycle completed for user {self.user_id}")
            return reflection_result
            
        except Exception as e:
            logger.error(f"Reflection cycle error: {e}")
            return {
                "error": str(e),
                "reflection_date": datetime.utcnow().isoformat(),
                "user_id": self.user_id
            }

def run_daily_reflection(user_id: int) -> Dict:
    """Convenience function to run daily reflection"""
    reflector = ReflectionAgent(user_id)
    return reflector.run_daily_reflection_cycle()

def create_strategy_guidance(user_id: int) -> Dict:
    """Convenience function to create strategy guidance"""
    reflector = ReflectionAgent(user_id)
    reflection_data = reflector.perform_daily_reflection()
    file_created = reflector.create_next_strategy_file(reflection_data)
    
    return {
        "success": file_created,
        "guidance_created": file_created,
        "reflection_data": reflection_data
    }

if __name__ == "__main__":
    # Test the reflection system
    print("🔄 Testing Reflection Agent...")
    result = run_daily_reflection(1)
    print(f"Reflection completed: {'error' not in result}")
    print(f"Strategy file created: {result.get('strategy_file_created', False)}")
    print(f"AI insights generated: {'ai_insights' in result}")