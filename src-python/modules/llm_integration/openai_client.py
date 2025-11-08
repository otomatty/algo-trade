"""
OpenAI API client implementation.

Related Documentation:
  ├─ Plan: docs/03_plans/llm-integration/README.md
  └─ Architecture: docs/03_plans/llm-integration/architecture.md

DEPENDENCY MAP:

Parents (Files that import this file):
  └─ src-python/modules/llm_integration/__init__.py

Dependencies (External files that this file imports):
  ├─ typing (standard library)
  ├─ logging (standard library)
  ├─ openai (external)
  ├─ src-python/modules/llm_integration/client.py
  └─ src-python/modules/llm_integration/exceptions.py
"""
import logging
from typing import Optional
from openai import OpenAI
from openai import APIError as OpenAIAPIError
from openai import RateLimitError as OpenAIRateLimitError
from openai import APITimeoutError

from .client import LLMClient
from .exceptions import RateLimitError, APIError, TimeoutError


logger = logging.getLogger(__name__)


class OpenAIClient(LLMClient):
    """OpenAI API client."""
    
    DEFAULT_MODEL = "gpt-4"
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
        Initialize OpenAI client.
        
        Args:
            api_key: OpenAI API key
            default_model: Default model to use (default: gpt-4)
            timeout: Request timeout in seconds (default: 60)
            max_retries: Maximum number of retry attempts (default: 3)
            retry_wait_min: Minimum wait time between retries in seconds (default: 4)
            retry_wait_max: Maximum wait time between retries in seconds (default: 10)
        """
        super().__init__(api_key, timeout, max_retries, retry_wait_min, retry_wait_max)
        self.default_model = default_model
        self.client = OpenAI(api_key=api_key, timeout=timeout)
    
    def generate(
        self,
        prompt: str,
        model: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: float = 0.7,
        **kwargs
    ) -> str:
        """
        Generate text using OpenAI API.
        
        Args:
            prompt: Input prompt text
            model: Model name (optional, uses default if not provided)
            max_tokens: Maximum tokens to generate (optional, uses default if not provided)
            temperature: Sampling temperature (default: 0.7)
            **kwargs: Additional OpenAI API parameters
            
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
            logger.debug(f"Calling OpenAI API with model: {model}")
            
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=temperature,
                **kwargs
            )
            
            content = response.choices[0].message.content
            if not content:
                raise APIError("Empty response from OpenAI API")
            
            logger.debug(f"OpenAI API response received: {len(content)} characters")
            return content
            
        except OpenAIRateLimitError as e:
            logger.error(f"OpenAI rate limit error: {e}")
            raise RateLimitError(f"OpenAI rate limit exceeded: {e}") from e
        except APITimeoutError as e:
            logger.error(f"OpenAI timeout error: {e}")
            raise TimeoutError(f"OpenAI request timed out: {e}") from e
        except OpenAIAPIError as e:
            logger.error(f"OpenAI API error: {e}")
            raise APIError(f"OpenAI API error: {e}", status_code=getattr(e, 'status_code', None)) from e
        except Exception as e:
            logger.error(f"Unexpected error calling OpenAI API: {e}")
            self._handle_error(e, "OpenAI API call failed")

