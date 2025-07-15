#!/usr/bin/env python3
"""
Quick start script to test your AutoGen Claude integration.
Connects directly to localhost:8000 where Claude wrapper is running natively.
"""

import asyncio
import sys
from pathlib import Path

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken
from config import get_model_client, ensure_health


async def quickstart():
    """Run a simple test to verify everything is working."""
    print("🚀 AutoGen Claude Integration Quick Start")
    print("=" * 50)
    
    print("📡 Connecting to Claude wrapper at: http://localhost:8000")
    print("✅ Using native wrapper authentication (Claude CLI OAuth)")
    
    # Health check
    print("\n🔍 Checking wrapper health...")
    try:
        ensure_health()
        print("✅ Wrapper is healthy and responding")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        print("\nPlease ensure:")
        print("1. Claude wrapper is running natively on port 8000")
        print("2. Start wrapper with: poetry run uvicorn main:app --host 0.0.0.0 --port 8000")
        print("3. Claude CLI is authenticated: claude auth login")
        return
    
    # Test with a simple agent
    print("\n🤖 Creating test agent...")
    try:
        model_client = get_model_client()
        
        assistant = AssistantAgent(
            name="test_assistant",
            model_client=model_client,
            system_message="You are a helpful AI assistant for testing the AutoGen integration."
        )
        
        # Test query
        test_query = "Hello! Can you confirm you're working through the AutoGen Claude integration?"
        print(f"\n📝 Test query: {test_query}")
        
        response = await assistant.on_messages([
            TextMessage(content=test_query, source="user")
        ], cancellation_token=CancellationToken())
        
        if response and hasattr(response, 'chat_message'):
            print(f"\n✅ Response received:")
            print(f"Assistant: {response.chat_message.content}")
            print("\n🎉 Success! Your AutoGen Claude integration is working!")
            
            # Show token usage if available
            if hasattr(response, 'usage'):
                print(f"\n📊 Token usage:")
                print(f"   Prompt tokens: {response.usage.prompt_tokens}")
                print(f"   Completion tokens: {response.usage.completion_tokens}")
        else:
            print("❌ No response received")
            
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        print("\nTroubleshooting:")
        print("1. Ensure wrapper is running: curl http://localhost:8000/v1/models")
        print("2. Check Claude CLI auth: claude auth status")
        print("3. Verify model name is correct")
    
    print("\n" + "=" * 50)
    print("\n📚 Next steps:")
    print("1. Try single agent examples: python examples/single_agent_example.py")
    print("2. Try multi-agent examples: python examples/multi_agent_examples.py")
    print("3. Read the README.md for detailed documentation")


if __name__ == "__main__":
    # Run with: python quickstart.py
    asyncio.run(quickstart())