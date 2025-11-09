"""
Pydantic schemas for LLM integration.

Related Documentation:
  ├─ Plan: docs/03_plans/llm-integration/README.md
  ├─ Data Model: docs/03_plans/llm-integration/data-model.md
  └─ Types: src/types/algorithm.ts, src/types/stock-prediction.ts

DEPENDENCY MAP:

Parents (Files that import this file):
  ├─ src-python/modules/llm_integration/response_parser.py
  └─ src-python/modules/llm_integration/fallback_handler.py

Dependencies (External files that this file imports):
  ├─ typing (standard library)
  ├─ pydantic (external)
"""
from typing import List, Optional, Union, Literal
from pydantic import BaseModel, Field, field_validator


class TokenUsage(BaseModel):
    """Token usage information."""
    prompt_tokens: int = Field(ge=0, description="Number of prompt tokens")
    completion_tokens: int = Field(ge=0, description="Number of completion tokens")
    total_tokens: int = Field(ge=0, description="Total number of tokens")


class LLMRequest(BaseModel):
    """LLM request model."""
    prompt: str = Field(description="Input prompt text")
    max_tokens: int = Field(default=2000, ge=1, description="Maximum tokens to generate")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0, description="Sampling temperature")


class LLMResponse(BaseModel):
    """LLM response model."""
    content: str = Field(description="Generated content")
    usage: Optional[TokenUsage] = Field(default=None, description="Token usage information")


# Algorithm Proposal Schemas

class TriggerCondition(BaseModel):
    """Trigger condition definition."""
    operator: Literal["gt", "lt", "gte", "lte", "eq", "between", "cross_above", "cross_below"] = Field(
        description="Comparison operator"
    )
    value: Union[float, List[float]] = Field(description="Comparison value or range")
    period: Optional[int] = Field(default=None, ge=1, description="Period for moving averages")
    indicator: Optional[str] = Field(default=None, description="Indicator name")


class TriggerDefinition(BaseModel):
    """Trigger definition."""
    type: str = Field(description="Trigger type (rsi, macd, price, volume, moving_average)")
    condition: TriggerCondition = Field(description="Trigger condition")
    logical_operator: Optional[Literal["AND", "OR"]] = Field(
        default=None, description="Logical operator for multiple triggers"
    )


class ActionParameters(BaseModel):
    """Action parameters."""
    quantity: Optional[float] = Field(default=None, ge=0, description="Quantity to trade")
    percentage: Optional[float] = Field(default=None, ge=0, le=100, description="Percentage of portfolio")
    stop_loss: Optional[float] = Field(default=None, ge=0, description="Stop loss percentage")
    take_profit: Optional[float] = Field(default=None, ge=0, description="Take profit percentage")
    limit_price: Optional[float] = Field(default=None, ge=0, description="Limit price")


class ActionDefinition(BaseModel):
    """Action definition."""
    type: Literal["buy", "sell", "hold"] = Field(description="Action type")
    parameters: ActionParameters = Field(description="Action parameters")
    execution_type: Optional[Literal["market", "limit", "stop"]] = Field(
        default="market", description="Execution type"
    )


class AlgorithmDefinition(BaseModel):
    """Algorithm definition."""
    triggers: List[TriggerDefinition] = Field(description="List of trigger definitions")
    actions: List[ActionDefinition] = Field(description="List of action definitions")


class ExpectedPerformance(BaseModel):
    """Expected performance information."""
    expected_return: Optional[float] = Field(default=None, description="Expected return percentage")
    risk_level: Optional[Literal["low", "medium", "high"]] = Field(
        default=None, description="Risk level"
    )


class AlgorithmProposal(BaseModel):
    """Algorithm proposal."""
    name: str = Field(description="Algorithm name")
    description: str = Field(description="Algorithm description")
    rationale: str = Field(description="Proposal rationale")
    expected_performance: Optional[ExpectedPerformance] = Field(
        default=None, description="Expected performance"
    )
    definition: AlgorithmDefinition = Field(description="Algorithm definition")
    confidence_score: float = Field(ge=0.0, le=1.0, description="Confidence score")


class AlgorithmProposalResponse(BaseModel):
    """Algorithm proposal response."""
    proposals: List[AlgorithmProposal] = Field(description="List of algorithm proposals")


# Stock Prediction Schemas

class AssociationStep(BaseModel):
    """Association step in prediction chain."""
    step: int = Field(ge=1, description="Step number")
    concept: str = Field(description="Concept or idea")
    connection: str = Field(description="Connection to next step")


class StockPrediction(BaseModel):
    """Stock prediction."""
    symbol: str = Field(description="Stock symbol code")
    name: str = Field(description="Stock name")
    rationale: str = Field(description="Prediction rationale")
    predicted_direction: Literal["up", "down", "sideways"] = Field(
        description="Predicted price direction"
    )
    predicted_change_percent: float = Field(description="Predicted price change percentage")
    confidence_score: float = Field(ge=0.0, le=1.0, description="Confidence score")
    recommended_action: Literal["buy", "sell", "hold", "watch"] = Field(description="Recommended action")
    risk_factors: List[str] = Field(default_factory=list, description="List of risk factors")
    time_horizon: Optional[Literal["短期", "中期", "長期"]] = Field(
        default=None, description="Time horizon"
    )
    association_chain: Optional[List[AssociationStep]] = Field(
        default_factory=list, description="Association chain steps"
    )


class StockPredictionResponse(BaseModel):
    """Stock prediction response."""
    predictions: List[StockPrediction] = Field(description="List of stock predictions")

