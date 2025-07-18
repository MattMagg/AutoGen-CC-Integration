#!/usr/bin/env python3
"""
Test Agent for AutoGen Studio
Following best practices from AutoGen documentation
"""

import asyncio
import json
from pathlib import Path

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import BaseGroupChat, RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination, MaxMessageTermination
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient

# Add parent directory to path to import config
import sys
sys.path.append(str(Path(__file__).parent.parent))
from config import get_model_client

async def create_test_agent():
    """Create a standalone test agent that can work with AutoGen Studio"""
    
    # Use the configured model client from our wrapper
    model_client = get_model_client()
    
    # Create a comprehensive test agent
    test_agent = AssistantAgent(
        name="comprehensive_test_agent",
        model_client=model_client,
        description="A comprehensive testing agent for software quality assurance",
        system_message="""You are a comprehensive testing agent specializing in all aspects of software testing.
        
Your capabilities include:
1. **Test Strategy**: Design test plans covering unit, integration, E2E, and performance tests
2. **Test Implementation**: Write clean, maintainable test code following best practices
3. **Test Automation**: Create automated test suites with proper CI/CD integration
4. **Quality Metrics**: Track coverage, identify gaps, and suggest improvements
5. **Bug Analysis**: Reproduce issues, create minimal test cases, and verify fixes

Testing principles you follow:
- Tests should be deterministic and independent
- Use AAA pattern (Arrange-Act-Assert)
- Mock external dependencies appropriately
- Ensure tests run quickly and reliably
- Maintain high code coverage (>80% for critical paths)

When asked to create tests, provide:
1. Test strategy overview
2. Actual test code with comments
3. Setup/teardown requirements
4. Expected coverage metrics
5. Integration with CI/CD pipelines

Always consider edge cases, error scenarios, and performance implications.""",
        tools=[],  # Add specific testing tools here if needed
        model_client_stream=True,
    )
    
    return test_agent

async def load_team_from_json():
    """Load the team configuration from JSON file"""
    team_config_path = Path(__file__).parent / "team.json"
    
    if not team_config_path.exists():
        print(f"Team configuration not found at {team_config_path}")
        return None
    
    with open(team_config_path, 'r') as f:
        team_config = json.load(f)
    
    # Load the team using BaseGroupChat
    team = BaseGroupChat.load_component(team_config)
    print(f"Loaded team: {team.name}")
    print(f"Participants: {[p.name for p in team._participants]}")
    
    return team

async def create_testing_team():
    """Create a testing team programmatically"""
    model_client = get_model_client()
    
    # Test Architect Agent
    test_architect = AssistantAgent(
        name="test_architect",
        model_client=model_client,
        description="Plans and designs comprehensive test strategies",
        system_message="""You are a test architect. Design test strategies that ensure:
        - Complete coverage of requirements
        - Risk-based testing approach
        - Balance between different test types
        - Clear test documentation
        Plan first, then delegate implementation.""",
    )
    
    # Test Developer Agent
    test_developer = AssistantAgent(
        name="test_developer",
        model_client=model_client,
        description="Implements high-quality test code",
        system_message="""You are a test developer. Your tasks:
        - Write clean, maintainable test code
        - Implement tests according to the architect's plan
        - Use appropriate testing frameworks
        - Ensure tests are fast and reliable""",
    )
    
    # Test Reviewer Agent
    test_reviewer = AssistantAgent(
        name="test_reviewer",
        model_client=model_client,
        description="Reviews and approves test quality",
        system_message="""You are a test reviewer. Ensure:
        - Tests cover all specified scenarios
        - Code follows best practices
        - Edge cases are handled
        - Tests are properly documented
        Respond with 'APPROVED' when satisfied.""",
    )
    
    # Define termination conditions
    text_termination = TextMentionTermination("APPROVED")
    max_messages = MaxMessageTermination(15)
    termination = text_termination | max_messages
    
    # Create the team
    team = RoundRobinGroupChat(
        participants=[test_architect, test_developer, test_reviewer],
        termination_condition=termination,
    )
    
    return team

async def run_test_task(team, task: str):
    """Run a testing task with the team"""
    print(f"\n🧪 Running test task: {task}\n")
    
    # Run the team on the task and stream output
    await Console(team.run_stream(task=task))

async def main():
    """Main function to demonstrate agent usage"""
    
    # Create individual test agent
    print("Creating individual test agent...")
    test_agent = await create_test_agent()
    print(f"✅ Created agent: {test_agent.name}")
    
    # Try to load team from JSON
    print("\nLoading team from JSON configuration...")
    json_team = await load_team_from_json()
    
    # Create team programmatically
    print("\nCreating team programmatically...")
    programmatic_team = await create_testing_team()
    print("✅ Created testing team")
    
    # Example test task
    test_task = """Create a comprehensive test suite for a user authentication system that includes:
    1. User registration with email validation
    2. Login with username/password
    3. Password reset functionality
    4. Session management
    
    Include unit tests, integration tests, and security tests."""
    
    # Run with the programmatic team
    if programmatic_team:
        await run_test_task(programmatic_team, test_task)
    
    # Close model client
    model_client = get_model_client()
    await model_client.close()

if __name__ == "__main__":
    print("🚀 AutoGen Studio Test Agent Demo")
    print("=" * 50)
    asyncio.run(main())