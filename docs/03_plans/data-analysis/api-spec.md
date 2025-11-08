# データ解析機能 API仕様書

## Tauriコマンド一覧

### `run_data_analysis`

データ解析ジョブを開始します。

#### リクエスト

```typescript
interface RunDataAnalysisRequest {
  data_set_id: number;
}
```

#### レスポンス

```typescript
{
  job_id: string;
}
```

### `get_analysis_status`

解析ジョブの進捗を取得します。

#### リクエスト

```typescript
interface GetAnalysisStatusRequest {
  job_id: string;
}
```

#### レスポンス

```typescript
{
  status: 'pending' | 'running' | 'completed' | 'failed';
  progress: number;
  message: string;
  error?: string;
}
```

### `get_analysis_results`

解析結果を取得します。

#### リクエスト

```typescript
interface GetAnalysisResultsRequest {
  job_id: string;
}
```

#### レスポンス

```typescript
{
  job_id: string;
  data_set_id: number;
  analysis_summary: {
    trend_direction: 'upward' | 'downward' | 'sideways';
    volatility_level: 'low' | 'medium' | 'high';
    dominant_patterns: string[];
  };
  technical_indicators: {
    rsi: { current: number; average: number; signal: string };
    macd: { current: number; signal_line: number; histogram: number; trend: string };
  };
  statistics: {
    price_range: { min: number; max: number; current: number };
    volume_average: number;
    price_change_percent: number;
  };
}
```

