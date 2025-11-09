"""
Prediction generator for stock predictions.

Related Documentation:
  ├─ Plan: docs/03_plans/stock-prediction/README.md
  └─ LLM Integration: docs/03_plans/llm-integration/README.md

DEPENDENCY MAP:

Parents (Files that import this file):
  └─ src-python/modules/stock_prediction/job_manager.py (future)

Dependencies (External files that this file imports):
  ├─ typing (standard library)
  ├─ logging (standard library)
  ├─ uuid (standard library)
  ├─ src-python/modules/llm_integration.api_key_manager
  ├─ src-python/modules/llm_integration.openai_client
  ├─ src-python/modules/llm_integration.anthropic_client
  ├─ src-python/modules/llm_integration.prompt_builder
  ├─ src-python/modules/llm_integration.fallback_handler
  └─ src-python/modules/llm_integration.exceptions
"""
import logging
import uuid
from typing import Dict, Any, List, Optional

from modules.llm_integration.api_key_manager import APIKeyManager
from modules.llm_integration.openai_client import OpenAIClient
from modules.llm_integration.anthropic_client import AnthropicClient
from modules.llm_integration.prompt_builder import PromptBuilder
from modules.llm_integration.fallback_handler import FallbackHandler
from modules.llm_integration.exceptions import LLMError, ParseError


logger = logging.getLogger(__name__)


class PredictionGenerator:
    """Generates stock predictions using LLM."""
    
    def __init__(
        self,
        llm_provider: str = "openai",
        model: Optional[str] = None,
        api_key_manager: Optional[APIKeyManager] = None
    ):
        """
        Initialize prediction generator.
        
        Args:
            llm_provider: LLM provider name ("openai" or "anthropic")
            model: Model name (optional, uses default if not provided)
            api_key_manager: API key manager instance (optional)
        """
        self.api_key_manager = api_key_manager or APIKeyManager()
        self.llm_provider = llm_provider
        self.model = model
        self.llm_client = self._create_llm_client()
        self.prompt_builder = PromptBuilder()
        self.fallback_handler = FallbackHandler()
    
    def _create_llm_client(self):
        """Create LLM client based on provider."""
        if self.llm_provider == "openai":
            api_key = self.api_key_manager.get_openai_api_key()
            return OpenAIClient(api_key=api_key)
        elif self.llm_provider == "anthropic":
            api_key = self.api_key_manager.get_anthropic_api_key()
            return AnthropicClient(api_key=api_key)
        else:
            raise LLMError(f"Unknown LLM provider: {self.llm_provider}")
    
    def _format_news_summary(self, news_list: List[Dict[str, Any]], max_items: int = 20) -> str:
        """
        Format news list into summary string.
        
        Args:
            news_list: List of news dictionaries
            max_items: Maximum number of news items to include
            
        Returns:
            Formatted news summary string
        """
        if not news_list:
            return "ニュース情報なし"
        
        items = news_list[:max_items]
        lines = []
        
        for i, news in enumerate(items, 1):
            title = news.get('title', 'タイトルなし')
            source = news.get('source', '不明')
            published_at = news.get('published_at', '')
            content = news.get('content', '')
            
            # Truncate content if too long
            if content and len(content) > 200:
                content = content[:200] + "..."
            
            lines.append(f"{i}. [{source}] {title}")
            if published_at:
                lines.append(f"   公開日時: {published_at}")
            if content:
                lines.append(f"   内容: {content}")
            lines.append("")
        
        if len(news_list) > max_items:
            lines.append(f"... 他 {len(news_list) - max_items}件のニュース")
        
        return "\n".join(lines)
    
    def generate_predictions(
        self,
        news_list: List[Dict[str, Any]],
        market_trends: Optional[str] = None,
        user_preferences: Optional[Dict[str, Any]] = None,
        num_predictions: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Generate stock predictions based on news and market trends.
        
        Args:
            news_list: List of news dictionaries
            market_trends: Market trends information (optional)
            user_preferences: User preferences dictionary (optional)
            num_predictions: Number of predictions to generate (default: 5)
            
        Returns:
            List of prediction dictionaries
            
        Raises:
            LLMError: If LLM API call fails
            ParseError: If response parsing fails
        """
        try:
            # Format news summary
            news_summary = self._format_news_summary(news_list)
            
            # Default market trends if not provided
            if not market_trends:
                market_trends = "市場トレンド情報なし"
            
            # Build prompt
            prompt = self.prompt_builder.build_stock_prediction_prompt(
                news_summary=news_summary,
                market_trends=market_trends,
                user_preferences=user_preferences,
                num_predictions=num_predictions
            )
            
            logger.info(f"Generating {num_predictions} stock predictions using {self.llm_provider}")
            
            # Call LLM API
            response_text = self.llm_client.generate(
                prompt,
                model=self.model,
                temperature=0.7,
                max_tokens=2000
            )
            
            # Parse response with fallback
            predictions = self.fallback_handler.parse_with_fallback(
                response_text,
                "stock_prediction"
            )
            
            # Ensure predictions is a list
            if not isinstance(predictions, list):
                if isinstance(predictions, dict) and 'predictions' in predictions:
                    predictions = predictions['predictions']
                else:
                    predictions = [predictions] if predictions else []
            
            # Add prediction IDs and ensure required fields
            for prediction in predictions:
                if 'prediction_id' not in prediction:
                    prediction['prediction_id'] = str(uuid.uuid4())
                
                # Ensure recommended_action maps to suggested_action for compatibility
                if 'recommended_action' in prediction and 'suggested_action' not in prediction:
                    action = prediction['recommended_action']
                    # Map 'hold' to 'watch' if needed, or keep as is
                    prediction['suggested_action'] = action if action != 'hold' else 'watch'
                
                # Ensure association_chain exists
                if 'association_chain' not in prediction:
                    prediction['association_chain'] = []
                
                # Ensure reasoning exists (use rationale if available)
                if 'reasoning' not in prediction and 'rationale' in prediction:
                    prediction['reasoning'] = prediction['rationale']
            
            logger.info(f"Generated {len(predictions)} stock predictions")
            return predictions
            
        except LLMError as e:
            logger.error(f"LLM API error: {e}")
            raise
        except ParseError as e:
            logger.error(f"Parse error: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in prediction generation: {e}")
            raise LLMError(f"Failed to generate predictions: {e}") from e

