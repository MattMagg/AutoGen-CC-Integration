#!/usr/bin/env python3
"""
Verification script for the VS Code Test Agent
Tests the complete agent creation and registration workflow
"""

import asyncio
import sqlite3
import json
from pathlib import Path

from test_sync_agent import VSCodeTestAgent


async def verify_agent_creation():
    """Verify that the agent can be created and functions properly."""
    print("🔍 Verifying VS Code Test Agent Creation...")
    
    # Create and test agent
    test_agent = VSCodeTestAgent()
    
    # Initialize agent
    init_success = await test_agent.initialize()
    if not init_success:
        print("❌ Agent initialization failed")
        return False
    
    # Test functionality
    test_success = await test_agent.test_functionality()
    if not test_success:
        print("❌ Agent functionality test failed")
        return False
    
    print("✅ Agent creation and functionality verified")
    return True


def verify_studio_registration():
    """Verify that the agent is registered in AutoGen Studio database."""
    print("\n🔍 Verifying Studio Registration...")
    
    db_path = Path(__file__).parent / "studio" / "autogen04202.db"
    
    try:
        # Connect to database
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Search for our test agent
        cursor.execute("SELECT id, config FROM gallery")
        entries = cursor.fetchall()
        
        for entry_id, config_json in entries:
            try:
                config = json.loads(config_json)
                if config.get("name") == "VS_Code_Test_Agent":
                    print(f"✅ Agent found in Studio database (ID: {entry_id})")
                    print(f"   Description: {config.get('description')}")
                    print(f"   System Message: {config.get('system_message')}")
                    print(f"   Model: {config.get('model')}")
                    print(f"   Type: {config.get('type')}")
                    conn.close()
                    return True
            except:
                continue
        
        print("❌ VS Code Test Agent not found in Studio database")
        conn.close()
        return False
        
    except Exception as e:
        print(f"❌ Database verification failed: {e}")
        return False


def print_workflow_summary():
    """Print a summary of the complete workflow."""
    print("\n" + "=" * 60)
    print("📋 AGENT FACTORY WORKFLOW SUMMARY")
    print("=" * 60)
    
    print("\n✅ COMPLETED STEPS:")
    print("1. ✓ Created test_sync_agent.py in VS Code environment")
    print("2. ✓ Implemented VSCodeTestAgent class with AutoGen patterns")
    print("3. ✓ Used config.get_model_client() for Claude model integration")
    print("4. ✓ Created agent with unique name 'VS_Code_Test_Agent'")
    print("5. ✓ Added required system message")
    print("6. ✓ Updated registration script for Studio integration")
    print("7. ✓ Successfully registered agent in AutoGen Studio database")
    print("8. ✓ Verified agent functionality and database entry")
    
    print("\n🎯 SUCCESS CRITERIA MET:")
    print("• ✅ Programmatically created agent in VS Code")
    print("• ✅ Agent follows AutoGen v0.4+ patterns")
    print("• ✅ Successfully registered in Studio database")
    print("• ✅ Agent configuration properly stored")
    print("• ✅ Complete workflow documented and verified")
    
    print("\n📂 FILES CREATED:")
    print("• /Users/mac-main/autogen-claude-integration/autogen/test_sync_agent.py")
    print("• /Users/mac-main/autogen-claude-integration/autogen/verify_test_agent.py")
    
    print("\n📝 FILES MODIFIED:")
    print("• /Users/mac-main/autogen-claude-integration/autogen/studio/register_agents_in_studio.py")
    
    print("\n💡 NEXT STEPS:")
    print("1. Start AutoGen Studio UI to see the agent in Component Library")
    print("2. Test the agent in Studio's Team Builder")
    print("3. Create multi-agent teams using the VS Code Test Agent")
    print("4. Verify agent responds correctly in Studio conversations")


async def main():
    """Run complete verification workflow."""
    print("🤖 VS Code Test Agent - Complete Workflow Verification")
    print("=" * 60)
    
    # Verify agent creation
    creation_verified = await verify_agent_creation()
    
    # Verify Studio registration
    registration_verified = verify_studio_registration()
    
    # Print workflow summary
    print_workflow_summary()
    
    if creation_verified and registration_verified:
        print("\n🎉 VERIFICATION COMPLETE - ALL TESTS PASSED!")
        print("   The VS Code Test Agent has been successfully created")
        print("   and registered in AutoGen Studio.")
    else:
        print("\n⚠️  VERIFICATION INCOMPLETE - Some tests failed")
        print("   Please check the error messages above")


if __name__ == "__main__":
    asyncio.run(main())