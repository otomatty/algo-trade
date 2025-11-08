# バックテスト機能 実装計画

## 概要

ユーザーが選択したアルゴリズムをバックテストで検証する機能です。バックテスト設定画面と結果表示画面の2つで構成されます。

## 関連ドキュメント

- **要件定義**: `docs/01_issues/open/2025_11/20251101_01_trend-association-algorithm-platform.md` (SCREEN-003, SCREEN-004)
- **仕様書**: 
  - `src/pages/BacktestSettings/BacktestSettings.spec.md` (作成予定)
  - `src/pages/BacktestResults/BacktestResults.spec.md` (作成予定)
- **テスト**: 
  - `src/pages/BacktestSettings/BacktestSettings.test.tsx` (作成予定)
  - `src/pages/BacktestResults/BacktestResults.test.tsx` (作成予定)

## 実装フェーズ

### Phase 1: バックテスト設定画面（基本UI）

**目標**: バックテスト設定画面の基本レイアウトを実装

**タスク**:
- [ ] アルゴリズム選択UIの実装
- [ ] 日付範囲選択UIの実装（DatePicker）
- [ ] データセット選択UIの実装
- [ ] 実行ボタンの実装
- [ ] バリデーション処理の実装

**技術スタック**:
- React 19.x
- TypeScript 5.x
- Mantine UI (DatePicker, Select)
- React Hook Form (バリデーション)

**依存関係**:
- アルゴリズム管理機能
- データ管理機能

### Phase 2: バックテスト実行（バックエンド）

**目標**: バックテストエンジンの実装

**タスク**:
- [ ] `run_backtest()` Tauriコマンドの実装
- [ ] バックテストエンジンの実装（Python）
- [ ] アルゴリズム定義のパース処理
- [ ] 取引シミュレーションロジックの実装
- [ ] パフォーマンス指標計算の実装

**技術スタック**:
- Python 3.10+
- Pandas, NumPy
- PyTauri

**依存関係**:
- Phase 1完了
- アルゴリズム定義スキーマ確定

### Phase 3: バックテストジョブ管理

**目標**: 非同期バックテストジョブの管理

**タスク**:
- [ ] `get_backtest_status()` Tauriコマンドの実装
- [ ] ジョブ管理システムの実装（バックエンド）
- [ ] ポーリング機能の実装（フロントエンド）
- [ ] 進捗表示の実装

**技術スタック**:
- Python threading / asyncio
- React useEffect / setInterval

**依存関係**:
- Phase 2完了

### Phase 4: バックテスト結果表示（基本）

**目標**: バックテスト結果の基本表示

**タスク**:
- [ ] `get_backtest_results()` Tauriコマンドの実装
- [ ] 結果画面の基本レイアウト
- [ ] パフォーマンス指標の表示（カード形式）
- [ ] 取引履歴テーブルの実装

**技術スタック**:
- Mantine Card, Table
- Tauri invoke API

**依存関係**:
- Phase 3完了

### Phase 5: チャート可視化

**目標**: バックテスト結果のチャート表示

**タスク**:
- [ ] 資産推移チャートの実装
- [ ] エントリー/エグジットポイントの可視化
- [ ] チャートライブラリの統合（ECharts / Lightweight Charts）

**技術スタック**:
- ECharts / Lightweight Charts
- React chart components

**依存関係**:
- Phase 4完了

### Phase 6: 結果詳細表示

**目標**: 詳細な分析結果の表示

**タスク**:
- [ ] 取引詳細モーダルの実装
- [ ] パフォーマンス分析の詳細表示
- [ ] エクスポート機能の実装（CSV, PDF等）

**技術スタック**:
- Mantine Modal
- CSV/PDF生成ライブラリ

**依存関係**:
- Phase 5完了

## 技術的な詳細

### コンポーネント構造

```
BacktestSettings/
├── BacktestSettings.tsx      # メインコンポーネント
├── AlgorithmSelector.tsx      # アルゴリズム選択
├── DateRangePicker.tsx        # 日付範囲選択
├── DataSetSelector.tsx       # データセット選択
└── BacktestSettings.spec.md  # 仕様書

BacktestResults/
├── BacktestResults.tsx       # メインコンポーネント
├── PerformanceMetrics.tsx     # パフォーマンス指標
├── TradeHistory.tsx           # 取引履歴
├── EquityChart.tsx            # 資産推移チャート
├── EntryExitChart.tsx         # エントリー/エグジットチャート
└── BacktestResults.spec.md   # 仕様書
```

### 状態管理

```typescript
interface BacktestSettingsState {
  selectedAlgorithmIds: number[];
  startDate: string;
  endDate: string;
  dataSetId: number | null;
  validationErrors: Record<string, string>;
}

interface BacktestResultsState {
  jobId: string | null;
  status: 'idle' | 'running' | 'completed' | 'error';
  progress: number;
  results: BacktestResult | null;
  loading: boolean;
  error: string | null;
}
```

### バックテストエンジン設計

```python
class BacktestEngine:
    def __init__(self, algorithm, data, start_date, end_date):
        self.algorithm = algorithm
        self.data = data
        self.start_date = start_date
        self.end_date = end_date
        
    def run(self):
        # 1. データフィルタリング
        # 2. アルゴリズム実行
        # 3. 取引シミュレーション
        # 4. パフォーマンス計算
        # 5. 結果返却
        pass
```

### API連携

- `run_backtest(params)`: バックテスト実行開始
- `get_backtest_status(job_id)`: 進捗状況取得
- `get_backtest_results(job_id)`: 結果取得
- `get_data_list()`: データセット一覧取得
- `get_selected_algorithms()`: アルゴリズム一覧取得

## テスト計画

### 単体テスト

- [ ] BacktestSettingsコンポーネントのテスト
- [ ] BacktestResultsコンポーネントのテスト
- [ ] バックテストエンジンのテスト
- [ ] パフォーマンス指標計算のテスト

### 統合テスト

- [ ] バックテスト実行フローの統合テスト
- [ ] ジョブ管理の統合テスト
- [ ] 結果取得と表示の統合テスト

### E2Eテスト

- [ ] バックテスト実行のE2Eテスト
- [ ] 結果表示のE2Eテスト

## 実装優先度

**最高**: Phase 1, Phase 2, Phase 3（核心機能）
**高**: Phase 4（必須機能）
**中**: Phase 5, Phase 6（可視化・詳細機能）

## 注意事項

- バックテストのパフォーマンス最適化（大量データ処理）
- メモリ使用量の管理
- エラーハンドリング（データ不足、日付範囲エラー等）
- チャートのレスポンシブ対応
- 取引履歴のページネーション（大量データ対応）

