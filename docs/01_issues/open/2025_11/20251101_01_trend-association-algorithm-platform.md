# 実装要件定義書：トレンド連想型アルゴリズム構築・検証プラットフォーム

## 1. はじめに

本ドキュメントは、トレンド連想型アルゴリズム構築・検証プラットフォームの実装要件を定義する。

### 1.1. 目的

本プラットフォームは、LLM（大規模言語モデル）が主体となってアルゴリズムを提案し、ユーザーが選択したアルゴリズムをバックテストで検証できるデスクトップアプリケーションとして開発する。アプリケーション側がデータの収集・解析を自動で行い、LLMがその解析結果を基に最適なアルゴリズムを提案する。ユーザーは提案されたアルゴリズムから使用するものを選択するだけで良い。Python-Tauri直接連携モデルを採用し、HTTP通信のオーバーヘッドを排除した高パフォーマンスな実装を目指す。

### 1.2. 対象読者

- 開発チーム
- プロジェクトマネージャー
- 品質保証担当者

### 1.3. ドキュメント管理

- **作成日**: 2025-11-01
- **最終更新日**: 2025-11-01
- **バージョン**: 2.1.0
- **ステータス**: Open

## 2. システム構成

### 2.1. 全体アーキテクチャ

**Python-Tauri直接連携モデル**を採用したデスクトップアプリケーションとして構築する。

#### クライアント（フロントエンド）

- **技術**: Tauri + React
- **役割**: 
  - UIの描画
  - ユーザー操作の受付
  - PyTauriを通じたバックエンド関数の直接呼び出し（invoke）
- **特徴**: HTTPサーバーを使用せず、関数呼び出しによって直接データを受け渡し

#### サーバー（バックエンド）

- **技術**: Python + PyTauri
- **役割**:
  - **データ収集**: 株価データの自動収集（外部API、CSVインポート等）
  - **データ解析**: 収集したデータのトレンド分析、テクニカル指標計算
  - **ニュース収集**: 金融ニュース、市場トレンド情報の自動収集
  - **市場トレンド分析**: ニュースや市場動向からトレンドを分析
  - **LLM連携**: LLM APIを通じたアルゴリズム提案生成、銘柄予測生成
  - **バックテスト実行**: 提案されたアルゴリズムの検証
  - **テクニカル分析**: 各種テクニカル指標の計算
  - 全てのコアロジックを関数として提供
- **特徴**: フロントエンドとは関数呼び出しによって直接データを受け渡し

### 2.2. 技術スタック

| 区分 | 技術 | バージョン/ライブラリ | 役割 |
|------|------|----------------------|------|
| **フロントエンド** | React | 19.x | UIフレームワーク |
| | TypeScript | 5.x | 言語 |
| | Vite | 5.x | ビルドツール |
| | Mantine | - | UIコンポーネントライブラリ |
| | Zustand / Redux Toolkit | - | 状態管理（推奨） |
| | ECharts / Lightweight Charts | - | チャート描画ライブラリ |
| **バックエンド** | Python | 3.10+ | 言語 |
| | PyTauri | - | Tauri-Pythonブリッジ |
| | Pandas, NumPy, TA-Lib | - | データ分析・テクニカル指標計算 |
| | OpenAI API / Anthropic API | - | LLM連携（アルゴリズム提案生成、銘柄予測生成） |
| | requests / httpx | - | 外部API連携（データ収集、ニュース収集） |
| | BeautifulSoup4 / feedparser | - | ニュース・RSSフィード解析 |
| **パッケージング** | Tauri | 2.x | デスクトップアプリ化 |
| **データベース** | SQLite | - | アルゴリズム定義、検証結果、解析結果の保存 |
| **バージョン管理** | Git | - | ソースコード管理 |

### 2.3. アーキテクチャ図

```
┌─────────────────────────────────────────────────────────┐
│                    Tauri Desktop App                     │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  ┌──────────────────┐         ┌──────────────────┐     │
│  │  React Frontend  │         │  Python Backend  │     │
│  │  (TypeScript)    │◄───────►│  (PyTauri)       │     │
│  │                  │ invoke  │                  │     │
│  │  - UI Components │         │  - Data Collection│     │
│  │  - State Mgmt    │         │  - Data Analysis │     │
│  │  - Charts        │         │  - LLM Integration│     │
│  │  - Algorithm     │         │  - Backtest      │     │
│  │    Selection     │         │  - Technical     │     │
│  └──────────────────┘         └──────────────────┘     │
│                                                           │
│                          ┌──────────────┐               │
│                          │   SQLite DB   │               │
│                          │  - Algorithms │               │
│                          │  - Results    │               │
│                          │  - OHLCV Data │               │
│                          │  - Analysis   │               │
│                          └──────────────┘               │
│                                                           │
│                    ┌──────────────┐                      │
│                    │  LLM API     │                      │
│                    │ (OpenAI/     │                      │
│                    │  Anthropic)  │                      │
│                    └──────────────┘                      │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

## 3. 機能要件

### 3.1. 画面一覧

| 画面ID | 画面名 | 説明 |
|--------|--------|------|
| SCREEN-001 | ダッシュボード | 選択済みアルゴリズム一覧、検証結果サマリーを表示 |
| SCREEN-002 | アルゴリズム提案 | LLMが提案したアルゴリズム一覧を表示し、ユーザーが選択する画面 |
| SCREEN-003 | バックテスト設定 | バックテストの実行条件を設定する画面 |
| SCREEN-004 | バックテスト結果 | バックテストの実行結果を表示する画面 |
| SCREEN-005 | データ管理 | 株価データのインポート・管理画面 |
| SCREEN-006 | データ解析 | データ収集・解析状況の確認、解析結果の表示画面 |
| SCREEN-007 | 銘柄予測・連想ゲーム | ニュース・トレンドから次に変動する銘柄を予測し、アクションを提案する画面 |

### 3.2. 各画面の機能詳細

#### SCREEN-001: ダッシュボード

**機能概要**: 
- ユーザーが選択したアルゴリズムの一覧表示
- 各アルゴリズムの最新検証結果サマリー
- クイックアクション（アルゴリズム提案の再生成、削除）

**バックエンド連携**:
- `get_selected_algorithms()`: 選択済みアルゴリズム一覧を取得
- `get_backtest_results()`: 最新の検証結果を取得

#### SCREEN-002: アルゴリズム提案

**機能概要**:
- LLMが生成したアルゴリズム提案の一覧表示
- 各提案アルゴリズムの説明・根拠の表示
- ユーザーによるアルゴリズムの選択（採用/非採用）
- アルゴリズム提案の再生成機能
- 選択したアルゴリズムの詳細確認

**バックエンド連携**:
- `generate_algorithm_proposals()`: LLMを使用してアルゴリズム提案を生成（非同期）
- `get_algorithm_proposals()`: 生成済みのアルゴリズム提案一覧を取得
- `select_algorithm()`: ユーザーが選択したアルゴリズムを保存
- `get_analysis_results()`: データ解析結果を取得（LLMへの入力として使用）

**実行フロー**:
1. ユーザーが「アルゴリズム提案を生成」ボタンを押下
2. フロントエンドが `invoke('generate_algorithm_proposals', params)` を実行
3. バックエンドがデータ解析結果を取得し、LLM APIに送信
4. バックエンドが即座に `job_id` を返す
5. フロントエンドが `get_proposal_generation_status(job_id)` を定期的にポーリング
6. 完了後、`get_algorithm_proposals(job_id)` で提案アルゴリズム一覧を取得
7. ユーザーが提案アルゴリズムを確認し、採用したいものを選択
8. `select_algorithm(proposal_id)` で選択したアルゴリズムを保存

#### SCREEN-003: バックテスト設定

**機能概要**:
- 実行対象アルゴリズムの選択
- 検証期間の設定（開始日、終了日）
- 対象データセットの選択

**バックエンド連携**:
- `run_backtest()`: バックテストの実行を開始（非同期）
- `get_data_list()`: 利用可能なデータセット一覧を取得

**実行フロー**:
1. ユーザーが「実行開始」ボタンを押下
2. フロントエンドが `invoke('run_backtest', params)` を実行
3. バックエンドが即座に `job_id` を返す
4. フロントエンドが `get_backtest_status(job_id)` を定期的にポーリング
5. 完了後、`get_backtest_results(job_id)` で結果を取得

#### SCREEN-004: バックテスト結果

**機能概要**:
- パフォーマンス指標の表示（リターン、シャープレシオ、最大ドローダウン等）
- 取引履歴の一覧表示
- チャートによる可視化（資産推移、エントリー/エグジットポイント）

**バックエンド連携**:
- `get_backtest_results()`: 完了したバックテストの結果を取得

#### SCREEN-005: データ管理

**機能概要**:
- CSV形式の株価データ（OHLCV）のインポート
- 外部APIからの自動データ収集設定
- インポート済みデータセットの一覧表示
- データの削除

**バックエンド連携**:
- `import_ohlcv_data()`: CSVファイルをインポート
- `get_data_list()`: インポート済みデータセットの一覧を取得
- `configure_data_collection()`: 外部APIからの自動データ収集設定

#### SCREEN-006: データ解析

**機能概要**:
- データ収集・解析ジョブの一覧表示
- 解析ジョブの実行状況確認
- 解析結果の表示（トレンド分析、テクニカル指標のサマリー等）
- 解析結果を基にしたアルゴリズム提案への遷移

**バックエンド連携**:
- `run_data_analysis()`: データ解析ジョブの実行を開始（非同期）
- `get_analysis_status()`: 解析ジョブの進捗状況を取得
- `get_analysis_results()`: 完了した解析結果を取得

#### SCREEN-007: 銘柄予測・連想ゲーム

**機能概要**:
- 最新のニュース・市場トレンドの表示
- LLMによる連想ゲーム的な銘柄予測の生成
- 予測された銘柄の変動理由（連想の過程）の可視化
- ユーザーへのアクション提案（買い/売り/様子見等）
- 予測結果の履歴表示
- 予測精度の追跡（過去の予測が的中したかどうか）

**バックエンド連携**:
- `collect_market_news()`: 市場ニュースの収集を開始（非同期）
- `get_news_status()`: ニュース収集ジョブの進捗状況を取得
- `generate_stock_predictions()`: LLMを使用して銘柄予測を生成（非同期）
- `get_prediction_status()`: 銘柄予測生成ジョブの進捗状況を取得
- `get_stock_predictions()`: 生成された銘柄予測一覧を取得
- `save_prediction_action()`: ユーザーが選択したアクションを保存
- `get_prediction_history()`: 過去の予測履歴を取得

**実行フロー**:
1. ユーザーが「銘柄予測を生成」ボタンを押下
2. フロントエンドが `invoke('collect_market_news', params)` を実行（最新ニュース収集）
3. バックエンドが即座に `news_job_id` を返す
4. フロントエンドが `get_news_status(news_job_id)` を定期的にポーリング
5. ニュース収集完了後、`invoke('generate_stock_predictions', params)` を実行
6. バックエンドがニュース・トレンド情報をLLM APIに送信
7. バックエンドが即座に `prediction_job_id` を返す
8. フロントエンドが `get_prediction_status(prediction_job_id)` を定期的にポーリング
9. 完了後、`get_stock_predictions(prediction_job_id)` で予測結果を取得
10. ユーザーが予測結果を確認し、提案されたアクションを選択
11. `save_prediction_action(prediction_id, action)` で選択したアクションを保存

### 3.3. Tauriコマンド仕様 (Pythonバックエンド関数)

フロントエンドから `invoke` で呼び出すPython関数（コマンド）の仕様を以下に定義する。

#### 3.3.1. LLM関連コマンド

##### `generate_algorithm_proposals`

**説明**: LLMを使用してアルゴリズム提案を生成する。データ解析結果を基に、最適なアルゴリズムを複数提案する。非同期で実行され、即座にジョブIDを返す。

**引数 (Payload)**:
```typescript
{
  data_set_id: number;        // 解析対象のデータセットID
  analysis_id?: number;       // オプション: 既存の解析結果ID（指定時は再解析をスキップ）
  num_proposals?: number;     // オプション: 生成する提案数（デフォルト: 5）
  user_preferences?: {        // オプション: ユーザーの好み設定
    risk_tolerance?: 'low' | 'medium' | 'high';
    trading_frequency?: 'low' | 'medium' | 'high';
    preferred_indicators?: string[];  // 例: ['RSI', 'MACD']
  };
}
```

**戻り値**:
```typescript
{
  job_id: string;  // アルゴリズム提案生成ジョブの一意なID
}
```

**エラーハンドリング**:
- データセットが存在しない場合: エラーを返す
- LLM APIキーが設定されていない場合: エラーを返す
- LLM API呼び出しに失敗した場合: エラーを返す

##### `get_proposal_generation_status`

**説明**: アルゴリズム提案生成ジョブの進捗状況を返す。フロントエンドはこれを定期的にポーリングする。

**引数 (Payload)**:
```typescript
{
  job_id: string;  // アルゴリズム提案生成ジョブID
}
```

**戻り値**:
```typescript
{
  status: 'pending' | 'analyzing' | 'generating' | 'completed' | 'failed';
  progress: number;  // 0.0 ~ 1.0 の進捗率
  message: string;   // ステータスメッセージ（例: "Analyzing data trends..."）
  error?: string;     // エラーが発生した場合のエラーメッセージ
}
```

**ポーリング推奨間隔**: 2秒

##### `get_algorithm_proposals`

**説明**: 生成されたアルゴリズム提案の一覧を返す。

**引数 (Payload)**:
```typescript
{
  job_id: string;  // アルゴリズム提案生成ジョブID
}
```

**戻り値**:
```typescript
{
  job_id: string;
  proposals: Array<{
    proposal_id: string;
    name: string;
    description: string;           // LLMが生成した説明
    rationale: string;            // なぜこのアルゴリズムが提案されたかの根拠
    expected_performance?: {      // LLMが予測したパフォーマンス（オプション）
      expected_return?: number;
      risk_level?: 'low' | 'medium' | 'high';
    };
    definition: {
      triggers: Array<TriggerDefinition>;
      actions: Array<ActionDefinition>;
    };
    confidence_score?: number;     // 0.0 ~ 1.0 の信頼度スコア
  }>;
}
```

**エラーハンドリング**:
- ジョブが未完了の場合: エラーを返す
- ジョブIDが存在しない場合: エラーを返す

##### `select_algorithm`

**説明**: ユーザーが選択したアルゴリズム提案を保存する。

**引数 (Payload)**:
```typescript
{
  proposal_id: string;  // 選択したアルゴリズム提案ID
  custom_name?: string; // オプション: カスタム名（省略時は提案名を使用）
}
```

**戻り値**:
```typescript
{
  algo_id: number;  // 保存されたアルゴリズムID
  success: boolean;
}
```

#### 3.3.2. データ解析関連コマンド

##### `run_data_analysis`

**説明**: 指定されたデータセットの解析を実行する。トレンド分析、テクニカル指標計算等を行う。非同期で実行され、即座にジョブIDを返す。

**引数 (Payload)**:
```typescript
{
  data_set_id: number;  // 解析対象のデータセットID
}
```

**戻り値**:
```typescript
{
  job_id: string;  // データ解析ジョブの一意なID
}
```

**エラーハンドリング**:
- データセットが存在しない場合: エラーを返す

##### `get_analysis_status`

**説明**: データ解析ジョブの進捗状況を返す。フロントエンドはこれを定期的にポーリングする。

**引数 (Payload)**:
```typescript
{
  job_id: string;  // データ解析ジョブID
}
```

**戻り値**:
```typescript
{
  status: 'pending' | 'running' | 'completed' | 'failed';
  progress: number;  // 0.0 ~ 1.0 の進捗率
  message: string;   // ステータスメッセージ（例: "Calculating technical indicators..."）
  error?: string;     // エラーが発生した場合のエラーメッセージ
}
```

**ポーリング推奨間隔**: 1秒

##### `get_analysis_results`

**説明**: 完了したデータ解析結果を返す。

**引数 (Payload)**:
```typescript
{
  job_id: string;  // データ解析ジョブID
}
```

**戻り値**:
```typescript
{
  job_id: string;
  data_set_id: number;
  analysis_summary: {
    trend_direction: 'upward' | 'downward' | 'sideways';
    volatility_level: 'low' | 'medium' | 'high';
    dominant_patterns: string[];  // 例: ['uptrend', 'consolidation']
  };
  technical_indicators: {
    rsi: {
      current: number;
      average: number;
      signal: 'oversold' | 'neutral' | 'overbought';
    };
    macd: {
      current: number;
      signal_line: number;
      histogram: number;
      trend: 'bullish' | 'bearish' | 'neutral';
    };
    // その他の指標...
  };
  statistics: {
    price_range: {
      min: number;
      max: number;
      current: number;
    };
    volume_average: number;
    price_change_percent: number;
  };
  created_at: string;
}
```

**エラーハンドリング**:
- ジョブが未完了の場合: エラーを返す
- ジョブIDが存在しない場合: エラーを返す

#### 3.3.3. バックテスト関連コマンド

##### `run_backtest`

**説明**: バックテストの実行を非同期で開始する。即座にジョブIDを返す。

**引数 (Payload)**:
```typescript
{
  algorithm_ids: number[];  // 実行対象のアルゴリズムIDのリスト
  start_date: string;       // 開始日 (YYYY-MM-DD形式)
  end_date: string;         // 終了日 (YYYY-MM-DD形式)
  data_set_id?: number;     // オプション: 使用するデータセットID
}
```

**戻り値**:
```typescript
{
  job_id: string;  // バックテストジョブの一意なID
}
```

**エラーハンドリング**:
- 無効なアルゴリズムIDが指定された場合: エラーを返す
- 日付範囲が不正な場合: エラーを返す
- データセットが存在しない場合: エラーを返す

##### `get_backtest_status`

**説明**: 指定したバックテストの進捗状況を返す。フロントエンドはこれを定期的にポーリングする。

**引数 (Payload)**:
```typescript
{
  job_id: string;  // バックテストジョブID
}
```

**戻り値**:
```typescript
{
  status: 'pending' | 'running' | 'completed' | 'failed';
  progress: number;  // 0.0 ~ 1.0 の進捗率
  message: string;   // ステータスメッセージ（例: "Processing 2023-01-15..."）
  error?: string;     // エラーが発生した場合のエラーメッセージ
}
```

**ポーリング推奨間隔**: 1秒

##### `get_backtest_results`

**説明**: 指定したバックテストの完了結果（パフォーマンス指標、取引履歴等）を返す。

**引数 (Payload)**:
```typescript
{
  job_id: string;  // バックテストジョブID
}
```

**戻り値**:
```typescript
{
  job_id: string;
  algorithm_id: number;
  start_date: string;
  end_date: string;
  performance: {
    total_return: number;        // 総リターン率 (%)
    sharpe_ratio: number;        // シャープレシオ
    max_drawdown: number;        // 最大ドローダウン (%)
    win_rate: number;            // 勝率 (%)
    total_trades: number;        // 総取引数
    average_profit: number;      // 平均利益
    average_loss: number;        // 平均損失
  };
  trades: Array<{
    entry_date: string;
    exit_date: string;
    entry_price: number;
    exit_price: number;
    quantity: number;
    profit: number;
    profit_rate: number;
  }>;
  equity_curve: Array<{
    date: string;
    equity: number;
  }>;
}
```

**エラーハンドリング**:
- ジョブが未完了の場合: エラーを返す
- ジョブIDが存在しない場合: エラーを返す

#### 3.3.4. アルゴリズム管理コマンド

##### `get_selected_algorithms`

**説明**: ユーザーが選択したアルゴリズムの一覧を返す。

**引数 (Payload)**: なし

**戻り値**:
```typescript
{
  algorithms: Array<{
    id: number;
    name: string;
    description?: string;
    proposal_id?: string;  // 元の提案ID（存在する場合）
    created_at: string;
    updated_at: string;
    definition: {
      triggers: Array<TriggerDefinition>;
      actions: Array<ActionDefinition>;
    };
  }>;
}
```

##### `delete_algorithm`

**説明**: 指定したIDのアルゴリズムを削除する。

**引数 (Payload)**:
```typescript
{
  algo_id: number;
}
```

**戻り値**:
```typescript
{
  success: boolean;
  message?: string;  // エラーメッセージ（失敗時）
}
```

#### 3.3.5. 銘柄予測・連想ゲーム関連コマンド

##### `collect_market_news`

**説明**: 市場ニュース、金融情報を収集する。RSSフィード、ニュースAPI等から最新情報を取得する。非同期で実行され、即座にジョブIDを返す。

**引数 (Payload)**:
```typescript
{
  sources?: string[];  // オプション: 収集元の指定（例: ['yahoo_finance', 'reuters']）
  keywords?: string[]; // オプション: 検索キーワード
  max_articles?: number; // オプション: 最大記事数（デフォルト: 50）
}
```

**戻り値**:
```typescript
{
  job_id: string;  // ニュース収集ジョブの一意なID
}
```

**エラーハンドリング**:
- ニュースソースへのアクセスに失敗した場合: エラーを返す

##### `get_news_status`

**説明**: ニュース収集ジョブの進捗状況を返す。フロントエンドはこれを定期的にポーリングする。

**引数 (Payload)**:
```typescript
{
  job_id: string;  // ニュース収集ジョブID
}
```

**戻り値**:
```typescript
{
  status: 'pending' | 'running' | 'completed' | 'failed';
  progress: number;  // 0.0 ~ 1.0 の進捗率
  message: string;   // ステータスメッセージ（例: "Collecting news from Yahoo Finance..."）
  error?: string;     // エラーが発生した場合のエラーメッセージ
}
```

**ポーリング推奨間隔**: 2秒

##### `get_collected_news`

**説明**: 収集されたニュース一覧を返す。

**引数 (Payload)**:
```typescript
{
  job_id: string;  // ニュース収集ジョブID
}
```

**戻り値**:
```typescript
{
  job_id: string;
  news: Array<{
    id: string;
    title: string;
    content: string;      // 記事本文（要約）
    source: string;      // ニュースソース名
    published_at: string; // 公開日時
    url?: string;         // 記事URL
    keywords?: string[];  // 抽出されたキーワード
    sentiment?: 'positive' | 'neutral' | 'negative'; // センチメント分析結果
  }>;
  collected_at: string;
}
```

**エラーハンドリング**:
- ジョブが未完了の場合: エラーを返す
- ジョブIDが存在しない場合: エラーを返す

##### `generate_stock_predictions`

**説明**: LLMを使用して、収集したニュース・トレンド情報から連想的に銘柄予測を生成する。非同期で実行され、即座にジョブIDを返す。

**引数 (Payload)**:
```typescript
{
  news_job_id: string;   // ニュース収集ジョブID
  market_trends?: {      // オプション: 市場トレンド情報
    sector_performance?: Array<{
      sector: string;
      performance: number; // パフォーマンス（%）
    }>;
    market_sentiment?: 'bullish' | 'bearish' | 'neutral';
  };
  num_predictions?: number; // オプション: 生成する予測数（デフォルト: 10）
  prediction_horizon?: 'short' | 'medium' | 'long'; // オプション: 予測期間（デフォルト: 'short'）
}
```

**戻り値**:
```typescript
{
  job_id: string;  // 銘柄予測生成ジョブの一意なID
}
```

**エラーハンドリング**:
- ニュースジョブIDが存在しない場合: エラーを返す
- LLM APIキーが設定されていない場合: エラーを返す
- LLM API呼び出しに失敗した場合: エラーを返す

##### `get_prediction_status`

**説明**: 銘柄予測生成ジョブの進捗状況を返す。フロントエンドはこれを定期的にポーリングする。

**引数 (Payload)**:
```typescript
{
  job_id: string;  // 銘柄予測生成ジョブID
}
```

**戻り値**:
```typescript
{
  status: 'pending' | 'analyzing' | 'generating' | 'completed' | 'failed';
  progress: number;  // 0.0 ~ 1.0 の進捗率
  message: string;   // ステータスメッセージ（例: "Analyzing market trends..."）
  error?: string;     // エラーが発生した場合のエラーメッセージ
}
```

**ポーリング推奨間隔**: 2秒

##### `get_stock_predictions`

**説明**: 生成された銘柄予測の一覧を返す。

**引数 (Payload)**:
```typescript
{
  job_id: string;  // 銘柄予測生成ジョブID
}
```

**戻り値**:
```typescript
{
  job_id: string;
  predictions: Array<{
    prediction_id: string;
    symbol: string;              // 銘柄コード
    company_name?: string;       // 会社名
    predicted_direction: 'up' | 'down' | 'sideways'; // 予測方向
    predicted_change_percent?: number; // 予測変動率（%）
    confidence_score: number;    // 0.0 ~ 1.0 の信頼度スコア
    reasoning: string;           // LLMが生成した予測理由（連想の過程）
    association_chain: Array<{   // 連想の連鎖を可視化
      step: number;
      concept: string;           // 連想された概念
      connection: string;         // 前の概念との関連
    }>;
    suggested_action: 'buy' | 'sell' | 'hold' | 'watch'; // 推奨アクション
    time_horizon: 'short' | 'medium' | 'long'; // 予測期間
    related_news?: Array<{        // 関連ニュース
      news_id: string;
      relevance: number;         // 関連度（0.0 ~ 1.0）
    }>;
    risk_level?: 'low' | 'medium' | 'high'; // リスクレベル
  }>;
  generated_at: string;
}
```

**エラーハンドリング**:
- ジョブが未完了の場合: エラーを返す
- ジョブIDが存在しない場合: エラーを返す

##### `save_prediction_action`

**説明**: ユーザーが選択したアクション（買い/売り等）を保存する。後で予測精度を追跡するために使用される。

**引数 (Payload)**:
```typescript
{
  prediction_id: string;  // 銘柄予測ID
  action: 'buy' | 'sell' | 'hold' | 'watch' | 'ignore'; // ユーザーが選択したアクション
  notes?: string;         // オプション: ユーザーのメモ
}
```

**戻り値**:
```typescript
{
  success: boolean;
  action_id?: number;  // 保存されたアクションID
}
```

##### `get_prediction_history`

**説明**: 過去の銘柄予測履歴を取得する。予測精度の追跡に使用される。

**引数 (Payload)**:
```typescript
{
  limit?: number;        // オプション: 取得件数（デフォルト: 50）
  start_date?: string;   // オプション: 開始日 (YYYY-MM-DD形式)
  end_date?: string;     // オプション: 終了日 (YYYY-MM-DD形式)
  symbol?: string;       // オプション: 銘柄コードでフィルタ
}
```

**戻り値**:
```typescript
{
  predictions: Array<{
    prediction_id: string;
    symbol: string;
    predicted_direction: 'up' | 'down' | 'sideways';
    predicted_at: string;
    actual_direction?: 'up' | 'down' | 'sideways'; // 実際の結果（計算済みの場合）
    actual_change_percent?: number; // 実際の変動率（%）
    accuracy?: boolean;              // 予測が的中したかどうか
    user_action?: 'buy' | 'sell' | 'hold' | 'watch' | 'ignore';
    reasoning: string;
  }>;
  accuracy_stats?: {
    total_predictions: number;
    correct_predictions: number;
    accuracy_rate: number; // 0.0 ~ 1.0
  };
}
```

##### `update_prediction_accuracy`

**説明**: 過去の予測に対して実際の結果を記録し、予測精度を更新する。定期的にバッチ処理で実行される想定。

**引数 (Payload)**:
```typescript
{
  prediction_id: string;  // 銘柄予測ID
  actual_price: number;   // 実際の価格
  actual_direction: 'up' | 'down' | 'sideways'; // 実際の方向
}
```

**戻り値**:
```typescript
{
  success: boolean;
  accuracy_updated: boolean; // 予測が的中したかどうか
}
```

#### 3.3.6. データ管理コマンド

##### `import_ohlcv_data`

**説明**: 指定されたパスの株価データ(CSV)をインポートする。

**引数 (Payload)**:
```typescript
{
  file_path: string;  // インポートするCSVファイルのパス
  name?: string;      // オプション: データセット名（省略時はファイル名から自動生成）
}
```

**戻り値**:
```typescript
{
  success: boolean;
  message: string;
  data_set_id?: number;  // 成功時のみ: インポートされたデータセットID
}
```

**CSV形式要件**:
- ヘッダー行必須
- カラム: `date`, `open`, `high`, `low`, `close`, `volume`
- 日付形式: `YYYY-MM-DD` または `YYYY/MM/DD`

##### `get_data_list`

**説明**: インポート済みのデータセットの一覧を返す。

**引数 (Payload)**: なし

**戻り値**:
```typescript
{
  data_list: Array<{
    id: number;
    name: string;
    symbol?: string;      // オプション: 銘柄コード
    start_date: string;   // データの開始日
    end_date: string;     // データの終了日
    record_count: number; // レコード数
    imported_at: string; // インポート日時
  }>;
}
```

## 4. 非機能要件

### 4.1. パフォーマンス要件

| 項目 | 要件 |
|------|------|
| バックテスト処理時間 | 1銘柄、1年分の日足データの計算処理が10秒以内に完了すること |
| データ解析処理時間 | 1銘柄、1年分の日足データの解析処理が30秒以内に完了すること |
| LLMアルゴリズム生成時間 | LLMによるアルゴリズム提案生成が60秒以内に完了すること |
| ニュース収集時間 | 市場ニュースの収集が30秒以内に完了すること |
| LLM銘柄予測生成時間 | LLMによる銘柄予測生成が90秒以内に完了すること |
| UI応答性 | UIの操作に対する応答が0.5秒以内であること |
| 通信オーバーヘッド | PyTauriによる直接関数呼び出しにより、HTTP通信のオーバーヘッドをなくし、応答性を高める |

### 4.2. セキュリティ要件

| 項目 | 要件 |
|------|------|
| APIキー管理 | 外部APIキー（LLM等）は、PC内の安全な場所に暗号化して保存すること |
| データ保護 | ユーザーがインポートした株価データは、ローカル環境のみに保存し、外部に送信しないこと |
| LLM API通信 | LLM APIへの通信はHTTPSで暗号化し、送信するデータは最小限にすること |
| 個人情報保護 | LLM APIに送信するデータには個人を特定できる情報を含めないこと |

### 4.3. ユーザビリティ要件

| 項目 | 要件 |
|------|------|
| 操作性 | アルゴリズム提案画面は、プログラミング経験がなくても直感的に操作できること |
| 説明の明確性 | LLMが生成したアルゴリズム提案には、分かりやすい説明と根拠を表示すること |
| ヘルプ機能 | 主要な機能にはツールチップによる簡単な説明を表示すること |
| エラーメッセージ | エラー発生時は、ユーザーが理解しやすい日本語のメッセージを表示すること |
| 進捗表示 | LLMによるアルゴリズム生成中は、進捗状況を明確に表示すること |

### 4.4. 拡張性要件

| 項目 | 要件 |
|------|------|
| テクニカル指標追加 | 新しいテクニカル指標を、バックエンドのPythonコード修正で容易に追加できる構造とすること |
| データソース追加 | 新しいデータソース（トリガー）を、バックエンドのPythonコード修正で容易に追加できる構造とすること |
| プラグイン機構 | 将来的にプラグイン機構を導入できるよう、インターフェースを明確に定義すること |

### 4.5. データ永続化要件

| 項目 | 要件 |
|------|------|
| データ保持 | ユーザーが作成したアルゴリズム、インポートしたデータ、検証結果は、アプリケーションを終了しても保持されること |
| データベース | ローカルのSQLiteデータベースに保存すること |
| バックアップ | データベースファイルのバックアップ機能を提供すること（将来実装） |

## 5. データモデル（概要）

### 5.1. データベーススキーマ概要

**SQLiteデータベース**: `algo_trader.db`

#### 主要テーブル

1. **algorithms**: ユーザーが選択したアルゴリズム定義
2. **algorithm_proposals**: LLMが生成したアルゴリズム提案（一時保存）
3. **backtest_jobs**: バックテストジョブ情報
4. **backtest_results**: バックテスト結果
5. **ohlcv_data**: 株価データ（OHLCV）
6. **data_sets**: データセット情報
7. **analysis_results**: データ解析結果
8. **analysis_jobs**: データ解析ジョブ情報
9. **market_news**: 収集された市場ニュース
10. **news_collection_jobs**: ニュース収集ジョブ情報
11. **stock_predictions**: LLMが生成した銘柄予測
12. **prediction_actions**: ユーザーが選択した予測アクション
13. **prediction_accuracy**: 予測精度の追跡結果

詳細なスキーマ定義は、実装計画フェーズで作成する。

## 6. 関連ドキュメント

- **実装計画**: `docs/03_plans/trend-association-algorithm-platform/` (作成予定)
- **技術調査**: `docs/02_research/2025_11/` (PyTauri関連調査予定)
- **仕様書**: `src/**/*.spec.md` (各コンポーネントの仕様書)

## 7. 変更履歴

| 日付 | バージョン | 変更内容 | 変更者 |
|------|-----------|---------|--------|
| 2025-11-01 | 1.0.0 | 初版作成 | - |
| 2025-11-01 | 1.0.1 | UIコンポーネントライブラリにMantineを追加 | - |
| 2025-11-01 | 2.0.0 | LLM主体のアルゴリズム提案モデルに全面改訂。ユーザー構築型からLLM提案型へ変更。データ収集・解析機能を追加 | - |
| 2025-11-01 | 2.1.0 | 銘柄予測・連想ゲーム機能を追加。ニュース収集、LLMによる連想的銘柄予測、アクション提案機能を実装 | - |

