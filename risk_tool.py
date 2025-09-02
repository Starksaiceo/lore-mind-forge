
from langchain.agents import Tool
from langchain_openai import ChatOpenAI
import os
import json
import re
from dotenv import load_dotenv

load_dotenv()

def risk_check(action: str) -> dict:
    """
    Uses an LLM to score the risk of a proposed business action
    on a 0–1 scale and provide a brief justification.
    """
    try:
        llm = ChatOpenAI(
            model="openai/gpt-4",
            temperature=0,
            openai_api_key=os.getenv("OPENROUTER_API_KEY"),
            openai_api_base="https://openrouter.ai/api/v1"
        )
        
        prompt = f"""You are a corporate compliance officer and risk assessment expert.
        
Rate the risk level for this business action on a scale of 0.0 to 1.0:
- 0.0 = No risk (completely safe and compliant)
- 0.3 = Low risk (minor considerations)
- 0.5 = Medium risk (requires caution)
- 0.7 = High risk (significant concerns)
- 1.0 = Extremely high risk (major legal/financial exposure)

Business Action: "{action}"

Consider:
- Legal compliance issues
- Financial risks
- Regulatory requirements
- Ethical concerns
- Reputation risks

Return ONLY valid JSON with this exact format:
{{"risk_score": 0.X, "justification": "Brief explanation of the risk assessment"}}"""

        response = llm.invoke(prompt)
        response_text = response.content.strip()
        
        # Extract JSON from response
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            json_str = json_match.group()
            risk_data = json.loads(json_str)
            
            # Validate risk_score is between 0 and 1
            risk_score = risk_data.get("risk_score", 0.5)
            if not isinstance(risk_score, (int, float)) or risk_score < 0 or risk_score > 1:
                risk_score = 0.5
            
            return {
                "success": True,
                "risk_score": float(risk_score),
                "justification": risk_data.get("justification", "Risk assessment completed"),
                "action": action,
                "risk_level": get_risk_level(risk_score)
            }
        else:
            # Fallback parsing
            return {
                "success": False,
                "risk_score": 0.5,
                "justification": f"Could not parse risk assessment: {response_text}",
                "action": action,
                "risk_level": "Medium"
            }
            
    except Exception as e:
        return {
            "success": False,
            "risk_score": 0.8,  # Default to high risk if assessment fails
            "justification": f"Risk assessment failed: {str(e)}. Defaulting to high risk for safety.",
            "action": action,
            "risk_level": "High"
        }

def get_risk_level(risk_score: float) -> str:
    """Convert risk score to descriptive level"""
    if risk_score <= 0.2:
        return "Very Low"
    elif risk_score <= 0.4:
        return "Low"
    elif risk_score <= 0.6:
        return "Medium"
    elif risk_score <= 0.8:
        return "High"
    else:
        return "Very High"

def compliance_check(business_area: str, proposed_action: str) -> dict:
    """
    Specific compliance check for different business areas
    """
    try:
        llm = ChatOpenAI(
            model="openai/gpt-4",
            temperature=0,
            openai_api_key=os.getenv("OPENROUTER_API_KEY"),
            openai_api_base="https://openrouter.ai/api/v1"
        )
        
        prompt = f"""You are a compliance expert specializing in {business_area}.

Analyze this proposed action for compliance issues:
Business Area: {business_area}
Proposed Action: {proposed_action}

Check for:
- Legal requirements
- Industry regulations
- Licensing needs
- Tax implications
- Data privacy concerns
- Consumer protection laws

Return JSON with:
{{"compliant": true/false, "issues": ["list of concerns"], "recommendations": ["suggested actions"]}}"""

        response = llm.invoke(prompt)
        response_text = response.content.strip()
        
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            compliance_data = json.loads(json_match.group())
            return {
                "success": True,
                "business_area": business_area,
                "proposed_action": proposed_action,
                **compliance_data
            }
        else:
            return {
                "success": False,
                "error": "Could not parse compliance check",
                "business_area": business_area,
                "proposed_action": proposed_action
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": f"Compliance check failed: {str(e)}",
            "business_area": business_area,
            "proposed_action": proposed_action
        }

# LangChain Tools
risk_check_tool = Tool(
    name="RiskCheck",
    func=risk_check,
    description="Assess the compliance/legal/financial risk of a proposed business action. Returns risk score (0-1) and justification."
)

compliance_check_tool = Tool(
    name="ComplianceCheck", 
    func=lambda input_str: compliance_check(*input_str.split(',', 1)),
    description="Check compliance for specific business areas. Usage: ComplianceCheck('e-commerce,launch payment processing')"
)

if __name__ == "__main__":
    # Test the risk assessment
    print("🔍 Testing Risk Assessment Tool...")
    
    test_actions = [
        "Launch an unregistered payment method in Germany",
        "Start dropshipping products from China",
        "Create affiliate marketing program",
        "Collect customer email addresses for newsletter"
    ]
    
    for action in test_actions:
        print(f"\n📋 Testing: {action}")
        result = risk_check(action)
        print(f"Risk Score: {result['risk_score']:.2f} ({result['risk_level']})")
        print(f"Justification: {result['justification']}")
    
    # Test compliance check
    print(f"\n🏛️ Testing Compliance Check...")
    compliance_result = compliance_check("e-commerce", "launch subscription billing service")
    print("Compliance result:", compliance_result)
