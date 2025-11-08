"""
Base LLM client class with common functionality.

Related Documentation:
  ├─ Plan: docs/03_plans/llm-integration/README.md
  └─ Architecture: docs/03_plans/llm-integration/architecture.md

DEPENDENCY MAP:

Parents (Files that import this file):
  ├─ src-python/modules/llm_integration/openai_client.py
  └─ src-python/modules/llm_integration/anthropic_client.py

Dependencies (External files that this file imports):
  ├─ abc (standard library)
  ├─ logging (standard library)
  ├─ typing (standard library)
  ├─ tenacity (external)
  └─ src-python/modules/llm_integration/exceptions.py
"""
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)

from .exceptions import LLMError, RateLimitError, APIError, TimeoutError


logger = logging.getLogger(__name__)


class LLMClient(ABC):
    """Abstract base class for LLM API clients."""
    
    def __init__(
        self,
        api_key: str,
        timeout: int = 60,
        max_retries: int = 3,
        retry_wait_min: int = 4,
        retry_wait_max: int = 10,
    ):
        """
        Initialize LLM client.
        
        Args:
            api_key: API key for the provider
            timeout: Request timeout in seconds (default: 60)
            max_retries: Maximum number of retry attempts (default: 3)
            retry_wait_min: Minimum wait time between retries in seconds (default: 4)
            retry_wait_max: Maximum wait time between retries in seconds (default: 10)
        """
        self.api_key = api_key
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_wait_min = retry_wait_min
        self.retry_wait_max = retry_wait_max
    
    @abstractmethod
    def generate(
        self,
        prompt: str,
        model: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: float = 0.7,
        **kwargs
    ) -> str:
        """
        Generate text using LLM.
        
        Args:
            prompt: Input prompt text
            model: Model name (optional, uses default if not provided)
            max_tokens: Maximum tokens to generate (optional)
            temperature: Sampling temperature (default: 0.7)
            **kwargs: Additional provider-specific parameters
            
        Returns:
            Generated text response
            
        Raises:
            LLMError: If generation fails
        """
        pass
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((RateLimitError, APIError)),
        reraise=True,
    )
    def _call_with_retry(self, func, *args, **kwargs):
        """
        Call a function with retry logic.
        
        Args:
            func: Function to call
            *args: Positional arguments
            **kwargs: Keyword arguments
            
        Returns:
            Function result
            
        Raises:
            LLMError: If all retries fail
        """
        try:
            return func(*args, **kwargs)
        except RateLimitError as e:
            logger.warning(f"Rate limit error: {e}. Retrying...")
            raise
        except APIError as e:
            logger.warning(f"API error: {e}. Retrying...")
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise LLMError(f"Unexpected error: {e}") from e
    
    def _handle_error(self, error: Exception, context: str = ""):
        """
        Handle and transform errors into custom exceptions.
        
        Args:
            error: Original exception
            context: Additional context information
            
        Raises:
            LLMError: Transformed exception
        """
        error_msg = f"{context}: {str(error)}" if context else str(error)
        logger.error(error_msg)
        
        # Transform common errors
        if "rate limit" in str(error).lower() or "429" in str(error):
            raise RateLimitError(error_msg) from error
        elif "timeout" in str(error).lower() or "timed out" in str(error).lower():
            raise TimeoutError(error_msg) from error
        else:
            raise APIError(error_msg) from error

