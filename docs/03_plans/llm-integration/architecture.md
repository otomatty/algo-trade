# LLM連携 アーキテクチャ設計

## システム構成

```
┌─────────────┐
│  Frontend   │
└──────┬──────┘
       │
       │ invoke('generate_algorithm_proposals')
       ▼
┌─────────────┐
│  Backend    │
│  PyTauri    │
└──────┬──────┘
       │
       │ LLMClient.generate()
       ▼
┌─────────────┐
│  LLM API    │
│ (OpenAI/    │
│  Anthropic) │
└─────────────┘
```

## クラス設計

```python
class LLMClient:
    def __init__(self, provider: str, api_key: str):
        self.provider = provider
        self.client = self._create_client(api_key)
    
    def generate(self, prompt: str) -> str:
        response = self.client.chat.completions.create(...)
        return response.choices[0].message.content
```

