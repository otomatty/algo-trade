"""
API key management for LLM providers.

Related Documentation:
  ├─ Plan: docs/03_plans/llm-integration/README.md
  └─ Architecture: docs/03_plans/llm-integration/architecture.md

DEPENDENCY MAP:

Parents (Files that import this file):
  ├─ src-python/modules/llm_integration/openai_client.py
  ├─ src-python/modules/llm_integration/anthropic_client.py
  └─ src-python/modules/llm_integration/client.py

Dependencies (External files that this file imports):
  ├─ os (standard library)
  ├─ pathlib (standard library)
  └─ python-dotenv (external)
"""
import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

from .exceptions import APIKeyError


class APIKeyManager:
    """Manages API keys for LLM providers."""
    
    # Environment variable names for each provider
    OPENAI_API_KEY_ENV = "OPENAI_API_KEY"
    ANTHROPIC_API_KEY_ENV = "ANTHROPIC_API_KEY"
    
    def __init__(self, env_file: Optional[str] = None):
        """
        Initialize API key manager.
        
        Args:
            env_file: Path to .env file (optional, defaults to project root/.env)
        """
        if env_file:
            load_dotenv(env_file)
        else:
            # Try to load .env from project root
            project_root = Path(__file__).parent.parent.parent.parent
            env_path = project_root / ".env"
            if env_path.exists():
                load_dotenv(env_path)
            else:
                # Also try loading from current directory
                load_dotenv()
    
    def get_openai_api_key(self) -> str:
        """
        Get OpenAI API key from environment variable.
        
        Returns:
            API key string
            
        Raises:
            APIKeyError: If API key is not found
        """
        api_key = os.getenv(self.OPENAI_API_KEY_ENV)
        if not api_key:
            raise APIKeyError(
                f"OpenAI API key not found. Please set {self.OPENAI_API_KEY_ENV} environment variable."
            )
        return api_key
    
    def get_anthropic_api_key(self) -> str:
        """
        Get Anthropic API key from environment variable.
        
        Returns:
            API key string
            
        Raises:
            APIKeyError: If API key is not found
        """
        api_key = os.getenv(self.ANTHROPIC_API_KEY_ENV)
        if not api_key:
            raise APIKeyError(
                f"Anthropic API key not found. Please set {self.ANTHROPIC_API_KEY_ENV} environment variable."
            )
        return api_key
    
    def has_openai_api_key(self) -> bool:
        """Check if OpenAI API key is available."""
        return bool(os.getenv(self.OPENAI_API_KEY_ENV))
    
    def has_anthropic_api_key(self) -> bool:
        """Check if Anthropic API key is available."""
        return bool(os.getenv(self.ANTHROPIC_API_KEY_ENV))

