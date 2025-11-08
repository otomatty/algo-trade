# ニュース収集 データモデル

## Pythonデータクラス

```python
@dataclass
class News:
    id: str
    title: str
    content: str
    source: str
    published_at: str
    sentiment: Optional[str]
```

