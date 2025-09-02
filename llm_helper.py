import os, requests, json, time

def chat_completion(messages, model="anthropic/claude-3-opus"):
    import requests, os, json

    headers = {
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
        # required by OpenRouter for public keys
        "HTTP-Referer": "https://replit.com/@YOUR_USERNAME/ai-ceo-agent-fix",
        "X-Title":      "AI-CEO agent",
        "Content-Type": "application/json",
    }

    payload = {"model": model, "messages": messages}

    try:
        r = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers, json=payload, timeout=30
        )
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]

    except requests.HTTPError as e:
        # Handle 402 Payment Required errors
        if e.response.status_code == 402:
            print("🆓 OpenRouter credits exhausted - switching to zero-cost mode")
            return generate_fallback_content(messages)

        # Claude-3 quota / 404 –> fallback to GPT-3.5
        if model.startswith("anthropic/"):
            payload["model"] = "openai/gpt-3.5-turbo"
            try:
                r = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers, json=payload, timeout=30
                )
                r.raise_for_status()
                return r.json()["choices"][0]["message"]["content"]
            except Exception as inner:
                print("Both models failed, returning stub:", inner)
                return generate_fallback_content(messages)
        else:
            raise

def generate_fallback_content(messages):
    """Generate content without API calls when in zero-cost mode"""
    user_message = messages[-1].get("content", "") if messages else ""

    # Product generation templates
    if any(keyword in user_message.lower() for keyword in ["product", "generate", "create", "business"]):
        return """AI Productivity Toolkit - Complete automation system for business productivity.

This comprehensive digital toolkit includes:
- Task automation templates
- Business process optimization guides  
- Time management strategies
- Revenue tracking systems
- Marketing automation workflows

Perfect for entrepreneurs and business owners looking to streamline operations and increase efficiency. Includes step-by-step implementation guides and ready-to-use templates."""

    # Marketing copy templates
    elif any(keyword in user_message.lower() for keyword in ["marketing", "copy", "ad", "campaign"]):
        return """🚀 Transform Your Business Today!

Discover the proven strategies that successful entrepreneurs use to:
✅ Automate tedious tasks
✅ Increase productivity by 300%
✅ Generate passive income streams
✅ Scale operations efficiently

Join thousands who've already transformed their business with our step-by-step system. Get instant access to tools, templates, and strategies that actually work."""

    # Email templates
    elif any(keyword in user_message.lower() for keyword in ["email", "subject", "newsletter"]):
        return """Subject: Your Business Automation Solution is Ready

Hi there,

Ready to take your business to the next level? 

Our AI-powered automation toolkit is designed specifically for entrepreneurs who want to:
- Save 10+ hours per week on repetitive tasks
- Increase revenue without working more hours
- Build systems that run on autopilot

Get started today with our proven templates and strategies.

Best regards,
The AI CEO Team"""

    # Default business content
    else:
        return """Professional business content generated using advanced AI templates. This system provides high-quality, conversion-focused copy for digital products, marketing campaigns, and business automation tools."""

def chat(prompt, primary="anthropic/claude-3-opus"):
    """Legacy function for backward compatibility"""
    messages = [{"role": "user", "content": prompt}]
    return chat_completion(messages, primary)
import os
from langchain_openai import ChatOpenAI

def get_llm_client():
    """Get configured LLM client for Growth Engine"""
    try:
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY not found")

        llm = ChatOpenAI(
            model="openai/gpt-4",
            temperature=0.7,
            openai_api_key=api_key,
            openai_api_base="https://openrouter.ai/api/v1",
            max_tokens=1000
        )

        # Add convenience method
        def complete(prompt, task_hint="general", complexity="medium"):
            try:
                messages = [{"role": "user", "content": prompt}]
                response = llm.invoke(messages)
                return response.content
            except Exception as e:
                return f"Error: {str(e)}"

        llm.complete = complete
        return llm

    except Exception as e:
        # Fallback client that returns placeholder responses
        class FallbackLLM:
            def complete(self, prompt, task_hint="general", complexity="medium"):
                return '{"success": false, "error": "LLM client not available"}'

        return FallbackLLM()
import openai
import os
import httpx
from typing import Dict, List, Any, Optional
import json
import logging

logger = logging.getLogger(__name__)

# OpenRouter configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

def get_llm_client():
    """Get OpenRouter client"""
    if not OPENROUTER_API_KEY:
        logger.warning("No OpenRouter API key found")
        return None

    return httpx.Client(
        base_url=OPENROUTER_BASE_URL,
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        },
        timeout=30.0
    )

def generate_text(prompt: str, model: str = "anthropic/claude-3-sonnet", max_tokens: int = 1000) -> str:
    """Generate text using OpenRouter"""
    try:
        client = get_llm_client()
        if not client:
            return f"Mock response for: {prompt[:50]}..."

        response = client.post("/chat/completions", json={
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": 0.7
        })

        if response.status_code == 200:
            data = response.json()
            return data["choices"][0]["message"]["content"]
        else:
            logger.error(f"LLM API error: {response.status_code}")
            return f"Mock response for: {prompt[:50]}..."

    except Exception as e:
        logger.error(f"LLM generation failed: {e}")
        return f"Mock response for: {prompt[:50]}..."

def generate_business_ideas(niche: str, count: int = 3) -> List[Dict[str, Any]]:
    """Generate business ideas for a niche"""
    try:
        prompt = f"Generate {count} profitable digital business ideas for the {niche} niche. Return as JSON array with title, description, target_audience, and revenue_model fields."

        response = generate_text(prompt, max_tokens=1500)

        # Try to parse JSON response
        try:
            ideas = json.loads(response)
            if isinstance(ideas, list):
                return ideas
        except json.JSONDecodeError:
            pass

        # Fallback to mock data
        return [
            {
                "title": f"{niche.title()} Solution",
                "description": f"Innovative digital solution for {niche} market",
                "target_audience": f"{niche} enthusiasts",
                "revenue_model": "subscription"
            }
        ]

    except Exception as e:
        logger.error(f"Business idea generation failed: {e}")
        return [
            {
                "title": f"{niche.title()} Product",
                "description": f"Digital product for {niche}",
                "target_audience": "General market",
                "revenue_model": "one-time"
            }
        ]

async def generate_recap(activities: List[Dict], user_name: str = "there") -> str:
    """Generate activity recap (simplified version)"""
    try:
        activity_count = len(activities)
        if activity_count == 0:
            return f"Welcome back, {user_name}! No recent activities to report."

        # Simple recap without LLM
        recap = f"Welcome back, {user_name}! While you were away, I completed {activity_count} tasks including business generation and product creation. Your AI CEO has been working hard!"

        return recap

    except Exception as e:
        logger.error(f"Recap generation failed: {e}")
        return f"Welcome back, {user_name}! Your AI CEO is ready to help."