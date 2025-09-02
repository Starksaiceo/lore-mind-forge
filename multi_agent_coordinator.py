"""
🤖 Multi-Agent Coordinator - AI CEO Intelligence Hub
Coordinates all 5 agents + memory + trend systems for autonomous business operations
"""

import logging
from datetime import datetime, timedelta
from models import db, AgentMemory, ProfitLog, StrategyCache
import json
import asyncio
from typing import Dict, List, Optional
import time

# Import all agents
from strategist import StrategistAgent, get_strategy_recommendation
from builder import BuilderAgent, build_product_from_strategy
from flipper import FlipperAgent, execute_flip_strategy
from marketer import MarketerAgent, execute_marketing_campaign
from accountant import AccountantAgent, generate_profit_report
from memory_analyzer import MemoryAnalyzer, analyze_user_memory
from reflect_and_adapt import ReflectionAgent, run_daily_reflection
from data_scraper import DataScraperAgent, scrape_trend_data

logger = logging.getLogger(__name__)

class MultiAgentCoordinator:
    """Orchestrates all AI agents for autonomous business operations"""
    
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.agents = {
            'strategist': StrategistAgent(user_id),
            'builder': BuilderAgent(user_id),
            'flipper': FlipperAgent(user_id),
            'marketer': MarketerAgent(user_id),
            'accountant': AccountantAgent(user_id),
            'memory_analyzer': MemoryAnalyzer(user_id),
            'reflection': ReflectionAgent(user_id),
            'data_scraper': DataScraperAgent()
        }
        self.cycle_history = []
    
    def run_autonomous_business_cycle(self) -> Dict:
        """Execute complete autonomous business cycle"""
        try:
            cycle_start = datetime.utcnow()
            cycle_id = f"cycle_{int(cycle_start.timestamp())}"
            
            logger.info(f"🚀 Starting autonomous business cycle {cycle_id} for user {self.user_id}")
            
            # Initialize cycle results
            cycle_results = {
                'cycle_id': cycle_id,
                'user_id': self.user_id,
                'start_time': cycle_start.isoformat(),
                'phases': {}
            }
            
            # Phase 1: Data Collection & Trend Analysis
            logger.info("📊 Phase 1: Data Collection & Trend Analysis")
            trend_data = self._collect_trend_data()
            cycle_results['phases']['trend_analysis'] = trend_data
            
            # Phase 2: Memory Analysis & Strategy Optimization
            logger.info("🧠 Phase 2: Memory Analysis & Strategy Optimization")
            memory_analysis = self._analyze_performance_memory()
            cycle_results['phases']['memory_analysis'] = memory_analysis
            
            # Phase 3: Strategic Decision Making
            logger.info("🎯 Phase 3: Strategic Decision Making")
            strategy_decision = self._make_strategic_decision(trend_data, memory_analysis)
            cycle_results['phases']['strategy_decision'] = strategy_decision
            
            # Phase 4: Product Creation or Optimization
            logger.info("🔨 Phase 4: Product Creation or Optimization")
            product_action = self._execute_product_action(strategy_decision)
            cycle_results['phases']['product_action'] = product_action
            
            # Phase 5: Marketing Campaign Execution
            logger.info("📢 Phase 5: Marketing Campaign Execution")
            marketing_results = self._execute_marketing_campaign(product_action)
            cycle_results['phases']['marketing'] = marketing_results
            
            # Phase 6: Financial Analysis & Profit Tracking
            logger.info("📊 Phase 6: Financial Analysis & Profit Tracking")
            financial_analysis = self._analyze_financials()
            cycle_results['phases']['financial_analysis'] = financial_analysis
            
            # Phase 7: Learning & Adaptation
            logger.info("🔄 Phase 7: Learning & Adaptation")
            learning_results = self._process_learning_and_adaptation(cycle_results)
            cycle_results['phases']['learning'] = learning_results
            
            # Complete cycle
            cycle_end = datetime.utcnow()
            cycle_duration = (cycle_end - cycle_start).total_seconds()
            
            cycle_results.update({
                'end_time': cycle_end.isoformat(),
                'duration_seconds': cycle_duration,
                'success': True,
                'summary': self._generate_cycle_summary(cycle_results)
            })
            
            # Save cycle to history
            self._save_cycle_results(cycle_results)
            
            logger.info(f"✅ Autonomous business cycle {cycle_id} completed in {cycle_duration:.2f} seconds")
            return cycle_results
            
        except Exception as e:
            logger.error(f"❌ Autonomous business cycle failed: {e}")
            return {
                'cycle_id': cycle_id if 'cycle_id' in locals() else 'unknown',
                'user_id': self.user_id,
                'success': False,
                'error': str(e),
                'timestamp': datetime.utcnow().isoformat()
            }
    
    def _collect_trend_data(self) -> Dict:
        """Phase 1: Collect and analyze trend data"""
        try:
            # Scrape latest trend data
            scraper_results = self.agents['data_scraper'].scrape_all_sources()
            
            # Get trending keywords for strategy
            trending_keywords = self.agents['data_scraper'].get_top_trends(20)
            
            return {
                'success': True,
                'scraper_results': scraper_results,
                'trending_keywords': trending_keywords,
                'top_trend': trending_keywords[0] if trending_keywords else None
            }
            
        except Exception as e:
            logger.error(f"Trend data collection error: {e}")
            return {'success': False, 'error': str(e)}
    
    def _analyze_performance_memory(self) -> Dict:
        """Phase 2: Analyze historical performance and memory"""
        try:
            # Run comprehensive memory analysis
            memory_analysis = self.agents['memory_analyzer'].generate_comprehensive_analysis()
            
            # Update strategy cache based on analysis
            self._update_strategy_cache(memory_analysis)
            
            return {
                'success': True,
                'analysis': memory_analysis,
                'recommendations': memory_analysis.get('overall_recommendations', [])
            }
            
        except Exception as e:
            logger.error(f"Memory analysis error: {e}")
            return {'success': False, 'error': str(e)}
    
    def _make_strategic_decision(self, trend_data: Dict, memory_analysis: Dict) -> Dict:
        """Phase 3: Make strategic decision using AI"""
        try:
            # Get strategy recommendation with trend and memory context
            strategy_result = self.agents['strategist'].decide_strategy()
            
            # Enhance with trend data
            if trend_data.get('top_trend'):
                strategy_result['trend_influence'] = trend_data['top_trend']
            
            # Enhance with memory insights
            if memory_analysis.get('success'):
                strategy_result['memory_insights'] = memory_analysis['analysis'].get('overall_recommendations', [])
            
            return {
                'success': True,
                'strategy': strategy_result,
                'decision_factors': {
                    'trend_data': trend_data.get('success', False),
                    'memory_analysis': memory_analysis.get('success', False)
                }
            }
            
        except Exception as e:
            logger.error(f"Strategic decision error: {e}")
            return {'success': False, 'error': str(e)}
    
    def _execute_product_action(self, strategy_decision: Dict) -> Dict:
        """Phase 4: Execute product creation or optimization"""
        try:
            if not strategy_decision.get('success'):
                return {'success': False, 'error': 'No valid strategy decision'}
            
            strategy = strategy_decision['strategy']
            recommended_strategy = strategy.get('recommended_strategy', '')
            strategy_type = strategy.get('strategy_type', 'ebook')
            
            # Decide between building new product or flipping existing
            action_type = self._decide_product_action()
            
            if action_type == 'build_new':
                # Build new product
                product_result = self.agents['builder'].build_product(
                    recommended_strategy, 
                    strategy_type
                )
                action_type_used = 'build_new'
                
            else:
                # Execute flip strategy on existing products
                product_result = self.agents['flipper'].execute_flip_strategy()
                action_type_used = 'flip_existing'
            
            return {
                'success': 'error' not in product_result,
                'action_type': action_type_used,
                'result': product_result,
                'product_created': product_result.get('title') or product_result.get('strategy')
            }
            
        except Exception as e:
            logger.error(f"Product action error: {e}")
            return {'success': False, 'error': str(e)}
    
    def _execute_marketing_campaign(self, product_action: Dict) -> Dict:
        """Phase 5: Execute marketing campaign for product"""
        try:
            if not product_action.get('success'):
                return {'success': False, 'error': 'No valid product for marketing'}
            
            # Prepare product data for marketing
            product_data = {
                'title': product_action['result'].get('title', 'Generated Product'),
                'description': product_action['result'].get('description', 'AI-generated product'),
                'price': product_action['result'].get('price', 19.99),
                'category': product_action['result'].get('category', 'digital')
            }
            
            # Execute marketing campaign
            marketing_result = self.agents['marketer'].execute_marketing_campaign(product_data)
            
            return {
                'success': marketing_result.get('success', False),
                'campaign': marketing_result,
                'content_generated': marketing_result.get('content_generated', 0),
                'posts_scheduled': marketing_result.get('posts_scheduled', 0)
            }
            
        except Exception as e:
            logger.error(f"Marketing execution error: {e}")
            return {'success': False, 'error': str(e)}
    
    def _analyze_financials(self) -> Dict:
        """Phase 6: Analyze financial performance"""
        try:
            # Generate comprehensive profit report
            financial_report = self.agents['accountant'].get_profit_report()
            
            # Log profit data
            self._log_cycle_profit(financial_report)
            
            return {
                'success': 'error' not in financial_report,
                'report': financial_report,
                'total_profit': financial_report.get('financial_snapshot', {}).get('total_profit', 0),
                'profit_margin': financial_report.get('financial_snapshot', {}).get('profit_margin', 0)
            }
            
        except Exception as e:
            logger.error(f"Financial analysis error: {e}")
            return {'success': False, 'error': str(e)}
    
    def _process_learning_and_adaptation(self, cycle_results: Dict) -> Dict:
        """Phase 7: Process learning and adapt strategies"""
        try:
            # Run reflection and adaptation
            reflection_result = self.agents['reflection'].run_daily_reflection_cycle()
            
            # Save cycle learnings to memory
            self._save_cycle_learnings(cycle_results)
            
            return {
                'success': 'error' not in reflection_result,
                'reflection': reflection_result,
                'strategy_file_created': reflection_result.get('strategy_file_created', False),
                'learnings_saved': True
            }
            
        except Exception as e:
            logger.error(f"Learning process error: {e}")
            return {'success': False, 'error': str(e)}
    
    def _decide_product_action(self) -> str:
        """Decide whether to build new product or flip existing ones"""
        try:
            # Check if user has existing products
            existing_products = self.agents['flipper'].get_existing_products()
            
            # Decision logic
            if len(existing_products) >= 3:
                # If 3+ products exist, 70% chance to flip, 30% to build new
                return 'flip_existing' if time.time() % 10 < 7 else 'build_new'
            elif len(existing_products) >= 1:
                # If 1-2 products exist, 50/50 chance
                return 'flip_existing' if time.time() % 2 else 'build_new'
            else:
                # No products exist, must build new
                return 'build_new'
                
        except Exception:
            # Default to building new product
            return 'build_new'
    
    def _update_strategy_cache(self, memory_analysis: Dict):
        """Update strategy performance cache"""
        try:
            if not memory_analysis.get('success'):
                return
            
            strategy_analysis = memory_analysis.get('analysis', {}).get('strategy_analysis', {})
            strategy_performance = strategy_analysis.get('strategy_performance', {})
            
            for strategy, metrics in strategy_performance.items():
                # Update or create strategy cache entry
                cache_entry = db.session.query(StrategyCache).filter_by(
                    user_id=self.user_id,
                    strategy=strategy
                ).first()
                
                if cache_entry:
                    # Update existing
                    cache_entry.average_profit = metrics.get('avg_profit', 0)
                    cache_entry.usage_count = metrics.get('total_attempts', 0)
                    cache_entry.success_rate = metrics.get('success_rate', 0)
                    cache_entry.last_used = datetime.utcnow()
                    cache_entry.performance_data = json.dumps(metrics)
                else:
                    # Create new
                    cache_entry = StrategyCache(
                        user_id=self.user_id,
                        strategy=strategy,
                        average_profit=metrics.get('avg_profit', 0),
                        usage_count=metrics.get('total_attempts', 0),
                        success_rate=metrics.get('success_rate', 0),
                        performance_data=json.dumps(metrics)
                    )
                    db.session.add(cache_entry)
            
            db.session.commit()
            
        except Exception as e:
            logger.error(f"Strategy cache update error: {e}")
    
    def _log_cycle_profit(self, financial_report: Dict):
        """Log cycle profit to database"""
        try:
            financial_snapshot = financial_report.get('financial_snapshot', {})
            
            # Log total profit
            profit_log = ProfitLog(
                user_id=self.user_id,
                source='autonomous_cycle',
                amount=financial_snapshot.get('total_profit', 0),
                profit_type='profit',
                additional_metadata=json.dumps({
                    'cycle_timestamp': datetime.utcnow().isoformat(),
                    'revenue_breakdown': financial_snapshot.get('revenue_breakdown', {}),
                    'profit_margin': financial_snapshot.get('profit_margin', 0)
                })
            )
            
            db.session.add(profit_log)
            db.session.commit()
            
        except Exception as e:
            logger.error(f"Profit logging error: {e}")
    
    def _save_cycle_learnings(self, cycle_results: Dict):
        """Save cycle results as learning memory"""
        try:
            # Extract key learnings
            learnings = {
                'cycle_id': cycle_results['cycle_id'],
                'strategy_success': cycle_results['phases'].get('strategy_decision', {}).get('success', False),
                'product_success': cycle_results['phases'].get('product_action', {}).get('success', False),
                'marketing_success': cycle_results['phases'].get('marketing', {}).get('success', False),
                'total_profit': cycle_results['phases'].get('financial_analysis', {}).get('total_profit', 0),
                'cycle_duration': cycle_results.get('duration_seconds', 0),
                'timestamp': cycle_results['start_time']
            }
            
            memory = AgentMemory(
                user_id=self.user_id,
                key='cycle_learnings',
                value=json.dumps(learnings)
            )
            
            db.session.add(memory)
            db.session.commit()
            
        except Exception as e:
            logger.error(f"Cycle learnings save error: {e}")
    
    def _save_cycle_results(self, cycle_results: Dict):
        """Save complete cycle results"""
        try:
            memory = AgentMemory(
                user_id=self.user_id,
                key='complete_cycle',
                value=json.dumps(cycle_results)
            )
            
            db.session.add(memory)
            db.session.commit()
            
            # Add to instance history
            self.cycle_history.append(cycle_results)
            
        except Exception as e:
            logger.error(f"Cycle results save error: {e}")
    
    def _generate_cycle_summary(self, cycle_results: Dict) -> Dict:
        """Generate human-readable cycle summary"""
        phases = cycle_results.get('phases', {})
        
        # Count successful phases
        successful_phases = sum(1 for phase in phases.values() if phase.get('success', False))
        total_phases = len(phases)
        
        # Extract key metrics
        profit = phases.get('financial_analysis', {}).get('total_profit', 0)
        product_created = phases.get('product_action', {}).get('product_created', 'None')
        posts_scheduled = phases.get('marketing', {}).get('posts_scheduled', 0)
        
        return {
            'phases_completed': f"{successful_phases}/{total_phases}",
            'success_rate': f"{(successful_phases/total_phases*100):.1f}%" if total_phases > 0 else "0%",
            'profit_generated': f"${profit:.2f}",
            'product_created': product_created,
            'marketing_posts': posts_scheduled,
            'cycle_status': 'success' if successful_phases >= total_phases * 0.7 else 'partial_success'
        }
    
    def get_cycle_history(self, limit: int = 10) -> List[Dict]:
        """Get recent cycle history"""
        return self.cycle_history[-limit:] if self.cycle_history else []
    
    def run_continuous_operation(self, cycles: int = 1, interval_minutes: int = 60) -> Dict:
        """Run multiple autonomous cycles with intervals"""
        continuous_results = {
            'start_time': datetime.utcnow().isoformat(),
            'cycles_planned': cycles,
            'interval_minutes': interval_minutes,
            'cycles_completed': [],
            'total_profit': 0
        }
        
        try:
            for cycle_num in range(cycles):
                logger.info(f"🔄 Starting continuous cycle {cycle_num + 1}/{cycles}")
                
                # Run autonomous cycle
                cycle_result = self.run_autonomous_business_cycle()
                continuous_results['cycles_completed'].append(cycle_result)
                
                # Track total profit
                cycle_profit = cycle_result.get('phases', {}).get('financial_analysis', {}).get('total_profit', 0)
                continuous_results['total_profit'] += cycle_profit
                
                # Wait before next cycle (if not last cycle)
                if cycle_num < cycles - 1:
                    logger.info(f"⏰ Waiting {interval_minutes} minutes before next cycle")
                    time.sleep(interval_minutes * 60)
            
            continuous_results['end_time'] = datetime.utcnow().isoformat()
            continuous_results['success'] = True
            
            logger.info(f"🏆 Continuous operation completed: {cycles} cycles, ${continuous_results['total_profit']:.2f} total profit")
            return continuous_results
            
        except Exception as e:
            logger.error(f"Continuous operation error: {e}")
            continuous_results.update({
                'success': False,
                'error': str(e),
                'end_time': datetime.utcnow().isoformat()
            })
            return continuous_results

def run_autonomous_cycle(user_id: int) -> Dict:
    """Convenience function to run single autonomous cycle"""
    coordinator = MultiAgentCoordinator(user_id)
    return coordinator.run_autonomous_business_cycle()

def run_continuous_business_operation(user_id: int, cycles: int = 3, interval_minutes: int = 30) -> Dict:
    """Convenience function for continuous operation"""
    coordinator = MultiAgentCoordinator(user_id)
    return coordinator.run_continuous_operation(cycles, interval_minutes)

if __name__ == "__main__":
    # Test the multi-agent coordinator
    print("🤖 Testing Multi-Agent Coordinator...")
    
    test_user_id = 1
    
    # Run single autonomous cycle
    result = run_autonomous_cycle(test_user_id)
    print(f"Cycle completed: {result.get('success')}")
    print(f"Phases completed: {result.get('summary', {}).get('phases_completed', '0/0')}")
    print(f"Profit generated: {result.get('summary', {}).get('profit_generated', '$0.00')}")
    
    if result.get('success'):
        print("✅ Multi-Agent Intelligence System is operational!")
    else:
        print(f"❌ System error: {result.get('error', 'Unknown error')}")