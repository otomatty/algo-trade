"""
Unit tests for LLM clients.

Related Documentation:
  ├─ Plan: docs/03_plans/llm-integration/README.md
  └─ Tests: src-python/tests/unit/test_llm_client.py
"""
import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from modules.llm_integration.openai_client import OpenAIClient
from modules.llm_integration.anthropic_client import AnthropicClient
from modules.llm_integration.exceptions import (
    LLMError,
    APIKeyError,
    RateLimitError,
    APIError,
    TimeoutError,
)


@pytest.mark.unit
class TestOpenAIClient:
    """Test cases for OpenAIClient."""
    
    def test_init(self):
        """Test OpenAI client initialization."""
        client = OpenAIClient(api_key="test-key")
        assert client.api_key == "test-key"
        assert client.default_model == "gpt-4"
        assert client.timeout == 60
    
    def test_init_custom_params(self):
        """Test OpenAI client initialization with custom parameters."""
        client = OpenAIClient(
            api_key="test-key",
            default_model="gpt-3.5-turbo",
            timeout=30,
            max_retries=5
        )
        assert client.default_model == "gpt-3.5-turbo"
        assert client.timeout == 30
        assert client.max_retries == 5
    
    @patch('modules.llm_integration.openai_client.OpenAI')
    def test_generate_success(self, mock_openai_class):
        """Test successful text generation."""
        # Setup mock
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Generated text"
        mock_client.chat.completions.create.return_value = mock_response
        
        client = OpenAIClient(api_key="test-key")
        result = client.generate("Test prompt")
        
        assert result == "Generated text"
        mock_client.chat.completions.create.assert_called_once()
    
    @patch('modules.llm_integration.openai_client.OpenAI')
    def test_generate_with_custom_model(self, mock_openai_class):
        """Test generation with custom model."""
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Generated text"
        mock_client.chat.completions.create.return_value = mock_response
        
        client = OpenAIClient(api_key="test-key")
        result = client.generate("Test prompt", model="gpt-3.5-turbo")
        
        call_args = mock_client.chat.completions.create.call_args
        assert call_args[1]["model"] == "gpt-3.5-turbo"
    
    @patch('modules.llm_integration.openai_client.OpenAI')
    def test_generate_rate_limit_error(self, mock_openai_class):
        """Test rate limit error handling."""
        from openai import RateLimitError as OpenAIRateLimitError
        
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        mock_client.chat.completions.create.side_effect = OpenAIRateLimitError(
            "Rate limit exceeded",
            response=Mock(),
            body=Mock()
        )
        
        client = OpenAIClient(api_key="test-key")
        with pytest.raises(RateLimitError):
            client.generate("Test prompt")
    
    @patch('modules.llm_integration.openai_client.OpenAI')
    def test_generate_timeout_error(self, mock_openai_class):
        """Test timeout error handling."""
        from openai import APITimeoutError
        
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        mock_request = Mock()
        mock_client.chat.completions.create.side_effect = APITimeoutError(mock_request)
        
        client = OpenAIClient(api_key="test-key")
        with pytest.raises(TimeoutError):
            client.generate("Test prompt")
    
    @patch('modules.llm_integration.openai_client.OpenAI')
    def test_generate_empty_response(self, mock_openai_class):
        """Test empty response handling."""
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = None
        mock_client.chat.completions.create.return_value = mock_response
        
        client = OpenAIClient(api_key="test-key")
        with pytest.raises(APIError):
            client.generate("Test prompt")


@pytest.mark.unit
class TestAnthropicClient:
    """Test cases for AnthropicClient."""
    
    def test_init(self):
        """Test Anthropic client initialization."""
        client = AnthropicClient(api_key="test-key")
        assert client.api_key == "test-key"
        assert client.default_model == "claude-3-opus-20240229"
        assert client.timeout == 60
    
    def test_init_custom_params(self):
        """Test Anthropic client initialization with custom parameters."""
        client = AnthropicClient(
            api_key="test-key",
            default_model="claude-3-sonnet-20240229",
            timeout=30,
            max_retries=5
        )
        assert client.default_model == "claude-3-sonnet-20240229"
        assert client.timeout == 30
        assert client.max_retries == 5
    
    @patch('modules.llm_integration.anthropic_client.Anthropic')
    def test_generate_success(self, mock_anthropic_class):
        """Test successful text generation."""
        # Setup mock
        mock_client = MagicMock()
        mock_anthropic_class.return_value = mock_client
        
        mock_content_block = MagicMock()
        mock_content_block.type = "text"
        mock_content_block.text = "Generated text"
        
        mock_response = MagicMock()
        mock_response.content = [mock_content_block]
        mock_client.messages.create.return_value = mock_response
        
        client = AnthropicClient(api_key="test-key")
        result = client.generate("Test prompt")
        
        assert result == "Generated text"
        mock_client.messages.create.assert_called_once()
    
    @patch('modules.llm_integration.anthropic_client.Anthropic')
    def test_generate_with_custom_model(self, mock_anthropic_class):
        """Test generation with custom model."""
        mock_client = MagicMock()
        mock_anthropic_class.return_value = mock_client
        
        mock_content_block = MagicMock()
        mock_content_block.type = "text"
        mock_content_block.text = "Generated text"
        
        mock_response = MagicMock()
        mock_response.content = [mock_content_block]
        mock_client.messages.create.return_value = mock_response
        
        client = AnthropicClient(api_key="test-key")
        result = client.generate("Test prompt", model="claude-3-sonnet-20240229")
        
        call_args = mock_client.messages.create.call_args
        assert call_args[1]["model"] == "claude-3-sonnet-20240229"
    
    @patch('modules.llm_integration.anthropic_client.Anthropic')
    def test_generate_rate_limit_error(self, mock_anthropic_class):
        """Test rate limit error handling."""
        from anthropic import RateLimitError as AnthropicRateLimitError
        
        mock_client = MagicMock()
        mock_anthropic_class.return_value = mock_client
        mock_client.messages.create.side_effect = AnthropicRateLimitError(
            "Rate limit exceeded",
            response=Mock(),
            body=Mock()
        )
        
        client = AnthropicClient(api_key="test-key")
        with pytest.raises(RateLimitError):
            client.generate("Test prompt")
    
    @patch('modules.llm_integration.anthropic_client.Anthropic')
    def test_generate_timeout_error(self, mock_anthropic_class):
        """Test timeout error handling."""
        from anthropic import APITimeoutError
        
        mock_client = MagicMock()
        mock_anthropic_class.return_value = mock_client
        mock_request = Mock()
        mock_client.messages.create.side_effect = APITimeoutError(mock_request)
        
        client = AnthropicClient(api_key="test-key")
        with pytest.raises(TimeoutError):
            client.generate("Test prompt")
    
    @patch('modules.llm_integration.anthropic_client.Anthropic')
    def test_generate_empty_response(self, mock_anthropic_class):
        """Test empty response handling."""
        mock_client = MagicMock()
        mock_anthropic_class.return_value = mock_client
        
        mock_response = MagicMock()
        mock_response.content = []  # Empty content
        mock_client.messages.create.return_value = mock_response
        
        client = AnthropicClient(api_key="test-key")
        with pytest.raises(APIError):
            client.generate("Test prompt")

