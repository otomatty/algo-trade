# Dashboard Component Specification

## Related Files

- Implementation: `src/pages/Dashboard/Dashboard.tsx`
- Tests: `src/pages/Dashboard/Dashboard.test.tsx`
- Sub-components:
  - `src/pages/Dashboard/Sidebar.tsx`
  - `src/pages/Dashboard/Header.tsx`
  - `src/pages/Dashboard/AlgorithmList.tsx`
  - `src/pages/Dashboard/AlgorithmCard.tsx`
  - `src/pages/Dashboard/ResultSummary.tsx`
  - `src/pages/Dashboard/PerformanceCard.tsx`
  - `src/pages/Dashboard/QuickActions.tsx`

## Related Documentation

- Plan: `docs/03_plans/dashboard/README.md`
- API Spec: `docs/03_plans/dashboard/api-spec.md`
- UI Design: `docs/03_plans/dashboard/ui-design.md`
- Data Model: `docs/03_plans/dashboard/data-model.md`
- Issue: `docs/01_issues/open/2025_11/20251101_01_trend-association-algorithm-platform.md` (SCREEN-001)

## Requirements

### Phase 1: 基本レイアウト構築

#### RQ-001: レイアウトコンポーネント
- Mantineの`AppShell`を使用したレイアウト
- サイドバーナビゲーション（`Sidebar.tsx`）
- ヘッダーコンポーネント（`Header.tsx`）
- メインコンテンツエリア

#### RQ-002: サイドバーナビゲーション
- ダッシュボードへのリンク
- アルゴリズム提案へのリンク
- バックテストへのリンク
- データ管理へのリンク
- データ解析へのリンク
- 銘柄予測へのリンク（将来実装）

#### RQ-003: ヘッダーコンポーネント
- アプリケーション名の表示
- ユーザー情報（将来実装）

#### RQ-004: レスポンシブデザイン
- モバイル: サイドバーをドロワーに変更
- タブレット: サイドバーを折りたたみ可能に
- デスクトップ: サイドバーを常時表示

### Phase 2: アルゴリズム一覧表示

#### RQ-005: アルゴリズム一覧取得
- `get_selected_algorithms()` Tauriコマンドの呼び出し
- データ取得中のローディング状態表示
- エラーハンドリング

#### RQ-006: アルゴリズムカード表示
- アルゴリズム名の表示
- 説明の表示（存在する場合）
- 最新のパフォーマンス指標（総リターン、シャープレシオ）
- アクションボタン（詳細、削除）

#### RQ-007: グリッドレイアウト
- デスクトップ: 3列表示
- タブレット: 2列表示
- モバイル: 1列表示

#### RQ-008: 空状態表示
- アルゴリズムがない場合の適切なメッセージ表示

### Phase 3: 検証結果サマリー表示

#### RQ-009: バックテスト結果取得
- `get_backtest_results_summary()` Tauriコマンドの呼び出し
- 複数のアルゴリズムIDを受け取り、各アルゴリズムの最新結果を取得
- データ取得中のローディング状態表示

#### RQ-010: パフォーマンス指標表示
- 総リターン率の表示
- シャープレシオの表示
- 最大ドローダウンの表示
- 勝率の表示
- 総取引数の表示

#### RQ-011: 結果サマリーコンポーネント
- アルゴリズムごとの最新結果をカード形式で表示
- パフォーマンス指標の可視化

### Phase 4: クイックアクション

#### RQ-012: アルゴリズム削除機能
- `delete_algorithm()` Tauriコマンドの呼び出し
- 削除確認ダイアログの表示
- 削除成功後の一覧更新

#### RQ-013: ナビゲーション機能
- アルゴリズム提案画面への遷移
- バックテスト画面への遷移
- データ管理画面への遷移
- データ解析画面への遷移

## Test Cases

### Phase 1

#### TC-001: コンポーネントのレンダリング
**Given**: Dashboardコンポーネントがマウントされる  
**When**: 初期状態  
**Then**: 
- AppShellが表示される
- Sidebarが表示される
- Headerが表示される
- メインコンテンツエリアが表示される

#### TC-002: サイドバーナビゲーション
**Given**: Dashboardコンポーネントがマウントされる  
**When**: サイドバーが表示される  
**Then**: 
- ダッシュボードへのリンクが表示される
- アルゴリズム提案へのリンクが表示される
- バックテストへのリンクが表示される
- データ管理へのリンクが表示される
- データ解析へのリンクが表示される

#### TC-003: レスポンシブデザイン
**Given**: Dashboardコンポーネントがマウントされる  
**When**: 画面サイズが変更される  
**Then**: 
- モバイル: サイドバーがドロワーに変更される
- タブレット: サイドバーが折りたたみ可能になる
- デスクトップ: サイドバーが常時表示される

### Phase 2

#### TC-004: アルゴリズム一覧の読み込み
**Given**: Dashboardコンポーネントがマウントされる  
**When**: `get_selected_algorithms()`が成功する  
**Then**: 
- アルゴリズム一覧が表示される
- ローディング状態が解除される

#### TC-005: アルゴリズム一覧の読み込みエラー
**Given**: Dashboardコンポーネントがマウントされる  
**When**: `get_selected_algorithms()`がエラーを返す  
**Then**: 
- エラーメッセージが表示される
- ユーザーは再試行できる

#### TC-006: アルゴリズムカードの表示
**Given**: アルゴリズム一覧が読み込まれている  
**When**: アルゴリズムが存在する  
**Then**: 
- アルゴリズム名が表示される
- 説明が表示される（存在する場合）
- パフォーマンス指標が表示される（存在する場合）

#### TC-007: 空状態の表示
**Given**: Dashboardコンポーネントがマウントされる  
**When**: アルゴリズムが存在しない  
**Then**: 
- 適切なメッセージが表示される（例: "No algorithms selected. Please generate algorithm proposals first."）

### Phase 3

#### TC-008: バックテスト結果の読み込み
**Given**: アルゴリズム一覧が読み込まれている  
**When**: `get_backtest_results_summary()`が成功する  
**Then**: 
- 各アルゴリズムの最新バックテスト結果が表示される
- パフォーマンス指標が表示される

#### TC-009: バックテスト結果の読み込みエラー
**Given**: アルゴリズム一覧が読み込まれている  
**When**: `get_backtest_results_summary()`がエラーを返す  
**Then**: 
- エラーメッセージが表示される
- アルゴリズム一覧は引き続き表示される

### Phase 4

#### TC-010: アルゴリズム削除
**Given**: アルゴリズム一覧が表示されている  
**When**: ユーザーが削除ボタンをクリックする  
**And**: 削除確認ダイアログで確認する  
**Then**: 
- `delete_algorithm()`が正しい`algo_id`で呼び出される
- アルゴリズムが一覧から削除される
- 成功メッセージが表示される

#### TC-011: アルゴリズム削除のキャンセル
**Given**: アルゴリズム一覧が表示されている  
**When**: ユーザーが削除ボタンをクリックする  
**And**: 削除確認ダイアログでキャンセルする  
**Then**: 
- アルゴリズムは削除されない
- ダイアログが閉じられる

#### TC-012: ナビゲーション
**Given**: Dashboardコンポーネントがマウントされる  
**When**: ユーザーがサイドバーのリンクをクリックする  
**Then**: 
- 適切なページに遷移する（現在はstateベースのナビゲーション）

## Component Structure

```
Dashboard
├── AppShell
│   ├── Header
│   │   └── App Name
│   ├── Sidebar
│   │   ├── Dashboard Link
│   │   ├── Algorithm Proposal Link
│   │   ├── Backtest Link
│   │   ├── Data Management Link
│   │   └── Data Analysis Link
│   └── Main Content
│       ├── AlgorithmList
│       │   └── AlgorithmCard[] (Grid)
│       └── ResultSummary
│           └── PerformanceCard[]
```

## State Management

```typescript
interface DashboardState {
  algorithms: Algorithm[];
  backtestResults: BacktestResultSummary[];
  loading: boolean;
  error: string | null;
  selectedAlgorithmId: number | null;
}
```

## API Integration

### Tauri Commands

#### `get_selected_algorithms()`
- **Purpose**: 選択済みアルゴリズム一覧を取得
- **Response**: `{ algorithms: Algorithm[] }`
- **Error Handling**: エラー時はエラーメッセージを表示

#### `get_backtest_results_summary(algorithm_ids?: number[], limit?: number)`
- **Purpose**: 複数のアルゴリズムの最新バックテスト結果を取得
- **Request**: `{ algorithm_ids?: number[], limit?: number }`
- **Response**: `{ results: BacktestResultSummary[] }`
- **Error Handling**: エラー時はエラーメッセージを表示

#### `delete_algorithm(algo_id: number)`
- **Purpose**: アルゴリズムを削除
- **Request**: `{ algo_id: number }`
- **Response**: `{ success: boolean, message?: string }`
- **Error Handling**: エラー時はエラーメッセージを表示

## Dependencies

### External Dependencies
- `@tauri-apps/api/core` - Tauriコマンド呼び出し
- `@mantine/core` - UIコンポーネント（AppShell, Grid, Card, Dialog等）
- `zustand` - 状態管理
- `src/types/dashboard` - Dashboard型定義
- `src/types/algorithm` - Algorithm型定義
- `src/types/backtest` - PerformanceMetrics型定義

### Internal Dependencies
- `Sidebar` - サイドバーナビゲーションコンポーネント
- `Header` - ヘッダーコンポーネント
- `AlgorithmList` - アルゴリズム一覧コンポーネント
- `AlgorithmCard` - アルゴリズムカードコンポーネント
- `ResultSummary` - 検証結果サマリーコンポーネント
- `PerformanceCard` - パフォーマンス指標カードコンポーネント
- `QuickActions` - クイックアクションコンポーネント
- `src/stores/dashboard` - Dashboard用Zustand store

