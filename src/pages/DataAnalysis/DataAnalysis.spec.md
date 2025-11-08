# DataAnalysis Component Specification

## Related Files

- Implementation: `src/pages/DataAnalysis/DataAnalysis.tsx`
- Tests: `src/pages/DataAnalysis/DataAnalysis.test.tsx`
- Sub-components:
  - `src/pages/DataAnalysis/AnalysisJobForm.tsx`
  - `src/pages/DataAnalysis/AnalysisProgress.tsx`
  - `src/pages/DataAnalysis/AnalysisResults.tsx`

## Related Documentation

- Plan: `docs/03_plans/data-analysis/README.md`
- API Spec: `docs/03_plans/data-analysis/api-spec.md`
- UI Design: `docs/03_plans/data-analysis/ui-design.md`
- Issue: `docs/01_issues/open/2025_11/20251101_01_trend-association-algorithm-platform.md` (SCREEN-006)

## Requirements

### Phase 1: 解析ジョブ実行UI

#### RQ-001: データセット選択機能
- ユーザーは利用可能なデータセット一覧から選択できる
- データセットは`get_data_list()` Tauriコマンドで取得
- データセットが存在しない場合は適切なメッセージを表示

#### RQ-002: 解析実行機能
- ユーザーは選択したデータセットに対して解析を実行できる
- `run_data_analysis(data_set_id)` Tauriコマンドを呼び出す
- 実行中はボタンを無効化し、ローディング状態を表示

#### RQ-003: エラーハンドリング
- Tauriコマンドのエラーを適切にキャッチして表示
- ネットワークエラー、データ不足エラー等を区別して表示

#### RQ-004: UIレイアウト
- Mantine UIコンポーネントを使用
- レスポンシブデザインに対応
- アクセシビリティを考慮

## Test Cases

### TC-001: コンポーネントのレンダリング
**Given**: DataAnalysisコンポーネントがマウントされる  
**When**: 初期状態  
**Then**: 
- "Data Analysis"タイトルが表示される
- データセット選択UIが表示される
- 解析実行ボタンが表示される（初期状態では無効）

### TC-002: データセット一覧の読み込み
**Given**: コンポーネントがマウントされる  
**When**: `get_data_list()`が成功する  
**Then**: 
- データセット一覧がSelectコンポーネントに表示される
- ローディング状態が解除される

### TC-003: データセット一覧の読み込みエラー
**Given**: コンポーネントがマウントされる  
**When**: `get_data_list()`がエラーを返す  
**Then**: 
- エラーメッセージが表示される
- ユーザーは再試行できる

### TC-004: データセット選択
**Given**: データセット一覧が読み込まれている  
**When**: ユーザーがデータセットを選択する  
**Then**: 
- 選択したデータセットIDが状態に保存される
- 解析実行ボタンが有効になる

### TC-005: 解析実行成功
**Given**: データセットが選択されている  
**When**: ユーザーが解析実行ボタンをクリックする  
**And**: `run_data_analysis()`が成功する  
**Then**: 
- `run_data_analysis()`が正しい`data_set_id`で呼び出される
- ジョブIDが返される
- 進捗表示コンポーネントが表示される（Phase 3で実装）

### TC-006: 解析実行エラー
**Given**: データセットが選択されている  
**When**: ユーザーが解析実行ボタンをクリックする  
**And**: `run_data_analysis()`がエラーを返す  
**Then**: 
- エラーメッセージが表示される
- ボタンが再度有効になる

### TC-007: データセットが存在しない場合
**Given**: データセット一覧が空  
**When**: コンポーネントがレンダリングされる  
**Then**: 
- 適切なメッセージが表示される（例: "No data sets available. Please import data first."）
- 解析実行ボタンは無効のまま

## Component Structure

```
DataAnalysis
├── Title: "Data Analysis"
├── AnalysisJobForm
│   ├── Select: Data Set Selection
│   └── Button: Run Analysis
├── AnalysisProgress (conditional, Phase 3)
└── AnalysisResults (conditional, Phase 4)
```

## State Management

```typescript
interface DataAnalysisState {
  dataSets: DataSet[];
  selectedDataSetId: number | null;
  jobId: string | null;
  loading: boolean;
  error: string | null;
}
```

## API Integration

### Tauri Commands

#### `get_data_list()`
- **Purpose**: データセット一覧を取得
- **Response**: `{ data_list: DataSet[] }`
- **Error Handling**: エラー時はエラーメッセージを表示

#### `run_data_analysis(data_set_id: number)`
- **Purpose**: データ解析ジョブを開始
- **Request**: `{ data_set_id: number }`
- **Response**: `{ job_id: string }`
- **Error Handling**: エラー時はエラーメッセージを表示

## Dependencies

### External Dependencies
- `@tauri-apps/api/core` - Tauriコマンド呼び出し
- `@mantine/core` - UIコンポーネント
- `src/types/data` - DataSet型定義
- `src/types/analysis` - AnalysisJob型定義

### Internal Dependencies
- `AnalysisJobForm` - ジョブ実行フォームコンポーネント
- `AnalysisProgress` - 進捗表示コンポーネント（Phase 3）
- `AnalysisResults` - 結果表示コンポーネント（Phase 4）

