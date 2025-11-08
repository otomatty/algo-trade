"""
Unit tests for proposal generator.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from typing import Dict, Any
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from modules.algorithm_proposal.proposal_generator import ProposalGenerator


@pytest.mark.unit
class TestProposalGenerator:
    """Test cases for ProposalGenerator class."""
    
    @pytest.fixture
    def mock_llm_client(self):
        """Create mock LLM client."""
        client = Mock()
        client.generate = Mock(return_value='{"proposals": []}')
        return client
    
    @pytest.fixture
    def mock_prompt_builder(self):
        """Create mock prompt builder."""
        builder = Mock()
        builder.build_algorithm_proposal_prompt = Mock(return_value="Test prompt")
        return builder
    
    @pytest.fixture
    def mock_response_parser(self):
        """Create mock response parser."""
        parser = Mock()
        parser.parse_algorithm_proposals = Mock(return_value=[])
        return parser
    
    @pytest.fixture
    def mock_fallback_handler(self, mock_response_parser):
        """Create mock fallback handler."""
        handler = Mock()
        handler.parse_with_fallback = Mock(return_value=[])
        return handler
    
    @pytest.fixture
    def mock_api_key_manager(self):
        """Create mock API key manager."""
        manager = Mock()
        manager.get_openai_api_key = Mock(return_value="test-openai-key")
        manager.get_anthropic_api_key = Mock(return_value="test-anthropic-key")
        return manager
    
    @pytest.fixture
    def generator(self, mock_llm_client, mock_prompt_builder, mock_fallback_handler, mock_api_key_manager):
        """Create ProposalGenerator instance with mocks."""
        with patch('modules.algorithm_proposal.proposal_generator.OpenAIClient', return_value=mock_llm_client), \
             patch('modules.algorithm_proposal.proposal_generator.PromptBuilder', return_value=mock_prompt_builder), \
             patch('modules.algorithm_proposal.proposal_generator.FallbackHandler', return_value=mock_fallback_handler):
            return ProposalGenerator(api_key_manager=mock_api_key_manager)
    
    def test_generate_proposals_success(self, generator, mock_llm_client, mock_prompt_builder, mock_fallback_handler):
        """Test successful proposal generation."""
        analysis_result = {
            'analysis_summary': {
                'trend_direction': 'upward',
                'volatility_level': 'medium',
                'dominant_patterns': ['uptrend'],
            },
            'technical_indicators': {
                'rsi': {'value': 60.0, 'period': 14, 'signal': 'neutral'},
            },
            'statistics': {
                'price_range': {'min': 100, 'max': 150, 'current': 140},
                'volume_average': 1000000,
                'price_change_percent': 5.0,
            },
        }
        
        user_preferences = {
            'risk_tolerance': 'medium',
            'trading_frequency': 'high',
            'preferred_indicators': ['RSI', 'MACD'],
        }
        
        mock_proposals = [
            {
                'name': 'Test Algorithm',
                'description': 'Test description',
                'rationale': 'Test rationale',
                'definition': {
                    'triggers': [],
                    'actions': [],
                },
                'confidence_score': 0.8,
            },
        ]
        
        mock_fallback_handler.parse_with_fallback.return_value = mock_proposals
        
        proposals = generator.generate_proposals(
            analysis_result,
            user_preferences,
            num_proposals=5
        )
        
        assert len(proposals) == 1
        assert proposals[0]['name'] == 'Test Algorithm'
        mock_prompt_builder.build_algorithm_proposal_prompt.assert_called_once()
        mock_llm_client.generate.assert_called_once()
        mock_fallback_handler.parse_with_fallback.assert_called_once()
    
    def test_generate_proposals_with_default_preferences(self, generator, mock_llm_client, mock_prompt_builder, mock_fallback_handler):
        """Test proposal generation with default user preferences."""
        analysis_result = {
            'analysis_summary': {},
            'technical_indicators': {},
            'statistics': {},
        }
        
        mock_fallback_handler.parse_with_fallback.return_value = []
        
        proposals = generator.generate_proposals(analysis_result)
        
        assert proposals == []
        mock_prompt_builder.build_algorithm_proposal_prompt.assert_called_once()
        # Should use default preferences when not provided
        call_args = mock_prompt_builder.build_algorithm_proposal_prompt.call_args
        # Check positional args or keyword args
        if len(call_args[0]) > 1:
            user_prefs = call_args[0][1]
        else:
            user_prefs = call_args[1].get('user_preferences')
        assert user_prefs is None or user_prefs == {}
    
    def test_generate_proposals_llm_error(self, generator, mock_llm_client, mock_prompt_builder):
        """Test proposal generation when LLM API fails."""
        from modules.llm_integration.exceptions import LLMError
        
        analysis_result = {
            'analysis_summary': {},
            'technical_indicators': {},
            'statistics': {},
        }
        
        mock_llm_client.generate.side_effect = LLMError("API error")
        
        with pytest.raises(LLMError):
            generator.generate_proposals(analysis_result)
    
    def test_generate_proposals_parse_error(self, generator, mock_llm_client, mock_prompt_builder, mock_fallback_handler):
        """Test proposal generation when parsing fails."""
        from modules.llm_integration.exceptions import ParseError
        
        analysis_result = {
            'analysis_summary': {},
            'technical_indicators': {},
            'statistics': {},
        }
        
        mock_fallback_handler.parse_with_fallback.side_effect = ParseError("Parse error")
        
        with pytest.raises(ParseError):
            generator.generate_proposals(analysis_result)

