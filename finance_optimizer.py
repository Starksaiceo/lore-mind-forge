from typing import Dict, List, Optional
from datetime import datetime, timedelta
import os

class FinanceOptimizer:
    def __init__(self):
        self.budget_rules = {
            "min_ad_budget": 10.0,
            "max_ad_percentage": 0.30,  # Max 30% of revenue for ads
            "reinvestment_rate": 0.25,  # 25% of profit for reinvestment
            "emergency_reserve": 0.15   # 15% emergency fund
        }

    def calculate_optimal_ad_budget(self) -> Dict:
        """Calculate optimal ad budget based on current financials"""
        try:
            from profit_tracker import get_real_stripe_revenue

            current_revenue = get_real_stripe_revenue()

            if current_revenue == 0:
                return {
                    "success": True,
                    "recommended_budget": 0.0,
                    "reasoning": "No revenue yet - focus on organic growth first",
                    "can_afford_ads": False
                }

            # Calculate recommended budget
            max_ad_budget = current_revenue * self.budget_rules["max_ad_percentage"]
            reinvestment_budget = current_revenue * self.budget_rules["reinvestment_rate"]

            recommended_budget = min(max_ad_budget, reinvestment_budget)

            # Ensure minimum budget
            if recommended_budget < self.budget_rules["min_ad_budget"]:
                recommended_budget = 0.0
                can_afford = False
            else:
                can_afford = True

            return {
                "success": True,
                "recommended_budget": round(recommended_budget, 2),
                "max_budget": round(max_ad_budget, 2),
                "current_revenue": current_revenue,
                "can_afford_ads": can_afford,
                "reasoning": f"Based on {self.budget_rules['reinvestment_rate']*100}% reinvestment rate"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def assess_financial_health(self) -> Dict:
        """Assess overall financial health"""
        try:
            from profit_tracker import get_real_stripe_revenue, calculate_total_profit

            revenue = get_real_stripe_revenue()
            total_profit = calculate_total_profit()

            # Calculate health metrics
            if revenue == 0:
                health_score = 25
                health_status = "Starting - No revenue yet"
            elif revenue < 100:
                health_score = 40
                health_status = "Early stage - Building momentum"
            elif revenue < 500:
                health_score = 65
                health_status = "Growing - Good progress"
            elif revenue < 1000:
                health_score = 80
                health_status = "Scaling - Strong performance"
            else:
                health_score = 95
                health_status = "Thriving - Excellent growth"

            return {
                "success": True,
                "health_score": health_score,
                "health_status": health_status,
                "current_revenue": revenue,
                "total_profit": total_profit,
                "recommendations": self._generate_recommendations(revenue, health_score)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _generate_recommendations(self, revenue: float, health_score: int) -> List[str]:
        """Generate financial recommendations"""
        recommendations = []

        if revenue == 0:
            recommendations = [
                "Focus on creating and launching first product",
                "Build email list for future launches",
                "Create social media presence"
            ]
        elif revenue < 100:
            recommendations = [
                "Scale successful products",
                "Improve conversion rates",
                "Consider small ad campaigns"
            ]
        elif revenue < 500:
            recommendations = [
                "Automate successful processes",
                "Increase ad spend gradually",
                "Diversify product portfolio"
            ]
        else:
            recommendations = [
                "Scale profitable campaigns aggressively",
                "Build team for growth",
                "Explore new market segments"
            ]

        return recommendations

    def optimize_pricing_strategy(self, product_data: Dict) -> Dict:
        """Optimize pricing strategy for a product"""
        try:
            current_price = product_data.get("price", 47.0)
            category = product_data.get("category", "business")

            # Market-based pricing recommendations
            pricing_bands = {
                "business": {"min": 47, "optimal": 67, "premium": 97},
                "marketing": {"min": 37, "optimal": 57, "premium": 87},
                "productivity": {"min": 27, "optimal": 47, "premium": 77}
            }

            band = pricing_bands.get(category, pricing_bands["business"])

            # Determine optimal price
            if current_price < band["min"]:
                recommended_price = band["optimal"]
                reasoning = "Price too low for market positioning"
            elif current_price > band["premium"]:
                recommended_price = band["premium"]
                reasoning = "Price may be too high for initial sales"
            else:
                recommended_price = current_price
                reasoning = "Price is well-positioned"

            return {
                "success": True,
                "recommended_price": recommended_price,
                "current_price": current_price,
                "reasoning": reasoning,
                "price_band": band,
                "potential_revenue_increase": max(0, (recommended_price - current_price) / current_price * 100)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def calculate_roi_projection(self, ad_budget: float, product_price: float) -> Dict:
        """Calculate ROI projection for ad campaign"""
        try:
            # Estimated conversion rates based on industry averages
            base_conversion_rate = 0.02  # 2%

            # Calculate projections
            estimated_clicks = ad_budget * 50  # $1 = ~50 clicks (rough estimate)
            estimated_conversions = estimated_clicks * base_conversion_rate
            estimated_revenue = estimated_conversions * product_price
            estimated_roi = (estimated_revenue - ad_budget) / ad_budget if ad_budget > 0 else 0

            return {
                "success": True,
                "ad_budget": ad_budget,
                "estimated_clicks": int(estimated_clicks),
                "estimated_conversions": round(estimated_conversions, 1),
                "estimated_revenue": round(estimated_revenue, 2),
                "estimated_roi": round(estimated_roi * 100, 1),  # As percentage
                "break_even_conversions": int(ad_budget / product_price) if product_price > 0 else 0
            }
        except Exception as e:
            return {"success": False, "error": str(e)}