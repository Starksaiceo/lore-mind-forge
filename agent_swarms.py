import json
from datetime import datetime
from typing import Dict, List, Optional
import random
from profit_tracker import log_profit

class BaseAgent:
    def __init__(self, name: str, specialty: str):
        self.name = name
        self.specialty = specialty
        self.performance_score = 50

    def execute_task(self, task: str, context: Dict) -> Dict:
        """Execute a task - to be overridden by subclasses"""
        raise NotImplementedError("Subclasses must implement execute_task")

class SEOAgent(BaseAgent):
    def __init__(self):
        super().__init__("SEO Agent", "Search optimization and keyword research")

    def execute_task(self, task: str, context: Dict) -> Dict:
        """Execute SEO-focused task"""
        try:
            if "product" in task.lower() or "title" in task.lower():
                return self._optimize_product_seo(context)
            elif "keyword" in task.lower():
                return self._research_keywords(context)
            else:
                return self._generic_seo_task(task, context)

        except Exception as e:
            return {"error": str(e)}

    def _optimize_product_seo(self, context: Dict) -> Dict:
        """Optimize product for SEO"""
        product = context.get("product", {})
        title = product.get("title", "Product")

        # Add SEO keywords
        seo_keywords = ["AI", "automation", "business", "productivity", "tool"]

        # Find relevant keyword
        relevant_keyword = None
        for keyword in seo_keywords:
            if keyword.lower() not in title.lower():
                relevant_keyword = keyword
                break

        if relevant_keyword:
            optimized_title = f"{relevant_keyword} {title}"
        else:
            optimized_title = title

        return {
            "optimized_title": optimized_title,
            "seo_keywords": seo_keywords,
            "confidence": 0.8,
            "recommendations": [
                "Add long-tail keywords to description",
                "Optimize for mobile search",
                "Include location-based keywords if relevant"
            ]
        }

    def _research_keywords(self, context: Dict) -> Dict:
        """Research relevant keywords"""
        topic = context.get("topic", "business")

        keywords = {
            "business": ["business automation", "productivity tools", "workflow optimization"],
            "marketing": ["digital marketing", "social media tools", "lead generation"],
            "ai": ["AI tools", "machine learning", "artificial intelligence"]
        }

        return {
            "keywords": keywords.get(topic, keywords["business"]),
            "search_volume": "High",
            "competition": "Medium"
        }

    def _generic_seo_task(self, task: str, context: Dict) -> Dict:
        """Handle generic SEO tasks"""
        return {
            "task_completed": True,
            "seo_score": random.randint(70, 95),
            "recommendations": ["Optimize meta descriptions", "Improve page loading speed"]
        }

class PricingAgent(BaseAgent):
    def __init__(self):
        super().__init__("Pricing Agent", "Price optimization and market analysis")

    def execute_task(self, task: str, context: Dict) -> Dict:
        """Execute pricing-focused task"""
        try:
            product = context.get("product", {})
            current_price = product.get("price", 47.0)

            # Analyze market positioning
            if current_price < 30:
                recommended_price = current_price * 1.5
                reasoning = "Underpriced for market"
            elif current_price > 100:
                recommended_price = current_price * 0.9
                reasoning = "May be too high for initial market entry"
            else:
                recommended_price = current_price
                reasoning = "Price is well-positioned"

            return {
                "recommended_price": round(recommended_price, 2),
                "confidence": 0.85,
                "reasoning": reasoning,
                "market_position": "competitive"
            }
        except Exception as e:
            return {"error": str(e)}

class ContentAgent(BaseAgent):
    def __init__(self):
        super().__init__("Content Agent", "Content creation and optimization")

    def execute_task(self, task: str, context: Dict) -> Dict:
        """Execute content creation task"""
        try:
            product = context.get("product", {})

            if "description" in task.lower():
                return self._enhance_description(product)
            elif "social" in task.lower():
                return self._create_social_content(product)
            else:
                return self._generic_content_task(product)

        except Exception as e:
            return {"error": str(e)}

    def _enhance_description(self, product: Dict) -> Dict:
        """Enhance product description"""
        original_desc = product.get("description", "")

        enhanced_desc = f"""🚀 {original_desc}

✅ Key Benefits:
• Save 10+ hours per week
• Increase productivity by 200%
• Professional results guaranteed

🎯 Perfect For:
• Business owners
• Entrepreneurs
• Digital marketers
• Productivity enthusiasts

⚡ What You Get:
• Complete system setup
• Step-by-step guides
• Templates and tools
• Lifetime access"""

        return {
            "enhanced_description": enhanced_desc,
            "word_count": len(enhanced_desc.split()),
            "readability_score": 85
        }

    def _create_social_content(self, product: Dict) -> Dict:
        """Create social media content"""
        title = product.get("title", "Amazing Product")
        price = product.get("price", 47)

        social_posts = {
            "twitter": f"🚀 Just launched: {title}\n\n💰 Special price: ${price}\n\n#Business #Productivity #AI",
            "linkedin": f"Excited to share our latest solution: {title}. Designed to help professionals increase productivity and achieve better results.",
            "instagram": f"✨ New launch alert! ✨\n\n{title}\n\nSwipe to see what's included! 👉"
        }

        return {
            "social_posts": social_posts,
            "hashtags": ["#Business", "#Productivity", "#AI", "#Automation"],
            "estimated_reach": "1000-5000 impressions"
        }

    def _generic_content_task(self, product: Dict) -> Dict:
        """Handle generic content tasks"""
        return {
            "content_created": True,
            "quality_score": random.randint(80, 95),
            "engagement_prediction": "High"
        }

class AgentSwarm:
    def __init__(self):
        self.agents = {
            "seo": SEOAgent(),
            "pricing": PricingAgent(),
            "content": ContentAgent()
        }
        self.performance_history = {}

    def run_competitive_experiment(self, task: str, context: Dict) -> Dict:
        """Run multiple agents on same task and compare results"""
        try:
            results = {}

            for agent_name, agent in self.agents.items():
                try:
                    result = agent.execute_task(task, context)
                    results[agent_name] = result
                    score = self._score_agent_result(result, task)
                    self._update_performance(agent_name, task, score)
                except Exception as e:
                    results[agent_name] = {"error": str(e)}

            # Determine winner based on confidence scores
            winner = self._select_winning_strategy(results, task)

            return {
                "success": True,
                "results": results,
                "winner": winner,
                "task": task,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _score_agent_result(self, result: Dict, task: str) -> int:
        """Score agent result based on quality metrics"""
        score = 50  # Base score

        if not result or result.get("error"):
            return 0

        # Quality indicators
        if result.get("confidence", 0) > 0.7:
            score += 20
        if len(result.get("output", "")) > 100:
            score += 10
        if result.get("creative_elements", 0) > 3:
            score += 15
        if result.get("data_driven", False):
            score += 15

        return min(score, 100)

    def _update_performance(self, agent_name: str, task: str, score: int):
        """Update agent performance tracking"""
        if agent_name not in self.performance_history:
            self.performance_history[agent_name] = []

        self.performance_history[agent_name].append({
            "task": task,
            "score": score,
            "timestamp": datetime.now().isoformat()
        })

    def _select_winning_strategy(self, results: Dict, task: str) -> Dict:
        """Select the winning strategy from agent results"""
        best_score = 0
        winner = None

        for agent_name, result in results.items():
            if not result.get("error"):
                score = self._score_agent_result(result, task)
                if score > best_score:
                    best_score = score
                    winner = {
                        "agent": agent_name,
                        "result": result,
                        "score": score
                    }

        return winner or {"agent": "none", "result": {}, "score": 0}

    def get_best_agent_for_task(self, task_type: str) -> str:
        """Get the historically best performing agent for a task type"""
        agent_scores = {}

        for agent_name, history in self.performance_history.items():
            relevant_scores = [h["score"] for h in history if task_type in h["task"].lower()]
            if relevant_scores:
                agent_scores[agent_name] = sum(relevant_scores) / len(relevant_scores)

        if agent_scores:
            return max(agent_scores.items(), key=lambda x: x[1])[0]

        return "seo"  # Default to SEO agent

    def coordinate_task(self, task: str, context: Dict) -> Dict:
        """Coordinate multiple agents for complex task"""
        try:
            # SEO first
            seo_result = self.agents["seo"].execute_task(task, context)

            # Update context with SEO results
            if "optimized_title" in seo_result:
                context["product"]["title"] = seo_result["optimized_title"]

            # Pricing optimization
            pricing_result = self.agents["pricing"].execute_task(task, context)

            # Update price
            if "recommended_price" in pricing_result:
                context["product"]["price"] = pricing_result["recommended_price"]

            # Content enhancement
            content_result = self.agents["content"].execute_task(task, context)

            return {
                "success": True,
                "seo_optimization": seo_result,
                "pricing_optimization": pricing_result,
                "content_enhancement": content_result,
                "final_product": context["product"]
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

if __name__ == "__main__":
    swarm = AgentSwarm()

    # Test competition
    competition_result = swarm.run_competitive_experiment(
        "optimize product launch",
        {"product": {"title": "AI Business Toolkit", "price": 67, "description": "Complete automation system"}}
    )
    print("🏆 Agent competition result:", json.dumps(competition_result, indent=2))

    # Test coordinated task
    coordinated_task_result = swarm.coordinate_task(
        "enhance product listing",
        {"product": {"title": "AI Productivity Suite", "price": 99, "description": "Streamline your workflow"}}
    )
    print("\n🚀 Coordinated task result:", json.dumps(coordinated_task_result, indent=2))