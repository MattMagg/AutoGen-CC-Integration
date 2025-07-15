"""
Utility functions for AutoGen Claude integration.
"""

import logging
import time
from typing import Dict, List, Any
from functools import wraps
import asyncio

logger = logging.getLogger(__name__)


class TokenUsageTracker:
    """Track token usage across conversations."""
    
    def __init__(self):
        self.total_prompt_tokens = 0
        self.total_completion_tokens = 0
        self.conversation_history = []
    
    def add_usage(self, prompt_tokens: int, completion_tokens: int, metadata: Dict[str, Any] = None):
        """Add token usage from a completion."""
        self.total_prompt_tokens += prompt_tokens
        self.total_completion_tokens += completion_tokens
        
        usage_record = {
            'timestamp': time.time(),
            'prompt_tokens': prompt_tokens,
            'completion_tokens': completion_tokens,
            'total_tokens': prompt_tokens + completion_tokens,
            'metadata': metadata or {}
        }
        self.conversation_history.append(usage_record)
    
    def get_summary(self) -> Dict[str, Any]:
        """Get usage summary."""
        total_tokens = self.total_prompt_tokens + self.total_completion_tokens
        return {
            'total_prompt_tokens': self.total_prompt_tokens,
            'total_completion_tokens': self.total_completion_tokens,
            'total_tokens': total_tokens,
            'num_completions': len(self.conversation_history),
            'average_tokens_per_completion': total_tokens / len(self.conversation_history) if self.conversation_history else 0
        }
    
    def reset(self):
        """Reset usage tracking."""
        self.total_prompt_tokens = 0
        self.total_completion_tokens = 0
        self.conversation_history = []


def async_retry(max_attempts: int = 3, delay: float = 1.0, backoff: float = 2.0):
    """
    Decorator for async functions with exponential backoff retry.
    
    Args:
        max_attempts: Maximum number of retry attempts
        delay: Initial delay between retries
        backoff: Backoff multiplier for exponential delay
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    if attempt < max_attempts - 1:
                        wait_time = delay * (backoff ** attempt)
                        logger.warning(f"{func.__name__} failed (attempt {attempt + 1}/{max_attempts}): {e}")
                        await asyncio.sleep(wait_time)
                    else:
                        logger.error(f"{func.__name__} failed after {max_attempts} attempts: {e}")
            raise last_error
        return wrapper
    return decorator


def format_conversation_history(messages: List[Dict[str, Any]], max_length: int = 1000) -> str:
    """
    Format conversation history for display.
    
    Args:
        messages: List of message dictionaries
        max_length: Maximum length per message
        
    Returns:
        Formatted conversation string
    """
    formatted = []
    for msg in messages:
        role = msg.get('role', 'unknown')
        content = msg.get('content', '')
        
        # Truncate long messages
        if len(content) > max_length:
            content = content[:max_length] + "... [truncated]"
        
        formatted.append(f"{role.upper()}: {content}")
    
    return "\n\n".join(formatted)


def extract_code_blocks(text: str) -> List[Dict[str, str]]:
    """
    Extract code blocks from text.
    
    Args:
        text: Text containing code blocks
        
    Returns:
        List of dictionaries with 'language' and 'code' keys
    """
    import re
    
    # Pattern to match code blocks with optional language
    pattern = r'```(\w*)\n(.*?)```'
    matches = re.findall(pattern, text, re.DOTALL)
    
    code_blocks = []
    for language, code in matches:
        code_blocks.append({
            'language': language or 'text',
            'code': code.strip()
        })
    
    return code_blocks


class ConversationLogger:
    """Log conversations for debugging and analysis."""
    
    def __init__(self, log_file: str = "autogen_conversations.log"):
        self.log_file = log_file
        self.file_handler = logging.FileHandler(log_file)
        self.file_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
        self.file_handler.setFormatter(formatter)
        
        self.logger = logging.getLogger("conversation")
        self.logger.addHandler(self.file_handler)
        self.logger.setLevel(logging.INFO)
    
    def log_message(self, agent_name: str, message: str, metadata: Dict[str, Any] = None):
        """Log a message from an agent."""
        log_entry = f"[{agent_name}] {message}"
        if metadata:
            log_entry += f" | Metadata: {metadata}"
        self.logger.info(log_entry)
    
    def log_error(self, error: str, context: Dict[str, Any] = None):
        """Log an error."""
        log_entry = f"ERROR: {error}"
        if context:
            log_entry += f" | Context: {context}"
        self.logger.error(log_entry)


def validate_model_response(response: Dict[str, Any]) -> bool:
    """
    Validate that a model response has expected structure.
    
    Args:
        response: Response dictionary from model
        
    Returns:
        bool: True if valid, False otherwise
    """
    required_fields = ['choices', 'usage']
    
    # Check required fields
    for field in required_fields:
        if field not in response:
            logger.error(f"Missing required field in response: {field}")
            return False
    
    # Check choices structure
    if not response['choices'] or not isinstance(response['choices'], list):
        logger.error("Invalid choices in response")
        return False
    
    # Check first choice has message
    first_choice = response['choices'][0]
    if 'message' not in first_choice:
        logger.error("Missing message in first choice")
        return False
    
    return True