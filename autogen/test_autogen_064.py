#!/usr/bin/env python3
"""
Test script for AutoGen 0.6.4 compatibility with Claude wrapper
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken
from config import get_model_client, ensure_health


async def test_autogen_064():
    """Test basic AutoGen 0.6.4 functionality"""
    print("🧪 Testing AutoGen 0.6.4 with Claude wrapper...")
    print("-" * 50)
    
    try:
        # Check wrapper health
        print("✓ Checking wrapper health...")
        ensure_health()
        print("✓ Wrapper is healthy!")
        
        # Create model client
        print("✓ Creating model client...")
        model_client = get_model_client()
        
        # Create assistant agent
        print("✓ Creating assistant agent...")
        assistant = AssistantAgent(
            name="test_assistant",
            model_client=model_client,
            system_message="You are a helpful AI assistant for testing AutoGen 0.6.4 compatibility."
        )
        
        # Test message
        print("✓ Sending test message...")
        response = await assistant.on_messages(
            [TextMessage(content="Say 'AutoGen 0.6.4 is working!' if you can hear me.", source="user")],
            CancellationToken()
        )
        
        print("\n📝 Response:")
        print(response.chat_message.content)
        
        # Close model client
        await model_client.close()
        
        print("\n✅ AutoGen 0.6.4 test completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_autogen_064())