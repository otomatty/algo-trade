# AlgorithmProposal Component Specification

## Related Files

- Implementation: `src/pages/AlgorithmProposal/AlgorithmProposal.tsx`
- Tests: `src/pages/AlgorithmProposal/AlgorithmProposal.test.tsx`
- Sub-components:
  - `src/pages/AlgorithmProposal/ProposalGenerationForm.tsx`
  - `src/pages/AlgorithmProposal/ProposalList.tsx`
  - `src/pages/AlgorithmProposal/ProgressIndicator.tsx`

## Related Documentation

- Plan: `docs/03_plans/algorithm-proposal/README.md`
- API Spec: `docs/03_plans/algorithm-proposal/api-spec.md`
- Data Model: `docs/03_plans/algorithm-proposal/data-model.md`
- Implementation Guide: `docs/03_plans/algorithm-proposal/IMPLEMENTATION_GUIDE.md`
- Issue: `docs/01_issues/open/2025_11/20251101_01_trend-association-algorithm-platform.md` (SCREEN-002)

## Requirements

### Phase 1: 基本UI構築

#### RQ-001: データセット選択機能
- ユーザーは利用可能なデータセット一覧から選択できる
- データセットは`get_data_list()` Tauriコマンドで取得
- データセットが存在しない場合は適切なメッセージを表示

#### RQ-002: ユーザー設定入力機能
- リスク許容度を選択できる（'low' | 'medium' | 'high'）
- 取引頻度を選択できる（'low' | 'medium' | 'high'）
- 好みの指標を複数選択できる（オプション、例: ['RSI', 'MACD', 'Bollinger Bands']）
- すべての設定はオプション（デフォルト値あり）

#### RQ-003: 提案数指定機能
- ユーザーは生成する提案数を指定できる
- デフォルト値: 5
- 最小値: 1、最大値: 10

#### RQ-004: UIレイアウト
- Mantine UIコンポーネントを使用
- レスポンシブデザインに対応
- アクセシビリティを考慮
- 既存のDataAnalysisコンポーネントと一貫性のあるデザイン

#### RQ-005: ローディング状態の表示
- データセット一覧の読み込み中はローディング状態を表示
- フォーム送信時（Phase 3で実装）のローディング状態に対応

#### RQ-006: エラーハンドリング
- Tauriコマンドのエラーを適切にキャッチして表示
- ネットワークエラー、データ不足エラー等を区別して表示
- ユーザーフレンドリーなエラーメッセージを表示

#### RQ-007: 提案生成ボタン（Phase 1では無効化）
- 提案生成ボタンを表示するが、Phase 1では無効化
- Phase 3で実装予定の`generate_algorithm_proposals` Tauriコマンド呼び出しの準備

## Test Cases

### TC-001: コンポーネントのレンダリング
**Given**: AlgorithmProposalコンポーネントがマウントされる  
**When**: 初期状態  
**Then**: 
- "Algorithm Proposal"または"アルゴリズム提案"タイトルが表示される
- データセット選択UIが表示される
- ユーザー設定入力UIが表示される
- 提案数指定UIが表示される
- 提案生成ボタンが表示される（初期状態では無効）

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
- フォームの他のフィールドが有効になる

### TC-005: ユーザー設定入力
**Given**: データセットが選択されている  
**When**: ユーザーがリスク許容度、取引頻度、好みの指標を入力する  
**Then**: 
- 入力値が状態に保存される
- すべての設定はオプションとして扱われる

### TC-006: 提案数指定
**Given**: データセットが選択されている  
**When**: ユーザーが提案数を変更する  
**Then**: 
- 提案数が状態に保存される
- 最小値・最大値のバリデーションが機能する

### TC-007: フォームバリデーション
**Given**: フォームが表示されている  
**When**: 必須フィールドが未入力の場合  
**Then**: 
- 適切なバリデーションメッセージが表示される
- 提案生成ボタンは無効のまま（Phase 1では常に無効）

### TC-008: エラーハンドリング
**Given**: フォームが表示されている  
**When**: Tauriコマンドがエラーを返す  
**Then**: 
- エラーメッセージがAlertコンポーネントで表示される
- エラーの種類に応じた適切なメッセージが表示される

### TC-009: データセットが存在しない場合
**Given**: データセット一覧が空  
**When**: コンポーネントがレンダリングされる  
**Then**: 
- 適切なメッセージが表示される（例: "No data sets available. Please import data first."）
- 提案生成ボタンは無効のまま

### TC-010: 提案一覧の初期表示
**Given**: コンポーネントがマウントされる  
**When**: 初期状態  
**Then**: 
- 提案一覧エリアが表示される
- "提案が生成されると、ここに表示されます"のようなメッセージが表示される

## Component Structure

```
AlgorithmProposal
├── Title: "Algorithm Proposal" / "アルゴリズム提案"
├── ProposalGenerationForm
│   ├── Select: Data Set Selection
│   ├── Select: Risk Tolerance (optional)
│   ├── Select: Trading Frequency (optional)
│   ├── MultiSelect: Preferred Indicators (optional)
│   ├── NumberInput: Number of Proposals
│   └── Button: Generate Proposals (disabled in Phase 1)
├── ProgressIndicator (conditional, Phase 4)
└── ProposalList
    └── Empty State Message (Phase 1)
```

## State Management

```typescript
interface AlgorithmProposalState {
  dataSetId: number | null;
  userPreferences: UserPreferences;
  numProposals: number;
  loading: boolean;
  error: string | null;
  jobId: string | null;  // Phase 4で使用
  showResults: boolean;  // Phase 5で使用
}

interface UserPreferences {
  risk_tolerance?: 'low' | 'medium' | 'high';
  trading_frequency?: 'low' | 'medium' | 'high';
  preferred_indicators?: string[];
}
```

## API Integration

### Tauri Commands

#### `get_data_list()`
- **Purpose**: データセット一覧を取得
- **Response**: `{ data_list: DataSet[] }`
- **Error Handling**: エラー時はエラーメッセージを表示

#### `generate_algorithm_proposals()` (Phase 3で実装)
- **Purpose**: アルゴリズム提案生成ジョブを開始
- **Request**: `{ data_set_id: number, analysis_id?: number, num_proposals?: number, user_preferences?: UserPreferences }`
- **Response**: `{ job_id: string }`
- **Error Handling**: エラー時はエラーメッセージを表示
- **Phase 1**: 未実装（ボタンは無効化）

## Dependencies

### External Dependencies
- `@tauri-apps/api/core` - Tauriコマンド呼び出し（`get_data_list`のみ）
- `@mantine/core` - UIコンポーネント
- `src/types/data` - DataSet型定義
- `src/types/algorithm` - UserPreferences型定義

### Internal Dependencies
- `ProposalGenerationForm` - 提案生成フォームコンポーネント
- `ProposalList` - 提案一覧コンポーネント（Phase 1では空の状態表示）
- `ProgressIndicator` - 進捗表示コンポーネント（Phase 4で実装予定）

## Implementation Notes

### Phase 1の制限事項
- 提案生成ボタンは無効化（Phase 3で実装）
- 進捗表示は基本構造のみ（Phase 4で実装）
- 提案一覧は空の状態を表示（Phase 5で実装）
- データ解析結果の取得は未実装（Phase 2で実装）

### 既存パターンの踏襲
- `DataAnalysis.tsx`の構造を参考に実装
- `AnalysisJobForm.tsx`のフォーム実装パターンを踏襲
- エラーハンドリングは`Alert`コンポーネントを使用
- ローディング状態は`Button`コンポーネントの`loading`プロパティを使用

