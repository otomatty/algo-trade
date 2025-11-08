"""
Anthropic API client implementation.

Related Documentation:
  ├─ Plan: docs/03_plans/llm-integration/README.md
  └─ Architecture: docs/03_plans/llm-integration/architecture.md

DEPENDENCY MAP:

Parents (Files that import this file):
  └─ src-python/modules/llm_integration/__init__.py

Dependencies (External files that this file imports):
  ├─ typing (standard library)
  ├─ logging (standard library)
  ├─ anthropic (external)
  ├─ src-python/modules/llm_integration/client.py
  └─ src-python/modules/llm_integration/exceptions.py
"""
import logging
from typing import Optional
from anthropic import Anthropic
from anthropic import APIError as AnthropicAPIError
from anthropic import RateLimitError as AnthropicRateLimitError
from anthropic import APITimeoutError

from .client import LLMClient
from .exceptions import RateLimitError, APIError, TimeoutError


logger = logging.getLogger(__name__)


class AnthropicClient(LLMClient):
    """Anthropic API client."""
    
    DEFAULT_MODEL = "claude-3-opus-20240229"
    DEFAULT_MAX_TOKENS = 2000
    
    def __init__(
        self,
        api_key: str,
        default_model: str = DEFAULT_MODEL,
        timeout: int = 60,
        max_retries: int = 3,
        retry_wait_min: int = 4,
        retry_wait_max: int = 10,
    ):
        """
        Initialize Anthropic client.
        
        Args:
            api_key: Anthropic API key
            default_model: Default model to use (default: claude-3-opus-20240229)
            timeout: Request timeout in seconds (default: 60)
            max_retries: Maximum number of retry attempts (default: 3)
            retry_wait_min: Minimum wait time between retries in seconds (default: 4)
            retry_wait_max: Maximum wait time between retries in seconds (default: 10)
        """
        super().__init__(api_key, timeout, max_retries, retry_wait_min, retry_wait_max)
        self.default_model = default_model
        self.client = Anthropic(api_key=api_key, timeout=timeout)
    
    def generate(
        self,
        prompt: str,
        model: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: float = 0.7,
        **kwargs
    ) -> str:
        """
        Generate text using Anthropic API.
        
        Args:
            prompt: Input prompt text
            model: Model name (optional, uses default if not provided)
            max_tokens: Maximum tokens to generate (optional, uses default if not provided)
            temperature: Sampling temperature (default: 0.7)
            **kwargs: Additional Anthropic API parameters
            
        Returns:
            Generated text response
            
        Raises:
            RateLimitError: If rate limit is exceeded
            APIError: If API call fails
            TimeoutError: If request times out
        """
        model = model or self.default_model
        max_tokens = max_tokens or self.DEFAULT_MAX_TOKENS
        
        try:
            logger.debug(f"Calling Anthropic API with model: {model}")
            
            response = self.client.messages.create(
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                **kwargs
            )
            
            # Anthropic returns a list of content blocks
            content = ""
            for block in response.content:
                if block.type == "text":
                    content += block.text
            
            if not content:
                raise APIError("Empty response from Anthropic API")
            
            logger.debug(f"Anthropic API response received: {len(content)} characters")
            return content
            
        except AnthropicRateLimitError as e:
            logger.error(f"Anthropic rate limit error: {e}")
            raise RateLimitError(f"Anthropic rate limit exceeded: {e}") from e
        except APITimeoutError as e:
            logger.error(f"Anthropic timeout error: {e}")
            raise TimeoutError(f"Anthropic request timed out: {e}") from e
        except AnthropicAPIError as e:
            logger.error(f"Anthropic API error: {e}")
            raise APIError(f"Anthropic API error: {e}", status_code=getattr(e, 'status_code', None)) from e
        except Exception as e:
            logger.error(f"Unexpected error calling Anthropic API: {e}")
            self._handle_error(e, "Anthropic API call failed")

