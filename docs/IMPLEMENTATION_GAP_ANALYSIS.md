# 実装計画と実装状況の差分分析

## 概要

本ドキュメントは、実装計画（`docs/03_plans/`）と現在の実装状況の差分を分析したものです。
調査日: 2025年11月8日（最新更新: 2025年11月10日）

**最新更新**: ニュース収集機能 Phase 1, 2, 4, 6 実装完了（2025年11月9日）、銘柄予測機能 Phase 4, 5, 6 実装完了（2025年11月9日）、銘柄予測機能 Phase 7, 8 実装完了（2025年11月9日）、データ管理機能 Phase 5 実装完了（2025年11月9日）、データ収集機能 Phase 4, 5 実装完了（2025年11月9日）、データ管理機能 Phase 4 実装完了（2025年11月9日）、lib.rsのリファクタリング完了（2025年11月10日）、国際化対応（i18n）Phase 1 実装完了（2025年11月10日）、国際化対応（i18n）Phase 2 実装完了（2025年11月10日）

---

## 1. データ収集（Data Collection）バックエンド

### 実装計画のPhase

- **Phase 1: CSVインポート処理** ✅ **完了**
- **Phase 2: 外部API連携基盤** ✅ **完了**
- **Phase 3: 主要データソース実装** ✅ **完了**
- **Phase 4: 自動収集スケジューラー** ✅ **完了** (2025年11月9日)
- **Phase 5: データ更新・差分管理** ✅ **完了** (2025年11月9日)

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
- **Phase 4: 自動収集スケジューラー**
  - データベーススキーマ拡張 (`src-python/database/schema.py`)
    - `data_collection_schedules`テーブル作成
    - `data_collection_jobs`テーブル作成
    - インデックス作成
  - ジョブ管理モジュール (`src-python/modules/data_collection/job_manager.py`)
    - `DataCollectionJobManager`クラス実装
    - ジョブ作成・状態更新機能
    - 進捗管理機能
  - スケジューラーモジュール (`src-python/modules/data_collection/scheduler.py`)
    - `DataCollectionScheduler`クラス実装（APScheduler使用）
    - スケジュール設定の保存・読み込み
    - ジョブの登録・削除・一時停止・再開
    - エラー通知機能
  - Pythonスクリプト実装
    - `configure_data_collection.py` - スケジュール設定の保存・更新・削除
    - `get_data_collection_schedules.py` - スケジュール一覧取得
    - `get_data_collection_status.py` - ジョブ状態取得
  - Tauriコマンド実装 (`src-tauri/src/lib.rs`)
    - `configure_data_collection()` コマンド
    - `get_data_collection_schedules()` コマンド
    - `get_data_collection_status()` コマンド
- **Phase 5: データ更新・差分管理**
  - データ更新チェック機能 (`src-python/modules/data_collection/data_updater.py`)
    - `DataUpdater`クラス実装
    - 既存データセットの最新日付取得
    - 更新が必要かどうかの判定
  - 差分データ取得・適用処理 (`src-python/modules/data_collection/data_updater.py`)
    - 差分データの抽出ロジック
    - 差分データの適用処理（追加・更新）
    - トランザクション管理
  - データ整合性チェック機能 (`src-python/modules/data_collection/data_validator.py`)
    - `DataValidator`クラス実装
    - 日付の連続性チェック
    - 価格データの妥当性チェック
    - 重複データの検出
    - ボリュームデータの妥当性チェック
  - Pythonスクリプト実装
    - `update_data_set.py` - データセットの更新実行
    - `check_data_integrity.py` - データ整合性チェック
  - Tauriコマンド実装 (`src-tauri/src/lib.rs`)
    - `update_data_set()` コマンド
    - `check_data_integrity()` コマンド

#### ❌ 未実装
- なし（全てのPhaseが完了）

### 差分サマリー

**完了率**: 100% (5/5 Phase完了)

**次の優先タスク**:
1. データ収集機能は完了。次はLLM連携の拡張機能の実装に着手

---

## 2. データ管理（Data Management）フロントエンド

### 実装計画のPhase

- **Phase 1: CSVインポート機能** ✅ **完了**
- **Phase 2: データセット一覧表示** ✅ **完了**
- **Phase 3: データ削除機能** ✅ **完了**
- **Phase 4: 外部API自動収集設定** ✅ **完了** (2025年11月9日)
- **Phase 5: データプレビュー機能** ✅ **完了** (2025年11月9日)

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
- **Phase 5: データプレビュー機能**
  - `get_data_preview()` Tauriコマンド (`src-tauri/src/lib.rs`)
  - `get_data_preview.py` スクリプト（OHLCVデータ取得と統計計算）
  - データプレビューモーダル (`DataPreviewModal.tsx`)
  - データテーブル表示（プレビュー用）
  - 基本統計情報の表示（平均、最小、最大、標準偏差）
  - プレビューボタン統合 (`DataManagement.tsx`)
  - 型定義 (`DataPreview`インターフェース)
  - テストファイル（バックエンド・フロントエンド）
- **Phase 4: 外部API自動収集設定**
  - 型定義追加 (`src/types/data.ts`)
    - `DataCollectionSchedule`インターフェース
    - `DataCollectionJob`インターフェース
    - `ConfigureDataCollectionRequest`インターフェース
    - `ConfigureDataCollectionResponse`インターフェース
  - API設定フォーム (`src/pages/DataManagement/APIConfigForm.tsx`)
    - データソース選択（Yahoo Finance / Alpha Vantage）
    - シンボル入力
    - APIキー入力（Alpha Vantage用）
    - 日付範囲選択
    - データセット名入力
    - スケジュール設定（cron形式）
    - 有効/無効トグル
    - 編集機能
  - スケジュール一覧表示 (`src/pages/DataManagement/ScheduleList.tsx`)
    - スケジュール一覧テーブル表示
    - 編集・削除・有効/無効切り替えボタン
    - ジョブ状態表示
  - メインコンポーネント統合 (`src/pages/DataManagement/DataManagement.tsx`)
    - タブでデータセットとスケジュールを分離
    - API設定フォームとスケジュール一覧の統合
  - Tauriコマンド連携
    - `configure_data_collection()` コマンド呼び出し
    - `get_data_collection_schedules()` コマンド呼び出し

#### ❌ 未実装
- データセット情報カード (`DataSetCard.tsx`) - 計画にはあるが未実装
- ソート・フィルタ機能

### 差分サマリー

**完了率**: 100% (5/5 Phase完了)

**次の優先タスク**:
1. データ管理機能は完了。次はデータセット情報カードの実装（オプション）

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
- **Phase 6: アルゴリズム提案への遷移機能**
  - `handleNavigateToProposal` 実装完了（`DataAnalysis.tsx`）
  - `App.tsx`でナビゲーションパラメータ管理機能追加
  - `AlgorithmProposal.tsx`でパラメータ受け取り機能追加
  - `ProposalGenerationForm.tsx`で初期値設定機能追加
  - `get_analysis_results.py`で`id`フィールドを返すように修正
  - 仕様書更新 (`AlgorithmProposalNavigation.spec.md`)

#### ❌ 未実装
- なし（全てのPhaseが完了）

### 差分サマリー

**完了率**: 100% (6/6 Phase完了)

**次の優先タスク**:
1. データ解析機能は完了。次はニュース収集機能の実装に着手

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
   - **実装場所**: `src-tauri/src/commands/llm.rs` を新規作成し、LLM関連コマンドを集約
   - 例: `get_llm_cost_stats()`, `get_token_count()`, `get_llm_cache_stats()` など
2. Phase 4: ストリーミング対応の実装（オプション、将来拡張）
   - **実装場所**: `src-tauri/src/commands/llm.rs` に追加
   - 例: `stream_llm_response()` など

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

- **Phase 1: 基本レイアウト構築** ✅ **完了** (2025年11月8日)
- **Phase 2: アルゴリズム一覧表示** ✅ **完了** (2025年11月8日)
- **Phase 3: 検証結果サマリー表示** ✅ **完了** (2025年11月8日)
- **Phase 4: クイックアクション** ✅ **完了** (2025年11月8日)

### 実装状況

#### ✅ 実装済み
- 型定義 (`src/types/dashboard.ts`)
- 仕様書 (`src/pages/Dashboard/Dashboard.spec.md`)
- メインコンポーネント (`Dashboard.tsx`)
- サイドバーナビゲーション (`Sidebar.tsx`)
- ヘッダーコンポーネント (`Header.tsx`)
- Zustand store (`src/stores/dashboard.ts`)
- `get_selected_algorithms()` Tauriコマンド（既に実装済み）
- アルゴリズム一覧コンポーネント (`AlgorithmList.tsx`)
- アルゴリズムカードコンポーネント (`AlgorithmCard.tsx`)
- `get_backtest_results_summary()` Tauriコマンド (`src-tauri/src/lib.rs`)
- バックエンドスクリプト (`get_backtest_results_summary.py`)
- 検証結果サマリーコンポーネント (`ResultSummary.tsx`)
- パフォーマンス指標カードコンポーネント (`PerformanceCard.tsx`)
- `delete_algorithm()` Tauriコマンド (`src-tauri/src/lib.rs`)
- バックエンドスクリプト (`delete_algorithm.py`)
- クイックアクションコンポーネント (`QuickActions.tsx`)
- 削除確認ダイアログ（Mantine Modals）
- ナビゲーション機能（stateベース）
- テストファイル（`Dashboard.test.tsx`, `AlgorithmList.test.tsx`, `AlgorithmCard.test.tsx`, `ResultSummary.test.tsx`, `QuickActions.test.tsx`）

#### ❌ 未実装
- なし（全てのPhaseが完了）

### 差分サマリー

**完了率**: 100% (4/4 Phase完了)

**次の優先タスク**:
1. ダッシュボード機能は完了。次はニュース収集機能の実装に着手

---

## 8. ニュース収集（News Collection）バックエンド

### 実装計画のPhase

- **Phase 1: RSSフィードパーサー** ✅ **完了** (2025年11月9日)
- **Phase 2: ニュースAPIクライアント** ✅ **完了** (2025年11月9日)
- **Phase 3: Webスクレイピング** ❌ **未実装**（オプション）
- **Phase 4: ニュースデータベース保存** ✅ **完了** (2025年11月9日)
- **Phase 5: センチメント分析** ❌ **未実装**（オプション）
- **Phase 6: 自動収集スケジューラー** ✅ **完了** (2025年11月9日)

### 実装状況

#### ✅ 実装済み
- モジュールディレクトリ構造 (`src-python/modules/news_collection/`)
- 依存関係の定義 (`requirements.txt`にfeedparser, beautifulsoup4等)
- **Phase 1: RSSフィードパーサー**
  - `RSSFeedParser`クラス (`rss_parser.py`)
  - 複数RSSフィードソース対応（Yahoo Finance, Reuters, Bloomberg）
  - SSL証明書検証の回避（開発環境用）
  - エラーハンドリングとリトライ機構
  - 日付パース処理
- **Phase 2: ニュースAPIクライアント**
  - `NewsAPIClient`クラス (`news_api_client.py`)
  - NewsAPI対応
  - APIキー管理（環境変数、.envファイル対応）
  - レート制限対応
  - エラーハンドリング
- **Phase 4: ニュースデータベース保存**
  - `NewsCollector`クラス (`news_collector.py`)
  - RSSとAPIから取得したニュースの統合
  - 重複チェック（URLベース）
  - データベース保存処理
  - `market_news`テーブルスキーマ（`src-python/database/schema.py`）
- **Phase 6: 自動収集スケジューラー**
  - `NewsCollectionJobManager`クラス (`job_manager.py`)
  - ジョブ状態管理（pending, running, completed, failed）
  - 進捗管理
  - エラーハンドリング
  - `news_collection_jobs`テーブルスキーマ
- **スクリプト実装**
  - `collect_market_news.py` - ニュース収集実行スクリプト
  - `get_news_collection_status.py` - 収集ジョブ状態取得スクリプト
  - `get_collected_news.py` - 収集済みニュース取得スクリプト
- **Tauriコマンド実装**
  - `collect_market_news()` - ニュース収集開始
  - `get_news_collection_status()` - 収集ジョブ状態取得
  - `get_collected_news()` - 収集済みニュース取得
- **テストファイル**
  - `test_rss_parser.py` - RSSパーサーのテスト
  - `test_news_api_client.py` - APIクライアントのテスト
  - `test_news_collector.py` - コレクターのテスト
  - `test_news_job_manager.py` - ジョブ管理のテスト
- **デバッグスクリプト**
  - `debug_news_collection.py` - ニュース収集機能のデバッグ用スクリプト

#### ❌ 未実装
- Webスクレイピング機能（Phase 3 - オプション）
- センチメント分析（Phase 5 - オプション）
- APSchedulerによる自動実行機能（Phase 6の拡張機能、現在はジョブ管理のみ）

### 差分サマリー

**完了率**: 67% (4/6 Phase完了、Phase 3と5はオプション)

**次の優先タスク**:
1. Phase 3: Webスクレイピングの実装（オプション、将来拡張）
   - **実装場所**: `src-tauri/src/commands/news.rs` に追加
   - 例: `scrape_news()` コマンド
2. Phase 5: センチメント分析の実装（オプション、将来拡張）
   - **実装場所**: `src-tauri/src/commands/news.rs` に追加
   - 例: `analyze_sentiment()` コマンド
3. APSchedulerによる自動実行機能の実装（Phase 6の拡張）
   - **実装場所**: 既存の `src-tauri/src/commands/news.rs` に追加、または `src-tauri/src/commands/data_collection.rs` と統合

---

## 9. 銘柄予測（Stock Prediction）

### 実装計画のPhase

- **Phase 1: ニュース収集機能（バックエンド）** ✅ **完了** (2025年11月9日)
- **Phase 2: ニュース収集UI** ✅ **完了** (2025年11月9日)
- **Phase 3: ニュース表示機能** ✅ **完了** (2025年11月9日)
- **Phase 4: LLM銘柄予測生成（バックエンド）** ✅ **完了** (2025年11月9日)
- **Phase 5: 予測生成UI** ✅ **完了** (2025年11月9日)
- **Phase 6: 予測結果表示** ✅ **完了** (2025年11月9日)
- **Phase 7: アクション提案機能** ✅ **完了** (2025年11月9日)
- **Phase 8: 予測履歴・精度追跡** ✅ **完了** (2025年11月9日)

### 実装状況

#### ✅ 実装済み
- 型定義 (`src/types/stock-prediction.ts`, `src/types/news.ts`)
- **Phase 1: ニュース収集機能（バックエンド）**
  - ニュース収集機能のバックエンド実装完了（ニュース収集機能参照）
- **Phase 2: ニュース収集UI**
  - ニュース収集フォーム (`NewsCollectionForm.tsx`)
  - RSSフィード/NewsAPI選択機能
  - APIキー入力機能
  - キーワード検索機能
  - エラーハンドリング
- **Phase 3: ニュース表示機能**
  - 銘柄予測ページ (`StockPrediction.tsx`)
  - ニュース一覧テーブル表示
  - ニュース詳細表示（タイトル、ソース、公開日時）
  - 外部リンク機能
  - リフレッシュ機能
- **Phase 4: LLM銘柄予測生成（バックエンド）**
  - データベーススキーマ拡張 (`src-python/database/schema.py`)
    - `stock_prediction_jobs`テーブル作成
    - `stock_predictions`テーブル作成
    - インデックス作成
  - LLMスキーマ拡張 (`src-python/modules/llm_integration/schemas.py`)
    - `AssociationStep`スキーマ追加
    - `StockPrediction`スキーマに連想チェーンフィールド追加
  - 予測生成モジュール (`src-python/modules/stock_prediction/prediction_generator.py`)
    - `PredictionGenerator`クラス実装
    - LLM連携機能
    - ニュースサマリー整形機能
    - 連想チェーン抽出機能
  - ジョブ管理モジュール (`src-python/modules/stock_prediction/job_manager.py`)
    - `StockPredictionJobManager`クラス実装
    - ジョブ作成・状態更新機能
    - 予測保存・取得機能
  - Pythonスクリプト実装
    - `generate_stock_predictions.py` - 予測生成スクリプト
    - `get_stock_prediction_status.py` - ジョブ状態取得スクリプト
    - `get_stock_predictions.py` - 予測結果取得スクリプト
  - Tauriコマンド実装 (`src-tauri/src/lib.rs`)
    - `generate_stock_predictions()` コマンド
    - `get_stock_prediction_status()` コマンド
    - `get_stock_predictions()` コマンド
  - 型定義更新 (`src/types/stock-prediction.ts`)
    - `AssociationStep`インターフェース修正
    - 予測生成ジョブの状態型追加
    - リクエスト・レスポンス型追加
  - プロンプトテンプレート更新 (`src-python/modules/llm_integration/templates/stock_prediction.txt`)
    - 連想チェーンの出力を明示的に要求するように更新
- **Phase 5: 予測生成UI**
  - 予測生成フォーム (`PredictionGenerationForm.tsx`)
    - ニュースジョブIDの入力（オプション、空欄なら最新ニュースを使用）
    - 予測数の指定（デフォルト5、範囲1-10）
    - ユーザー設定の入力（リスク許容度、投資期間、投資スタイル）
    - 市場トレンドの入力（テキストエリア）
    - エラーハンドリング
    - `generate_stock_predictions` Tauriコマンドの呼び出し
  - 進捗表示コンポーネント (`PredictionProgress.tsx`)
    - ジョブ状態のポーリング（2秒間隔）
    - 進捗バーの表示（0-100%）
    - ステータスメッセージの表示
    - エラー表示
    - 完了・エラー時のコールバック
  - メインページの更新 (`StockPrediction.tsx`)
    - 予測生成フォームと進捗表示の統合
    - 予測生成ジョブIDの状態管理
    - 予測生成状態の管理（idle/generating/completed/error）
- **Phase 6: 予測結果表示**
  - 予測カードコンポーネント (`PredictionCard.tsx`)
    - シンボル、会社名の表示
    - 予測方向（up/down/sideways）のバッジ表示
    - 信頼度スコアのバッジ表示
    - 推奨アクション（buy/sell/hold/watch）のバッジ表示
    - 予測変化率の表示
    - 詳細表示ボタン
  - 予測一覧コンポーネント (`PredictionList.tsx`)
    - グリッドレイアウト（レスポンシブ）
    - `PredictionCard`を使用したカード表示
    - `PredictionDetailModal`の統合
    - 空状態の表示
  - 予測詳細モーダル (`PredictionDetailModal.tsx`)
    - 予測ID、信頼度、方向、アクションの表示
    - 会社名、予測変化率、時間軸の表示
    - 推論理由の表示
    - リスク要因の表示
    - 連想チェーンの表示
    - 作成日時の表示
  - 連想チェーン可視化コンポーネント (`AssociationChain.tsx`)
    - ステップ番号のバッジ表示
    - 概念と関連性の表示
    - ステップ間の矢印表示
    - ステップ番号でソート
  - メインページの更新 (`StockPrediction.tsx`)
    - 予測結果の状態管理
    - `loadPredictions`関数の実装
    - `handlePredictionCompleted`で予測結果を自動読み込み
    - `PredictionList`コンポーネントの統合
    - ローディング状態の表示
- **Phase 7: アクション提案機能**
  - データベーススキーマ拡張 (`src-python/database/schema.py`)
    - `prediction_actions`テーブル作成
    - インデックス作成
  - バックエンドスクリプト実装
    - `save_prediction_action.py` - アクション保存スクリプト
    - 予測IDの存在確認
    - 重複チェック（upsert動作）
    - アクション検証（buy/sell/hold/watch/ignore）
  - Tauriコマンド実装 (`src-tauri/src/lib.rs`)
    - `save_prediction_action()` コマンド
  - 型定義追加 (`src/types/stock-prediction.ts`)
    - `SavePredictionActionRequest`インターフェース
    - `SavePredictionActionResponse`インターフェース
  - フロントエンド実装
    - アクション提案コンポーネント (`ActionProposal.tsx`)
      - アクション選択UI（Radioボタン）
      - メモ入力フィールド（Textarea）
      - 保存ボタン
      - 成功/失敗通知
      - 推奨アクションの表示
    - 予測詳細モーダルへの統合 (`PredictionDetailModal.tsx`)
      - `ActionProposal`コンポーネントの統合
  - テストファイル
    - `test_save_prediction_action.py` - バックエンドテスト
    - `ActionProposal.test.tsx` - フロントエンドテスト
- **Phase 8: 予測履歴・精度追跡**
  - データベーススキーマ拡張 (`src-python/database/schema.py`)
    - `stock_predictions`テーブルに精度追跡カラム追加
      - `actual_direction` (TEXT)
      - `actual_change_percent` (REAL)
      - `accuracy` (INTEGER)
      - `accuracy_updated_at` (TEXT)
  - バックエンドスクリプト実装
    - `get_prediction_history.py` - 予測履歴取得スクリプト
      - フィルタリング機能（limit, start_date, end_date, symbol）
      - 精度統計の計算
      - 予測履歴の取得
    - `update_prediction_accuracy.py` - 精度更新スクリプト
      - 予測IDと実際の価格・方向を受け取り、精度を更新
      - 予測が的中したかどうかの判定ロジック
  - バックエンドモジュール実装
    - `accuracy_updater.py` - バッチ処理用モジュール
      - `AccuracyUpdater`クラス実装
      - 精度更新が必要な予測の取得
      - バッチ処理による精度更新機能
      - 実際の価格取得機能（プレースホルダー）
  - Tauriコマンド実装 (`src-tauri/src/lib.rs`)
    - `get_prediction_history()` コマンド
    - `update_prediction_accuracy()` コマンド
  - 型定義追加 (`src/types/stock-prediction.ts`)
    - `GetPredictionHistoryRequest`インターフェース
    - `GetPredictionHistoryResponse`インターフェース
    - `PredictionHistory`インターフェース
    - `AccuracyStats`インターフェース
    - `UpdatePredictionAccuracyRequest`インターフェース
    - `UpdatePredictionAccuracyResponse`インターフェース
  - フロントエンド実装
    - 予測履歴コンポーネント (`PredictionHistory.tsx`)
      - 予測履歴テーブル表示
      - フィルタリングUI（日付範囲、銘柄コード、limit）
      - 精度統計カード表示
      - リフレッシュ機能
      - 予測方向、実際の方向、精度、ユーザーアクションの表示
    - 精度統計コンポーネント (`AccuracyStats.tsx`)
      - 精度統計の可視化（カード、プログレスバー）
      - 総予測数、的中数、的中率の表示
    - メインページへの統合 (`StockPrediction.tsx`)
      - `PredictionHistory`コンポーネントの統合
  - テストファイル
    - `test_get_prediction_history.py` - バックエンドテスト
    - `test_update_prediction_accuracy.py` - バックエンドテスト
    - `test_accuracy_updater.py` - バックエンドテスト
- **ルーティング**
  - `App.tsx`に`stock-prediction`ページを追加
  - サイドバーに「銘柄予測」メニュー項目が存在

#### ❌ 未実装
- フィルタ・ソート機能の拡張

### 差分サマリー

**完了率**: 100% (8/8 Phase完了)

**依存関係**: LLM連携機能の実装が必要（Phase 4以降）✅ **完了**

**次の優先タスク**:
1. フィルタ・ソート機能の拡張
   - **実装場所**: フロントエンドのみ（Tauriコマンド追加不要）
2. 精度更新の自動化（外部API連携による実際の価格取得）
   - **実装場所**: `src-tauri/src/commands/stock_prediction.rs` に追加
   - 例: `update_prediction_accuracy_batch()` コマンド

---

## 10. 国際化対応（Internationalization / i18n）

### 実装計画のPhase

- **Phase 1: 基盤整備** ✅ **完了** (2025年11月10日)
- **Phase 2: 新機能と並行実装** ✅ **完了** (2025年11月10日)
- **Phase 3: 既存機能の段階的移行** ⏳ **未着手**
- **Phase 4: 最適化・改善** ⏳ **未着手**

### 実装状況

#### ✅ 実装済み
- **Phase 1: 基盤整備**
  - react-i18next パッケージのインストール (`react-i18next`, `i18next`, `i18next-browser-languagedetector`)
  - i18next設定ファイル作成 (`src/i18n/index.ts`)
    - 言語検出設定（ブラウザ言語、ローカルストレージ）
    - リソースバンドル設定
    - フォールバック言語設定（日本語）
  - 翻訳リソース構造の作成
    - `src/i18n/locales/ja/common.json` - 共通翻訳（日本語）
    - `src/i18n/locales/ja/navigation.json` - ナビゲーション翻訳（日本語）
    - `src/i18n/locales/en/common.json` - 共通翻訳（英語）
    - `src/i18n/locales/en/navigation.json` - ナビゲーション翻訳（英語）
  - 型定義ファイル作成 (`src/i18n/resources.ts`)
    - TypeScript型安全性確保
  - App.tsx での i18next 初期化
    - `src/i18n` をインポートして初期化
  - 共通コンポーネント（Sidebar, Header）の国際化
    - Sidebarコンポーネント: `useTranslation('navigation')` を使用、メニュー項目を翻訳キーに置き換え
    - Headerコンポーネント: `useTranslation('navigation')` を使用、アプリタイトルを翻訳キーに置き換え、言語切り替えUI（Selectコンポーネント）を追加
  - 新規コンポーネント用のテンプレート作成 (`docs/rules/i18n-template.md`)
  - 開発ガイドライン作成 (`docs/rules/i18n-guidelines.md`)
  - テストファイル作成
    - `src/pages/Dashboard/Sidebar.test.tsx` - 5テストケース、全て通過
    - `src/pages/Dashboard/Header.test.tsx` - 6テストケース、全て通過
- **Phase 2: 新機能と並行実装**
  - 新規コンポーネント作成チェックリスト作成 (`docs/rules/i18n-checklist.md`)
    - 基本実装、翻訳ファイル、i18n設定、翻訳キーの品質、名前空間の選択、テスト、コードレビュー観点のチェックリスト
    - よくあるミスと良い例を追加
  - コードレビューガイドライン追加 (`docs/rules/i18n-guidelines.md`)
    - ハードコードされたテキストの検出方法
    - 翻訳キーの命名規則チェック
    - 名前空間の適切な使用確認
    - 翻訳ファイルの構造チェック
    - i18n設定の確認
    - テストでの国際化対応確認
  - テンプレート拡張 (`docs/rules/i18n-template.md`)
    - 動的な翻訳キーの使用方法
    - 数値や日付のフォーマット方法
    - エラーメッセージの国際化対応例
    - テストファイルでの国際化対応例
    - 条件付き翻訳の使用例
  - 開発ワークフロー整備 (`docs/rules/i18n-workflow.md`)
    - 新規コンポーネント作成時の標準ワークフロー（6ステップ）
    - 各ステップの作業内容と例を記載
    - よくある質問と回答を追加
  - 共通翻訳リソース拡充 (`src/i18n/locales/ja/common.json`, `src/i18n/locales/en/common.json`)
    - フォーム関連（placeholder、validation messages）
    - テーブル関連（列ヘッダー、ソート、フィルタ、ページネーション）
    - モーダル関連（タイトル、メッセージ）
    - ステータス関連（pending、running、completed、failed など）
    - 日付・時刻フォーマット
  - VS Codeスニペット作成 (`.vscode/i18n.code-snippets`)
    - `i18n-component`: 国際化対応済みコンポーネントのテンプレート
    - `i18n-t`: 翻訳キー使用のスニペット
    - `i18n-use`: useTranslation フックのスニペット
    - `i18n-use-multi`: 複数名前空間のスニペット
    - `i18n-test`: テスト用のI18nextProviderラッパー

#### ❌ 未実装
- **Phase 2: 新機能と並行実装**（継続的）
  - LLM連携拡張機能実装時の国際化対応（新機能実装時に実施）
  - ニュース収集拡張機能実装時の国際化対応（新機能実装時に実施）
- **Phase 3: 既存機能の段階的移行**
  - Dashboard コンポーネントの国際化
  - DataManagement コンポーネントの国際化
  - AlgorithmProposal コンポーネントの国際化
  - Backtest コンポーネントの国際化
  - DataAnalysis コンポーネントの国際化
  - StockPrediction コンポーネントの国際化
- **Phase 4: 最適化・改善**
  - 翻訳ファイルの整理・最適化
  - 翻訳品質の向上
  - テストカバレッジの向上
  - パフォーマンス最適化

### 実装アプローチ

**段階的導入アプローチ**を採用：

1. **Phase 1: 基盤整備**（1-2日）
   - 新機能実装前に基盤を整備
   - 共通コンポーネントから国際化対応を開始
   - 新規コンポーネント用のテンプレートとガイドラインを作成

2. **Phase 2: 新機能と並行実装**（継続的）
   - 新機能実装時に最初から国際化対応
   - 既存機能への影響を最小限に抑制

3. **Phase 3: 既存機能の段階的移行**（2-3週間）
   - 優先度の高い機能から順次移行
   - 機能単位で完全移行を実施

4. **Phase 4: 最適化・改善**（継続的）
   - 翻訳品質の向上
   - パフォーマンス最適化

### 技術スタック

- **ライブラリ**: react-i18next + i18next
- **言語検出**: i18next-browser-languagedetector
- **型安全性**: TypeScript型定義
- **UI統合**: Mantine UI の国際化対応

### 翻訳リソース構造

```
src/i18n/
├── index.ts                    # i18next設定
├── resources.ts                # 型定義
└── locales/
    ├── ja/
    │   ├── common.json        # 共通翻訳
    │   ├── dashboard.json     # ダッシュボード
    │   ├── data-management.json
    │   ├── data-analysis.json
    │   ├── algorithm-proposal.json
    │   ├── backtest.json
    │   ├── stock-prediction.json
    │   └── news.json
    └── en/
        ├── common.json
        └── ...
```

### 差分サマリー

**完了率**: 50% (2/4 Phase完了)

**次の優先タスク**:
1. Phase 2: 新機能と並行実装（継続的）
   - **実装場所**: 新機能実装時に `src/i18n/locales/` に翻訳ファイルを追加
   - LLM連携拡張機能実装時に国際化対応を併せて実施
   - ニュース収集拡張機能実装時に国際化対応を併せて実施
   - 新規コンポーネントは最初から国際化対応（標準化完了）
2. Phase 3: 既存機能の段階的移行（2-3週間）
   - **実装場所**: 既存コンポーネントファイル
   - 優先度の高い機能から順次移行
   - Dashboard → DataManagement → AlgorithmProposal → Backtest → DataAnalysis → StockPrediction

---

### 実装完了率（Phase単位）

| 機能 | 完了Phase | 総Phase数 | 完了率 |
|------|----------|----------|--------|
| データ収集（バックエンド） | 5 | 5 | 100% |
| データ管理（フロントエンド） | 5 | 5 | 100% |
| データ解析 | 6 | 6 | 100% |
| LLM連携（バックエンド） | 3 | 5 | 60% |
| アルゴリズム提案 | 6 | 6 | 100% |
| バックテスト | 6 | 6 | 100% |
| ダッシュボード | 4 | 4 | 100% |
| ニュース収集（バックエンド） | 4 | 6 | 67% |
| 銘柄予測 | 8 | 8 | 100% |
| 国際化対応（i18n） | 2 | 4 | 50% |

**全体完了率**: 約88% (49/58 Phase完了)

**注意**: 上記の完了率は機能別のPhase完了率のみを計算しており、ナビゲーションシステムなどの基盤機能は含まれていない。ナビゲーションシステムはstateベースの実装が完了しており、`App.tsx`でページ間の遷移が可能になった。

### 実装優先度（推奨順序）

1. **国際化対応（i18n）** - Phase 2: 新機能と並行実装、Phase 3: 既存機能の段階的移行（優先度：高）
2. **LLM連携の拡張** - ストリーミング対応、コスト管理・最適化（Phase 4, 5）
3. **ニュース収集の拡張** - Webスクレイピング、センチメント分析（オプション）
4. **銘柄予測の拡張** - フィルタ・ソート機能の拡張、精度更新の自動化
5. **データ管理の拡張** - データセット情報カード、ソート・フィルタ機能（オプション）

### 重要な未実装機能

#### 基盤機能
- **ナビゲーションシステム** ✅ **実装完了** - stateベースのナビゲーションを実装。`App.tsx`でページ間の遷移が可能になった。
- **国際化対応（i18n）** 🔄 **Phase 1, 2完了、Phase 3-4進行中** - react-i18next基盤整備完了。Phase 2（新機能と並行実装）の標準化完了。Phase 3（既存機能の段階的移行）に着手可能。

#### バックエンド
- ニュース収集機能の拡張（Webスクレイピング、センチメント分析）
  - **実装場所**: `src-tauri/src/commands/news.rs` に追加
- LLM連携の拡張機能（ストリーミング対応、コスト管理）
  - **実装場所**: `src-tauri/src/commands/llm.rs` を新規作成
- ~~LLM銘柄予測生成機能~~ ✅ **実装完了**
- ~~データ収集自動スケジューラー~~ ✅ **実装完了**
- ~~データ更新・差分管理機能~~ ✅ **実装完了**

#### フロントエンド
- **国際化対応（i18n）** 🔄 **Phase 1, 2完了、Phase 3-4進行中**
  - **実装場所**: `src/i18n/` ディレクトリ（Phase 1完了）、`docs/rules/` ディレクトリ（Phase 2完了）
  - **アプローチ**: 段階的導入（基盤整備完了 → 新機能と並行実装の標準化完了 → 既存機能移行）
  - **優先度**: 高（Phase 3: 既存機能の段階的移行）
- 銘柄予測UIの拡張（フィルタ・ソート機能の拡張）
- ~~外部API自動収集設定UI~~ ✅ **実装完了**

### 依存関係マップ

```
データ管理 ✅ (100%)
    ↓
データ収集 ✅ (100%)
    ↓
データ解析 ✅ → アルゴリズム提案 ✅ → バックテスト ✅
    ↓                    ↓
LLM連携 ✅ (60%) ────────────┘
    ↓
ニュース収集 ✅ (67%) → 銘柄予測 ✅ (100%)
    ↓
ダッシュボード ✅（他の機能と並行実装可能）
    ↓
国際化対応 🔄（基盤機能、全機能に影響）
```

### 次のアクションアイテム

1. **即座に着手すべき**:
   - ~~LLM銘柄予測生成機能の実装（銘柄予測 Phase 4）~~ ✅ **完了**
   - ~~予測生成UIの実装（銘柄予測 Phase 5）~~ ✅ **完了**
   - ~~予測結果表示の実装（銘柄予測 Phase 6）~~ ✅ **完了**
   - ~~アクション提案機能の実装（銘柄予測 Phase 7）~~ ✅ **完了**
   - ~~予測履歴・精度追跡の実装（銘柄予測 Phase 8）~~ ✅ **完了**
   - ~~データプレビュー機能の実装（データ管理 Phase 5）~~ ✅ **完了**
   - ~~自動収集スケジューラーの実装（データ収集 Phase 4）~~ ✅ **完了**
   - ~~外部API自動収集設定UIの実装（データ管理 Phase 4）~~ ✅ **完了**
   - ~~データ更新・差分管理機能の実装（データ収集 Phase 5）~~ ✅ **完了**
   - ~~国際化対応（i18n）Phase 1: 基盤整備~~ ✅ **完了** (2025年11月10日)
     - react-i18next セットアップ完了
     - 共通コンポーネント（Sidebar, Header）の国際化完了
     - 新規コンポーネント用のテンプレート作成完了
     - 開発ガイドライン作成完了
   - ~~国際化対応（i18n）Phase 2: 新機能と並行実装の標準化~~ ✅ **完了** (2025年11月10日)
     - 新規コンポーネント作成チェックリスト作成完了
     - コードレビューガイドライン追加完了
     - テンプレート拡張完了（動的翻訳、数値・日付フォーマット、エラーメッセージ、テスト対応、条件付き翻訳）
     - 開発ワークフロー整備完了（6ステップの標準ワークフロー）
     - 共通翻訳リソース拡充完了（フォーム、テーブル、モーダル、ステータス、日付・時刻）
     - VS Codeスニペット作成完了

2. **短期（1-2週間）**:
   - **国際化対応 Phase 2: 新機能と並行実装**（継続的、標準化完了）
     - LLM連携拡張機能実装時に国際化対応を併せて実施
     - ニュース収集拡張機能実装時に国際化対応を併せて実施
     - 新規コンポーネントは最初から国際化対応（標準化完了、チェックリスト・ワークフロー・スニペット使用）
   - LLM連携の拡張機能（コスト管理・最適化、Phase 5）
     - **実装場所**: `src-tauri/src/commands/llm.rs` を新規作成
     - **注意**: 実装時に国際化対応を併せて実施
   - ニュース収集機能の拡張（Webスクレイピング、センチメント分析）
     - **実装場所**: `src-tauri/src/commands/news.rs` に追加
     - **注意**: 実装時に国際化対応を併せて実施

3. **中期（1ヶ月）**:
   - **国際化対応 Phase 2: 新機能と並行実装**（継続的、標準化完了）
     - LLM連携拡張機能実装時に国際化対応
     - ニュース収集拡張機能実装時に国際化対応
     - 新規コンポーネントは最初から国際化対応（標準化完了）
   - **国際化対応 Phase 3: 既存機能の段階的移行**
     - 優先度の高い機能から順次移行
     - Dashboard（高頻度使用）
     - DataManagement（高頻度使用）
     - AlgorithmProposal
     - Backtest
     - DataAnalysis
     - StockPrediction
   - LLM連携の拡張機能（ストリーミング対応、Phase 4）
     - **実装場所**: `src-tauri/src/commands/llm.rs` に追加
     - **注意**: 実装時に国際化対応を併せて実施
   - 精度更新の自動化（外部API連携による実際の価格取得）
     - **実装場所**: `src-tauri/src/commands/stock_prediction.rs` に追加
   - データ管理の拡張機能（データセット情報カード、ソート・フィルタ機能）
     - **実装場所**: フロントエンドのみ（Tauriコマンド追加不要）
     - **注意**: 実装時に国際化対応を併せて実施

4. **長期（2-3ヶ月）**:
   - LLM連携の拡張機能（コスト管理の高度化）
     - **実装場所**: `src-tauri/src/commands/llm.rs` に追加
   - **国際化対応 Phase 4: 最適化・改善**
     - 翻訳ファイルの整理・最適化
     - 翻訳品質の向上
     - テストカバレッジの向上

---

## 注意事項

- 仕様書（`.spec.md`）が未作成の機能が多いため、実装前に仕様書の作成を推奨
- テストファイル（`.test.tsx`）も未作成のため、TDDの原則に従ってテストを先に作成することを推奨
- ジョブ管理システムは複数の機能で必要になるため、共通化を検討すべき
- **ナビゲーションシステムの実装**: stateベースのナビゲーションを実装済み。`App.tsx`でページ間の遷移が可能になった。将来的にReact Routerなどのルーティングライブラリへの移行を検討。
- **Tauriコマンドの実装ガイドライン**: 
  - **重要**: `src-tauri/src/lib.rs`は約1800行から約70行にリファクタリングされ、機能別モジュールに分割されました。
  - 新しいTauriコマンドを実装する際は、**必ず適切なモジュールに配置**してください。`lib.rs`に直接書かないでください。
  - **モジュール構造**:
    - `src-tauri/src/utils.rs` - 共通処理（`execute_python_script`関数など）
    - `src-tauri/src/commands/data_management.rs` - データ管理関連コマンド
    - `src-tauri/src/commands/data_analysis.rs` - データ分析関連コマンド
    - `src-tauri/src/commands/algorithm.rs` - アルゴリズム関連コマンド
    - `src-tauri/src/commands/backtest.rs` - バックテスト関連コマンド
    - `src-tauri/src/commands/news.rs` - ニュース関連コマンド
    - `src-tauri/src/commands/stock_prediction.rs` - 株価予測関連コマンド
    - `src-tauri/src/commands/data_collection.rs` - データ収集スケジュール関連コマンド
    - `src-tauri/src/commands/misc.rs` - その他コマンド
  - **今後の実装で推奨されるモジュール分割**:
    - **LLM連携の拡張機能**（ストリーミング対応、コスト管理）:
      - `src-tauri/src/commands/llm.rs` を新規作成し、LLM関連コマンドを集約
      - 例: `get_llm_cost_stats()`, `stream_llm_response()` など
    - **ニュース収集の拡張機能**（Webスクレイピング、センチメント分析）:
      - 既存の `src-tauri/src/commands/news.rs` に追加
      - 例: `scrape_news()`, `analyze_sentiment()` など
    - **その他の新機能**:
      - 機能ごとに新しいモジュールを作成するか、既存のモジュールに追加
      - `src-tauri/src/commands/mod.rs` でモジュールを公開
      - `src-tauri/src/lib.rs` の `invoke_handler` にコマンドを登録
- **国際化対応（i18n）の実装ガイドライン**: 
  - **重要**: 段階的導入アプローチを採用しています。**Phase 1: 基盤整備、Phase 2: 新機能と並行実装の標準化が完了しました**（2025年11月10日）。新規コンポーネントは最初から国際化対応を行います。
  - **実装場所**: `src/i18n/` ディレクトリ（Phase 1完了）、`docs/rules/` ディレクトリ（Phase 2完了）
  - **ライブラリ**: react-i18next + i18next + i18next-browser-languagedetector
  - **翻訳リソース構造**: 機能ごとに名前空間で分割（`common.json`, `navigation.json`, `dashboard.json`, `data-management.json` など）
  - **新規コンポーネント実装時の注意**:
    - ハードコードされたテキストは使用しない
    - `useTranslation()` フックを使用して `t()` 関数で翻訳を取得
    - 翻訳キーは名前空間付きで記述（例: `t('navigation.dashboard')`）
    - 翻訳ファイルは機能ごとの名前空間に配置
    - **チェックリストを使用**: `docs/rules/i18n-checklist.md` を参照
    - **ワークフローに従う**: `docs/rules/i18n-workflow.md` の6ステップに従う
    - **VS Codeスニペットを使用**: `.vscode/i18n.code-snippets` のスニペットを活用
  - **既存コンポーネントの移行**:
    - 優先度の高い機能から順次移行（Phase 3で実施予定）
    - 機能単位で完全移行を実施
    - テストとレビューを実施
  - **テンプレート・ガイドライン**: 
    - 新規コンポーネント用テンプレート: `docs/rules/i18n-template.md`
    - 開発ガイドライン: `docs/rules/i18n-guidelines.md`
    - チェックリスト: `docs/rules/i18n-checklist.md`
    - 開発ワークフロー: `docs/rules/i18n-workflow.md`
    - VS Codeスニペット: `.vscode/i18n.code-snippets`
  - **詳細**: 実装計画は `docs/03_plans/i18n/` に作成予定（未作成）
- **実装ガイドライン**: 
  - アルゴリズム提案機能の実装方法については、`docs/03_plans/algorithm-proposal/IMPLEMENTATION_GUIDE.md` を参照してください。**Phase 1-6は全て完了しています。**
  - バックテスト機能の実装方法については、`docs/03_plans/backtest/README.md` を参照してください。**Phase 1-6は全て完了しています。**
  - ダッシュボード機能の実装方法については、`docs/03_plans/dashboard/README.md` を参照してください。**Phase 1-4は全て完了しています。**
  - ニュース収集機能の実装方法については、`docs/03_plans/news-collection/README.md` を参照してください。**Phase 1, 2, 4, 6は完了しています。**
  - 銘柄予測機能の実装方法については、`docs/03_plans/stock-prediction/README.md` を参照してください。**Phase 1, 2, 3, 4, 5, 6, 7, 8は完了しています。**
  - データ管理機能の実装方法については、`docs/03_plans/data-management/README.md` を参照してください。**Phase 1, 2, 3, 4, 5は全て完了しています。**
  - データ収集機能の実装方法については、`docs/03_plans/data-collection/README.md` を参照してください。**Phase 1, 2, 3, 4, 5は全て完了しています。**

## テストカバレッジ

**全体カバレッジ**: 92% (2,103ステートメント中174未カバー)

**主要モジュールのカバレッジ**:
- LLM連携モジュール: 平均 75% (exceptions: 100%, schemas: 100%, api_key_manager: 97%, clients: 95%)
- データ解析モジュール: 平均 88% (statistics: 100%, analyzer: 84%, technical_indicators: 90%)
- データ収集モジュール: 平均 93% (csv_importer: 94%, api_clients: 91%)
- バックテストモジュール: 実装完了（テストカバレッジは今後測定予定）

**詳細**: `src-python/htmlcov/index.html` を参照してください。

