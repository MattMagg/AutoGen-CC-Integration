"""
Configuration module for AutoGen with Claude Code OpenAI wrapper.
Handles native localhost connection and model client creation.
"""

import asyncio
import logging
from functools import wraps
import requests
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.models import ModelInfo

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ClaudeCodeConfig:
    """Manages configuration for Claude Code OpenAI wrapper integration."""
    
    def __init__(self):
        self.base_url = "http://localhost:8000/v1"
        self.wrapper_host = "http://localhost:8000"
    
    def health_check(self) -> bool:
        """
        Check if the wrapper is accessible and responding.
        
        Returns:
            bool: True if wrapper is healthy, False otherwise
        """
        try:
            # Test the models endpoint
            # Note: Auth is handled natively by the wrapper via Claude CLI OAuth
            response = requests.get(
                f"{self.wrapper_host}/v1/models",
                timeout=5
            )
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False
    
    def get_model_client(
        self,
        model: str = "claude-opus-4-20250514",
        temperature: float = 0.7,
        max_retries: int = 3,
        retry_delay: float = 1.0
    ) -> OpenAIChatCompletionClient:
        """
        Create an OpenAI-compatible client for Claude Code wrapper.
        
        Args:
            model: The model to use
            temperature: Temperature for generation
            max_retries: Number of retry attempts
            retry_delay: Initial delay between retries (exponential backoff)
            
        Returns:
            OpenAIChatCompletionClient: Configured client instance
        """
        # Note: Auth is handled by the native wrapper via Claude CLI OAuth
        # No API key needed - wrapper uses host's authenticated Claude CLI
        
        # Create the client with Claude's capabilities
        client = OpenAIChatCompletionClient(
            model=model,
            api_key="not-needed",  # Wrapper handles auth natively
            base_url=self.base_url,
            temperature=temperature,
            model_info=ModelInfo(
                vision=True,          # Claude supports images
                function_calling=True, # Claude supports tool use
                json_output=True,     # Claude can output JSON
                family="claude",      # Model family
                structured_output=True
            )
        )
        
        # Wrap client methods with retry logic
        original_create = client.create
        
        @wraps(original_create)
        async def create_with_retry(*args, **kwargs):
            last_error = None
            for attempt in range(max_retries):
                try:
                    return await original_create(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    if attempt < max_retries - 1:
                        wait_time = retry_delay * (2 ** attempt)
                        logger.warning(f"Request failed (attempt {attempt + 1}/{max_retries}): {e}")
                        logger.info(f"Retrying in {wait_time} seconds...")
                        await asyncio.sleep(wait_time)
                    else:
                        logger.error(f"All retry attempts failed: {e}")
            raise last_error
        
        client.create = create_with_retry
        return client


# Global configuration instance
config = ClaudeCodeConfig()


def get_model_client(**kwargs) -> OpenAIChatCompletionClient:
    """Convenience function to get a configured model client."""
    return config.get_model_client(**kwargs)


def ensure_health():
    """Ensure the wrapper is healthy before proceeding."""
    if not config.health_check():
        raise ConnectionError(
            "Claude Code wrapper is not accessible on localhost:8000. "
            "Please ensure the wrapper is running natively with: "
            "poetry run uvicorn main:app --host 0.0.0.0 --port 8000"
        )