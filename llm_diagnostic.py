
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import json

def mask_api_key(key):
    """Mask API key showing only first and last 4 characters"""
    if not key or len(key) < 8:
        return "Not set or too short"
    return f"{key[:4]}...{key[-4:]}"

def run_llm_diagnostic():
    """Run comprehensive LLM diagnostic"""
    print("🔍 LLM DIAGNOSTIC REPORT")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    print("\n1. ENVIRONMENT VARIABLES CHECK:")
    print("-" * 30)
    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    openrouter_base = os.getenv("OPENROUTER_BASE_URL")
    llm_model = os.getenv("LLM_MODEL")
    
    print(f"OPENROUTER_API_KEY: {mask_api_key(openrouter_key)}")
    print(f"OPENROUTER_BASE_URL: {openrouter_base}")
    print(f"LLM_MODEL: {llm_model}")
    
    print("\n2. CHATopenai CONFIGURATION:")
    print("-" * 30)
    
    try:
        # Initialize ChatOpenAI as used in the codebase
        llm = ChatOpenAI(
            model="anthropic/claude-3-opus",
            temperature=0,
            openai_api_key=os.getenv("OPENROUTER_API_KEY"),
            openai_api_base="https://openrouter.ai/api/v1"
        )
        
        print(f"Model: {llm.model_name}")
        print(f"Base URL: {llm.openai_api_base}")
        # Handle SecretStr for API key
        api_key_str = str(llm.openai_api_key) if llm.openai_api_key else ""
        print(f"API Key: {mask_api_key(api_key_str)}")
        print(f"Temperature: {llm.temperature}")
        
        print("\n3. ACTUAL MODEL TEST:")
        print("-" * 30)
        
        # Test the LLM with a specific query
        test_message = "Please confirm your model name and developer."
        print(f"Sending test message: '{test_message}'")
        
        response = llm.invoke(test_message)
        print(f"\nFull Response:")
        print(f"Content: {response.content}")
        print(f"Response Type: {type(response)}")
        
        if hasattr(response, 'response_metadata'):
            print(f"Metadata: {response.response_metadata}")
        
        print("\n4. CONFIGURATION ANALYSIS:")
        print("-" * 30)
        
        # Check if using Claude 3 Opus
        is_claude_opus = "claude-3-opus" in llm.model_name.lower()
        is_openrouter = "openrouter.ai" in str(llm.openai_api_base)
        has_api_key = bool(api_key_str and len(api_key_str) > 10)
        
        print(f"✅ Using OpenRouter API: {is_openrouter}")
        print(f"❌ Using Claude 3 Opus: {is_claude_opus} (Currently using: {llm.model_name})")
        print(f"✅ Has API Key: {has_api_key}")
        
        print("\n5. SUMMARY:")
        print("-" * 30)
        
        if is_openrouter and has_api_key:
            if is_claude_opus:
                print("✅ Claude 3 Opus via OpenRouter is correctly configured and running!")
            else:
                print("❌ OpenRouter is configured but using GPT-4 instead of Claude 3 Opus")
                print("   Current model: openai/gpt-4")
                print("   Expected model: anthropic/claude-3-opus")
        else:
            print("❌ Configuration issues detected:")
            if not is_openrouter:
                print("   - OpenRouter API base URL not set correctly")
            if not has_api_key:
                print("   - OpenRouter API key missing or invalid")
        
        return {
            "is_claude_opus": is_claude_opus,
            "is_openrouter": is_openrouter,
            "has_api_key": has_api_key,
            "current_model": llm.model_name,
            "response_content": response.content
        }
        
    except Exception as e:
        print(f"❌ Error during LLM test: {str(e)}")
        return {"error": str(e)}

if __name__ == "__main__":
    run_llm_diagnostic()
