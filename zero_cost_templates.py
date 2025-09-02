
import os
import json
from datetime import datetime

# Business templates that work without AI
BUSINESS_TEMPLATES = {
    "digital_products": [
        {
            "title": "AI Business Automation Checklist",
            "price": 27,
            "content": """# AI Business Automation Checklist

## Phase 1: Foundation (Week 1)
- [ ] Set up business email
- [ ] Create social media profiles
- [ ] Design basic logo/branding
- [ ] Set up payment processing

## Phase 2: Product Creation (Week 2)
- [ ] Research target market
- [ ] Create minimum viable product
- [ ] Set up landing page
- [ ] Write sales copy

## Phase 3: Marketing (Week 3)
- [ ] Launch social media campaigns
- [ ] Start email list building
- [ ] Create content calendar
- [ ] Network with potential customers

## Phase 4: Scale (Week 4)
- [ ] Analyze metrics
- [ ] Optimize conversion rates
- [ ] Expand product line
- [ ] Automate processes
""",
            "category": "business"
        },
        {
            "title": "Productivity Planner Template",
            "price": 19,
            "content": """# Ultimate Productivity Planner

## Daily Planning Template

### Morning Routine
- [ ] Review today's priorities
- [ ] Set 3 main goals
- [ ] Time block calendar
- [ ] Eliminate distractions

### Work Sessions
**Session 1 (9-11 AM)**
Focus: ___________________
Tasks:
- [ ] ___________________
- [ ] ___________________

**Session 2 (11 AM-1 PM)**
Focus: ___________________
Tasks:
- [ ] ___________________
- [ ] ___________________

### Evening Review
- What went well?
- What could improve?
- Tomorrow's priorities:
""",
            "category": "productivity"
        }
    ],
    "content_templates": [
        {
            "platform": "LinkedIn",
            "template": """🚀 Just discovered a game-changing approach to [TOPIC]

Here's what I learned:

💡 Key insight #1: [INSIGHT]
📈 Key insight #2: [INSIGHT]  
🎯 Key insight #3: [INSIGHT]

The biggest mistake people make? [MISTAKE]

Instead, try this: [SOLUTION]

What's been your experience with [TOPIC]?

#business #productivity #growth""",
            "engagement_score": 85
        },
        {
            "platform": "Twitter",
            "template": """🧵 Thread: How to [ACHIEVE GOAL] in 30 days

1/ The problem: [PROBLEM]

2/ Why most people fail: [REASON]

3/ The solution: [SOLUTION]

4/ Step-by-step process:
- Step 1: [ACTION]
- Step 2: [ACTION]
- Step 3: [ACTION]

5/ Pro tip: [TIP]

Retweet if this was helpful! 🔄""",
            "engagement_score": 78
        }
    ]
}

def create_zero_cost_product(category="business"):
    """Create a product without AI using templates"""
    products = BUSINESS_TEMPLATES["digital_products"]
    template = None
    
    for product in products:
        if product["category"] == category:
            template = product
            break
    
    if not template:
        template = products[0]  # Default to first product
    
    # Create unique filename
    timestamp = int(datetime.now().timestamp())
    filename = f"product_{timestamp}.md"
    
    # Write to file
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# {template['title']}\n\n")
        f.write(f"**Price: ${template['price']}**\n\n")
        f.write(template['content'])
    
    return {
        "title": template['title'],
        "price": template['price'],
        "filename": filename,
        "category": category,
        "created": True
    }

def create_social_content(platform="LinkedIn", topic="business"):
    """Create social media content using templates"""
    templates = BUSINESS_TEMPLATES["content_templates"]
    
    # Find template for platform
    template = None
    for t in templates:
        if t["platform"] == platform:
            template = t
            break
    
    if not template:
        template = templates[0]  # Default
    
    # Customize template
    content = template["template"]
    content = content.replace("[TOPIC]", topic)
    content = content.replace("[GOAL]", f"master {topic}")
    content = content.replace("[PROBLEM]", f"Most people struggle with {topic}")
    
    return {
        "platform": platform,
        "content": content,
        "engagement_score": template["engagement_score"],
        "topic": topic
    }

def generate_business_plan(business_type="digital products"):
    """Generate a business plan using templates"""
    plan = f"""# {business_type.title()} Business Plan

## Executive Summary
Launch a profitable {business_type} business using proven templates and strategies.

## Market Analysis
- Target market: Entrepreneurs, small business owners, professionals
- Market size: $50B+ digital products market
- Competition: Moderate, opportunity for differentiation

## Product Strategy
1. Create high-value templates and checklists
2. Price between $19-97 for maximum accessibility
3. Focus on immediate value and actionability

## Marketing Strategy
1. Content marketing on LinkedIn and Twitter
2. Email list building with lead magnets
3. Partnership with complementary businesses
4. Organic social media growth

## Financial Projections
- Month 1: $500-1,000 revenue
- Month 3: $2,000-5,000 revenue  
- Month 6: $5,000-10,000 revenue
- Month 12: $10,000-20,000 revenue

## Action Steps
1. Create first product using templates
2. Set up payment processing (Stripe)
3. Build simple landing page
4. Launch social media marketing
5. Collect customer feedback and iterate
"""
    
    filename = f"business_plan_{int(datetime.now().timestamp())}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(plan)
    
    return {
        "business_type": business_type,
        "filename": filename,
        "success": True
    }

if __name__ == "__main__":
    print("🚀 Testing Zero-Cost Templates...")
    
    # Test product creation
    product = create_zero_cost_product("business")
    print(f"Created product: {product}")
    
    # Test content creation
    content = create_social_content("LinkedIn", "AI automation")
    print(f"Created content: {content['content'][:100]}...")
    
    # Test business plan
    plan = generate_business_plan("AI tools")
    print(f"Created business plan: {plan}")
