# 銘柄予測機能 API仕様書

## Tauriコマンド一覧

### `collect_market_news`

市場ニュースを収集します。

#### リクエスト

```typescript
interface CollectMarketNewsRequest {
  sources?: string[];
  keywords?: string[];
  max_articles?: number;
}
```

#### レスポンス

```typescript
{
  job_id: string;
}
```

### `generate_stock_predictions`

銘柄予測を生成します。

#### リクエスト

```typescript
interface GenerateStockPredictionsRequest {
  news_job_id: string;
  market_trends?: MarketTrends;
  num_predictions?: number;
  prediction_horizon?: 'short' | 'medium' | 'long';
}
```

#### レスポンス

```typescript
{
  job_id: string;
}
```

### `get_stock_predictions`

予測結果を取得します。

#### レスポンス

```typescript
{
  job_id: string;
  predictions: Array<{
    prediction_id: string;
    symbol: string;
    predicted_direction: 'up' | 'down' | 'sideways';
    confidence_score: number;
    reasoning: string;
    association_chain: Array<{
      step: number;
      concept: string;
      connection: string;
    }>;
    suggested_action: 'buy' | 'sell' | 'hold' | 'watch';
  }>;
}
```

