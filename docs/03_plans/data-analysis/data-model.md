# データ解析機能 データモデル詳細

## TypeScript型定義

```typescript
interface AnalysisResult {
  job_id: string;
  data_set_id: number;
  analysis_summary: AnalysisSummary;
  technical_indicators: TechnicalIndicators;
  statistics: Statistics;
}

interface AnalysisSummary {
  trend_direction: 'upward' | 'downward' | 'sideways';
  volatility_level: 'low' | 'medium' | 'high';
  dominant_patterns: string[];
}

interface TechnicalIndicators {
  rsi: RSIResult;
  macd: MACDResult;
}

interface Statistics {
  price_range: { min: number; max: number; current: number };
  volume_average: number;
  price_change_percent: number;
}
```

