"""
Unit tests for prompt builder.

Related Documentation:
  ├─ Plan: docs/03_plans/llm-integration/README.md
  └─ Tests: src-python/tests/unit/test_prompt_builder.py
"""
import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from modules.llm_integration.prompt_builder import PromptBuilder
from modules.llm_integration.prompt_templates import PromptTemplateManager
from modules.llm_integration.exceptions import LLMError


@pytest.mark.unit
class TestPromptBuilder:
    """Test cases for PromptBuilder."""
    
    def test_init_default(self):
        """Test prompt builder initialization with default template manager."""
        builder = PromptBuilder()
        assert builder.template_manager is not None
    
    def test_init_custom_manager(self):
        """Test prompt builder initialization with custom template manager."""
        manager = PromptTemplateManager()
        builder = PromptBuilder(template_manager=manager)
        assert builder.template_manager == manager
    
    def test_build_algorithm_proposal_prompt(self, tmp_path):
        """Test algorithm proposal prompt building."""
        # Create template file
        template_dir = tmp_path / "templates"
        template_dir.mkdir()
        template_file = template_dir / "algorithm_proposal.txt"
        template_file.write_text(
            "Test prompt: {trend_direction}, {volatility_level}, {num_proposals}"
        )
        
        manager = PromptTemplateManager(templates_dir=template_dir)
        builder = PromptBuilder(template_manager=manager)
        
        analysis_result = {
            "analysis_summary": {
                "trend_direction": "upward",
                "volatility_level": "high",
                "dominant_patterns": ["pattern1", "pattern2"]
            },
            "technical_indicators": {
                "rsi": {"value": 65.5, "signal": "neutral"}
            },
            "statistics": {
                "price_range": {"min": 100, "max": 150, "current": 125},
                "price_change_percent": 5.5,
                "volume_average": 1000000
            }
        }
        
        prompt = builder.build_algorithm_proposal_prompt(
            analysis_result,
            num_proposals=3
        )
        
        assert "upward" in prompt
        assert "high" in prompt
        assert "3" in prompt
    
    def test_build_algorithm_proposal_prompt_with_preferences(self, tmp_path):
        """Test algorithm proposal prompt building with user preferences."""
        template_dir = tmp_path / "templates"
        template_dir.mkdir()
        template_file = template_dir / "algorithm_proposal.txt"
        template_file.write_text(
            "Risk: {risk_tolerance}, Frequency: {trading_frequency}"
        )
        
        manager = PromptTemplateManager(templates_dir=template_dir)
        builder = PromptBuilder(template_manager=manager)
        
        analysis_result = {
            "analysis_summary": {},
            "technical_indicators": {},
            "statistics": {}
        }
        
        user_preferences = {
            "risk_tolerance": "low",
            "trading_frequency": "high"
        }
        
        prompt = builder.build_algorithm_proposal_prompt(
            analysis_result,
            user_preferences=user_preferences
        )
        
        assert "low" in prompt
        assert "high" in prompt
    
    def test_build_stock_prediction_prompt(self, tmp_path):
        """Test stock prediction prompt building."""
        template_dir = tmp_path / "templates"
        template_dir.mkdir()
        template_file = template_dir / "stock_prediction.txt"
        template_file.write_text(
            "News: {news_summary}, Trends: {market_trends}, Predictions: {num_predictions}"
        )
        
        manager = PromptTemplateManager(templates_dir=template_dir)
        builder = PromptBuilder(template_manager=manager)
        
        prompt = builder.build_stock_prediction_prompt(
            news_summary="Test news",
            market_trends="Test trends",
            num_predictions=3
        )
        
        assert "Test news" in prompt
        assert "Test trends" in prompt
        assert "3" in prompt
    
    def test_format_analysis_summary(self):
        """Test analysis summary formatting."""
        builder = PromptBuilder()
        
        analysis_result = {
            "analysis_summary": {
                "trend_direction": "upward",
                "volatility_level": "high",
                "dominant_patterns": ["pattern1", "pattern2"]
            }
        }
        
        summary = builder._format_analysis_summary(analysis_result)
        
        assert "upward" in summary
        assert "high" in summary
        assert "pattern1" in summary
    
    def test_format_technical_indicators_rsi(self):
        """Test technical indicators formatting with RSI."""
        builder = PromptBuilder()
        
        technical_indicators = {
            "rsi": {
                "value": 65.5,
                "signal": "neutral"
            }
        }
        
        formatted = builder._format_technical_indicators(technical_indicators)
        
        assert "RSI" in formatted
        assert "65.5" in formatted
        assert "neutral" in formatted
    
    def test_format_technical_indicators_macd(self):
        """Test technical indicators formatting with MACD."""
        builder = PromptBuilder()
        
        technical_indicators = {
            "macd": {
                "macd": 1.5,
                "signal": 1.2,
                "histogram": 0.3,
                "signal_type": "bullish"
            }
        }
        
        formatted = builder._format_technical_indicators(technical_indicators)
        
        assert "MACD" in formatted
        assert "1.5" in formatted
        assert "bullish" in formatted
    
    def test_format_technical_indicators_empty(self):
        """Test technical indicators formatting with empty data."""
        builder = PromptBuilder()
        
        technical_indicators = {}
        
        formatted = builder._format_technical_indicators(technical_indicators)
        
        assert "データなし" in formatted

