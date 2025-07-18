#!/usr/bin/env python3
"""
Test complete AutoGen Studio integration
"""

import asyncio
import json
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

async def test_integration():
    """Test the complete integration"""
    
    print("🧪 Testing Complete AutoGen Studio Integration")
    print("=" * 60)
    
    # 1. Test wrapper connectivity
    print("\n1️⃣ Testing Claude Wrapper...")
    try:
        import requests
        response = requests.get("http://localhost:8000/v1/models")
        if response.status_code == 200:
            models = response.json()
            print(f"✅ Wrapper is running! Found {len(models['data'])} models")
            print(f"   Available: {[m['id'] for m in models['data']]}")
        else:
            print(f"❌ Wrapper error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to wrapper: {e}")
        print("   Make sure wrapper is running on port 8000")
        return False
    
    # 2. Test AutoGen imports
    print("\n2️⃣ Testing AutoGen Installation...")
    try:
        from autogen_agentchat.agents import AssistantAgent
        from autogen_ext.models.openai import OpenAIChatCompletionClient
        print("✅ AutoGen imports successful")
    except Exception as e:
        print(f"❌ AutoGen import error: {e}")
        return False
    
    # 3. Test model client creation
    print("\n3️⃣ Testing Model Client...")
    try:
        from config import get_model_client
        model_client = get_model_client()
        print("✅ Model client created successfully")
    except Exception as e:
        print(f"❌ Model client error: {e}")
        return False
    
    # 4. Test workflow file
    print("\n4️⃣ Checking Workflow Files...")
    workflow_path = Path(__file__).parent / "test_workflow.json"
    if workflow_path.exists():
        with open(workflow_path, 'r') as f:
            workflow = json.load(f)
        print(f"✅ Workflow file exists: {workflow['name']}")
        print(f"   Agents: {len(workflow['receiver']['agents'])}")
    else:
        print("❌ Workflow file not found")
    
    # 5. Test simple agent interaction
    print("\n5️⃣ Testing Agent Interaction...")
    try:
        agent = AssistantAgent(
            name="test_agent",
            model_client=model_client,
            system_message="You are a helpful testing assistant. Respond concisely."
        )
        
        # Simple test
        response = await agent.run(task="Say 'AutoGen Studio integration test successful!' if you can hear me.")
        print(f"✅ Agent response: {response.messages[-1].content}")
        
        await model_client.close()
    except Exception as e:
        print(f"❌ Agent interaction error: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("✅ All tests passed! Integration is working correctly.")
    
    print("\n📋 Next Steps:")
    print("1. Go to AutoGen Studio: http://localhost:8080")
    print("2. In Team Builder:")
    print("   - Create agents using 'AssistantAgent' from Component Library")
    print("   - Configure with your system messages")
    print("   - Set model to: claude-opus-4-20250514")
    print("   - Set base URL to: http://localhost:8000/v1")
    print("3. Or in Playground:")
    print("   - Import the workflow file")
    print("   - Start chatting with your test team!")
    
    return True

if __name__ == "__main__":
    success = asyncio.run(test_integration())
    sys.exit(0 if success else 1)