"""
AWS Lambda handler for AutoGen agents using Claude Code wrapper.
Deploy this as a Lambda function to run AutoGen workflows serverlessly.
"""

import os
import json
import asyncio
import logging
from typing import Dict, Any
import boto3
from botocore.exceptions import ClientError

# AutoGen imports
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.models import ModelInfo

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# AWS clients
secrets_client = boto3.client('secretsmanager')
ssm_client = boto3.client('ssm')


def get_secret(secret_name: str) -> Dict[str, Any]:
    """Retrieve secret from AWS Secrets Manager."""
    try:
        response = secrets_client.get_secret_value(SecretId=secret_name)
        return json.loads(response['SecretString'])
    except ClientError as e:
        logger.error(f"Error retrieving secret {secret_name}: {e}")
        raise


def get_parameter(parameter_name: str) -> str:
    """Retrieve parameter from AWS Systems Manager Parameter Store."""
    try:
        response = ssm_client.get_parameter(Name=parameter_name, WithDecryption=True)
        return response['Parameter']['Value']
    except ClientError as e:
        logger.error(f"Error retrieving parameter {parameter_name}: {e}")
        raise


def get_model_client() -> OpenAIChatCompletionClient:
    """Create model client for Claude Code wrapper."""
    # Get configuration from environment or AWS services
    wrapper_url = os.environ.get('CLAUDE_WRAPPER_URL') or get_parameter('/autogen/claude-wrapper-url')
    
    # Get auth token from Secrets Manager
    secret_name = os.environ.get('CLAUDE_AUTH_SECRET', '/autogen/claude-auth')
    auth_data = get_secret(secret_name)
    auth_token = auth_data.get('token')
    
    if not wrapper_url or not auth_token:
        raise ValueError("Missing required configuration")
    
    # Create client
    return OpenAIChatCompletionClient(
        model="claude-opus-4-20250514",
        api_key=auth_token,
        base_url=f"{wrapper_url}/v1",
        temperature=0.7,
        model_info=ModelInfo(
            vision=True,
            function_calling=True,
            json_output=True,
            family="claude",
            structured_output=True
        )
    )


async def run_single_agent(task: str, agent_type: str = "assistant") -> Dict[str, Any]:
    """Run a single agent task."""
    model_client = get_model_client()
    
    # Define agent configurations
    agent_configs = {
        "assistant": {
            "name": "claude_assistant",
            "system_message": "You are a helpful AI assistant. Provide clear and accurate responses."
        },
        "analyst": {
            "name": "data_analyst",
            "system_message": "You are a data analyst. Analyze information and provide insights with supporting evidence."
        },
        "coder": {
            "name": "code_expert",
            "system_message": "You are an expert programmer. Write clean, efficient code with proper error handling."
        },
        "writer": {
            "name": "content_writer",
            "system_message": "You are a professional writer. Create well-structured, engaging content."
        }
    }
    
    config = agent_configs.get(agent_type, agent_configs["assistant"])
    
    # Create agent
    agent = AssistantAgent(
        name=config["name"],
        model_client=model_client,
        system_message=config["system_message"]
    )
    
    # Execute task
    try:
        response = await agent.on_messages([TextMessage(content=task, source="user")])
        
        return {
            "success": True,
            "agent": config["name"],
            "response": response.chat_message.content,
            "usage": {
                "prompt_tokens": getattr(response, 'usage', {}).get('prompt_tokens', 0),
                "completion_tokens": getattr(response, 'usage', {}).get('completion_tokens', 0)
            }
        }
    except Exception as e:
        logger.error(f"Agent execution failed: {e}")
        return {
            "success": False,
            "error": str(e),
            "agent": config["name"]
        }


async def run_multi_agent_pipeline(task: str, pipeline: str = "research") -> Dict[str, Any]:
    """Run a multi-agent pipeline."""
    model_client = get_model_client()
    
    if pipeline == "research":
        # Research → Analysis → Summary pipeline
        agents = [
            AssistantAgent(
                name="researcher",
                model_client=model_client,
                system_message="Research the topic thoroughly and gather relevant information."
            ),
            AssistantAgent(
                name="analyst",
                model_client=model_client,
                system_message="Analyze the research findings and identify key insights."
            ),
            AssistantAgent(
                name="summarizer",
                model_client=model_client,
                system_message="Create a concise summary with actionable recommendations."
            )
        ]
        
        results = []
        current_input = task
        
        for agent in agents:
            try:
                response = await agent.on_messages([TextMessage(content=current_input, source="pipeline")])
                result = {
                    "agent": agent.name,
                    "output": response.chat_message.content
                }
                results.append(result)
                current_input = f"Based on this: {response.chat_message.content}\n\nPlease proceed with your task."
            except Exception as e:
                logger.error(f"Pipeline step {agent.name} failed: {e}")
                return {
                    "success": False,
                    "error": f"Pipeline failed at {agent.name}: {str(e)}",
                    "partial_results": results
                }
        
        return {
            "success": True,
            "pipeline": pipeline,
            "results": results,
            "final_output": results[-1]["output"] if results else None
        }
    
    else:
        return {
            "success": False,
            "error": f"Unknown pipeline type: {pipeline}"
        }


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    AWS Lambda handler for AutoGen workflows.
    
    Event structure:
    {
        "action": "single_agent" | "multi_agent",
        "task": "The task to perform",
        "agent_type": "assistant" | "analyst" | "coder" | "writer" (for single_agent),
        "pipeline": "research" | "development" | "review" (for multi_agent)
    }
    """
    logger.info(f"Received event: {json.dumps(event)}")
    
    # Extract parameters
    action = event.get('action', 'single_agent')
    task = event.get('task')
    
    if not task:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Missing required parameter: task'})
        }
    
    # Run the appropriate workflow
    try:
        if action == 'single_agent':
            agent_type = event.get('agent_type', 'assistant')
            result = asyncio.run(run_single_agent(task, agent_type))
        elif action == 'multi_agent':
            pipeline = event.get('pipeline', 'research')
            result = asyncio.run(run_multi_agent_pipeline(task, pipeline))
        else:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': f'Unknown action: {action}'})
            }
        
        return {
            'statusCode': 200,
            'body': json.dumps(result)
        }
        
    except Exception as e:
        logger.error(f"Lambda execution failed: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': 'Internal server error',
                'message': str(e)
            })
        }


# For local testing
if __name__ == "__main__":
    test_event = {
        "action": "single_agent",
        "task": "Explain the benefits of serverless architecture",
        "agent_type": "assistant"
    }
    
    result = lambda_handler(test_event, None)
    print(json.dumps(result, indent=2))