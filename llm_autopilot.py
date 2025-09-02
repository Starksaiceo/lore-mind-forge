import os, httpx, asyncio, json
from typing import List, Dict

OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY")
BASE_URL = "https://openrouter.ai/api/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_KEY}",
    "HTTP-Referer": "https://replit.com",
    "X-Title": "AI CEO Autopilot",
}

SYSTEM_PERSONA = (
    "You are AI CEO, a rigorous, ethical, profit-focused business partner. "
    "Think in steps. Offer concrete, actionable business ideas. "
    "Focus on digital products, online services, and scalable businesses. "
    "Avoid illegal or high-risk activities. Be specific and practical."
)

def pick_model(task_hint: str = "", complexity: str = "auto") -> str:
    """Pick appropriate model based on task"""
    if complexity == "high" or "strategy" in task_hint:
        return "anthropic/claude-3.5-sonnet"
    elif complexity == "low" or "summary" in task_hint:
        return "meta-llama/llama-3.1-8b-instruct:free"
    else:
        return "openai/gpt-4o-mini"

def fallback_chain(primary_model: str) -> List[str]:
    """Model fallback chain"""
    models = [
        primary_model,
        "openai/gpt-4o-mini",
        "meta-llama/llama-3.1-8b-instruct:free",
        "google/gemma-2-9b-it:free"
    ]
    return list(dict.fromkeys(models))  # Remove duplicates while preserving order

async def complete(messages: List[dict], task_hint: str = "", complexity: str = "auto", max_tokens: int = 1000) -> str:
    """Complete chat with OpenRouter"""
    if not OPENROUTER_KEY:
        return "OpenRouter API key not configured. Please add OPENROUTER_API_KEY to your environment."

    model = pick_model(task_hint, complexity)

    for mid in fallback_chain(model):
        try:
            async with httpx.AsyncClient(timeout=90) as client:
                req = {
                    "model": mid,
                    "stream": False,
                    "max_tokens": max_tokens,
                    "messages": [{"role": "system", "content": SYSTEM_PERSONA}] + messages,
                }
                r = await client.post(BASE_URL, headers=HEADERS, json=req)
                r.raise_for_status()
                data = r.json()
                return data["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"Model {mid} failed: {e}")
            continue

    return "I tried several AI models but couldn't complete that request right now. Please try again later."

async def generate_business_ideas(user_context: str = "") -> List[str]:
    """Generate business ideas"""
    context_part = f" Context: {user_context}" if user_context else ""
    prompt = (
        f"Generate 5 online business/product ideas I can start this week with:"
        f"- Low startup cost (under $100)"
        f"- Clear target niche"
        f"- Simple fulfillment (digital preferred)"
        f"- High profit margin (70%+)"
        f"- Scalable with automation{context_part}"
        f"\nReturn as a numbered list with brief explanations."
    )

    response = await complete([{"role": "user", "content": prompt}], 
                            task_hint="ideation", complexity="high", max_tokens=800)

    # Extract ideas from response
    ideas = []
    for line in response.splitlines():
        line = line.strip()
        if line and (line[0].isdigit() or line.startswith('-') or line.startswith('•')):
            idea = line.lstrip('0123456789.-• ').strip()
            if idea and len(idea) > 10:  # Filter out too short ideas
                ideas.append(idea)

    return ideas[:5] if ideas else ["Digital course on a trending skill", "SaaS tool for small businesses"]

async def validate_and_rank_ideas(ideas: List[str]) -> Dict:
    """Validate and rank business ideas"""
    ideas_text = "\n".join([f"{i+1}. {idea}" for i, idea in enumerate(ideas)])

    prompt = (
        f"Analyze these business ideas and score each 1-10 for:\n"
        f"- Market Demand\n"
        f"- Competition Level (lower is better)\n"
        f"- Profit Margin Potential\n"
        f"- Speed to Launch\n"
        f"- Scalability\n\n"
        f"Ideas:\n{ideas_text}\n\n"
        f"Pick the BEST one overall and explain why in 2-3 sentences. "
        f"Return the analysis in this format:\n"
        f"BEST IDEA: [idea text]\n"
        f"REASONING: [brief explanation]\n"
        f"SCORES: [show scores for the best idea]"
    )

    response = await complete([{"role": "user", "content": prompt}], 
                            task_hint="validation", complexity="high")

    # Extract best idea
    best_idea = ideas[0]  # fallback
    reasoning = response

    for line in response.splitlines():
        if line.startswith("BEST IDEA:"):
            best_idea = line.replace("BEST IDEA:", "").strip()
            break

    return {
        "best_idea": best_idea,
        "analysis": response,
        "reasoning": reasoning
    }

async def create_product_copy(idea: str, target_price: float = 19.0) -> Dict:
    """Create product copy for the idea"""
    prompt = (
        f"Turn this business idea into a sellable product:\n"
        f"Idea: {idea}\n"
        f"Target Price: ${target_price}\n\n"
        f"Create:\n"
        f"1. PRODUCT TITLE: (under 60 characters, compelling)\n"
        f"2. DESCRIPTION: (120-200 words with benefits, features, and strong CTA)\n"
        f"3. KEY FEATURES: (3-5 bullet points)\n"
        f"4. TARGET AUDIENCE: (who would buy this)\n\n"
        f"Make it conversion-focused and professional."
    )

    response = await complete([{"role": "user", "content": prompt}], 
                            task_hint="copywriting", complexity="medium")

    # Extract components
    lines = response.splitlines()
    title = idea[:50]  # fallback
    description = response
    features = []
    audience = "entrepreneurs and business owners"

    current_section = None
    for line in lines:
        line = line.strip()
        if line.startswith("1. PRODUCT TITLE:") or line.startswith("PRODUCT TITLE:"):
            title = line.split(":", 1)[1].strip()
        elif line.startswith("2. DESCRIPTION:") or line.startswith("DESCRIPTION:"):
            current_section = "description"
            description = line.split(":", 1)[1].strip() if ":" in line else ""
        elif line.startswith("3. KEY FEATURES:") or line.startswith("KEY FEATURES:"):
            current_section = "features"
        elif line.startswith("4. TARGET AUDIENCE:") or line.startswith("TARGET AUDIENCE:"):
            audience = line.split(":", 1)[1].strip()
        elif current_section == "description" and line:
            description += " " + line
        elif current_section == "features" and line and (line.startswith("-") or line.startswith("•")):
            features.append(line.lstrip("-• ").strip())

    return {
        "title": title[:100],  # Ensure reasonable length
        "description": description.strip(),
        "features": features,
        "audience": audience,
        "price": target_price
    }

async def generate_recap(activities: List[Dict], user_name: str = "there") -> str:
    """Generate an intelligent recap of autopilot activities"""
    try:
        if not activities:
            return f"Welcome back, {user_name}! No autopilot activities since your last visit. Ready to start building?"

        # Analyze activities
        activity_types = {}
        total_activities = len(activities)
        growth_activities = {"posts": 0, "ads": 0, "social_platforms": set()}

        for activity in activities:
            activity_type = activity.get('activity_type', 'unknown')
            activity_types[activity_type] = activity_types.get(activity_type, 0) + 1

            # Track growth engine activities
            if activity_type in ['social', 'social_simulated']:
                growth_activities["posts"] += 1
                # Extract platform from details if available
                try:
                    details = json.loads(activity.get('details', '{}'))
                    platform = details.get('platform', 'unknown')
                    if platform != 'unknown':
                        growth_activities["social_platforms"].add(platform)
                except:
                    pass
            elif activity_type in ['ads', 'ads_simulated']:
                growth_activities["ads"] += 1

        # Generate natural language recap
        recap_parts = [f"Welcome back, {user_name}!"]

        if 'launch' in activity_types:
            recap_parts.append(f"🚀 Launched {activity_types['launch']} new product(s)")

        if 'research' in activity_types:
            recap_parts.append(f"🔍 Conducted {activity_types['research']} market research sessions")

        if 'copywriting' in activity_types:
            recap_parts.append(f"✍️ Generated {activity_types['copywriting']} pieces of marketing copy")

        # Growth Engine highlights
        if growth_activities["posts"] > 0 or growth_activities["ads"] > 0:
            growth_parts = []

            if growth_activities["posts"] > 0:
                platforms_text = f" across {len(growth_activities['social_platforms'])} platforms" if growth_activities["social_platforms"] else ""
                growth_parts.append(f"📱 Posted {growth_activities['posts']} times{platforms_text}")

            if growth_activities["ads"] > 0:
                ad_status = "simulated" if 'ads_simulated' in activity_types else "live"
                growth_parts.append(f"📢 Created {growth_activities['ads']} ad campaign(s) ({ad_status})")

            if growth_parts:
                recap_parts.append("🎯 Growth Highlights: " + ", ".join(growth_parts))

        if total_activities > 0:
            recap_parts.append(f"📊 Total activities: {total_activities}")

        return " ".join(recap_parts)

    except Exception as e:
        return f"Welcome back, {user_name}! There was an issue generating your recap, but I'm ready to help you build!"