#!/usr/bin/env python3
"""
AutoGen Studio Setup Helper
Creates agents and teams that can be used in AutoGen Studio
"""

import json
from pathlib import Path
from autogenstudio.database import DatabaseManager

def setup_autogen_studio():
    """Setup agents and teams in AutoGen Studio database"""
    
    print("🔧 AutoGen Studio Setup Helper")
    print("=" * 50)
    
    # Initialize database
    db_path = Path(__file__).parent / "autogen04202.db"
    print(f"📊 Using database: {db_path}")
    
    db = DatabaseManager(
        engine_uri=f"sqlite:///{db_path}",
        base_dir=str(Path(__file__).parent)
    )
    
    # Initialize database tables
    db.initialize_database()
    
    print("\n📝 Creating model configuration...")
    
    # Create model config for Claude via wrapper
    model_config = {
        "model": "claude-opus-4-20250514",
        "api_type": "openai",
        "base_url": "http://localhost:8000/v1",
        "api_key": "not-needed"  # OAuth handled by wrapper
    }
    
    print("✅ Model configuration created")
    
    # Create workflow file for AutoGen Studio
    workflow = {
        "name": "Test Development Workflow",
        "description": "A workflow for comprehensive software testing",
        "sender": {
            "type": "userproxy",
            "name": "user_proxy",
            "human_input_mode": "NEVER",
            "max_consecutive_auto_reply": 10,
            "system_message": "You are a helpful assistant.",
            "llm_config": False,
            "code_execution_config": False
        },
        "receiver": {
            "type": "groupchat",
            "name": "test_team",
            "description": "Testing team for software QA",
            "agents": [
                {
                    "type": "assistant",
                    "name": "test_architect",
                    "system_message": """You are a test architect specializing in software testing strategies. Your role is to:
1. Analyze testing requirements
2. Design comprehensive test plans
3. Identify edge cases and potential issues
4. Recommend appropriate testing frameworks and tools
5. Ensure test coverage across unit, integration, and end-to-end tests

Always consider both functional and non-functional requirements.""",
                    "llm_config": model_config
                },
                {
                    "type": "assistant",
                    "name": "test_developer",
                    "system_message": """You are a test developer focused on implementing high-quality tests. Your responsibilities include:
1. Writing clean, maintainable test code
2. Implementing unit tests with proper mocking
3. Creating integration tests for API endpoints
4. Developing end-to-end tests for user workflows
5. Following best practices like AAA (Arrange-Act-Assert) pattern

Always ensure tests are deterministic and independent.""",
                    "llm_config": model_config
                },
                {
                    "type": "assistant",
                    "name": "test_reviewer",
                    "system_message": """You are a test reviewer ensuring test quality and coverage. Your tasks are to:
1. Review test code for completeness and correctness
2. Verify edge cases are covered
3. Check for proper error handling in tests
4. Ensure tests follow established patterns and conventions
5. Provide constructive feedback for improvements

Respond with 'APPROVED' when the test suite meets all quality standards.""",
                    "llm_config": model_config
                }
            ],
            "admin_name": "Admin",
            "messages": [],
            "max_round": 15,
            "speaker_selection_method": "round_robin",
            "allow_repeat_speaker": True
        }
    }
    
    # Save workflow
    workflow_path = Path(__file__).parent / "test_workflow.json"
    with open(workflow_path, 'w') as f:
        json.dump(workflow, f, indent=2)
    
    print(f"\n✅ Created workflow file: {workflow_path}")
    
    # Create a simple agent config that can be imported
    simple_agent = {
        "type": "assistant",
        "name": "comprehensive_test_agent",
        "system_message": """You are a comprehensive testing agent specializing in all aspects of software testing.

Your capabilities include:
1. Test Strategy: Design test plans covering unit, integration, E2E, and performance tests
2. Test Implementation: Write clean, maintainable test code following best practices
3. Test Automation: Create automated test suites with proper CI/CD integration
4. Quality Metrics: Track coverage, identify gaps, and suggest improvements
5. Bug Analysis: Reproduce issues, create minimal test cases, and verify fixes

Always consider edge cases, error scenarios, and performance implications.""",
        "llm_config": model_config,
        "human_input_mode": "NEVER",
        "max_consecutive_auto_reply": 10,
        "code_execution_config": False
    }
    
    agent_path = Path(__file__).parent / "simple_test_agent.json"
    with open(agent_path, 'w') as f:
        json.dump(simple_agent, f, indent=2)
    
    print(f"✅ Created agent file: {agent_path}")
    
    print("\n📋 Instructions for AutoGen Studio:")
    print("1. In AutoGen Studio UI, go to 'Playground' section")
    print("2. Click 'Import' or 'Load' workflow")
    print(f"3. Select: {workflow_path}")
    print("4. The test team will be available in your playground")
    print("\nAlternatively:")
    print("1. In Team Builder, you can manually add agents")
    print("2. Use 'AssistantAgent' type from Component Library")
    print("3. Copy the system messages from our configs")
    print("4. Set model to use base_url: http://localhost:8000/v1")
    
    return workflow_path, agent_path

def create_importable_configs():
    """Create configs in AutoGen Studio's expected format"""
    
    print("\n🎯 Creating AutoGen Studio importable configs...")
    
    configs_dir = Path(__file__).parent / "studio_configs"
    configs_dir.mkdir(exist_ok=True)
    
    # Agent configuration in Studio format
    agent_spec = {
        "version": "0.0.1",
        "agents": [
            {
                "type": "assistant",
                "name": "test_architect",
                "description": "Plans and designs test strategies",
                "system_message": "You are a test architect. Design comprehensive test strategies.",
                "model": "claude-opus-4-20250514",
                "base_url": "http://localhost:8000/v1",
                "api_type": "openai",
                "temperature": 0.7
            },
            {
                "type": "assistant", 
                "name": "test_developer",
                "description": "Implements test code",
                "system_message": "You are a test developer. Write high-quality test code.",
                "model": "claude-opus-4-20250514",
                "base_url": "http://localhost:8000/v1",
                "api_type": "openai",
                "temperature": 0.3
            }
        ]
    }
    
    agent_spec_path = configs_dir / "test_agents.json"
    with open(agent_spec_path, 'w') as f:
        json.dump(agent_spec, f, indent=2)
    
    print(f"✅ Created: {agent_spec_path}")
    
    # Team spec
    team_spec = {
        "version": "0.0.1",
        "team": {
            "name": "Testing Team",
            "description": "Comprehensive testing team",
            "participants": ["test_architect", "test_developer"],
            "type": "round_robin",
            "max_rounds": 10
        }
    }
    
    team_spec_path = configs_dir / "test_team.json"
    with open(team_spec_path, 'w') as f:
        json.dump(team_spec, f, indent=2)
    
    print(f"✅ Created: {team_spec_path}")
    
    return configs_dir

if __name__ == "__main__":
    # Run setup
    workflow_path, agent_path = setup_autogen_studio()
    configs_dir = create_importable_configs()
    
    print("\n✨ Setup complete!")
    print("\n🚀 Quick Start:")
    print("1. Go to AutoGen Studio UI (http://localhost:8080)")
    print("2. Navigate to 'Playground'")
    print("3. Start a new session")
    print("4. You can now:")
    print("   - Use the default agents with your Claude model")
    print("   - Import the workflow file created")
    print("   - Build custom teams in Team Builder")
    
    print("\n💡 Model Configuration:")
    print("When creating agents in the UI, use these settings:")
    print("- Model: claude-opus-4-20250514")
    print("- API Type: OpenAI")  
    print("- Base URL: http://localhost:8000/v1")
    print("- API Key: (leave empty or put 'not-needed')")