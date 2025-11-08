"""
Unit tests for API key manager.

Related Documentation:
  ├─ Plan: docs/03_plans/llm-integration/README.md
  └─ Tests: src-python/tests/unit/test_api_key_manager.py
"""
import pytest
import os
import sys
from pathlib import Path
from unittest.mock import patch, mock_open

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from modules.llm_integration.api_key_manager import APIKeyManager
from modules.llm_integration.exceptions import APIKeyError


@pytest.mark.unit
class TestAPIKeyManager:
    """Test cases for APIKeyManager."""
    
    def test_init_default(self):
        """Test API key manager initialization with default settings."""
        manager = APIKeyManager()
        assert manager is not None
    
    def test_init_with_env_file(self, tmp_path):
        """Test API key manager initialization with custom env file."""
        env_file = tmp_path / ".env"
        env_file.write_text("OPENAI_API_KEY=test-openai-key\nANTHROPIC_API_KEY=test-anthropic-key\n")
        
        manager = APIKeyManager(env_file=str(env_file))
        assert manager.has_openai_api_key()
        assert manager.has_anthropic_api_key()
    
    @patch.dict(os.environ, {"OPENAI_API_KEY": "test-openai-key"})
    def test_get_openai_api_key_success(self):
        """Test successful OpenAI API key retrieval."""
        manager = APIKeyManager()
        key = manager.get_openai_api_key()
        assert key == "test-openai-key"
    
    @patch.dict(os.environ, {}, clear=True)
    def test_get_openai_api_key_missing(self):
        """Test OpenAI API key retrieval when key is missing."""
        manager = APIKeyManager()
        with pytest.raises(APIKeyError) as exc_info:
            manager.get_openai_api_key()
        assert "OPENAI_API_KEY" in str(exc_info.value)
    
    @patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-anthropic-key"})
    def test_get_anthropic_api_key_success(self):
        """Test successful Anthropic API key retrieval."""
        manager = APIKeyManager()
        key = manager.get_anthropic_api_key()
        assert key == "test-anthropic-key"
    
    @patch.dict(os.environ, {}, clear=True)
    def test_get_anthropic_api_key_missing(self):
        """Test Anthropic API key retrieval when key is missing."""
        manager = APIKeyManager()
        with pytest.raises(APIKeyError) as exc_info:
            manager.get_anthropic_api_key()
        assert "ANTHROPIC_API_KEY" in str(exc_info.value)
    
    @patch.dict(os.environ, {"OPENAI_API_KEY": "test-openai-key"})
    def test_has_openai_api_key_true(self):
        """Test OpenAI API key availability check when key exists."""
        manager = APIKeyManager()
        assert manager.has_openai_api_key() is True
    
    @patch.dict(os.environ, {}, clear=True)
    def test_has_openai_api_key_false(self):
        """Test OpenAI API key availability check when key is missing."""
        manager = APIKeyManager()
        assert manager.has_openai_api_key() is False
    
    @patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-anthropic-key"})
    def test_has_anthropic_api_key_true(self):
        """Test Anthropic API key availability check when key exists."""
        manager = APIKeyManager()
        assert manager.has_anthropic_api_key() is True
    
    @patch.dict(os.environ, {}, clear=True)
    def test_has_anthropic_api_key_false(self):
        """Test Anthropic API key availability check when key is missing."""
        manager = APIKeyManager()
        assert manager.has_anthropic_api_key() is False

