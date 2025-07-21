#!/usr/bin/env python3
"""
Test Agent created programmatically in VS Code environment
This agent will be registered in AutoGen Studio for synchronization testing
"""

import asyncio
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken
import logging

from config import get_model_client, ensure_health

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class VSCodeTestAgent:
    """
    Test agent created programmatically in VS Code environment.
    Demonstrates creation patterns and Studio synchronization.
    """
    
    def __init__(self):
        self.name = "VS_Code_Test_Agent"
        self.agent = None
        self.system_message = "I am a test agent created programmatically in VS Code"
        
    async def initialize(self):
        """Initialize the agent with Claude model client."""
        try:
            # Ensure wrapper is healthy
            ensure_health()
            logger.info("Claude wrapper health check passed")
            
            # Create model client
            model_client = get_model_client(
                model="claude-opus-4-20250514",
                temperature=0.7
            )
            logger.info("Model client created successfully")
            
            # Create the assistant agent
            self.agent = AssistantAgent(
                name=self.name,
                model_client=model_client,
                system_message=self.system_message
            )
            logger.info(f"Agent '{self.name}' initialized successfully")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize agent: {e}")
            return False
    
    async def test_functionality(self):
        """Test basic agent functionality."""
        if not self.agent:
            logger.error("Agent not initialized")
            return False
            
        try:
            # Test query
            test_query = "Hello! Can you confirm you're the VS Code test agent?"
            logger.info(f"Testing agent with query: {test_query}")
            
            # Get response
            response = await self.agent.on_messages([
                TextMessage(content=test_query, source="user")
            ], CancellationToken())
            
            if response and hasattr(response, 'chat_message'):
                response_content = response.chat_message.content
                logger.info(f"Agent response: {response_content}")
                print(f"\n✅ Agent Response: {response_content}")
                return True
            else:
                logger.error("No response received from agent")
                return False
                
        except Exception as e:
            logger.error(f"Agent test failed: {e}")
            return False
    
    def get_config(self):
        """Return configuration for Studio registration."""
        return {
            "name": self.name,
            "description": "Test agent created programmatically in VS Code environment",
            "system_message": self.system_message,
            "type": "assistant",
            "model_client": {
                "model": "claude-opus-4-20250514",
                "temperature": 0.7,
                "max_tokens": 4096
            }
        }


async def create_and_test_agent():
    """Create and test the VS Code test agent."""
    print("\n🤖 Creating VS Code Test Agent")
    print("=" * 50)
    
    # Create agent instance
    test_agent = VSCodeTestAgent()
    
    # Initialize agent
    print("📡 Initializing agent with Claude model client...")
    if await test_agent.initialize():
        print("✅ Agent initialized successfully")
    else:
        print("❌ Agent initialization failed")
        return None
    
    # Test functionality
    print("\n🧪 Testing agent functionality...")
    if await test_agent.test_functionality():
        print("✅ Agent test passed")
    else:
        print("❌ Agent test failed")
        return None
    
    print(f"\n✨ Agent '{test_agent.name}' created and tested successfully!")
    return test_agent


async def main():
    """Main function to create and test the agent."""
    print("VS Code Test Agent Creation")
    print("=" * 60)
    print("📡 Connecting to Claude wrapper at: http://localhost:8000")
    
    # Create and test agent
    agent = await create_and_test_agent()
    
    if agent:
        print("\n📋 Agent Configuration:")
        config = agent.get_config()
        for key, value in config.items():
            print(f"  {key}: {value}")
        
        print("\n💡 Next steps:")
        print("1. Run the registration script to add this agent to AutoGen Studio")
        print("2. Verify agent appears in Studio Component Library")
        print("3. Test agent in Studio UI")
    else:
        print("\n❌ Agent creation failed")


if __name__ == "__main__":
    # Run with: python test_sync_agent.py
    asyncio.run(main())