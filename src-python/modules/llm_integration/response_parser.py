"""
Response parser for LLM integration.

Related Documentation:
  ├─ Plan: docs/03_plans/llm-integration/README.md
  └─ Data Model: docs/03_plans/llm-integration/data-model.md

DEPENDENCY MAP:

Parents (Files that import this file):
  └─ src-python/modules/llm_integration/fallback_handler.py

Dependencies (External files that this file imports):
  ├─ json (standard library)
  ├─ logging (standard library)
  ├─ typing (standard library)
  ├─ pydantic (external)
  ├─ src-python/modules/llm_integration/schemas.py
  └─ src-python/modules/llm_integration/exceptions.py
"""
import json
import logging
from typing import Dict, Any, List, Type, TypeVar

from pydantic import ValidationError

from .schemas import (
    AlgorithmProposalResponse,
    StockPredictionResponse,
    AlgorithmProposal,
    StockPrediction,
)
from .exceptions import ParseError


logger = logging.getLogger(__name__)

T = TypeVar('T')


class ResponseParser:
    """Parser for LLM responses."""
    
    def parse_algorithm_proposals(self, response_text: str) -> List[Dict[str, Any]]:
        """
        Parse algorithm proposal response from LLM.
        
        Args:
            response_text: Raw response text from LLM
            
        Returns:
            List of algorithm proposal dictionaries
            
        Raises:
            ParseError: If parsing fails
        """
        try:
            # Parse JSON
            data = self._parse_json(response_text)
            
            # Validate schema
            validated = AlgorithmProposalResponse(**data)
            
            # Convert to dictionaries
            proposals = [proposal.model_dump() for proposal in validated.proposals]
            
            # Validate each proposal
            for proposal in proposals:
                self._validate_proposal(proposal)
            
            logger.debug(f"Parsed {len(proposals)} algorithm proposals")
            return proposals
            
        except json.JSONDecodeError as e:
            raise ParseError(f"Invalid JSON in response: {e}") from e
        except ValidationError as e:
            raise ParseError(f"Schema validation failed: {e}") from e
        except Exception as e:
            raise ParseError(f"Failed to parse algorithm proposals: {e}") from e
    
    def parse_stock_predictions(self, response_text: str) -> List[Dict[str, Any]]:
        """
        Parse stock prediction response from LLM.
        
        Args:
            response_text: Raw response text from LLM
            
        Returns:
            List of stock prediction dictionaries
            
        Raises:
            ParseError: If parsing fails
        """
        try:
            # Parse JSON
            data = self._parse_json(response_text)
            
            # Validate schema
            validated = StockPredictionResponse(**data)
            
            # Convert to dictionaries
            predictions = [prediction.model_dump() for prediction in validated.predictions]
            
            logger.debug(f"Parsed {len(predictions)} stock predictions")
            return predictions
            
        except json.JSONDecodeError as e:
            raise ParseError(f"Invalid JSON in response: {e}") from e
        except ValidationError as e:
            raise ParseError(f"Schema validation failed: {e}") from e
        except Exception as e:
            raise ParseError(f"Failed to parse stock predictions: {e}") from e
    
    def _parse_json(self, text: str) -> Dict[str, Any]:
        """
        Parse JSON from text, handling markdown code blocks.
        
        Args:
            text: Text containing JSON
            
        Returns:
            Parsed JSON dictionary
            
        Raises:
            json.JSONDecodeError: If JSON parsing fails
        """
        # Try direct JSON parse first
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass
        
        # Try to extract JSON from markdown code blocks
        import re
        
        # Look for JSON code blocks
        json_pattern = r'```(?:json)?\s*(\{.*?\})\s*```'
        matches = re.findall(json_pattern, text, re.DOTALL)
        
        if matches:
            # Try to parse the first match
            for match in matches:
                try:
                    return json.loads(match)
                except json.JSONDecodeError:
                    continue
        
        # Try to find JSON object in text
        json_obj_pattern = r'\{.*\}'
        matches = re.findall(json_obj_pattern, text, re.DOTALL)
        
        if matches:
            # Try to parse the longest match (likely the main JSON)
            matches.sort(key=len, reverse=True)
            for match in matches:
                try:
                    return json.loads(match)
                except json.JSONDecodeError:
                    continue
        
        # If all else fails, raise error
        raise json.JSONDecodeError("No valid JSON found in response", text, 0)
    
    def _validate_proposal(self, proposal: Dict[str, Any]) -> None:
        """
        Validate algorithm proposal structure.
        
        Args:
            proposal: Proposal dictionary
            
        Raises:
            ParseError: If validation fails
        """
        # Check required fields
        required_fields = ["name", "description", "rationale", "definition"]
        for field in required_fields:
            if field not in proposal:
                raise ParseError(f"Missing required field in proposal: {field}")
        
        # Validate definition structure
        definition = proposal.get("definition", {})
        if not isinstance(definition, dict):
            raise ParseError("Invalid definition structure")
        
        if "triggers" not in definition or not isinstance(definition["triggers"], list):
            raise ParseError("Invalid triggers structure")
        
        if "actions" not in definition or not isinstance(definition["actions"], list):
            raise ParseError("Invalid actions structure")
        
        # Validate confidence score range
        confidence_score = proposal.get("confidence_score")
        if confidence_score is not None:
            if not isinstance(confidence_score, (int, float)):
                raise ParseError("Invalid confidence_score type")
            if not (0.0 <= confidence_score <= 1.0):
                raise ParseError(f"Invalid confidence_score range: {confidence_score}")

