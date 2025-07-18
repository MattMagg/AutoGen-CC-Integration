#!/usr/bin/env python3
"""
Demo script to test AutoGen Studio agent configurations
"""

import asyncio
import json
from pathlib import Path
import sys

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from autogenstudio.teammanager import TeamManager
from autogenstudio.database import DatabaseManager

async def test_studio_integration():
    """Test if AutoGen Studio recognizes our configurations"""
    
    print("🔍 Testing AutoGen Studio Integration")
    print("=" * 50)
    
    # Check if configurations exist
    config_dir = Path(__file__).parent / "configs"
    print(f"\n📁 Configuration directory: {config_dir}")
    
    configs = list(config_dir.glob("*.json"))
    print(f"Found {len(configs)} configuration files:")
    for config in configs:
        print(f"  - {config.name}")
    
    # Initialize database manager
    print("\n📊 Initializing database...")
    db_manager = DatabaseManager(
        engine_uri="sqlite:///autogen04202.db",
        base_dir=str(Path(__file__).parent)
    )
    
    # Check if team configuration can be loaded
    team_json_path = Path(__file__).parent / "team.json"
    if team_json_path.exists():
        print(f"\n📋 Loading team configuration from {team_json_path.name}")
        with open(team_json_path, 'r') as f:
            team_config = json.load(f)
        print(f"Team name: {team_config.get('name', 'Unknown')}")
        print(f"Team type: {team_config.get('team_type', 'Unknown')}")
        print(f"Participants: {len(team_config.get('participants', []))}")
    
    # Try to use TeamManager
    print("\n🤖 Testing TeamManager...")
    try:
        wm = TeamManager()
        print("✅ TeamManager initialized successfully")
        
        # List available teams/workflows
        print("\n📋 Available configurations in database:")
        # Note: Actual implementation would query the database
        
    except Exception as e:
        print(f"⚠️ TeamManager initialization warning: {e}")
    
    print("\n✨ Configuration test complete!")
    print("\n💡 Next steps:")
    print("1. Refresh the AutoGen Studio UI (http://localhost:8080)")
    print("2. Check the 'Agents' and 'Teams' sections in the UI")
    print("3. Try creating a new session with the test agents")
    print("4. You may need to restart AutoGen Studio to see new configurations")

async def quick_agent_test():
    """Quick test of agent functionality"""
    print("\n🧪 Quick Agent Test")
    print("=" * 50)
    
    try:
        # Import agent creation function
        from test_agent import create_test_agent, get_model_client
        
        # Create agent
        print("Creating test agent...")
        agent = await create_test_agent()
        print(f"✅ Agent created: {agent.name}")
        
        # Simple test task
        test_prompt = "Create a simple unit test for a function that adds two numbers"
        print(f"\n📝 Test prompt: {test_prompt}")
        
        # Run agent
        from autogen_agentchat.ui import Console
        print("\n🚀 Running agent...")
        await Console(agent.run_stream(task=test_prompt))
        
        # Close model client
        model_client = get_model_client()
        await model_client.close()
        
    except Exception as e:
        print(f"❌ Error during agent test: {e}")
        print("Make sure the Claude wrapper is running on port 8000")

async def main():
    """Main demo function"""
    print("🎯 AutoGen Studio Test Agent Demo")
    print("=" * 70)
    
    # Test studio integration
    await test_studio_integration()
    
    # Ask if user wants to run quick test
    print("\n" + "=" * 70)
    response = input("\n🤔 Would you like to run a quick agent test? (y/n): ")
    
    if response.lower() == 'y':
        await quick_agent_test()
    
    print("\n✅ Demo complete!")
    print("\n📌 Remember:")
    print("- AutoGen Studio UI: http://localhost:8080")
    print("- Claude wrapper must be running on port 8000")
    print("- You may need to restart AutoGen Studio to see new agents")

if __name__ == "__main__":
    asyncio.run(main())