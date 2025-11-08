"""
Unit tests for response parser and schemas.

Related Documentation:
  ├─ Plan: docs/03_plans/llm-integration/README.md
  └─ Tests: src-python/tests/unit/test_response_parser.py, test_schemas.py
"""
import pytest
import sys
from pathlib import Path
from pydantic import ValidationError

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from modules.llm_integration.response_parser import ResponseParser
from modules.llm_integration.fallback_handler import FallbackHandler
from modules.llm_integration.schemas import (
    AlgorithmProposalResponse,
    StockPredictionResponse,
    AlgorithmProposal,
    StockPrediction,
    TriggerDefinition,
    ActionDefinition,
    AlgorithmDefinition,
)
from modules.llm_integration.exceptions import ParseError


@pytest.mark.unit
class TestResponseParser:
    """Test cases for ResponseParser."""
    
    def test_parse_algorithm_proposals_success(self):
        """Test successful algorithm proposal parsing."""
        parser = ResponseParser()
        
        response_text = """{
  "proposals": [
    {
      "name": "Test Algorithm",
      "description": "Test description",
      "rationale": "Test rationale",
      "definition": {
        "triggers": [
          {
            "type": "rsi",
            "condition": {
              "operator": "lt",
              "value": 30
            }
          }
        ],
        "actions": [
          {
            "type": "buy",
            "parameters": {}
          }
        ]
      },
      "confidence_score": 0.8
    }
  ]
}"""
        
        proposals = parser.parse_algorithm_proposals(response_text)
        
        assert len(proposals) == 1
        assert proposals[0]["name"] == "Test Algorithm"
        assert proposals[0]["confidence_score"] == 0.8
    
    def test_parse_algorithm_proposals_markdown(self):
        """Test parsing from markdown code block."""
        parser = ResponseParser()
        
        response_text = """Here is the response:
```json
{
  "proposals": [
    {
      "name": "Test Algorithm",
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
        
        proposals = parser.parse_algorithm_proposals(response_text)
        assert len(proposals) == 1
    
    def test_parse_algorithm_proposals_invalid_json(self):
        """Test parsing with invalid JSON."""
        parser = ResponseParser()
        
        response_text = "This is not JSON"
        
        with pytest.raises(ParseError):
            parser.parse_algorithm_proposals(response_text)
    
    def test_parse_stock_predictions_success(self):
        """Test successful stock prediction parsing."""
        parser = ResponseParser()
        
        response_text = """{
  "predictions": [
    {
      "symbol": "7203",
      "name": "トヨタ自動車",
      "rationale": "Test rationale",
      "predicted_direction": "up",
      "predicted_change_percent": 5.5,
      "confidence_score": 0.75,
      "recommended_action": "buy",
      "risk_factors": []
    }
  ]
}"""
        
        predictions = parser.parse_stock_predictions(response_text)
        
        assert len(predictions) == 1
        assert predictions[0]["symbol"] == "7203"
        assert predictions[0]["predicted_direction"] == "up"
    
    def test_parse_json_markdown_code_block(self):
        """Test JSON extraction from markdown code block."""
        parser = ResponseParser()
        
        text = """Some text before
```json
{"key": "value"}
```
Some text after"""
        
        result = parser._parse_json(text)
        assert result == {"key": "value"}
    
    def test_validate_proposal_missing_field(self):
        """Test proposal validation with missing field."""
        parser = ResponseParser()
        
        proposal = {
            "name": "Test",
            "description": "Test",
            # Missing rationale
            "definition": {
                "triggers": [],
                "actions": []
            }
        }
        
        with pytest.raises(ParseError):
            parser._validate_proposal(proposal)
    
    def test_validate_proposal_invalid_confidence(self):
        """Test proposal validation with invalid confidence score."""
        parser = ResponseParser()
        
        proposal = {
            "name": "Test",
            "description": "Test",
            "rationale": "Test",
            "definition": {
                "triggers": [],
                "actions": []
            },
            "confidence_score": 1.5  # Invalid: > 1.0
        }
        
        with pytest.raises(ParseError):
            parser._validate_proposal(proposal)


@pytest.mark.unit
class TestFallbackHandler:
    """Test cases for FallbackHandler."""
    
    def test_parse_with_fallback_success(self):
        """Test successful parsing without fallback."""
        handler = FallbackHandler()
        
        response_text = """{
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
}"""
        
        proposals = handler.parse_with_fallback(response_text, "algorithm_proposal")
        assert len(proposals) == 1
    
    def test_parse_with_fallback_markdown(self):
        """Test parsing with markdown fallback."""
        handler = FallbackHandler()
        
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
    
    def test_clean_response_text(self):
        """Test response text cleaning."""
        handler = FallbackHandler()
        
        text = """```json
{"key": "value"}
```"""
        
        cleaned = handler._clean_response_text(text)
        assert "```" not in cleaned
        assert "json" not in cleaned.lower()


@pytest.mark.unit
class TestSchemas:
    """Test cases for Pydantic schemas."""
    
    def test_algorithm_proposal_schema(self):
        """Test AlgorithmProposal schema validation."""
        proposal = AlgorithmProposal(
            name="Test Algorithm",
            description="Test description",
            rationale="Test rationale",
            definition=AlgorithmDefinition(
                triggers=[],
                actions=[]
            ),
            confidence_score=0.8
        )
        
        assert proposal.name == "Test Algorithm"
        assert proposal.confidence_score == 0.8
    
    def test_algorithm_proposal_invalid_confidence(self):
        """Test AlgorithmProposal with invalid confidence score."""
        with pytest.raises(ValidationError):
            AlgorithmProposal(
                name="Test",
                description="Test",
                rationale="Test",
                definition=AlgorithmDefinition(
                    triggers=[],
                    actions=[]
                ),
                confidence_score=1.5  # Invalid: > 1.0
            )
    
    def test_stock_prediction_schema(self):
        """Test StockPrediction schema validation."""
        prediction = StockPrediction(
            symbol="7203",
            name="トヨタ自動車",
            rationale="Test rationale",
            predicted_direction="up",
            predicted_change_percent=5.5,
            confidence_score=0.75,
            recommended_action="buy"
        )
        
        assert prediction.symbol == "7203"
        assert prediction.predicted_direction == "up"
    
    def test_trigger_definition_schema(self):
        """Test TriggerDefinition schema validation."""
        trigger = TriggerDefinition(
            type="rsi",
            condition={
                "operator": "lt",
                "value": 30
            }
        )
        
        assert trigger.type == "rsi"
        assert trigger.condition.operator == "lt"

