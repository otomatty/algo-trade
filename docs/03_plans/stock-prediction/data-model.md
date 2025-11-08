# 銘柄予測機能 データモデル詳細

## TypeScript型定義

```typescript
interface StockPrediction {
  prediction_id: string;
  symbol: string;
  predicted_direction: 'up' | 'down' | 'sideways';
  confidence_score: number;
  reasoning: string;
  association_chain: AssociationStep[];
  suggested_action: 'buy' | 'sell' | 'hold' | 'watch';
}

interface AssociationStep {
  step: number;
  concept: string;
  connection: string;
}

interface News {
  id: string;
  title: string;
  content: string;
  source: string;
  published_at: string;
  sentiment?: 'positive' | 'neutral' | 'negative';
}
```

