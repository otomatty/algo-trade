# バックテスト機能 API仕様書

## 概要

バックテスト機能で使用するTauriコマンドの詳細仕様です。

## 関連ドキュメント

- **実装計画**: `docs/03_plans/backtest/README.md`
- **要件定義**: `docs/01_issues/open/2025_11/20251101_01_trend-association-algorithm-platform.md` (SCREEN-003, SCREEN-004)

## Tauriコマンド一覧

### `run_backtest`

バックテストの実行を非同期で開始します。即座にジョブIDを返します。

#### リクエスト

```typescript
interface RunBacktestRequest {
  algorithm_ids: number[];
  start_date: string;  // YYYY-MM-DD形式
  end_date: string;    // YYYY-MM-DD形式
  data_set_id?: number;
}

invoke('run_backtest', {
  algorithm_ids: [1, 2],
  start_date: '2023-01-01',
  end_date: '2023-12-31',
  data_set_id: 1
})
```

#### レスポンス

```typescript
{
  job_id: string;
}
```

#### 型定義

```typescript
interface RunBacktestRequest {
  algorithm_ids: number[];
  start_date: string;
  end_date: string;
  data_set_id?: number;
}

interface RunBacktestResponse {
  job_id: string;
}
```

#### エラーハンドリング

| エラーコード | 説明 | HTTPステータス相当 |
|------------|------|-------------------|
| `INVALID_ALGORITHM_ID` | 無効なアルゴリズムID | 400 |
| `INVALID_DATE_RANGE` | 日付範囲が不正 | 400 |
| `DATA_SET_NOT_FOUND` | データセットが存在しない | 404 |
| `INSUFFICIENT_DATA` | データが不足している | 400 |

#### 使用例

```typescript
import { invoke } from '@tauri-apps/api/core';

async function runBacktest(
  algorithmIds: number[],
  startDate: string,
  endDate: string,
  dataSetId?: number
) {
  try {
    const response = await invoke<RunBacktestResponse>('run_backtest', {
      algorithm_ids: algorithmIds,
      start_date: startDate,
      end_date: endDate,
      data_set_id: dataSetId
    });
    return response.job_id;
  } catch (error) {
    console.error('Failed to run backtest:', error);
    throw error;
  }
}
```

---

### `get_backtest_status`

バックテストジョブの進捗状況を取得します。

#### リクエスト

```typescript
interface GetBacktestStatusRequest {
  job_id: string;
}

invoke('get_backtest_status', { job_id: 'job-123' })
```

#### レスポンス

```typescript
{
  status: 'pending' | 'running' | 'completed' | 'failed';
  progress: number;  // 0.0 ~ 1.0
  message: string;
  error?: string;
}
```

#### 型定義

```typescript
interface GetBacktestStatusRequest {
  job_id: string;
}

interface GetBacktestStatusResponse {
  status: 'pending' | 'running' | 'completed' | 'failed';
  progress: number;
  message: string;
  error?: string;
}
```

#### ポーリング推奨間隔

1秒間隔でポーリングすることを推奨します。

---

### `get_backtest_results`

バックテストの完了結果を取得します。

#### リクエスト

```typescript
interface GetBacktestResultsRequest {
  job_id: string;
}

invoke('get_backtest_results', { job_id: 'job-123' })
```

#### レスポンス

```typescript
{
  job_id: string;
  algorithm_id: number;
  start_date: string;
  end_date: string;
  performance: {
    total_return: number;
    sharpe_ratio: number;
    max_drawdown: number;
    win_rate: number;
    total_trades: number;
    average_profit: number;
    average_loss: number;
  };
  trades: Array<{
    entry_date: string;
    exit_date: string;
    entry_price: number;
    exit_price: number;
    quantity: number;
    profit: number;
    profit_rate: number;
  }>;
  equity_curve: Array<{
    date: string;
    equity: number;
  }>;
}
```

#### 型定義

詳細は`data-model.md`を参照してください。

#### エラーハンドリング

| エラーコード | 説明 | HTTPステータス相当 |
|------------|------|-------------------|
| `JOB_NOT_FOUND` | ジョブIDが存在しない | 404 |
| `JOB_NOT_COMPLETED` | ジョブが未完了 | 400 |

## エラー型定義

```typescript
interface TauriError {
  code: string;
  message: string;
  details?: Record<string, unknown>;
}
```

