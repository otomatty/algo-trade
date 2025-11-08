"""
Prompt builder for LLM integration.

Related Documentation:
  ├─ Plan: docs/03_plans/llm-integration/README.md
  ├─ Prompt Design: docs/03_plans/algorithm-proposal/llm-prompt-design.md
  └─ Types: src/types/analysis.ts

DEPENDENCY MAP:

Parents (Files that import this file):
  └─ src-python/modules/llm_integration/__init__.py (future)

Dependencies (External files that this file imports):
  ├─ typing (standard library)
  ├─ logging (standard library)
  ├─ src-python/modules/llm_integration/prompt_templates.py
  └─ src-python/modules/llm_integration/exceptions.py
"""
import logging
from typing import Dict, Any, Optional, List

from .prompt_templates import PromptTemplateManager
from .exceptions import LLMError


logger = logging.getLogger(__name__)


class PromptBuilder:
    """Builds prompts for LLM integration."""
    
    def __init__(self, template_manager: Optional[PromptTemplateManager] = None):
        """
        Initialize prompt builder.
        
        Args:
            template_manager: Prompt template manager (optional, creates new if not provided)
        """
        self.template_manager = template_manager or PromptTemplateManager()
    
    def build_algorithm_proposal_prompt(
        self,
        analysis_result: Dict[str, Any],
        user_preferences: Optional[Dict[str, Any]] = None,
        num_proposals: int = 5
    ) -> str:
        """
        Build prompt for algorithm proposal generation.
        
        Args:
            analysis_result: Analysis result dictionary (from AnalysisResult type)
            user_preferences: User preferences dictionary (optional)
            num_proposals: Number of proposals to generate (default: 5)
            
        Returns:
            Formatted prompt string
            
        Raises:
            LLMError: If prompt building fails
        """
        user_prefs = user_preferences or {}
        
        # Format analysis summary
        analysis_summary = self._format_analysis_summary(analysis_result)
        
        # Format technical indicators
        technical_summary = self._format_technical_indicators(
            analysis_result.get("technical_indicators", {})
        )
        
        # Extract analysis summary data
        analysis_summary_data = analysis_result.get("analysis_summary", {})
        trend_direction = analysis_summary_data.get("trend_direction", "sideways")
        volatility_level = analysis_summary_data.get("volatility_level", "medium")
        dominant_patterns = analysis_summary_data.get("dominant_patterns", [])
        
        # Extract statistics
        statistics = analysis_result.get("statistics", {})
        price_range = statistics.get("price_range", {})
        price_min = price_range.get("min", 0)
        price_max = price_range.get("max", 0)
        current_price = price_range.get("current", 0)
        price_change_percent = statistics.get("price_change_percent", 0)
        volume_average = statistics.get("volume_average", 0)
        
        # Extract user preferences
        risk_tolerance = user_prefs.get("risk_tolerance", "medium")
        trading_frequency = user_prefs.get("trading_frequency", "medium")
        preferred_indicators = user_prefs.get("preferred_indicators", [])
        preferred_indicators_str = ", ".join(preferred_indicators) if preferred_indicators else "なし"
        
        try:
            prompt = self.template_manager.render_template(
                "algorithm_proposal",
                analysis_results_summary=analysis_summary,
                trend_direction=trend_direction,
                volatility_level=volatility_level,
                dominant_patterns=", ".join(dominant_patterns) if dominant_patterns else "なし",
                technical_indicators_summary=technical_summary,
                price_min=price_min,
                price_max=price_max,
                current_price=current_price,
                price_change_percent=price_change_percent,
                volume_average=volume_average,
                risk_tolerance=risk_tolerance,
                trading_frequency=trading_frequency,
                preferred_indicators=preferred_indicators_str,
                num_proposals=num_proposals
            )
            
            logger.debug(f"Built algorithm proposal prompt ({len(prompt)} characters)")
            return prompt
            
        except Exception as e:
            raise LLMError(f"Failed to build algorithm proposal prompt: {e}") from e
    
    def build_stock_prediction_prompt(
        self,
        news_summary: str,
        market_trends: str,
        user_preferences: Optional[Dict[str, Any]] = None,
        num_predictions: int = 5
    ) -> str:
        """
        Build prompt for stock prediction generation.
        
        Args:
            news_summary: Summary of news articles
            market_trends: Market trends information
            user_preferences: User preferences dictionary (optional)
            num_predictions: Number of predictions to generate (default: 5)
            
        Returns:
            Formatted prompt string
            
        Raises:
            LLMError: If prompt building fails
        """
        user_prefs = user_preferences or {}
        
        risk_tolerance = user_prefs.get("risk_tolerance", "medium")
        investment_horizon = user_prefs.get("investment_horizon", "medium")
        investment_style = user_prefs.get("investment_style", "balanced")
        
        try:
            prompt = self.template_manager.render_template(
                "stock_prediction",
                news_summary=news_summary,
                market_trends=market_trends,
                risk_tolerance=risk_tolerance,
                investment_horizon=investment_horizon,
                investment_style=investment_style,
                num_predictions=num_predictions
            )
            
            logger.debug(f"Built stock prediction prompt ({len(prompt)} characters)")
            return prompt
            
        except Exception as e:
            raise LLMError(f"Failed to build stock prediction prompt: {e}") from e
    
    def _format_analysis_summary(self, analysis_result: Dict[str, Any]) -> str:
        """
        Format analysis summary for prompt.
        
        Args:
            analysis_result: Analysis result dictionary
            
        Returns:
            Formatted summary string
        """
        analysis_summary = analysis_result.get("analysis_summary", {})
        trend_direction = analysis_summary.get("trend_direction", "sideways")
        volatility_level = analysis_summary.get("volatility_level", "medium")
        dominant_patterns = analysis_summary.get("dominant_patterns", [])
        
        patterns_str = ", ".join(dominant_patterns) if dominant_patterns else "なし"
        
        return f"""トレンド方向: {trend_direction}
ボラティリティレベル: {volatility_level}
主要パターン: {patterns_str}"""
    
    def _format_technical_indicators(self, technical_indicators: Dict[str, Any]) -> str:
        """
        Format technical indicators for prompt.
        
        Args:
            technical_indicators: Technical indicators dictionary
            
        Returns:
            Formatted indicators string
        """
        lines = []
        
        # RSI
        if "rsi" in technical_indicators:
            rsi = technical_indicators["rsi"]
            value = rsi.get("value", 0)
            signal = rsi.get("signal", "neutral")
            lines.append(f"RSI: {value:.2f} (シグナル: {signal})")
        
        # MACD
        if "macd" in technical_indicators:
            macd = technical_indicators["macd"]
            macd_value = macd.get("macd", 0)
            signal_line = macd.get("signal", 0)
            histogram = macd.get("histogram", 0)
            signal_type = macd.get("signal_type", "neutral")
            lines.append(f"MACD: {macd_value:.2f} (シグナルライン: {signal_line:.2f}, ヒストグラム: {histogram:.2f}, トレンド: {signal_type})")
        
        # SMA
        if "sma" in technical_indicators:
            sma_list = technical_indicators["sma"]
            if isinstance(sma_list, list):
                sma_strs = [f"SMA({sma.get('period', 0)}): {sma.get('value', 0):.2f}" for sma in sma_list]
                lines.extend(sma_strs)
        
        # EMA
        if "ema" in technical_indicators:
            ema_list = technical_indicators["ema"]
            if isinstance(ema_list, list):
                ema_strs = [f"EMA({ema.get('period', 0)}): {ema.get('value', 0):.2f}" for ema in ema_list]
                lines.extend(ema_strs)
        
        # Bollinger Bands
        if "bollinger_bands" in technical_indicators:
            bb = technical_indicators["bollinger_bands"]
            upper = bb.get("upper", 0)
            middle = bb.get("middle", 0)
            lower = bb.get("lower", 0)
            lines.append(f"ボリンジャーバンド: 上限={upper:.2f}, 中央={middle:.2f}, 下限={lower:.2f}")
        
        return "\n".join(lines) if lines else "テクニカル指標データなし"

