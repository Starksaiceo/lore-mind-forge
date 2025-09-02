
#!/usr/bin/env python3

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    """Main entry point for running the agent in shell"""
    print("🚀 Starting AI CEO Agent in Shell Mode...")
    print("=" * 50)
    
    # Check environment
    api_key = os.getenv("OPENROUTER_API_KEY")
    xano_url = os.getenv("XANO_BASE_URL")
    
    if not api_key:
        print("❌ OPENROUTER_API_KEY not found in environment")
        return
    
    if not xano_url:
        print("❌ XANO_BASE_URL not found in environment")
        return
    
    print(f"✅ Environment configured")
    print(f"🔗 Xano URL: {xano_url}")
    print(f"🤖 AI Model: openai/gpt-4")
    print("=" * 50)
    
    try:
        # Import and run the agent
        from langchain_agent import run_langchain_agent_on_goals
        
        print("🎯 Fetching goals and starting agent execution...")
        results = run_langchain_agent_on_goals()
        
        print("\n" + "=" * 50)
        print("📊 EXECUTION SUMMARY")
        print("=" * 50)
        
        for i, result in enumerate(results, 1):
            print(f"\nGoal {i}: {result['goal'][:60]}...")
            print(f"Status: {result['status']}")
            if result['status'] == 'completed':
                print(f"Result: {result['result'][:100]}...")
            
        print(f"\n✅ Completed {len([r for r in results if r['status'] == 'completed'])} of {len(results)} goals")
        
    except Exception as e:
        print(f"❌ Error running agent: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
