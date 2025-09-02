import re
from typing import Dict, List, Optional

class PsychologyEngine:
    def __init__(self):
        self.psychological_triggers = [
            "scarcity", "authority", "social_proof", "urgency", "reciprocity"
        ]

    def enhance_product_copy(self, title: str, description: str, price: float) -> Dict:
        """Enhance product copy with psychological principles"""
        try:
            enhanced_title = self._enhance_title(title, price)
            enhanced_description = self._enhance_description(description, price)
            conversion_score = self._calculate_conversion_score(enhanced_title, enhanced_description)

            return {
                "success": True,
                "enhanced_title": enhanced_title,
                "enhanced_description": enhanced_description,
                "conversion_score": conversion_score,
                "psychological_triggers_used": ["authority", "scarcity", "social_proof"]
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _enhance_title(self, title: str, price: float) -> str:
        """Add psychological triggers to title"""
        enhancements = []

        if "AI" not in title:
            enhancements.append("AI-Powered")
        if "Professional" not in title:
            enhancements.append("Professional")

        enhanced = " ".join(enhancements + [title])

        # Add urgency/scarcity
        if price > 50:
            enhanced += " - Limited Time"

        return enhanced

    def _enhance_description(self, description: str, price: float) -> str:
        """Enhance description with psychological triggers"""
        # Add social proof
        social_proof = "\n\n✅ Trusted by 1000+ business professionals"

        # Add scarcity
        scarcity = "\n\n⏰ Limited availability - Get yours today!"

        # Add authority
        authority = "\n\n🎯 Developed by industry experts with 10+ years experience"

        enhanced = description + social_proof + authority + scarcity

        return enhanced

    def _calculate_conversion_score(self, title: str, description: str) -> int:
        """Calculate conversion potential score"""
        score = 50  # Base score

        # Check for power words
        power_words = ["professional", "expert", "proven", "guaranteed", "exclusive"]
        for word in power_words:
            if word.lower() in title.lower() or word.lower() in description.lower():
                score += 10

        # Check for psychological triggers
        triggers = ["limited", "exclusive", "trusted", "expert"]
        for trigger in triggers:
            if trigger.lower() in description.lower():
                score += 5

        return min(score, 100)

    def optimize_pricing_psychology(self, current_price: float) -> Dict:
        """Optimize pricing using psychological principles"""
        try:
            # Charm pricing (ending in 7 or 9)
            if current_price == int(current_price):
                optimized_price = current_price - 0.01 if current_price > 10 else current_price + 6.00
            else:
                optimized_price = current_price

            # Psychological anchoring
            if optimized_price < 100:
                anchor_price = optimized_price * 1.5  # Show higher "original" price
            else:
                anchor_price = optimized_price * 1.3

            return {
                "success": True,
                "optimized_price": round(optimized_price, 2),
                "anchor_price": round(anchor_price, 2),
                "psychological_principle": "charm_pricing"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}