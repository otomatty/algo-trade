# アルゴリズム提案機能 API仕様書

## 概要

アルゴリズム提案機能で使用するTauriコマンドの詳細仕様です。

## 関連ドキュメント

- **実装計画**: `docs/03_plans/algorithm-proposal/README.md`
- **要件定義**: `docs/01_issues/open/2025_11/20251101_01_trend-association-algorithm-platform.md` (SCREEN-002)

## Tauriコマンド一覧

### `generate_algorithm_proposals`

LLMを使用してアルゴリズム提案を生成します。非同期で実行され、即座にジョブIDを返します。

#### リクエスト

```typescript
interface GenerateAlgorithmProposalsRequest {
  data_set_id: number;
  analysis_id?: number;
  num_proposals?: number;
  user_preferences?: {
    risk_tolerance?: 'low' | 'medium' | 'high';
    trading_frequency?: 'low' | 'medium' | 'high';
    preferred_indicators?: string[];
  };
}

invoke('generate_algorithm_proposals', {
  data_set_id: 1,
  num_proposals: 5,
  user_preferences: {
    risk_tolerance: 'medium',
    trading_frequency: 'high',
    preferred_indicators: ['RSI', 'MACD']
  }
})
```

#### レスポンス

```typescript
{
  job_id: string;  // アルゴリズム提案生成ジョブの一意なID
}
```

#### 型定義

```typescript
interface GenerateAlgorithmProposalsRequest {
  data_set_id: number;
  analysis_id?: number;
  num_proposals?: number;
  user_preferences?: UserPreferences;
}

interface UserPreferences {
  risk_tolerance?: 'low' | 'medium' | 'high';
  trading_frequency?: 'low' | 'medium' | 'high';
  preferred_indicators?: string[];
}

interface GenerateAlgorithmProposalsResponse {
  job_id: string;
}
```

#### エラーハンドリング

| エラーコード | 説明 | HTTPステータス相当 |
|------------|------|-------------------|
| `DATA_SET_NOT_FOUND` | データセットが存在しない | 404 |
| `ANALYSIS_NOT_FOUND` | 解析結果が存在しない | 404 |
| `LLM_API_KEY_NOT_SET` | LLM APIキーが設定されていない | 400 |
| `LLM_API_ERROR` | LLM API呼び出しエラー | 500 |
| `DATABASE_ERROR` | データベースアクセスエラー | 500 |

#### 使用例

```typescript
import { invoke } from '@tauri-apps/api/core';

async function generateProposals(dataSetId: number, preferences?: UserPreferences) {
  try {
    const response = await invoke<GenerateAlgorithmProposalsResponse>(
      'generate_algorithm_proposals',
      {
        data_set_id: dataSetId,
        num_proposals: 5,
        user_preferences: preferences
      }
    );
    return response.job_id;
  } catch (error) {
    console.error('Failed to generate proposals:', error);
    throw error;
  }
}
```

---

### `get_proposal_generation_status`

アルゴリズム提案生成ジョブの進捗状況を取得します。

#### リクエスト

```typescript
interface GetProposalGenerationStatusRequest {
  job_id: string;
}

invoke('get_proposal_generation_status', { job_id: 'job-123' })
```

#### レスポンス

```typescript
{
  status: 'pending' | 'analyzing' | 'generating' | 'completed' | 'failed';
  progress: number;  // 0.0 ~ 1.0 の進捗率
  message: string;   // ステータスメッセージ
  error?: string;     // エラーメッセージ（失敗時）
}
```

#### 型定義

```typescript
interface GetProposalGenerationStatusRequest {
  job_id: string;
}

interface GetProposalGenerationStatusResponse {
  status: 'pending' | 'analyzing' | 'generating' | 'completed' | 'failed';
  progress: number;
  message: string;
  error?: string;
}
```

#### ポーリング推奨間隔

2秒間隔でポーリングすることを推奨します。

#### 使用例

```typescript
import { invoke } from '@tauri-apps/api/core';

async function pollProposalStatus(jobId: string): Promise<GetProposalGenerationStatusResponse> {
  const response = await invoke<GetProposalGenerationStatusResponse>(
    'get_proposal_generation_status',
    { job_id: jobId }
  );
  return response;
}

// ポーリング例
async function waitForCompletion(jobId: string) {
  while (true) {
    const status = await pollProposalStatus(jobId);
    if (status.status === 'completed') {
      return status;
    }
    if (status.status === 'failed') {
      throw new Error(status.error || 'Generation failed');
    }
    await new Promise(resolve => setTimeout(resolve, 2000));
  }
}
```

---

### `get_algorithm_proposals`

生成されたアルゴリズム提案の一覧を取得します。

#### リクエスト

```typescript
interface GetAlgorithmProposalsRequest {
  job_id: string;
}

invoke('get_algorithm_proposals', { job_id: 'job-123' })
```

#### レスポンス

```typescript
{
  job_id: string;
  proposals: Array<{
    proposal_id: string;
    name: string;
    description: string;
    rationale: string;
    expected_performance?: {
      expected_return?: number;
      risk_level?: 'low' | 'medium' | 'high';
    };
    definition: {
      triggers: Array<TriggerDefinition>;
      actions: Array<ActionDefinition>;
    };
    confidence_score?: number;  // 0.0 ~ 1.0
  }>;
}
```

#### 型定義

```typescript
interface GetAlgorithmProposalsRequest {
  job_id: string;
}

interface GetAlgorithmProposalsResponse {
  job_id: string;
  proposals: AlgorithmProposal[];
}

interface AlgorithmProposal {
  proposal_id: string;
  name: string;
  description: string;
  rationale: string;
  expected_performance?: ExpectedPerformance;
  definition: AlgorithmDefinition;
  confidence_score?: number;
}

interface ExpectedPerformance {
  expected_return?: number;
  risk_level?: 'low' | 'medium' | 'high';
}

interface AlgorithmDefinition {
  triggers: TriggerDefinition[];
  actions: ActionDefinition[];
}
```

#### エラーハンドリング

| エラーコード | 説明 | HTTPステータス相当 |
|------------|------|-------------------|
| `JOB_NOT_FOUND` | ジョブIDが存在しない | 404 |
| `JOB_NOT_COMPLETED` | ジョブが未完了 | 400 |
| `DATABASE_ERROR` | データベースアクセスエラー | 500 |

#### 使用例

```typescript
import { invoke } from '@tauri-apps/api/core';

async function fetchProposals(jobId: string) {
  try {
    const response = await invoke<GetAlgorithmProposalsResponse>(
      'get_algorithm_proposals',
      { job_id: jobId }
    );
    return response.proposals;
  } catch (error) {
    console.error('Failed to fetch proposals:', error);
    throw error;
  }
}
```

---

### `select_algorithm`

ユーザーが選択したアルゴリズム提案を保存します。

#### リクエスト

```typescript
interface SelectAlgorithmRequest {
  proposal_id: string;
  custom_name?: string;
}

invoke('select_algorithm', {
  proposal_id: 'proposal-123',
  custom_name: 'My Custom Algorithm'
})
```

#### レスポンス

```typescript
{
  algo_id: number;  // 保存されたアルゴリズムID
  success: boolean;
}
```

#### 型定義

```typescript
interface SelectAlgorithmRequest {
  proposal_id: string;
  custom_name?: string;
}

interface SelectAlgorithmResponse {
  algo_id: number;
  success: boolean;
}
```

#### エラーハンドリング

| エラーコード | 説明 | HTTPステータス相当 |
|------------|------|-------------------|
| `PROPOSAL_NOT_FOUND` | 提案IDが存在しない | 404 |
| `DATABASE_ERROR` | データベースアクセスエラー | 500 |

#### 使用例

```typescript
import { invoke } from '@tauri-apps/api/core';

async function selectAlgorithm(proposalId: string, customName?: string) {
  try {
    const response = await invoke<SelectAlgorithmResponse>(
      'select_algorithm',
      {
        proposal_id: proposalId,
        custom_name: customName
      }
    );
    return response.algo_id;
  } catch (error) {
    console.error('Failed to select algorithm:', error);
    throw error;
  }
}
```

---

### `get_analysis_results`

データ解析結果を取得します。LLMへの入力として使用されます。

#### リクエスト

```typescript
interface GetAnalysisResultsRequest {
  job_id: string;
}

invoke('get_analysis_results', { job_id: 'analysis-job-123' })
```

#### レスポンス

データ解析機能の`get_analysis_results`と同じレスポンス形式です。詳細は`docs/03_plans/data-analysis/api-spec.md`を参照してください。

## エラー型定義

```typescript
interface TauriError {
  code: string;
  message: string;
  details?: Record<string, unknown>;
}
```

## 注意事項

- ジョブIDは一意な文字列として生成されます（UUID推奨）
- 進捗状況のポーリングは適切な間隔で実行してください（推奨: 2秒）
- LLM APIのレート制限に注意してください
- エラー発生時は適切なエラーハンドリングを実装してください

