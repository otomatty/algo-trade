# ダッシュボード機能 実装計画

## 概要

ダッシュボードは、アプリケーションのメイン画面として、ユーザーが選択したアルゴリズムの一覧と最新の検証結果サマリーを表示する機能です。

## 関連ドキュメント

- **要件定義**: `docs/01_issues/open/2025_11/20251101_01_trend-association-algorithm-platform.md` (SCREEN-001)
- **仕様書**: `src/pages/Dashboard/Dashboard.spec.md` (作成予定)
- **テスト**: `src/pages/Dashboard/Dashboard.test.tsx` (作成予定)

## 実装フェーズ

### Phase 1: 基本レイアウト構築

**目標**: ダッシュボードの基本レイアウトとナビゲーションを実装

**タスク**:
- [ ] Mantineを使用したレイアウトコンポーネントの作成
- [ ] サイドバーナビゲーションの実装
- [ ] ヘッダーコンポーネントの実装
- [ ] レスポンシブデザインの対応

**技術スタック**:
- React 19.x
- TypeScript 5.x
- Mantine UI
- Zustand (状態管理)

**依存関係**:
- なし（最初に実装する画面）

### Phase 2: アルゴリズム一覧表示

**目標**: 選択済みアルゴリズムの一覧を表示

**タスク**:
- [ ] `get_selected_algorithms()` Tauriコマンドの実装（バックエンド）
- [ ] アルゴリズム一覧コンポーネントの作成
- [ ] アルゴリズムカードコンポーネントの作成
- [ ] データ取得と状態管理の実装

**技術スタック**:
- Tauri invoke API
- Zustand store

**依存関係**:
- Phase 1完了
- バックエンド: アルゴリズム管理コマンド実装

### Phase 3: 検証結果サマリー表示

**目標**: 各アルゴリズムの最新検証結果を表示

**タスク**:
- [ ] `get_backtest_results()` Tauriコマンドの実装（バックエンド）
- [ ] 検証結果サマリーコンポーネントの作成
- [ ] パフォーマンス指標の可視化（カード形式）
- [ ] チャートライブラリの統合準備

**技術スタック**:
- ECharts / Lightweight Charts
- Tauri invoke API

**依存関係**:
- Phase 2完了
- バックエンド: バックテスト結果取得コマンド実装

### Phase 4: クイックアクション

**目標**: アルゴリズムの削除、アルゴリズム提案画面への遷移など

**タスク**:
- [ ] アクションボタンコンポーネントの作成
- [ ] `delete_algorithm()` Tauriコマンドの実装（バックエンド）
- [ ] 削除確認ダイアログの実装
- [ ] ナビゲーション統合

**技術スタック**:
- Mantine Dialog
- React Router (またはTauriのナビゲーション)

**依存関係**:
- Phase 2完了
- バックエンド: アルゴリズム削除コマンド実装

## 技術的な詳細

### コンポーネント構造

```
Dashboard/
├── Dashboard.tsx          # メインコンポーネント
├── AlgorithmList.tsx      # アルゴリズム一覧
├── AlgorithmCard.tsx      # アルゴリズムカード
├── ResultSummary.tsx      # 検証結果サマリー
├── QuickActions.tsx      # クイックアクション
└── Dashboard.spec.md     # 仕様書
```

### 状態管理

```typescript
interface DashboardState {
  algorithms: Algorithm[];
  backtestResults: BacktestResult[];
  loading: boolean;
  error: string | null;
}
```

### API連携

- `get_selected_algorithms()`: 選択済みアルゴリズム一覧取得
- `get_backtest_results()`: 最新の検証結果取得
- `delete_algorithm(algo_id)`: アルゴリズム削除

## テスト計画

### 単体テスト

- [ ] Dashboardコンポーネントのレンダリングテスト
- [ ] AlgorithmListコンポーネントのテスト
- [ ] AlgorithmCardコンポーネントのテスト
- [ ] ResultSummaryコンポーネントのテスト

### 統合テスト

- [ ] Tauriコマンド呼び出しのテスト
- [ ] データ取得と表示の統合テスト
- [ ] エラーハンドリングのテスト

### E2Eテスト

- [ ] ダッシュボード表示のE2Eテスト
- [ ] アルゴリズム削除のE2Eテスト

## 実装優先度

**高**: Phase 1, Phase 2（基本機能として最優先）
**中**: Phase 3（検証結果表示）
**低**: Phase 4（クイックアクション）

## 注意事項

- Mantineのテーマ設定を統一する
- レスポンシブデザインを考慮した実装
- エラーハンドリングとローディング状態の適切な表示
- アクセシビリティの考慮（ARIA属性等）

