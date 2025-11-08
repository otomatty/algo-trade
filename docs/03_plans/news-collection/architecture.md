# ニュース収集 アーキテクチャ設計

## システム構成

```
┌─────────────┐
│  Frontend   │
└──────┬──────┘
       │
       │ invoke('collect_market_news')
       ▼
┌─────────────┐
│  Backend    │
│  News       │
│  Collector  │
└──────┬──────┘
       │
       ├─→ RSS Feed Parser
       ├─→ News API Client
       └─→ Web Scraper
       │
       ▼
┌─────────────┐
│  SQLite DB  │
│  market_news│
└─────────────┘
```

