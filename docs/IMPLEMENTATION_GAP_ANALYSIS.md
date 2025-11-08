# 実装計画と実装状況の差分分析

## 概要

本ドキュメントは、実装計画（`docs/03_plans/`）と現在の実装状況の差分を分析したものです。
調査日: 2025年11月8日（最新更新: 2025年11月8日）

**最新更新**: バックテスト Phase 1-6 実装完了（2025年11月8日）

---

## 1. データ収集（Data Collection）バックエンド

### 実装計画のPhase

- **Phase 1: CSVインポート処理** ✅ **完了**
- **Phase 2: 外部API連携基盤** ✅ **完了**
- **Phase 3: 主要データソース実装** ✅ **完了**
- **Phase 4: 自動収集スケジューラー** ❌ **未実装**
- **Phase 5: データ更新・差分管理** ❌ **未実装**

### 実装状況

#### ✅ 実装済み
- CSVパーサー (`csv_importer.py`)
- データバリデーション
- データ正規化処理
- データベース保存処理
- HTTPクライアント基盤 (`api_clients.py`)
- Yahoo Finance APIクライアント
- Alpha Vantage APIクライアント
- `collect_from_api()` Tauriコマンド (`src-tauri/src/lib.rs`)
- レート制限対応
- エラーハンドリング

#### ❌ 未実装
- 自動収集スケジューラー（APScheduler）
- スケジュール設定の保存・読み込み
- ジョブ管理機能
- エラー通知機能
- データ更新チェック機能
- 差分データの取得・適用処理
- データ整合性チェック機能

### 差分サマリー

**完了率**: 60% (3/5 Phase完了)

**次の優先タスク**:
1. 自動収集スケジューラーの実装（Phase 4）
2. データ更新・差分管理機能の実装（Phase 5）

---

## 2. データ管理（Data Management）フロントエンド

### 実装計画のPhase

- **Phase 1: CSVインポート機能** ✅ **完了**
- **Phase 2: データセット一覧表示** ✅ **完了**
- **Phase 3: データ削除機能** ✅ **完了**
- **Phase 4: 外部API自動収集設定** ❌ **未実装**
- **Phase 5: データプレビュー機能** ❌ **未実装**

### 実装状況

#### ✅ 実装済み
- ファイル選択UI (`DataImportForm.tsx`)
- `import_ohlcv_data()` Tauriコマンド
- CSVパース処理（バックエンド）
- データバリデーション（バックエンド）
- インポート進捗表示（基本的な実装）
- エラーハンドリング
- `get_data_list()` Tauriコマンド
- データセット一覧テーブル (`DataManagement.tsx`)
- 削除ボタン
- 削除確認ダイアログ（`confirm()`使用）
- `delete_data_set()` Tauriコマンド

#### ❌ 未実装
- `configure_data_collection()` Tauriコマンド
- API設定フォーム (`APIConfigForm.tsx`)
- スケジュール設定UI
- 設定保存機能
- データプレビューモーダル (`DataPreviewModal.tsx`)
- データテーブル表示（プレビュー用）
- 基本統計情報の表示
- データセット情報カード (`DataSetCard.tsx`) - 計画にはあるが未実装
- ソート・フィルタ機能

### 差分サマリー

**完了率**: 60% (3/5 Phase完了)

**次の優先タスク**:
1. データプレビュー機能の実装（Phase 5）
2. 外部API自動収集設定UIの実装（Phase 4）

---

## 3. データ解析（Data Analysis）

### 実装計画のPhase

- **Phase 1: 解析ジョブ実行UI** ✅ **完了**
- **Phase 2: 解析エンジン実装（バックエンド）** ✅ **完了**
- **Phase 3: 進捗表示機能** ✅ **完了**
- **Phase 4: 解析結果表示** ✅ **完了**
- **Phase 5: 結果可視化** ✅ **完了**
- **Phase 6: アルゴリズム提案への遷移** ⚠️ **部分的実装**（アルゴリズム提案機能は完了したが、遷移機能は未実装）

### 実装状況

#### ✅ 実装済み
- 型定義 (`src/types/analysis.ts`)
- モジュールディレクトリ構造 (`src-python/modules/data_analysis/`)
- **データセット選択UI** (`AnalysisJobForm.tsx`)
- **解析実行ボタン** (`AnalysisJobForm.tsx`)
- **`run_data_analysis()` Tauriコマンド** (`src-tauri/src/lib.rs`)
- **`get_analysis_status()` Tauriコマンド** (`src-tauri/src/lib.rs`)
- **`get_analysis_results()` Tauriコマンド** (`src-tauri/src/lib.rs`)
- **トレンド分析ロジック** (`trend_analyzer.py`)
- **テクニカル指標計算** (`technical_indicators.py` - RSI, MACD, ボリンジャーバンド等)
- **統計情報計算** (`statistics.py`)
- **解析結果の構造化** (`analyzer.py`)
- **ジョブ管理システム** (`run_data_analysis.py`, `get_analysis_status.py`)
- **進捗表示UI** (`AnalysisProgress.tsx`)
- **解析結果表示コンポーネント** (`AnalysisResults.tsx`)
- **チャート可視化** (`DataAnalysisCharts.tsx` - Recharts使用)
- **トレンド分析表示** (`TrendAnalysis.tsx`)
- **テクニカル指標表示** (`TechnicalIndicators.tsx`)
- **統計情報表示** (`Statistics.tsx`)
- **Pythonスクリプト** (`run_data_analysis.py`, `get_analysis_status.py`, `get_analysis_results.py`)
- **テストファイル** (`DataAnalysis.test.tsx`, `AnalysisJobForm.test.tsx`, `AnalysisProgress.test.tsx`, `DataAnalysisCharts.test.tsx`)

#### ❌ 未実装
- Phase 6: アルゴリズム提案への遷移機能
  - `handleNavigateToProposal` はTODOコメントのみ（`DataAnalysis.tsx`）
  - `AlgorithmProposalNavigation.spec.md`は存在するが、実装は未完了（TODOコメントのみ）
  - アルゴリズム提案機能自体は完了しているが、データ解析画面からの遷移機能は未実装

### 差分サマリー

**完了率**: 83% (5/6 Phase完了、Phase 6は部分的実装)

**次の優先タスク**:
1. Phase 6: アルゴリズム提案への遷移機能の実装（アルゴリズム提案機能は完了しているため、遷移機能のみ実装すれば完了）

---

## 4. LLM連携（LLM Integration）バックエンド

### 実装計画のPhase

- **Phase 1: LLM APIクライアント基盤** ✅ **完了**
- **Phase 2: プロンプトエンジニアリング** ✅ **完了**
- **Phase 3: レスポンスパース処理** ✅ **完了**
- **Phase 4: ストリーミング対応** ❌ **未実装**（オプション）
- **Phase 5: コスト管理・最適化** ❌ **未実装**

### 実装状況

#### ✅ 実装済み
- モジュールディレクトリ構造 (`src-python/modules/llm_integration/`)
- 依存関係の定義 (`requirements.txt`にopenai, anthropic等)
- **カスタム例外クラス** (`exceptions.py` - LLMError, APIKeyError, RateLimitError, APIError, TimeoutError, ParseError)
- **APIキー管理機能** (`api_key_manager.py` - 環境変数からの読み込み、.envファイル対応)
- **LLMクライアント基盤** (`client.py` - 抽象基底クラス、リトライ機構、エラーハンドリング)
- **OpenAI APIクライアント** (`openai_client.py` - GPT-4, GPT-3.5-turbo対応)
- **Anthropic APIクライアント** (`anthropic_client.py` - Claude-3-Opus, Claude-3-Sonnet対応)
- **プロンプトテンプレート管理** (`prompt_templates.py` - テンプレート読み込み、バージョン管理、バリデーション)
- **プロンプト生成ロジック** (`prompt_builder.py` - アルゴリズム提案用、銘柄予測用プロンプト生成)
- **プロンプトテンプレート** (`templates/algorithm_proposal.txt`, `templates/stock_prediction.txt`)
- **Pydanticスキーマ定義** (`schemas.py` - AlgorithmProposalResponse, StockPredictionResponse等)
- **レスポンスパーサー** (`response_parser.py` - JSONパース、スキーマバリデーション、マークダウンコードブロック対応)
- **フォールバック処理** (`fallback_handler.py` - パース失敗時の処理、部分データ抽出)
- **単体テスト** (`test_llm_client.py`, `test_api_key_manager.py`, `test_prompt_builder.py`, `test_response_parser.py`)
- **統合テスト** (`test_llm_integration.py`)

#### ❌ 未実装
- ストリーミング対応（Phase 4 - オプション）
- トークン数計算（Phase 5）
- コスト追跡機能（Phase 5）
- プロンプト最適化（Phase 5）
- キャッシュ機能（Phase 5）

### 差分サマリー

**完了率**: 60% (3/5 Phase完了、Phase 4はオプション)

**次の優先タスク**:
1. Phase 5: コスト管理・最適化の実装（トークン数計算、コスト追跡、キャッシュ機能）
2. Phase 4: ストリーミング対応の実装（オプション、将来拡張）

---

## 5. アルゴリズム提案（Algorithm Proposal）

### 実装計画のPhase

- **Phase 1: 基本UI構築** ✅ **完了** (2025年11月8日)
- **Phase 2: データ解析結果取得** ✅ **完了** (2025年11月8日)
- **Phase 3: LLM連携（バックエンド）** ✅ **完了** (2025年11月8日)
- **Phase 4: 提案生成ジョブ管理** ✅ **完了** (2025年11月8日)
- **Phase 5: 提案一覧表示** ✅ **完了** (2025年11月8日)
- **Phase 6: アルゴリズム選択機能** ✅ **完了** (2025年11月8日)

### 実装状況

#### ✅ 実装済み
- 型定義 (`src/types/algorithm.ts`)
- **Phase 1: 基本UI構築**
  - メインコンポーネント (`AlgorithmProposal.tsx`)
  - 提案生成フォーム (`ProposalGenerationForm.tsx`)
    - データセット選択機能
    - ユーザー設定入力（リスク許容度、取引頻度、好みの指標）
    - 提案数指定機能
    - エラーハンドリング
  - 提案一覧コンポーネント (`ProposalList.tsx`)
  - 進捗表示コンポーネント (`ProgressIndicator.tsx`)
  - 仕様書 (`AlgorithmProposal.spec.md`)
  - テストファイル (`AlgorithmProposal.test.tsx` - 10テストケース、全て通過)
- **Phase 2: データ解析結果取得**
  - `get_latest_analysis_results()` Tauriコマンド (`src-tauri/src/lib.rs`)
  - `get_latest_analysis_results.py` スクリプト
  - データセット選択時の解析結果取得機能 (`ProposalGenerationForm.tsx`)
  - テストファイル（4テストケース、全て通過）
- **Phase 3: LLM連携（バックエンド）**
  - `generate_algorithm_proposals()` Tauriコマンド (`src-tauri/src/lib.rs`)
  - `generate_algorithm_proposals.py` スクリプト
  - `proposal_generator.py` モジュール
  - `job_manager.py` モジュール
  - LLM API連携（OpenAI/Anthropic）
  - プロンプト生成・レスポンスパース処理
  - テストファイル（proposal_generator: 4テストケース、job_manager: 3テストケース、全て通過）
- **Phase 4: 提案生成ジョブ管理**
  - `get_proposal_generation_status()` Tauriコマンド (`src-tauri/src/lib.rs`)
  - `get_proposal_generation_status.py` スクリプト
  - 進捗表示コンポーネント (`ProgressIndicator.tsx` - ポーリング機能含む）
  - テストファイル（ProgressIndicator: 4テストケース、get_proposal_generation_status: 4テストケース、全て通過）
- **Phase 5: 提案一覧表示**
  - `get_algorithm_proposals()` Tauriコマンド (`src-tauri/src/lib.rs`)
  - `get_algorithm_proposals.py` スクリプト
  - 提案カードコンポーネント (`ProposalCard.tsx`)
  - 提案詳細モーダル (`ProposalDetailModal.tsx`)
  - 提案一覧表示機能 (`ProposalList.tsx`)
  - `react-markdown`依存関係追加
  - テストファイル（ProposalCard: 9テストケース、ProposalList: 4テストケース、ProposalDetailModal: 10テストケース、get_algorithm_proposals: 3テストケース、全て通過）
- **Phase 6: アルゴリズム選択機能**
  - `select_algorithm()` Tauriコマンド (`src-tauri/src/lib.rs`)
  - `select_algorithm.py` スクリプト
  - 選択確認ダイアログ (`SelectAlgorithmDialog.tsx`)
  - 選択機能統合 (`ProposalList.tsx`)
  - カスタム名入力機能
  - 成功/失敗通知機能
  - テストファイル（バックエンド: 4テストケース、フロントエンド: SelectAlgorithmDialog 11テストケース、ProposalList 3テストケース追加、全て通過）

#### ❌ 未実装
- なし（全てのPhaseが完了）

### 差分サマリー

**完了率**: 100% (6/6 Phase完了)

**次の優先タスク**:
1. アルゴリズム提案機能は完了。次はバックテスト機能の実装に着手

---

## 6. バックテスト（Backtest）

### 実装計画のPhase

- **Phase 1: バックテスト設定画面（基本UI）** ✅ **完了** (2025年11月8日)
- **Phase 2: バックテスト実行（バックエンド）** ✅ **完了** (2025年11月8日)
- **Phase 3: バックテストジョブ管理** ✅ **完了** (2025年11月8日)
- **Phase 4: バックテスト結果表示（基本）** ✅ **完了** (2025年11月8日)
- **Phase 5: チャート可視化** ✅ **完了** (2025年11月8日)
- **Phase 6: 結果詳細表示** ✅ **完了** (2025年11月8日)

### 実装状況

#### ✅ 実装済み
- 型定義 (`src/types/backtest.ts`)
- モジュールディレクトリ構造 (`src-python/modules/backtest/`)
- **Phase 1: バックテスト設定画面（基本UI）**
  - `get_selected_algorithms()` Tauriコマンド (`src-tauri/src/lib.rs`)
  - `get_selected_algorithms.py` スクリプト
  - メインコンポーネント (`BacktestSettings.tsx`)
  - アルゴリズム選択コンポーネント (`AlgorithmSelector.tsx`)
  - データセット選択コンポーネント (`DataSetSelector.tsx`)
  - 日付範囲選択UI（Mantine DatePickerInput）
  - バリデーション処理
  - 仕様書 (`BacktestSettings.spec.md`)
  - テストファイル (`BacktestSettings.test.tsx`)
- **Phase 2: バックテスト実行（バックエンド）**
  - `run_backtest()` Tauriコマンド (`src-tauri/src/lib.rs`)
  - `run_backtest.py` スクリプト
  - バックテストエンジン (`backtest_engine.py`)
  - アルゴリズムパーサー (`algorithm_parser.py`)
  - シグナル生成 (`signal_generator.py`)
  - 取引シミュレーション (`trade_simulator.py`)
  - パフォーマンス計算 (`performance_calculator.py`)
  - ジョブ管理システム (`job_manager.py`)
- **Phase 3: バックテストジョブ管理**
  - `get_backtest_status()` Tauriコマンド (`src-tauri/src/lib.rs`)
  - `get_backtest_status.py` スクリプト
  - 進捗表示コンポーネント (`BacktestProgress.tsx` - ポーリング機能含む）
- **Phase 4: バックテスト結果表示（基本）**
  - `get_backtest_results()` Tauriコマンド (`src-tauri/src/lib.rs`)
  - `get_backtest_results.py` スクリプト
  - 結果表示コンポーネント (`BacktestResults.tsx`)
  - パフォーマンス指標表示 (`PerformanceMetrics.tsx`)
  - 取引履歴テーブル (`TradeHistory.tsx`)
- **Phase 5: チャート可視化**
  - 資産推移チャート (`EquityChart.tsx` - Recharts使用)
  - エントリー/エグジットチャート (`EntryExitChart.tsx`)
- **Phase 6: 結果詳細表示**
  - 取引詳細モーダル (`TradeDetailModal.tsx`)
  - CSVエクスポート機能 (`ExportButton.tsx`)

#### ❌ 未実装
- なし（全てのPhaseが完了）

### 差分サマリー

**完了率**: 100% (6/6 Phase完了)

**次の優先タスク**:
1. バックテスト機能は完了。次はダッシュボード機能の実装に着手

---

## 7. ダッシュボード（Dashboard）

### 実装計画のPhase

- **Phase 1: 基本レイアウト構築** ❌ **未実装**
- **Phase 2: アルゴリズム一覧表示** ❌ **未実装**
- **Phase 3: 検証結果サマリー表示** ❌ **未実装**
- **Phase 4: クイックアクション** ❌ **未実装**

### 実装状況

#### ✅ 実装済み
- なし（完全に未実装）

#### ❌ 未実装
- すべてのPhaseが未実装
- レイアウトコンポーネント
- サイドバーナビゲーション
- ヘッダーコンポーネント
- `get_selected_algorithms()` Tauriコマンド
- アルゴリズム一覧コンポーネント
- アルゴリズムカードコンポーネント
- `get_backtest_results()` Tauriコマンド
- 検証結果サマリーコンポーネント
- パフォーマンス指標の可視化
- `delete_algorithm()` Tauriコマンド
- アクションボタンコンポーネント

### 差分サマリー

**完了率**: 0% (0/4 Phase完了)

**依存関係**: アルゴリズム管理機能とバックテスト機能の実装が必要

**次の優先タスク**:
1. Phase 1: 基本レイアウト構築から開始（他の機能と並行して実装可能）

---

## 8. ニュース収集（News Collection）バックエンド

### 実装計画のPhase

- **Phase 1: RSSフィードパーサー** ❌ **未実装**
- **Phase 2: ニュースAPIクライアント** ❌ **未実装**
- **Phase 3: Webスクレイピング** ❌ **未実装**（オプション）
- **Phase 4: ニュースデータベース保存** ❌ **未実装**
- **Phase 5: センチメント分析** ❌ **未実装**（オプション）
- **Phase 6: 自動収集スケジューラー** ❌ **未実装**

### 実装状況

#### ✅ 実装済み
- モジュールディレクトリ構造 (`src-python/modules/news_collection/`)
- 依存関係の定義 (`requirements.txt`にfeedparser, beautifulsoup4等)

#### ❌ 未実装
- すべてのPhaseが未実装
- RSSフィードパーサー
- ニュースAPIクライアント（NewsAPI, Alpha Vantage等）
- Webスクレイピング機能
- ニュースデータベーススキーマ
- データベース保存処理
- 重複チェック機能
- センチメント分析
- 自動収集スケジューラー

### 差分サマリー

**完了率**: 0% (0/6 Phase完了、Phase 3と5はオプション)

**次の優先タスク**:
1. Phase 1: RSSフィードパーサーの実装
2. Phase 2: ニュースAPIクライアントの実装
3. Phase 4: ニュースデータベース保存の実装

---

## 9. 銘柄予測（Stock Prediction）

### 実装計画のPhase

- **Phase 1: ニュース収集機能（バックエンド）** ❌ **未実装**
- **Phase 2: ニュース収集UI** ❌ **未実装**
- **Phase 3: ニュース表示機能** ❌ **未実装**
- **Phase 4: LLM銘柄予測生成（バックエンド）** ❌ **未実装**
- **Phase 5: 予測生成UI** ❌ **未実装**
- **Phase 6: 予測結果表示** ❌ **未実装**
- **Phase 7: アクション提案機能** ❌ **未実装**
- **Phase 8: 予測履歴・精度追跡** ❌ **未実装**

### 実装状況

#### ✅ 実装済み
- 型定義 (`src/types/stock-prediction.ts`, `src/types/news.ts`)

#### ❌ 未実装
- すべてのPhaseが未実装
- ニュース収集機能（バックエンド）
- ニュース収集UI
- ニュース表示機能
- LLM銘柄予測生成（バックエンド）
- 予測生成UI
- 予測結果表示
- アクション提案機能
- 予測履歴・精度追跡

### 差分サマリー

**完了率**: 0% (0/8 Phase完了)

**依存関係**: ニュース収集機能とLLM連携機能の実装が必要

**次の優先タスク**:
1. ニュース収集機能とLLM連携機能の実装完了後、Phase 1から開始

---

## 全体サマリー

### 実装完了率（Phase単位）

| 機能 | 完了Phase | 総Phase数 | 完了率 |
|------|----------|----------|--------|
| データ収集（バックエンド） | 3 | 5 | 60% |
| データ管理（フロントエンド） | 3 | 5 | 60% |
| データ解析 | 5 | 6 | 83% |
| LLM連携（バックエンド） | 3 | 5 | 60% |
| アルゴリズム提案 | 6 | 6 | 100% |
| バックテスト | 6 | 6 | 100% |
| ダッシュボード | 0 | 4 | 0% |
| ニュース収集（バックエンド） | 0 | 6 | 0% |
| 銘柄予測 | 0 | 8 | 0% |

**全体完了率**: 約53% (27/51 Phase完了)

**注意**: 上記の完了率は機能別のPhase完了率のみを計算しており、ナビゲーションシステムなどの基盤機能は含まれていない。ナビゲーションシステムが未実装のため、現在は`App.tsx`で直接ページを切り替える必要がある。

### 実装優先度（推奨順序）

1. **ダッシュボード** - メイン画面（他の機能と並行実装可能）
2. **ニュース収集** - 銘柄予測の前提機能
3. **銘柄予測** - 連想ゲーム機能
4. **データ収集・管理の拡張** - Phase 4, 5の実装
5. **LLM連携の拡張** - ストリーミング対応、コスト管理・最適化（Phase 4, 5）
6. **データ解析の拡張** - Phase 6（アルゴリズム提案への遷移機能）

### 重要な未実装機能

#### 基盤機能
- **ナビゲーションシステム** - ルーティングシステムが未実装のため、現在は`App.tsx`で直接ページを切り替えている

#### バックエンド
- ニュース収集機能
- LLM連携の拡張機能（ストリーミング対応、コスト管理）

#### フロントエンド
- ダッシュボード
- 銘柄予測UI

### 依存関係マップ

```
データ管理 ✅
    ↓
データ解析 ✅ → アルゴリズム提案 ✅ → バックテスト ✅
    ↓                    ↓
LLM連携 ✅ ────────────┘
    ↓
ニュース収集 ❌ → 銘柄予測 ❌
    ↓
ダッシュボード ❌（他の機能と並行実装可能）
```

### 次のアクションアイテム

1. **即座に着手すべき**:
   - ダッシュボード機能の実装（バックテスト機能が完了したため）

2. **短期（1-2週間）**:
   - ダッシュボードの基本実装
   - データ解析からアルゴリズム提案への遷移機能の実装（データ解析 Phase 6）

3. **中期（1ヶ月）**:
   - ダッシュボードの完成
   - ニュース収集機能の基本実装

4. **長期（2-3ヶ月）**:
   - ニュース収集と銘柄予測機能の実装
   - データ収集・管理の拡張機能

---

## 注意事項

- 仕様書（`.spec.md`）が未作成の機能が多いため、実装前に仕様書の作成を推奨
- テストファイル（`.test.tsx`）も未作成のため、TDDの原則に従ってテストを先に作成することを推奨
- ジョブ管理システムは複数の機能で必要になるため、共通化を検討すべき
- **ナビゲーションシステムの実装が必要**: 現在は`App.tsx`で直接`DataAnalysis`を表示しており、ルーティングシステムが未実装。ページ間の遷移は実装されていないため、各機能へのアクセスには`App.tsx`の直接編集が必要。
- **実装ガイドライン**: 
  - アルゴリズム提案機能の実装方法については、`docs/03_plans/algorithm-proposal/IMPLEMENTATION_GUIDE.md` を参照してください。**Phase 1-6は全て完了しています。**
  - バックテスト機能の実装方法については、`docs/03_plans/backtest/README.md` を参照してください。**Phase 1-6は全て完了しています。**

## テストカバレッジ

**全体カバレッジ**: 92% (2,103ステートメント中174未カバー)

**主要モジュールのカバレッジ**:
- LLM連携モジュール: 平均 75% (exceptions: 100%, schemas: 100%, api_key_manager: 97%, clients: 95%)
- データ解析モジュール: 平均 88% (statistics: 100%, analyzer: 84%, technical_indicators: 90%)
- データ収集モジュール: 平均 93% (csv_importer: 94%, api_clients: 91%)
- バックテストモジュール: 実装完了（テストカバレッジは今後測定予定）

**詳細**: `src-python/htmlcov/index.html` を参照してください。

