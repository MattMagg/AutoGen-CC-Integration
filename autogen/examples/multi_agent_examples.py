"""
Multi-agent examples using AutoGen with Claude Code wrapper.
Demonstrates sequential chat, group chat, and nested chat patterns.
"""

import asyncio
import sys
import os
from pathlib import Path
from typing import List, Sequence

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat, SelectorGroupChat
from autogen_agentchat.messages import TextMessage, StopMessage
from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination
from autogen_agentchat.ui import Console

from config import get_model_client, ensure_health
from utils.helpers import TokenUsageTracker, ConversationLogger
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


async def sequential_chat_example():
    """
    Sequential chat pattern: Research → Analysis → Report Writing
    Each agent processes the output of the previous agent.
    """
    print("\n=== Sequential Chat Example ===")
    print("Pipeline: Research → Analysis → Report Writing\n")
    
    try:
        # Ensure wrapper is healthy
        ensure_health()
        
        # Create model client
        model_client = get_model_client(temperature=0.7)
        
        # Create specialized agents
        researcher = AssistantAgent(
            name="researcher",
            model_client=model_client,
            system_message="""You are a research specialist. Your job is to:
            1. Gather relevant information about the given topic
            2. Identify key facts and data points
            3. List credible sources and references
            4. Present findings in a structured format
            Keep your research factual and comprehensive."""
        )
        
        analyst = AssistantAgent(
            name="analyst",
            model_client=model_client,
            system_message="""You are a data analyst. Your job is to:
            1. Analyze the research findings provided
            2. Identify patterns and insights
            3. Draw meaningful conclusions
            4. Highlight important implications
            Base your analysis solely on the research provided."""
        )
        
        writer = AssistantAgent(
            name="writer",
            model_client=model_client,
            system_message="""You are a technical writer. Your job is to:
            1. Create a well-structured report from the analysis
            2. Use clear, professional language
            3. Include an executive summary
            4. Format with appropriate sections
            5. Conclude with actionable recommendations"""
        )
        
        # Topic for the pipeline
        topic = "The impact of Large Language Models on software development practices"
        
        print(f"Topic: {topic}\n")
        
        # Step 1: Research
        print("Step 1: Researching...")
        research_response = await researcher.on_messages([
            TextMessage(content=f"Research the following topic: {topic}", source="user")
        ])
        research_content = research_response.chat_message.content
        print(f"\nResearch Output:\n{research_content[:500]}...\n")
        
        # Step 2: Analysis
        print("Step 2: Analyzing...")
        analysis_response = await analyst.on_messages([
            TextMessage(
                content=f"Analyze the following research findings:\n\n{research_content}",
                source="researcher"
            )
        ])
        analysis_content = analysis_response.chat_message.content
        print(f"\nAnalysis Output:\n{analysis_content[:500]}...\n")
        
        # Step 3: Report Writing
        print("Step 3: Writing Report...")
        report_response = await writer.on_messages([
            TextMessage(
                content=f"Write a professional report based on this analysis:\n\n{analysis_content}",
                source="analyst"
            )
        ])
        report_content = report_response.chat_message.content
        print(f"\nFinal Report:\n{report_content[:800]}...\n")
        
        print("Sequential pipeline completed successfully!")
        
    except Exception as e:
        logger.error(f"Sequential chat failed: {e}")
        print(f"\nError in sequential chat: {e}")


async def group_chat_brainstorming_example():
    """
    Group chat pattern: Multiple agents brainstorming together.
    Uses RoundRobinGroupChat for equal participation.
    """
    print("\n=== Group Chat Brainstorming Example ===")
    print("Multiple perspectives on product development\n")
    
    try:
        # Ensure wrapper is healthy
        ensure_health()
        
        # Create model client
        model_client = get_model_client(temperature=0.8)  # Higher temperature for creativity
        
        # Create diverse team members
        product_manager = AssistantAgent(
            name="product_manager",
            model_client=model_client,
            system_message="""You are a product manager. Focus on:
            - User needs and market fit
            - Feature prioritization
            - Business value and ROI
            - Go-to-market strategy"""
        )
        
        engineer = AssistantAgent(
            name="engineer",
            model_client=model_client,
            system_message="""You are a senior engineer. Focus on:
            - Technical feasibility
            - Architecture and scalability
            - Implementation complexity
            - Performance considerations"""
        )
        
        designer = AssistantAgent(
            name="designer",
            model_client=model_client,
            system_message="""You are a UX designer. Focus on:
            - User experience and interface
            - Accessibility and usability
            - Visual design and branding
            - User journey and workflows"""
        )
        
        data_scientist = AssistantAgent(
            name="data_scientist",
            model_client=model_client,
            system_message="""You are a data scientist. Focus on:
            - Data requirements and analytics
            - ML/AI opportunities
            - Metrics and KPIs
            - A/B testing strategies"""
        )
        
        # Create group chat with termination condition
        termination = MaxMessageTermination(max_messages=12)
        
        team_chat = RoundRobinGroupChat(
            participants=[product_manager, engineer, designer, data_scientist],
            termination_condition=termination
        )
        
        # Start brainstorming
        task = """Let's brainstorm ideas for an AI-powered code review assistant.
        Each team member should contribute their perspective on:
        1. Key features and capabilities
        2. Potential challenges
        3. Success metrics
        4. Implementation approach"""
        
        print(f"Brainstorming Task:\n{task}\n")
        print("Starting group discussion...\n")
        
        # Run the group chat
        result = await team_chat.run(task=task)
        
        # Display summary
        print("\n=== Brainstorming Summary ===")
        print(f"Total messages: {len(result.messages)}")
        print(f"Participants: {', '.join([p.name for p in team_chat._participants])}")
        
        # Show last few messages
        print("\nFinal thoughts:")
        for msg in result.messages[-3:]:
            if hasattr(msg, 'content') and hasattr(msg, 'source'):
                print(f"\n{msg.source}: {msg.content[:200]}...")
        
    except Exception as e:
        logger.error(f"Group chat failed: {e}")
        print(f"\nError in group chat: {e}")


async def selector_chat_example():
    """
    Selector chat pattern: Dynamic agent selection based on needs.
    The selector chooses which agent should respond next.
    """
    print("\n=== Selector Chat Example ===")
    print("Dynamic expert selection for problem-solving\n")
    
    try:
        # Ensure wrapper is healthy
        ensure_health()
        
        # Create model clients
        model_client = get_model_client(temperature=0.7)
        selector_client = get_model_client(temperature=0.3)  # Lower temp for selection
        
        # Create specialist agents
        python_expert = AssistantAgent(
            name="python_expert",
            model_client=model_client,
            system_message="You are a Python expert. Help with Python-specific questions, best practices, and code optimization."
        )
        
        database_expert = AssistantAgent(
            name="database_expert",
            model_client=model_client,
            system_message="You are a database expert. Help with SQL, NoSQL, database design, and query optimization."
        )
        
        devops_expert = AssistantAgent(
            name="devops_expert",
            model_client=model_client,
            system_message="You are a DevOps expert. Help with CI/CD, containerization, cloud services, and infrastructure."
        )
        
        security_expert = AssistantAgent(
            name="security_expert",
            model_client=model_client,
            system_message="You are a security expert. Help with security best practices, vulnerability assessment, and secure coding."
        )
        
        # Create selector chat
        termination = MaxMessageTermination(max_messages=10)
        
        expert_team = SelectorGroupChat(
            participants=[python_expert, database_expert, devops_expert, security_expert],
            model_client=selector_client,
            termination_condition=termination,
            selector_prompt="""Based on the conversation history and the current question,
            select the most appropriate expert to answer:
            - python_expert: For Python code, libraries, and language-specific questions
            - database_expert: For database design, queries, and data persistence
            - devops_expert: For deployment, CI/CD, and infrastructure
            - security_expert: For security concerns and best practices
            
            Current experts: {roles}
            Conversation so far: {history}
            
            Select only the expert name, nothing else."""
        )
        
        # Complex multi-domain question
        complex_task = """I'm building a Python web application that needs to:
        1. Store user credentials securely
        2. Connect to PostgreSQL with connection pooling
        3. Deploy on AWS with auto-scaling
        4. Implement proper logging and monitoring
        
        Can you help me design this system properly?"""
        
        print(f"Task:\n{complex_task}\n")
        print("Expert team is discussing...\n")
        
        # Run the selector chat
        result = await expert_team.run(task=complex_task)
        
        # Show which experts contributed
        print("\n=== Expert Contributions ===")
        expert_contributions = {}
        for msg in result.messages:
            if hasattr(msg, 'source') and msg.source in [p.name for p in expert_team._participants]:
                expert_contributions[msg.source] = expert_contributions.get(msg.source, 0) + 1
        
        for expert, count in expert_contributions.items():
            print(f"{expert}: {count} contributions")
        
    except Exception as e:
        logger.error(f"Selector chat failed: {e}")
        print(f"\nError in selector chat: {e}")


async def nested_chat_example():
    """
    Nested chat pattern: Main coordinator delegates to sub-teams.
    Demonstrates hierarchical organization of agents.
    """
    print("\n=== Nested Chat Example ===")
    print("Project coordinator with specialized sub-teams\n")
    
    try:
        # Ensure wrapper is healthy
        ensure_health()
        
        # Create model client
        model_client = get_model_client(temperature=0.7)
        
        # Create sub-team for frontend
        frontend_lead = AssistantAgent(
            name="frontend_lead",
            model_client=model_client,
            system_message="You lead the frontend team. Coordinate UI/UX decisions and implementation."
        )
        
        frontend_dev = AssistantAgent(
            name="frontend_dev",
            model_client=model_client,
            system_message="You implement frontend features using modern frameworks."
        )
        
        # Create sub-team for backend
        backend_lead = AssistantAgent(
            name="backend_lead",
            model_client=model_client,
            system_message="You lead the backend team. Design APIs and system architecture."
        )
        
        backend_dev = AssistantAgent(
            name="backend_dev",
            model_client=model_client,
            system_message="You implement backend services and database operations."
        )
        
        # Create project coordinator that works with sub-teams
        coordinator = AssistantAgent(
            name="project_coordinator",
            model_client=model_client,
            system_message="""You are the project coordinator. You:
            1. Break down project requirements
            2. Delegate tasks to frontend and backend teams
            3. Ensure teams are aligned
            4. Summarize progress and decisions
            
            When you need specific implementation details:
            - Consult with frontend_lead for UI/UX matters
            - Consult with backend_lead for API and architecture matters"""
        )
        
        # Simulate nested conversations
        project_request = """We need to build a real-time collaborative document editor with:
        - Rich text editing capabilities
        - Real-time synchronization
        - User presence indicators
        - Version history
        - Access control"""
        
        print(f"Project Request:\n{project_request}\n")
        
        # Coordinator analyzes the request
        print("Coordinator analyzing requirements...\n")
        coord_response = await coordinator.on_messages([
            TextMessage(content=project_request, source="client")
        ])
        print(f"Coordinator: {coord_response.chat_message.content[:400]}...\n")
        
        # Frontend team discussion (nested)
        print("Frontend team planning...\n")
        frontend_task = "Design the UI for a real-time collaborative document editor with rich text editing"
        
        # Simulate frontend sub-team discussion
        frontend_lead_response = await frontend_lead.on_messages([
            TextMessage(content=frontend_task, source="coordinator")
        ])
        
        frontend_dev_response = await frontend_dev.on_messages([
            TextMessage(
                content=f"Based on the lead's plan: {frontend_lead_response.chat_message.content[:200]}... What specific technologies should we use?",
                source="frontend_lead"
            )
        ])
        
        print(f"Frontend Lead: {frontend_lead_response.chat_message.content[:300]}...")
        print(f"Frontend Dev: {frontend_dev_response.chat_message.content[:300]}...\n")
        
        # Backend team discussion (nested)
        print("Backend team planning...\n")
        backend_task = "Design the backend architecture for real-time document synchronization with conflict resolution"
        
        # Simulate backend sub-team discussion
        backend_lead_response = await backend_lead.on_messages([
            TextMessage(content=backend_task, source="coordinator")
        ])
        
        backend_dev_response = await backend_dev.on_messages([
            TextMessage(
                content=f"Based on the architecture: {backend_lead_response.chat_message.content[:200]}... How should we implement the WebSocket layer?",
                source="backend_lead"
            )
        ])
        
        print(f"Backend Lead: {backend_lead_response.chat_message.content[:300]}...")
        print(f"Backend Dev: {backend_dev_response.chat_message.content[:300]}...\n")
        
        # Coordinator summarizes
        print("Coordinator creating final plan...\n")
        final_summary = await coordinator.on_messages([
            TextMessage(
                content=f"""Based on team discussions:
                Frontend team suggests: {frontend_dev_response.chat_message.content[:200]}
                Backend team suggests: {backend_dev_response.chat_message.content[:200]}
                
                Please create a unified implementation plan.""",
                source="teams"
            )
        ])
        
        print(f"Final Plan:\n{final_summary.chat_message.content[:600]}...")
        
        print("\n\nNested conversation completed successfully!")
        
    except Exception as e:
        logger.error(f"Nested chat failed: {e}")
        print(f"\nError in nested chat: {e}")


async def main():
    """Run all multi-agent examples."""
    print("AutoGen Claude Code Integration - Multi-Agent Examples")
    print("=" * 60)
    print("📡 Connecting to Claude wrapper at: http://localhost:8000")
    
    # Run examples
    await sequential_chat_example()
    print("\n" + "=" * 60 + "\n")
    
    await group_chat_brainstorming_example()
    print("\n" + "=" * 60 + "\n")
    
    await selector_chat_example()
    print("\n" + "=" * 60 + "\n")
    
    await nested_chat_example()
    print("\n" + "=" * 60 + "\n")
    
    print("All multi-agent examples completed!")


if __name__ == "__main__":
    # Run with: python multi_agent_examples.py
    asyncio.run(main())