"""
Fallback handler for LLM response parsing.

Related Documentation:
  ├─ Plan: docs/03_plans/llm-integration/README.md
  └─ Data Model: docs/03_plans/llm-integration/data-model.md

DEPENDENCY MAP:

Parents (Files that import this file):
  └─ src-python/modules/llm_integration/__init__.py (future)

Dependencies (External files that this file imports):
  ├─ logging (standard library)
  ├─ typing (standard library)
  ├─ src-python/modules/llm_integration/response_parser.py
  └─ src-python/modules/llm_integration/exceptions.py
"""
import logging
import re
from typing import Dict, Any, List, Optional

from .response_parser import ResponseParser
from .exceptions import ParseError


logger = logging.getLogger(__name__)


class FallbackHandler:
    """Handles fallback scenarios for LLM response parsing."""
    
    def __init__(self, parser: Optional[ResponseParser] = None):
        """
        Initialize fallback handler.
        
        Args:
            parser: Response parser instance (optional, creates new if not provided)
        """
        self.parser = parser or ResponseParser()
    
    def parse_with_fallback(
        self,
        response_text: str,
        response_type: str = "algorithm_proposal"
    ) -> List[Dict[str, Any]]:
        """
        Parse response with fallback handling.
        
        Args:
            response_text: Raw response text from LLM
            response_type: Type of response ("algorithm_proposal" or "stock_prediction")
            
        Returns:
            Parsed response data
            
        Raises:
            ParseError: If all parsing attempts fail
        """
        # Try normal parsing first
        try:
            if response_type == "algorithm_proposal":
                return self.parser.parse_algorithm_proposals(response_text)
            elif response_type == "stock_prediction":
                return self.parser.parse_stock_predictions(response_text)
            else:
                raise ParseError(f"Unknown response type: {response_type}")
        except ParseError as e:
            logger.warning(f"Initial parse failed: {e}. Attempting fallback...")
        
        # Try fallback methods
        try:
            cleaned_text = self._clean_response_text(response_text)
            if response_type == "algorithm_proposal":
                return self.parser.parse_algorithm_proposals(cleaned_text)
            elif response_type == "stock_prediction":
                return self.parser.parse_stock_predictions(cleaned_text)
        except ParseError as e:
            logger.warning(f"Fallback parse failed: {e}")
        
        # Try partial extraction
        try:
            return self._extract_partial_data(response_text, response_type)
        except Exception as e:
            logger.error(f"Partial extraction failed: {e}")
            raise ParseError(f"All parsing attempts failed. Last error: {e}") from e
    
    def _clean_response_text(self, text: str) -> str:
        """
        Clean response text for parsing.
        
        Args:
            text: Raw response text
            
        Returns:
            Cleaned text
        """
        # Remove markdown formatting
        text = re.sub(r'```json\s*', '', text)
        text = re.sub(r'```\s*', '', text)
        
        # Remove leading/trailing whitespace
        text = text.strip()
        
        # Remove common prefixes/suffixes
        text = re.sub(r'^Here is.*?:\s*', '', text, flags=re.IGNORECASE)
        text = re.sub(r'\s*Note:.*$', '', text, flags=re.IGNORECASE | re.DOTALL)
        
        return text
    
    def _extract_partial_data(
        self,
        text: str,
        response_type: str
    ) -> List[Dict[str, Any]]:
        """
        Extract partial data from malformed response.
        
        Args:
            text: Response text
            response_type: Type of response
            
        Returns:
            List of partial data dictionaries
            
        Raises:
            ParseError: If extraction fails
        """
        results = []
        
        if response_type == "algorithm_proposal":
            # Try to extract proposal-like structures
            proposal_pattern = r'"name"\s*:\s*"([^"]+)"'
            names = re.findall(proposal_pattern, text)
            
            if not names:
                raise ParseError("Could not extract any proposal data")
            
            # Create minimal proposal structures
            for i, name in enumerate(names):
                proposal = {
                    "name": name,
                    "description": f"Proposal {i+1}",
                    "rationale": "Extracted from partial response",
                    "definition": {
                        "triggers": [],
                        "actions": []
                    },
                    "confidence_score": 0.5
                }
                results.append(proposal)
        
        elif response_type == "stock_prediction":
            # Try to extract prediction-like structures
            symbol_pattern = r'"symbol"\s*:\s*"([^"]+)"'
            symbols = re.findall(symbol_pattern, text)
            
            if not symbols:
                raise ParseError("Could not extract any prediction data")
            
            # Create minimal prediction structures
            for i, symbol in enumerate(symbols):
                prediction = {
                    "symbol": symbol,
                    "name": f"Stock {i+1}",
                    "rationale": "Extracted from partial response",
                    "predicted_direction": "sideways",
                    "predicted_change_percent": 0.0,
                    "confidence_score": 0.5,
                    "recommended_action": "hold",
                    "risk_factors": []
                }
                results.append(prediction)
        
        if not results:
            raise ParseError("Could not extract any data from response")
        
        logger.warning(f"Extracted {len(results)} partial {response_type} entries")
        return results

