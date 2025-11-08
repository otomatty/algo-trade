# ダッシュボード機能 API仕様書

## 概要

ダッシュボード機能で使用するTauriコマンドの詳細仕様です。

## 関連ドキュメント

- **実装計画**: `docs/03_plans/dashboard/README.md`
- **要件定義**: `docs/01_issues/open/2025_11/20251101_01_trend-association-algorithm-platform.md` (SCREEN-001)

## Tauriコマンド一覧

### `get_selected_algorithms`

選択済みアルゴリズムの一覧を取得します。

#### リクエスト

```typescript
// 引数なし
invoke('get_selected_algorithms')
```

#### レスポンス

```typescript
{
  algorithms: Array<{
    id: number;
    name: string;
    description?: string;
    proposal_id?: string;  // 元の提案ID（存在する場合）
    created_at: string;    // ISO 8601形式
    updated_at: string;    // ISO 8601形式
    definition: {
      triggers: Array<TriggerDefinition>;
      actions: Array<ActionDefinition>;
    };
  }>;
}
```

#### 型定義

```typescript
interface GetSelectedAlgorithmsResponse {
  algorithms: Algorithm[];
}

interface Algorithm {
  id: number;
  name: string;
  description?: string;
  proposal_id?: string;
  created_at: string;
  updated_at: string;
  definition: AlgorithmDefinition;
}

interface AlgorithmDefinition {
  triggers: TriggerDefinition[];
  actions: ActionDefinition[];
}

interface TriggerDefinition {
  type: string;
  condition: Record<string, unknown>;
}

interface ActionDefinition {
  type: string;
  parameters: Record<string, unknown>;
}
```

#### エラーハンドリング

| エラーコード | 説明 | HTTPステータス相当 |
|------------|------|-------------------|
| `DATABASE_ERROR` | データベースアクセスエラー | 500 |
| `UNKNOWN_ERROR` | 予期しないエラー | 500 |

#### 使用例

```typescript
import { invoke } from '@tauri-apps/api/core';

async function fetchAlgorithms() {
  try {
    const response = await invoke<GetSelectedAlgorithmsResponse>('get_selected_algorithms');
    return response.algorithms;
  } catch (error) {
    console.error('Failed to fetch algorithms:', error);
    throw error;
  }
}
```

---

### `get_backtest_results`

最新のバックテスト結果を取得します。各アルゴリズムの最新検証結果を返します。

#### リクエスト

```typescript
interface GetBacktestResultsRequest {
  algorithm_ids?: number[];  // オプション: 特定のアルゴリズムIDのみ取得
  limit?: number;            // オプション: 取得件数（デフォルト: 10）
}

invoke('get_backtest_results', { algorithm_ids: [1, 2], limit: 5 })
```

#### レスポンス

```typescript
{
  results: Array<{
    job_id: string;
    algorithm_id: number;
    algorithm_name: string;
    start_date: string;      // YYYY-MM-DD形式
    end_date: string;        // YYYY-MM-DD形式
    completed_at: string;    // ISO 8601形式
    performance: {
      total_return: number;        // 総リターン率 (%)
      sharpe_ratio: number;        // シャープレシオ
      max_drawdown: number;        // 最大ドローダウン (%)
      win_rate: number;            // 勝率 (%)
      total_trades: number;        // 総取引数
      average_profit: number;      // 平均利益
      average_loss: number;        // 平均損失
    };
  }>;
}
```

#### 型定義

```typescript
interface GetBacktestResultsRequest {
  algorithm_ids?: number[];
  limit?: number;
}

interface GetBacktestResultsResponse {
  results: BacktestResultSummary[];
}

interface BacktestResultSummary {
  job_id: string;
  algorithm_id: number;
  algorithm_name: string;
  start_date: string;
  end_date: string;
  completed_at: string;
  performance: PerformanceMetrics;
}

interface PerformanceMetrics {
  total_return: number;
  sharpe_ratio: number;
  max_drawdown: number;
  win_rate: number;
  total_trades: number;
  average_profit: number;
  average_loss: number;
}
```

#### エラーハンドリング

| エラーコード | 説明 | HTTPステータス相当 |
|------------|------|-------------------|
| `INVALID_ALGORITHM_ID` | 無効なアルゴリズムID | 400 |
| `DATABASE_ERROR` | データベースアクセスエラー | 500 |
| `UNKNOWN_ERROR` | 予期しないエラー | 500 |

#### 使用例

```typescript
import { invoke } from '@tauri-apps/api/core';

async function fetchBacktestResults(algorithmIds?: number[]) {
  try {
    const response = await invoke<GetBacktestResultsResponse>(
      'get_backtest_results',
      { algorithm_ids: algorithmIds, limit: 10 }
    );
    return response.results;
  } catch (error) {
    console.error('Failed to fetch backtest results:', error);
    throw error;
  }
}
```

---

### `delete_algorithm`

指定したアルゴリズムを削除します。

#### リクエスト

```typescript
interface DeleteAlgorithmRequest {
  algo_id: number;
}

invoke('delete_algorithm', { algo_id: 1 })
```

#### レスポンス

```typescript
{
  success: boolean;
  message?: string;  // エラーメッセージ（失敗時）
}
```

#### 型定義

```typescript
interface DeleteAlgorithmRequest {
  algo_id: number;
}

interface DeleteAlgorithmResponse {
  success: boolean;
  message?: string;
}
```

#### エラーハンドリング

| エラーコード | 説明 | HTTPステータス相当 |
|------------|------|-------------------|
| `ALGORITHM_NOT_FOUND` | アルゴリズムが見つからない | 404 |
| `DATABASE_ERROR` | データベースアクセスエラー | 500 |
| `UNKNOWN_ERROR` | 予期しないエラー | 500 |

#### 使用例

```typescript
import { invoke } from '@tauri-apps/api/core';

async function deleteAlgorithm(algorithmId: number) {
  try {
    const response = await invoke<DeleteAlgorithmResponse>(
      'delete_algorithm',
      { algo_id: algorithmId }
    );
    if (!response.success) {
      throw new Error(response.message || 'Failed to delete algorithm');
    }
    return response;
  } catch (error) {
    console.error('Failed to delete algorithm:', error);
    throw error;
  }
}
```

## エラー型定義

```typescript
interface TauriError {
  code: string;
  message: string;
  details?: Record<string, unknown>;
}
```

## 注意事項

- すべての日付はISO 8601形式（`YYYY-MM-DDTHH:mm:ss.sssZ`）または`YYYY-MM-DD`形式で返されます
- 数値は浮動小数点数として扱われます
- オプショナルフィールドは`undefined`の可能性があります
- エラー発生時は適切なエラーハンドリングを実装してください

