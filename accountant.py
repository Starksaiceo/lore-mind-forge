"""
📊 Accountant Agent - AI CEO Multi-Agent Intelligence
Tracks profit/loss, calculates metrics, and generates financial summaries
"""

import logging
from datetime import datetime, timedelta
from models import db, ProductStore, Subscription, ShopifyOrder, AgentMemory
from sqlalchemy import func, desc
import json
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class AccountantAgent:
    """AI accountant that tracks finances and generates reports"""
    
    def __init__(self, user_id: int):
        self.user_id = user_id
    
    def calculate_product_revenue(self) -> Dict:
        """Calculate total revenue from products"""
        try:
            # Get all user products and their revenue
            products = db.session.query(ProductStore).filter_by(
                user_id=self.user_id
            ).all()
            
            total_revenue = sum(p.revenue or 0 for p in products)
            total_products = len(products)
            published_products = len([p for p in products if p.status == 'published'])
            avg_product_price = sum(p.price or 0 for p in products) / total_products if total_products > 0 else 0
            
            # Best performing product
            best_product = max(products, key=lambda p: p.revenue or 0) if products else None
            
            return {
                "total_revenue": round(total_revenue, 2),
                "total_products": total_products,
                "published_products": published_products,
                "avg_product_price": round(avg_product_price, 2),
                "best_product": {
                    "title": best_product.title if best_product else "None",
                    "revenue": best_product.revenue if best_product else 0
                } if best_product else None
            }
            
        except Exception as e:
            logger.error(f"Product revenue calculation error: {e}")
            return {"total_revenue": 0, "total_products": 0, "published_products": 0}
    
    def calculate_subscription_revenue(self) -> Dict:
        """Calculate MRR and subscription metrics"""
        try:
            # Get active subscriptions
            active_subs = db.session.query(Subscription).filter_by(
                user_id=self.user_id,
                status='active'
            ).all()
            
            # Calculate MRR by plan
            plan_revenue = {}
            total_mrr = 0
            
            for sub in active_subs:
                plan = sub.plan_id or 'starter'
                
                # Standard pricing (would be from config in real app)
                plan_prices = {
                    'starter': 29,
                    'pro': 99,
                    'enterprise': 299
                }
                
                plan_price = plan_prices.get(plan, 29)
                plan_revenue[plan] = plan_revenue.get(plan, 0) + plan_price
                total_mrr += plan_price
            
            return {
                "mrr": total_mrr,
                "active_subscriptions": len(active_subs),
                "plan_breakdown": plan_revenue,
                "arr": total_mrr * 12  # Annual recurring revenue
            }
            
        except Exception as e:
            logger.error(f"Subscription revenue calculation error: {e}")
            return {"mrr": 0, "active_subscriptions": 0, "arr": 0}
    
    def calculate_shopify_revenue(self) -> Dict:
        """Calculate revenue from Shopify orders"""
        try:
            # Get Shopify orders for user
            orders = db.session.query(ShopifyOrder).filter_by(
                user_id=self.user_id
            ).all()
            
            total_shopify_revenue = sum(o.total_price or 0 for o in orders)
            total_orders = len(orders)
            
            # Recent orders (last 30 days)
            thirty_days_ago = datetime.utcnow() - timedelta(days=30)
            recent_orders = [o for o in orders if o.created_at >= thirty_days_ago]
            recent_revenue = sum(o.total_price or 0 for o in recent_orders)
            
            return {
                "total_shopify_revenue": round(total_shopify_revenue, 2),
                "total_orders": total_orders,
                "recent_orders_30d": len(recent_orders),
                "recent_revenue_30d": round(recent_revenue, 2),
                "avg_order_value": round(total_shopify_revenue / total_orders, 2) if total_orders > 0 else 0
            }
            
        except Exception as e:
            logger.error(f"Shopify revenue calculation error: {e}")
            return {"total_shopify_revenue": 0, "total_orders": 0, "recent_revenue_30d": 0}
    
    def calculate_total_profit(self) -> Dict:
        """Calculate total profit across all revenue streams"""
        try:
            product_data = self.calculate_product_revenue()
            subscription_data = self.calculate_subscription_revenue()
            shopify_data = self.calculate_shopify_revenue()
            
            # Calculate costs (simplified)
            estimated_costs = self._calculate_estimated_costs(product_data, subscription_data)
            
            total_revenue = (
                product_data["total_revenue"] + 
                subscription_data["mrr"] + 
                shopify_data["total_shopify_revenue"]
            )
            
            total_profit = total_revenue - estimated_costs["total_costs"]
            profit_margin = (total_profit / total_revenue * 100) if total_revenue > 0 else 0
            
            return {
                "total_revenue": round(total_revenue, 2),
                "total_costs": round(estimated_costs["total_costs"], 2),
                "total_profit": round(total_profit, 2),
                "profit_margin": round(profit_margin, 2),
                "revenue_breakdown": {
                    "products": product_data["total_revenue"],
                    "subscriptions": subscription_data["mrr"], 
                    "shopify": shopify_data["total_shopify_revenue"]
                },
                "cost_breakdown": estimated_costs["breakdown"]
            }
            
        except Exception as e:
            logger.error(f"Total profit calculation error: {e}")
            return {"total_revenue": 0, "total_costs": 0, "total_profit": 0, "profit_margin": 0}
    
    def _calculate_estimated_costs(self, product_data: Dict, subscription_data: Dict) -> Dict:
        """Estimate business costs"""
        # Simplified cost calculation
        ai_api_costs = product_data["total_products"] * 0.50  # $0.50 per product for AI
        shopify_costs = 29 if product_data["total_products"] > 0 else 0  # Monthly Shopify fee
        marketing_costs = subscription_data["mrr"] * 0.15  # 15% of MRR for marketing
        payment_processing = subscription_data["mrr"] * 0.029  # 2.9% payment processing
        
        total_costs = ai_api_costs + shopify_costs + marketing_costs + payment_processing
        
        return {
            "total_costs": total_costs,
            "breakdown": {
                "ai_api": ai_api_costs,
                "shopify": shopify_costs,
                "marketing": marketing_costs,
                "payment_processing": payment_processing
            }
        }
    
    def generate_financial_summary(self) -> Dict:
        """Generate comprehensive financial summary"""
        try:
            profit_data = self.calculate_total_profit()
            
            # Get historical performance (last 7 days of memories)
            seven_days_ago = datetime.utcnow() - timedelta(days=7)
            historical_profits = db.session.query(AgentMemory).filter(
                AgentMemory.user_id == self.user_id,
                AgentMemory.key == 'daily_summary',
                AgentMemory.created_at >= seven_days_ago
            ).order_by(desc(AgentMemory.created_at)).limit(7).all()
            
            # Calculate trends
            daily_profits = []
            for memory in historical_profits:
                try:
                    data = json.loads(memory.value)
                    daily_profits.append(data.get('total_profit', 0))
                except:
                    continue
            
            # Calculate growth trends
            growth_trend = "stable"
            if len(daily_profits) >= 2:
                recent_avg = sum(daily_profits[:3]) / 3 if len(daily_profits) >= 3 else daily_profits[0]
                older_avg = sum(daily_profits[-3:]) / 3 if len(daily_profits) >= 3 else daily_profits[-1]
                
                if recent_avg > older_avg * 1.1:
                    growth_trend = "growing"
                elif recent_avg < older_avg * 0.9:
                    growth_trend = "declining"
            
            summary = {
                "date": datetime.utcnow().isoformat(),
                "financial_snapshot": profit_data,
                "performance_metrics": {
                    "growth_trend": growth_trend,
                    "days_tracked": len(daily_profits),
                    "avg_daily_profit": round(sum(daily_profits) / len(daily_profits), 2) if daily_profits else 0
                },
                "recommendations": self._generate_recommendations(profit_data, growth_trend),
                "next_goals": self._set_next_goals(profit_data)
            }
            
            return summary
            
        except Exception as e:
            logger.error(f"Financial summary error: {e}")
            return {
                "date": datetime.utcnow().isoformat(),
                "error": str(e),
                "financial_snapshot": {"total_profit": 0}
            }
    
    def _generate_recommendations(self, profit_data: Dict, growth_trend: str) -> List[str]:
        """Generate AI recommendations based on financial data"""
        recommendations = []
        
        profit_margin = profit_data.get("profit_margin", 0)
        total_revenue = profit_data.get("total_revenue", 0)
        
        if profit_margin < 20:
            recommendations.append("Consider reducing costs or increasing prices to improve profit margin")
        
        if total_revenue < 1000:
            recommendations.append("Focus on product creation and marketing to increase revenue")
        
        if growth_trend == "declining":
            recommendations.append("Analyze recent strategies and pivot to more profitable approaches")
        elif growth_trend == "growing":
            recommendations.append("Scale successful strategies and increase marketing budget")
        
        revenue_breakdown = profit_data.get("revenue_breakdown", {})
        if revenue_breakdown.get("subscriptions", 0) < revenue_breakdown.get("products", 0):
            recommendations.append("Focus on subscription growth for more predictable revenue")
        
        return recommendations[:3]  # Limit to top 3 recommendations
    
    def _set_next_goals(self, profit_data: Dict) -> List[Dict]:
        """Set next financial goals"""
        current_revenue = profit_data.get("total_revenue", 0)
        
        goals = []
        
        if current_revenue < 500:
            goals.append({"target": "Reach $500/month revenue", "timeline": "30 days"})
        elif current_revenue < 1000:
            goals.append({"target": "Reach $1,000/month revenue", "timeline": "60 days"})
        else:
            next_milestone = ((current_revenue // 1000) + 1) * 1000
            goals.append({"target": f"Reach ${next_milestone}/month revenue", "timeline": "90 days"})
        
        profit_margin = profit_data.get("profit_margin", 0)
        if profit_margin < 30:
            goals.append({"target": "Achieve 30% profit margin", "timeline": "45 days"})
        
        return goals
    
    def save_daily_summary(self) -> Dict:
        """Save daily financial summary to memory"""
        try:
            summary = self.generate_financial_summary()
            
            # Save to agent memory
            memory = AgentMemory(
                user_id=self.user_id,
                key="daily_summary",
                value=json.dumps(summary)
            )
            db.session.add(memory)
            db.session.commit()
            
            logger.info(f"Daily summary saved for user {self.user_id}")
            return {"success": True, "summary": summary}
            
        except Exception as e:
            logger.error(f"Daily summary save error: {e}")
            return {"success": False, "error": str(e)}
    
    def get_profit_report(self) -> Dict:
        """Main method: Generate complete profit/loss report"""
        try:
            # Get all financial data
            summary = self.generate_financial_summary()
            
            # Add additional insights
            insights = self._generate_insights(summary)
            
            report = {
                **summary,
                "insights": insights,
                "report_generated": datetime.utcnow().isoformat(),
                "user_id": self.user_id
            }
            
            # Save this report
            self.save_daily_summary()
            
            logger.info(f"Profit report generated for user {self.user_id}")
            return report
            
        except Exception as e:
            logger.error(f"Profit report error: {e}")
            return {
                "error": str(e),
                "report_generated": datetime.utcnow().isoformat(),
                "user_id": self.user_id
            }
    
    def _generate_insights(self, summary: Dict) -> List[str]:
        """Generate business insights from financial data"""
        insights = []
        
        financial_data = summary.get("financial_snapshot", {})
        revenue_breakdown = financial_data.get("revenue_breakdown", {})
        
        # Revenue diversification insight
        revenue_sources = sum(1 for v in revenue_breakdown.values() if v > 0)
        if revenue_sources == 1:
            insights.append("Consider diversifying revenue streams for stability")
        elif revenue_sources >= 3:
            insights.append("Great job diversifying revenue across multiple streams")
        
        # Growth insight
        growth_trend = summary.get("performance_metrics", {}).get("growth_trend")
        if growth_trend == "growing":
            insights.append("Your business is showing positive growth momentum")
        elif growth_trend == "declining":
            insights.append("Focus on customer retention and new acquisition strategies")
        
        # Profit margin insight
        profit_margin = financial_data.get("profit_margin", 0)
        if profit_margin > 50:
            insights.append("Excellent profit margins - you're running an efficient business")
        elif profit_margin > 30:
            insights.append("Healthy profit margins with room for reinvestment")
        elif profit_margin > 0:
            insights.append("Profitable but consider optimizing costs for better margins")
        else:
            insights.append("Focus on reducing costs and increasing revenue to achieve profitability")
        
        return insights

def generate_profit_report(user_id: int) -> Dict:
    """Convenience function to generate profit report"""
    accountant = AccountantAgent(user_id)
    return accountant.get_profit_report()

def save_daily_financial_summary(user_id: int) -> Dict:
    """Convenience function to save daily summary"""
    accountant = AccountantAgent(user_id)
    return accountant.save_daily_summary()

if __name__ == "__main__":
    # Test the accountant
    print("📊 Testing Accountant Agent...")
    report = generate_profit_report(1)
    print(f"Total Revenue: ${report.get('financial_snapshot', {}).get('total_revenue', 0)}")
    print(f"Total Profit: ${report.get('financial_snapshot', {}).get('total_profit', 0)}")
    print(f"Recommendations: {len(report.get('recommendations', []))}")