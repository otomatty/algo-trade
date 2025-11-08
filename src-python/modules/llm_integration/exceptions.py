"""
Custom exception classes for LLM integration.

Related Documentation:
  ├─ Plan: docs/03_plans/llm-integration/README.md
  └─ Architecture: docs/03_plans/llm-integration/architecture.md
"""


class LLMError(Exception):
    """Base exception class for all LLM-related errors."""
    pass


class APIKeyError(LLMError):
    """Raised when API key is missing or invalid."""
    pass


class RateLimitError(LLMError):
    """Raised when API rate limit is exceeded."""
    pass


class APIError(LLMError):
    """Raised when API call fails."""
    
    def __init__(self, message: str, status_code: int = None, response_body: str = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_body = response_body


class TimeoutError(LLMError):
    """Raised when API call times out."""
    pass


class ParseError(LLMError):
    """Raised when response parsing fails."""
    pass

