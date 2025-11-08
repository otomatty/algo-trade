# ニュース収集（バックエンド）実装計画

## 概要

市場ニュース、金融情報を自動収集するバックエンド機能の実装計画です。RSSフィード、ニュースAPI等から情報を取得します。

## 関連ドキュメント

- **要件定義**: `docs/01_issues/open/2025_11/20251101_01_trend-association-algorithm-platform.md` (SCREEN-007)
- **依存機能**: 銘柄予測機能 (`docs/03_plans/stock-prediction/`)

## 実装フェーズ

### Phase 1: RSSフィードパーサー

**目標**: RSSフィードからニュースを取得

**タスク**:
- [ ] feedparserライブラリの統合
- [ ] RSSフィードパーサーの実装
- [ ] 複数フィードソースの対応
- [ ] エラーハンドリングの実装

**技術スタック**:
- Python 3.10+
- feedparser
- requests / httpx

**依存関係**:
- なし（最初に実装）

### Phase 2: ニュースAPIクライアント

**目標**: ニュースAPIから情報を取得

**タスク**:
- [ ] 主要ニュースAPIクライアントの実装
  - NewsAPI
  - Alpha Vantage News & Sentiment
  - その他
- [ ] API認証処理の実装
- [ ] レート制限対応の実装

**技術スタック**:
- Python 3.10+
- requests / httpx

**依存関係**:
- Phase 1完了

### Phase 3: Webスクレイピング（オプション）

**目標**: Webサイトからニュースをスクレイピング

**タスク**:
- [ ] BeautifulSoup4の統合
- [ ] 主要ニュースサイトのスクレイパー実装
- [ ] robots.txt遵守の実装
- [ ] レート制限の実装

**技術スタック**:
- Python 3.10+
- BeautifulSoup4
- requests / httpx

**依存関係**:
- Phase 2完了
- 注意: 著作権・利用規約への配慮が必要

### Phase 4: ニュースデータベース保存

**目標**: 収集したニュースをデータベースに保存

**タスク**:
- [ ] ニューステーブルスキーマの設計
- [ ] データベース保存処理の実装
- [ ] 重複チェック機能の実装
- [ ] インデックス最適化

**技術スタック**:
- SQLite
- Python sqlite3

**依存関係**:
- Phase 1完了

### Phase 5: センチメント分析（オプション）

**目標**: ニュースのセンチメント（感情）分析

**タスク**:
- [ ] センチメント分析ライブラリの統合
- [ ] センチメント分析処理の実装
- [ ] 結果のデータベース保存

**技術スタック**:
- TextBlob / VADER Sentiment
- またはLLM APIを使用

**依存関係**:
- Phase 4完了
- 低優先度（将来実装）

### Phase 6: 自動収集スケジューラー

**目標**: 定期的なニュース収集の自動化

**タスク**:
- [ ] スケジューラー実装（APScheduler等）
- [ ] スケジュール設定の保存・読み込み
- [ ] ジョブ管理機能の実装

**技術スタック**:
- APScheduler
- SQLite

**依存関係**:
- Phase 4完了

## 技術的な詳細

### RSSフィードパーサー設計

```python
import feedparser

class RSSFeedParser:
    def __init__(self):
        self.feeds = [
            'https://feeds.finance.yahoo.com/rss/2.0/headline',
            # その他のフィード
        ]
    
    def parse_feeds(self) -> List[News]:
        all_news = []
        for feed_url in self.feeds:
            news = self._parse_feed(feed_url)
            all_news.extend(news)
        return all_news
    
    def _parse_feed(self, feed_url: str) -> List[News]:
        feed = feedparser.parse(feed_url)
        news_list = []
        for entry in feed.entries:
            news = News(
                title=entry.title,
                content=entry.summary,
                url=entry.link,
                published_at=entry.published,
                source=self._extract_source(feed_url)
            )
            news_list.append(news)
        return news_list
```

### ニュースAPIクライアント設計

```python
class NewsAPIClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = 'https://newsapi.org/v2'
    
    def fetch_news(self, keywords: List[str] = None, max_articles: int = 50):
        params = {
            'apiKey': self.api_key,
            'language': 'en',
            'sortBy': 'publishedAt',
            'pageSize': max_articles
        }
        if keywords:
            params['q'] = ' OR '.join(keywords)
        
        response = requests.get(f'{self.base_url}/everything', params=params)
        return self._parse_response(response.json())
```

### データベーススキーマ

```sql
CREATE TABLE market_news (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT,
    source TEXT NOT NULL,
    url TEXT,
    published_at TEXT NOT NULL,
    collected_at TEXT NOT NULL,
    keywords TEXT, -- JSON配列
    sentiment TEXT, -- 'positive' | 'neutral' | 'negative'
    UNIQUE(url) -- 重複防止
);

CREATE INDEX idx_market_news_published_at ON market_news(published_at);
CREATE INDEX idx_market_news_source ON market_news(source);
```

### 重複チェック

```python
def is_duplicate_news(news: News, db_connection) -> bool:
    cursor = db_connection.cursor()
    cursor.execute(
        'SELECT id FROM market_news WHERE url = ?',
        (news.url,)
    )
    return cursor.fetchone() is not None
```

### センチメント分析

```python
from textblob import TextBlob

class SentimentAnalyzer:
    def analyze(self, text: str) -> str:
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        
        if polarity > 0.1:
            return 'positive'
        elif polarity < -0.1:
            return 'negative'
        else:
            return 'neutral'
```

## テスト計画

### 単体テスト

- [ ] RSSフィードパーサーのテスト
- [ ] ニュースAPIクライアントのテスト（モック）
- [ ] センチメント分析のテスト
- [ ] 重複チェックのテスト

### 統合テスト

- [ ] ニュース収集フローの統合テスト
- [ ] データベース保存の統合テスト
- [ ] スケジューラーの統合テスト

## 実装優先度

**最高**: Phase 1, Phase 2, Phase 4（必須機能）
**高**: Phase 6（自動化）
**中**: Phase 3, Phase 5（オプション機能）

## 注意事項

- **著作権・利用規約への配慮**: Webスクレイピングは利用規約を確認
- **robots.txt遵守**: スクレイピング時はrobots.txtを確認
- **レート制限**: APIやWebサイトへの過度なアクセスを避ける
- **データの信頼性**: ニュースソースの信頼性を考慮
- **エラーハンドリング**: ネットワークエラー、APIエラーへの対応
- **重複防止**: 同じニュースの重複収集を防ぐ
- **パフォーマンス**: 大量のニュース収集時のパフォーマンス最適化

