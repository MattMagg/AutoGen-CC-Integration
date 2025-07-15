"""
Single agent examples using AutoGen with Claude Code wrapper.
Demonstrates basic usage, error handling, and different agent types.
"""

import asyncio
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken
import tempfile

from config import get_model_client, ensure_health
from utils.helpers import TokenUsageTracker, ConversationLogger, async_retry
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


async def basic_assistant_example():
    """
    Basic assistant agent example with error handling.
    """
    print("\n=== Basic Assistant Example ===\n")
    
    # Initialize tracking
    token_tracker = TokenUsageTracker()
    conversation_logger = ConversationLogger()
    
    try:
        # Ensure wrapper is healthy
        ensure_health()
        
        # Create model client
        model_client = get_model_client(temperature=0.7)
        
        # Create assistant agent
        assistant = AssistantAgent(
            name="claude_assistant",
            model_client=model_client,
            system_message="""You are a helpful AI assistant powered by Claude Opus.
            You provide clear, accurate, and thoughtful responses.
            When you're not sure about something, you say so."""
        )
        
        # Example queries
        queries = [
            "What are the key principles of writing clean, maintainable code?",
            "Can you explain the concept of dependency injection with a simple example?",
            "What are some best practices for error handling in Python?"
        ]
        
        for query in queries:
            print(f"\nUser: {query}")
            conversation_logger.log_message("user", query)
            
            try:
                # Get response with retry
                response = await async_retry(max_attempts=3)(
                    lambda: assistant.on_messages([TextMessage(content=query, source="user")], CancellationToken())
                )()
                
                if response and hasattr(response, 'chat_message'):
                    print(f"\nAssistant: {response.chat_message.content}")
                    conversation_logger.log_message("assistant", response.chat_message.content)
                    
                    # Track token usage if available
                    if hasattr(response, 'usage'):
                        token_tracker.add_usage(
                            response.usage.prompt_tokens,
                            response.usage.completion_tokens,
                            {'query': query[:50]}
                        )
                
            except Exception as e:
                logger.error(f"Failed to get response: {e}")
                conversation_logger.log_error(str(e), {'query': query})
                print(f"\nError: Failed to get response - {e}")
        
        # Print usage summary
        print("\n=== Token Usage Summary ===")
        summary = token_tracker.get_summary()
        for key, value in summary.items():
            print(f"{key}: {value}")
            
    except Exception as e:
        logger.error(f"Example failed: {e}")
        print(f"\nError: {e}")


async def coding_assistant_example():
    """
    Agent that provides coding assistance and explanations.
    Note: Code execution is not directly supported in current AutoGen v0.4+
    """
    print("\n=== Coding Assistant Example ===\n")
    
    try:
        # Ensure wrapper is healthy
        ensure_health()
        
        # Create model client
        model_client = get_model_client(temperature=0.1)  # Lower temperature for code
        
        # Create coding assistant
        coding_assistant = AssistantAgent(
            name="claude_coder",
            model_client=model_client,
            system_message="""You are an expert Python programmer.
            When asked to solve a problem:
            1. Write clean, well-commented code
            2. Include error handling
            3. Add tests to verify the solution
            4. Explain how the code works"""
        )
        
        # Example coding tasks
        tasks = [
            "Write a function to calculate the factorial of a number recursively. Include tests and explain the logic.",
            "Create a Python class for a simple todo list with add, remove, and list methods. Show usage examples.",
            "Write a function that finds all prime numbers up to n using the Sieve of Eratosthenes. Explain the algorithm."
        ]
        
        for task in tasks:
            print(f"\nTask: {task}")
            
            try:
                response = await coding_assistant.on_messages([
                    TextMessage(content=task, source="user")
                ], CancellationToken())
                
                if response and hasattr(response, 'chat_message'):
                    print(f"\nCoding Assistant Response:")
                    print(response.chat_message.content)
                    
            except Exception as e:
                logger.error(f"Coding assistance failed: {e}")
                print(f"\nError during coding assistance: {e}")
        
    except Exception as e:
        logger.error(f"Coding assistant example failed: {e}")
        print(f"\nError: {e}")


async def tool_using_agent_example():
    """
    Agent that uses tools for enhanced capabilities.
    """
    print("\n=== Tool-Using Agent Example ===\n")
    
    try:
        # Ensure wrapper is healthy
        ensure_health()
        
        # Define some tools
        async def calculate(expression: str) -> str:
            """Calculate a mathematical expression."""
            try:
                # Safe evaluation of mathematical expressions
                import ast
                import operator as op
                
                # Supported operators
                operators = {
                    ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul,
                    ast.Div: op.truediv, ast.Pow: op.pow, ast.USub: op.neg
                }
                
                def eval_expr(node):
                    if isinstance(node, ast.Num):
                        return node.n
                    elif isinstance(node, ast.BinOp):
                        return operators[type(node.op)](eval_expr(node.left), eval_expr(node.right))
                    elif isinstance(node, ast.UnaryOp):
                        return operators[type(node.op)](eval_expr(node.operand))
                    else:
                        raise TypeError(node)
                
                result = eval_expr(ast.parse(expression, mode='eval').body)
                return f"The result of {expression} is {result}"
            except Exception as e:
                return f"Error calculating {expression}: {str(e)}"
        
        async def get_current_time() -> str:
            """Get the current time and date."""
            from datetime import datetime
            return f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        async def word_count(text: str) -> str:
            """Count words in the given text."""
            words = len(text.split())
            chars = len(text)
            return f"Word count: {words}, Character count: {chars}"
        
        # Create model client
        model_client = get_model_client(temperature=0.5)
        
        # Create tool-using assistant
        tool_assistant = AssistantAgent(
            name="claude_tool_user",
            model_client=model_client,
            system_message="""You are a helpful assistant with access to various tools.
            Use the appropriate tools to answer questions accurately.
            Always explain what tools you're using and why.""",
            tools=[calculate, get_current_time, word_count]
        )
        
        # Example queries that require tools
        queries = [
            "What is 1234 * 5678?",
            "What's the current time?",
            "How many words are in this sentence: 'The quick brown fox jumps over the lazy dog'?",
            "Calculate the compound interest on $10,000 at 5% annual rate for 10 years (use the formula A = P(1 + r)^t)"
        ]
        
        for query in queries:
            print(f"\nUser: {query}")
            
            try:
                response = await tool_assistant.on_messages([
                    TextMessage(content=query, source="user")
                ], CancellationToken())
                
                if response and hasattr(response, 'chat_message'):
                    print(f"\nAssistant: {response.chat_message.content}")
                    
            except Exception as e:
                logger.error(f"Tool usage failed: {e}")
                print(f"\nError using tools: {e}")
        
    except Exception as e:
        logger.error(f"Tool-using example failed: {e}")
        print(f"\nError: {e}")


async def main():
    """Run all single agent examples."""
    print("AutoGen Claude Code Integration - Single Agent Examples")
    print("=" * 60)
    print("📡 Connecting to Claude wrapper at: http://localhost:8000")
    
    # Run examples
    await basic_assistant_example()
    print("\n" + "=" * 60 + "\n")
    
    await coding_assistant_example()
    print("\n" + "=" * 60 + "\n")
    
    await tool_using_agent_example()
    print("\n" + "=" * 60 + "\n")
    
    print("All examples completed!")


if __name__ == "__main__":
    # Run with: python single_agent_example.py
    asyncio.run(main())