# BacktestSettings Component Specification

## Related Files

- Implementation: `src/pages/Backtest/BacktestSettings.tsx`
- Tests: `src/pages/Backtest/BacktestSettings.test.tsx`
- Sub-components:
  - `src/pages/Backtest/AlgorithmSelector.tsx`
  - `src/pages/Backtest/DataSetSelector.tsx`
  - `src/pages/Backtest/DateRangePicker.tsx` (future)

## Related Documentation

- Plan: `docs/03_plans/backtest/README.md`
- API Spec: `docs/03_plans/backtest/api-spec.md`
- Data Model: `docs/03_plans/backtest/data-model.md`
- UI Design: `docs/03_plans/backtest/ui-design.md`
- Issue: `docs/01_issues/open/2025_11/20251101_01_trend-association-algorithm-platform.md` (SCREEN-003)

## Requirements

### Phase 1: バックテスト設定画面（基本UI）

#### RQ-001: アルゴリズム選択機能
- ユーザーは選択済みアルゴリズム一覧から複数選択できる
- アルゴリズムは`get_selected_algorithms()` Tauriコマンドで取得
- アルゴリズムが存在しない場合は適切なメッセージを表示
- 複数選択はチェックボックス形式（MultiSelect）

#### RQ-002: 日付範囲選択機能
- ユーザーは開始日と終了日を選択できる
- Mantine DatePickerInputを使用
- 開始日は終了日より前である必要がある
- 両方の日付が必須

#### RQ-003: データセット選択機能
- ユーザーは利用可能なデータセット一覧から選択できる
- データセットは`get_data_list()` Tauriコマンドで取得
- データセットが存在しない場合は適切なメッセージを表示

#### RQ-004: バリデーション処理
- アルゴリズムが1つ以上選択されている必要がある
- データセットが選択されている必要がある
- 開始日と終了日が両方選択されている必要がある
- 開始日は終了日より前である必要がある

#### RQ-005: UIレイアウト
- Mantine UIコンポーネントを使用
- レスポンシブデザインに対応
- アクセシビリティを考慮
- 既存のDataAnalysisコンポーネントと一貫性のあるデザイン

#### RQ-006: ローディング状態の表示
- アルゴリズム一覧の読み込み中はローディング状態を表示
- データセット一覧の読み込み中はローディング状態を表示
- フォーム送信時（Phase 2で実装）のローディング状態に対応

#### RQ-007: エラーハンドリング
- Tauriコマンドのエラーを適切にキャッチして表示
- ネットワークエラー、データ不足エラー等を区別して表示
- ユーザーフレンドリーなエラーメッセージを表示
- バリデーションエラーも適切に表示

#### RQ-008: 実行ボタン（Phase 1では警告表示）
- バックテスト実行ボタンを表示するが、Phase 1では実行機能は未実装
- Phase 2で実装予定の`run_backtest()` Tauriコマンド呼び出しの準備
- バリデーションが通った場合でも、実行時は警告メッセージを表示

## Test Cases

### TC-001: コンポーネントのレンダリング
**Given**: BacktestSettingsコンポーネントがマウントされる  
**When**: 初期状態  
**Then**: 
- "Backtest Settings"タイトルが表示される
- アルゴリズム選択UIが表示される
- データセット選択UIが表示される
- 開始日選択UIが表示される
- 終了日選択UIが表示される
- バックテスト実行ボタンが表示される（初期状態では無効）

### TC-002: アルゴリズム一覧の読み込み
**Given**: コンポーネントがマウントされる  
**When**: `get_selected_algorithms()`が成功する  
**Then**: 
- アルゴリズム一覧がMultiSelectコンポーネントに表示される
- ローディング状態が解除される

### TC-003: アルゴリズム一覧の読み込みエラー
**Given**: コンポーネントがマウントされる  
**When**: `get_selected_algorithms()`がエラーを返す  
**Then**: 
- エラーメッセージが表示される
- ユーザーは再試行できる

### TC-004: アルゴリズムが存在しない場合
**Given**: アルゴリズム一覧が空  
**When**: コンポーネントがレンダリングされる  
**Then**: 
- 適切なメッセージが表示される（例: "No algorithms available. Please select algorithms from the Algorithm Proposal page first."）
- バックテスト実行ボタンは無効のまま

### TC-005: アルゴリズム選択
**Given**: アルゴリズム一覧が読み込まれている  
**When**: ユーザーがアルゴリズムを選択する  
**Then**: 
- 選択したアルゴリズムIDが状態に保存される
- 複数選択が可能

### TC-006: データセット一覧の読み込み
**Given**: コンポーネントがマウントされる  
**When**: `get_data_list()`が成功する  
**Then**: 
- データセット一覧がSelectコンポーネントに表示される
- ローディング状態が解除される

### TC-007: データセット選択
**Given**: データセット一覧が読み込まれている  
**When**: ユーザーがデータセットを選択する  
**Then**: 
- 選択したデータセットIDが状態に保存される

### TC-008: 日付範囲選択
**Given**: コンポーネントが表示されている  
**When**: ユーザーが開始日と終了日を選択する  
**Then**: 
- 選択した日付が状態に保存される
- 開始日が終了日より前の場合、バリデーションエラーが表示されない

### TC-009: 日付範囲バリデーション
**Given**: 開始日と終了日が選択されている  
**When**: 開始日が終了日より後または同じ日付の場合  
**Then**: 
- バリデーションエラーメッセージが表示される
- バックテスト実行ボタンは無効のまま

### TC-010: フォームバリデーション
**Given**: フォームが表示されている  
**When**: 必須フィールドが未入力の場合  
**Then**: 
- バックテスト実行ボタンは無効のまま
- 適切なバリデーションメッセージが表示される（必要に応じて）

### TC-011: バックテスト実行ボタンクリック（Phase 1）
**Given**: すべての必須フィールドが入力されている  
**When**: ユーザーがバックテスト実行ボタンをクリックする  
**Then**: 
- 警告メッセージが表示される（"Backtest execution is not yet implemented. Phase 2 will implement this feature."）
- 実際のバックテストは実行されない

### TC-012: エラーハンドリング
**Given**: フォームが表示されている  
**When**: Tauriコマンドがエラーを返す  
**Then**: 
- エラーメッセージがAlertコンポーネントで表示される
- エラーの種類に応じた適切なメッセージが表示される

## Component Structure

```
BacktestSettings
├── Title: "Backtest Settings"
├── Paper
│   ├── Alert: Error Messages (conditional)
│   ├── AlgorithmSelector
│   │   └── MultiSelect: Algorithm Selection
│   ├── DataSetSelector
│   │   └── Select: Data Set Selection
│   ├── DatePickerInput: Start Date
│   ├── DatePickerInput: End Date
│   └── Button: Run Backtest
```

## State Management

```typescript
interface BacktestSettingsState {
  algorithms: Algorithm[];
  selectedAlgorithmIds: number[];
  dataSets: DataSet[];
  selectedDataSetId: number | null;
  startDate: Date | null;
  endDate: Date | null;
  loading: boolean;
  error: string | null;
}
```

## API Integration

### Tauri Commands

#### `get_selected_algorithms()`
- **Purpose**: 選択済みアルゴリズム一覧を取得
- **Response**: `{ algorithms: Algorithm[] }`
- **Error Handling**: エラー時はエラーメッセージを表示

#### `get_data_list()`
- **Purpose**: データセット一覧を取得
- **Response**: `{ data_list: DataSet[] }`
- **Error Handling**: エラー時はエラーメッセージを表示

#### `run_backtest()` (Phase 2で実装)
- **Purpose**: バックテストジョブを開始
- **Request**: `{ algorithm_ids: number[], start_date: string, end_date: string, data_set_id?: number }`
- **Response**: `{ job_id: string }`
- **Error Handling**: エラー時はエラーメッセージを表示
- **Phase 1**: 未実装（ボタンクリック時は警告表示）

## Dependencies

### External Dependencies
- `@tauri-apps/api/core` - Tauriコマンド呼び出し
- `@mantine/core` - UIコンポーネント
- `@mantine/dates` - DatePickerInputコンポーネント
- `src/types/algorithm` - Algorithm型定義
- `src/types/data` - DataSet型定義

### Internal Dependencies
- `AlgorithmSelector` - アルゴリズム選択コンポーネント
- `DataSetSelector` - データセット選択コンポーネント

## Implementation Notes

### Phase 1の制限事項
- バックテスト実行ボタンは警告表示のみ（Phase 2で実装）
- 進捗表示は未実装（Phase 3で実装）
- 結果表示は未実装（Phase 4で実装）

### 既存パターンの踏襲
- `DataAnalysis.tsx`の構造を参考に実装
- `AnalysisJobForm.tsx`のフォーム実装パターンを踏襲
- `ProposalGenerationForm.tsx`のデータセット選択パターンを踏襲
- エラーハンドリングは`Alert`コンポーネントを使用
- ローディング状態は`Button`コンポーネントの`loading`プロパティを使用

