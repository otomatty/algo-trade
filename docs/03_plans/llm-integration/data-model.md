# LLM連携 データモデル

## リクエスト/レスポンス

```python
@dataclass
class LLMRequest:
    prompt: str
    max_tokens: int = 2000
    temperature: float = 0.7

@dataclass
class LLMResponse:
    content: str
    usage: TokenUsage

@dataclass
class TokenUsage:
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
```

