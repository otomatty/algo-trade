"""
Integration tests for LLM integration.

Related Documentation:
  ├─ Plan: docs/03_plans/llm-integration/README.md
  └─ Tests: src-python/tests/integration/test_llm_integration.py
"""
import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from modules.llm_integration.api_key_manager import APIKeyManager
from modules.llm_integration.openai_client import OpenAIClient
from modules.llm_integration.anthropic_client import AnthropicClient
from modules.llm_integration.prompt_builder import PromptBuilder
from modules.llm_integration.response_parser import ResponseParser
from modules.llm_integration.fallback_handler import FallbackHandler
from modules.llm_integration.exceptions import (
    LLMError,
    APIKeyError,
    RateLimitError,
    APIError,
    ParseError,
)


@pytest.mark.integration
class TestLLMIntegration:
    """Integration tests for LLM integration."""
    
    @patch.dict('os.environ', {'OPENAI_API_KEY': 'test-openai-key'})
    def test_api_key_manager_openai(self):
        """Test API key manager with OpenAI key."""
        manager = APIKeyManager()
        assert manager.has_openai_api_key()
        key = manager.get_openai_api_key()
        assert key == "test-openai-key"
    
    @patch.dict('os.environ', {'ANTHROPIC_API_KEY': 'test-anthropic-key'})
    def test_api_key_manager_anthropic(self):
        """Test API key manager with Anthropic key."""
        manager = APIKeyManager()
        assert manager.has_anthropic_api_key()
        key = manager.get_anthropic_api_key()
        assert key == "test-anthropic-key"
    
    @patch('modules.llm_integration.openai_client.OpenAI')
    def test_openai_client_integration(self, mock_openai_class):
        """Test OpenAI client integration."""
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = '{"proposals": []}'
        mock_client.chat.completions.create.return_value = mock_response
        
        client = OpenAIClient(api_key="test-key")
        result = client.generate("Test prompt")
        
        assert result == '{"proposals": []}'
        mock_client.chat.completions.create.assert_called_once()
    
    @patch('modules.llm_integration.anthropic_client.Anthropic')
    def test_anthropic_client_integration(self, mock_anthropic_class):
        """Test Anthropic client integration."""
        mock_client = MagicMock()
        mock_anthropic_class.return_value = mock_client
        
        mock_content_block = MagicMock()
        mock_content_block.type = "text"
        mock_content_block.text = '{"predictions": []}'
        
        mock_response = MagicMock()
        mock_response.content = [mock_content_block]
        mock_client.messages.create.return_value = mock_response
        
        client = AnthropicClient(api_key="test-key")
        result = client.generate("Test prompt")
        
        assert result == '{"predictions": []}'
        mock_client.messages.create.assert_called_once()
    
    def test_prompt_builder_algorithm_proposal(self, tmp_path):
        """Test prompt builder for algorithm proposal."""
        # Create template
        template_dir = tmp_path / "templates"
        template_dir.mkdir()
        template_file = template_dir / "algorithm_proposal.txt"
        template_file.write_text("Trend: {trend_direction}, Proposals: {num_proposals}")
        
        from modules.llm_integration.prompt_templates import PromptTemplateManager
        
        manager = PromptTemplateManager(templates_dir=template_dir)
        builder = PromptBuilder(template_manager=manager)
        
        analysis_result = {
            "analysis_summary": {
                "trend_direction": "upward",
                "volatility_level": "high",
                "dominant_patterns": []
            },
            "technical_indicators": {},
            "statistics": {
                "price_range": {"min": 100, "max": 150, "current": 125},
                "price_change_percent": 5.5,
                "volume_average": 1000000
            }
        }
        
        prompt = builder.build_algorithm_proposal_prompt(analysis_result, num_proposals=3)
        
        assert "upward" in prompt
        assert "3" in prompt
    
    def test_response_parser_algorithm_proposal(self):
        """Test response parser for algorithm proposal."""
        parser = ResponseParser()
        
        response_text = """{
  "proposals": [
    {
      "name": "Test Algorithm",
      "description": "Test description",
      "rationale": "Test rationale",
      "definition": {
        "triggers": [],
        "actions": []
      },
      "confidence_score": 0.8
    }
  ]
}"""
        
        proposals = parser.parse_algorithm_proposals(response_text)
        assert len(proposals) == 1
        assert proposals[0]["name"] == "Test Algorithm"
    
    def test_fallback_handler_integration(self):
        """Test fallback handler integration."""
        handler = FallbackHandler()
        
        # Test with markdown wrapped JSON
        response_text = """Here is the response:
```json
{
  "proposals": [
    {
      "name": "Test",
      "description": "Test",
      "rationale": "Test",
      "definition": {
        "triggers": [],
        "actions": []
      },
      "confidence_score": 0.7
    }
  ]
}
```"""
        
        proposals = handler.parse_with_fallback(response_text, "algorithm_proposal")
        assert len(proposals) == 1
    
    @patch('modules.llm_integration.openai_client.OpenAI')
    def test_end_to_end_algorithm_proposal(self, mock_openai_class, tmp_path):
        """Test end-to-end algorithm proposal flow."""
        # Setup template
        template_dir = tmp_path / "templates"
        template_dir.mkdir()
        template_file = template_dir / "algorithm_proposal.txt"
        template_file.write_text("Prompt: {trend_direction}")
        
        # Setup mock OpenAI client
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = """{
  "proposals": [
    {
      "name": "Test Algorithm",
      "description": "Test",
      "rationale": "Test",
      "definition": {
        "triggers": [],
        "actions": []
      },
      "confidence_score": 0.8
    }
  ]
}"""
        mock_client.chat.completions.create.return_value = mock_response
        
        # Build prompt
        from modules.llm_integration.prompt_templates import PromptTemplateManager
        
        manager = PromptTemplateManager(templates_dir=template_dir)
        builder = PromptBuilder(template_manager=manager)
        
        analysis_result = {
            "analysis_summary": {
                "trend_direction": "upward",
                "volatility_level": "high",
                "dominant_patterns": []
            },
            "technical_indicators": {},
            "statistics": {
                "price_range": {"min": 100, "max": 150, "current": 125},
                "price_change_percent": 5.5,
                "volume_average": 1000000
            }
        }
        
        prompt = builder.build_algorithm_proposal_prompt(analysis_result)
        
        # Generate response (mocked)
        client = OpenAIClient(api_key="test-key")
        response_text = client.generate(prompt)
        
        # Parse response
        parser = ResponseParser()
        proposals = parser.parse_algorithm_proposals(response_text)
        
        assert len(proposals) == 1
        assert proposals[0]["name"] == "Test Algorithm"

