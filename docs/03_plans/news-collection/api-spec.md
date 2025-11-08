# ニュース収集 API仕様

## 内部API

ニュース収集は主にバックエンド内部で使用されます。

### RSSFeedParser

```python
class RSSFeedParser:
    def parse_feeds(self) -> List[News]:
        pass
```

### NewsAPIClient

```python
class NewsAPIClient:
    def fetch_news(self, keywords: List[str] = None) -> List[News]:
        pass
```

