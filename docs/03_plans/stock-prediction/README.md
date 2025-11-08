# 銘柄予測・連想ゲーム機能 実装計画

## 概要

ニュース・市場トレンドから連想的に銘柄予測を生成し、ユーザーにアクションを提案する機能です。LLMを使用した連想ゲーム的な予測が特徴です。

## 関連ドキュメント

- **要件定義**: `docs/01_issues/open/2025_11/20251101_01_trend-association-algorithm-platform.md` (SCREEN-007)
- **仕様書**: `src/pages/StockPrediction/StockPrediction.spec.md` (作成予定)
- **テスト**: `src/pages/StockPrediction/StockPrediction.test.tsx` (作成予定)

## 実装フェーズ

### Phase 1: ニュース収集機能（バックエンド）

**目標**: 市場ニュースの自動収集機能を実装

**タスク**:
- [ ] `collect_market_news()` Tauriコマンドの実装
- [ ] RSSフィードパーサーの実装
- [ ] ニュースAPIクライアントの実装
- [ ] ニュースデータベース保存処理の実装
- [ ] センチメント分析の実装（オプション）

**技術スタック**:
- Python 3.10+
- BeautifulSoup4 / feedparser
- requests / httpx
- PyTauri

**依存関係**:
- なし（独立機能）

### Phase 2: ニュース収集UI

**目標**: ニュース収集の実行と進捗表示UI

**タスク**:
- [ ] ニュース収集ボタンの実装
- [ ] `get_news_status()` Tauriコマンドの実装
- [ ] 進捗表示の実装
- [ ] ポーリング機能の実装

**技術スタック**:
- React 19.x
- TypeScript 5.x
- Mantine UI
- Tauri invoke API

**依存関係**:
- Phase 1完了

### Phase 3: ニュース表示機能

**目標**: 収集したニュースの表示

**タスク**:
- [ ] `get_collected_news()` Tauriコマンドの実装
- [ ] ニュース一覧コンポーネントの実装
- [ ] ニュースカードコンポーネントの実装
- [ ] フィルタ・ソート機能の実装

**技術スタック**:
- Mantine Card, Table
- Tauri invoke API

**依存関係**:
- Phase 2完了

### Phase 4: LLM銘柄予測生成（バックエンド）

**目標**: LLMを使用した連想的銘柄予測の生成

**タスク**:
- [ ] `generate_stock_predictions()` Tauriコマンドの実装
- [ ] LLM APIクライアントの実装
- [ ] 連想ゲームプロンプトの設計・実装
- [ ] レスポンスパース処理の実装
- [ ] 連想チェーンの抽出処理

**技術スタック**:
- Python 3.10+
- OpenAI API / Anthropic API
- PyTauri

**依存関係**:
- Phase 3完了
- LLM APIキーの設定

### Phase 5: 予測生成UI

**目標**: 銘柄予測生成の実行と進捗表示UI

**タスク**:
- [ ] 予測生成ボタンの実装
- [ ] `get_prediction_status()` Tauriコマンドの実装
- [ ] 進捗表示の実装
- [ ] ポーリング機能の実装

**技術スタック**:
- React 19.x
- TypeScript 5.x
- Mantine UI

**依存関係**:
- Phase 4完了

### Phase 6: 予測結果表示

**目標**: 生成された銘柄予測の表示

**タスク**:
- [ ] `get_stock_predictions()` Tauriコマンドの実装
- [ ] 予測一覧コンポーネントの実装
- [ ] 予測カードコンポーネントの実装
- [ ] 連想チェーンの可視化コンポーネントの実装

**技術スタック**:
- Mantine Card
- React Flow / D3.js (連想チェーンの可視化)

**依存関係**:
- Phase 5完了

### Phase 7: アクション提案機能

**目標**: ユーザーへのアクション提案と選択機能

**タスク**:
- [ ] アクション提案UIの実装
- [ ] `save_prediction_action()` Tauriコマンドの実装
- [ ] アクション選択UIの実装
- [ ] アクション保存処理の実装

**技術スタック**:
- Mantine Button, Radio
- Tauri invoke API

**依存関係**:
- Phase 6完了

### Phase 8: 予測履歴・精度追跡

**目標**: 過去の予測履歴と精度の追跡

**タスク**:
- [ ] `get_prediction_history()` Tauriコマンドの実装
- [ ] `update_prediction_accuracy()` Tauriコマンドの実装
- [ ] 予測履歴一覧の実装
- [ ] 精度統計の表示
- [ ] バッチ処理による精度更新機能（バックエンド）

**技術スタック**:
- Mantine Table
- Python scheduler (定期実行)

**依存関係**:
- Phase 7完了

## 技術的な詳細

### コンポーネント構造

```
StockPrediction/
├── StockPrediction.tsx        # メインコンポーネント
├── NewsCollection.tsx          # ニュース収集
├── NewsList.tsx               # ニュース一覧
├── NewsCard.tsx               # ニュースカード
├── PredictionGeneration.tsx   # 予測生成
├── PredictionList.tsx         # 予測一覧
├── PredictionCard.tsx         # 予測カード
├── AssociationChain.tsx       # 連想チェーン可視化
├── ActionProposal.tsx         # アクション提案
├── PredictionHistory.tsx      # 予測履歴
└── StockPrediction.spec.md    # 仕様書
```

### 状態管理

```typescript
interface StockPredictionState {
  newsJobId: string | null;
  newsStatus: 'idle' | 'collecting' | 'completed' | 'error';
  news: News[];
  predictionJobId: string | null;
  predictionStatus: 'idle' | 'generating' | 'completed' | 'error';
  predictions: StockPrediction[];
  selectedPredictionId: string | null;
  predictionHistory: PredictionHistory[];
  accuracyStats: AccuracyStats | null;
}
```

### 連想ゲームプロンプト設計

```python
prompt_template = """
以下のニュースと市場トレンドを基に、連想的に銘柄予測を行ってください。

【収集したニュース】
{news_summary}

【市場トレンド】
{market_trends}

【連想ゲームのルール】
1. ニュースから関連する業界・セクターを連想
2. その業界・セクターに関連する銘柄を連想
3. 各連想ステップを明確に記録
4. 最終的な銘柄予測とその根拠を提示

【出力形式】
JSON形式で以下の構造で出力してください：
{
  "predictions": [
    {
      "symbol": "銘柄コード",
      "predicted_direction": "up|down|sideways",
      "reasoning": "予測理由",
      "association_chain": [
        {"step": 1, "concept": "概念", "connection": "関連性"},
        ...
      ],
      "suggested_action": "buy|sell|hold|watch",
      "confidence_score": 0.0-1.0
    }
  ]
}
"""
```

### 連想チェーンの可視化

```typescript
interface AssociationChain {
  step: number;
  concept: string;
  connection: string;
}

// React Flowを使用した可視化
const visualizeChain = (chain: AssociationChain[]) => {
  // ノードとエッジを生成
  // グラフとして表示
};
```

### API連携

- `collect_market_news(params)`: ニュース収集開始
- `get_news_status(job_id)`: ニュース収集進捗取得
- `get_collected_news(job_id)`: 収集ニュース取得
- `generate_stock_predictions(params)`: 銘柄予測生成開始
- `get_prediction_status(job_id)`: 予測生成進捗取得
- `get_stock_predictions(job_id)`: 予測結果取得
- `save_prediction_action(prediction_id, action)`: アクション保存
- `get_prediction_history(params)`: 予測履歴取得
- `update_prediction_accuracy(prediction_id, actual)`: 精度更新

## テスト計画

### 単体テスト

- [ ] NewsCollectionコンポーネントのテスト
- [ ] PredictionListコンポーネントのテスト
- [ ] AssociationChainコンポーネントのテスト
- [ ] ニュース収集ロジックのテスト
- [ ] LLM APIクライアントのテスト（モック）

### 統合テスト

- [ ] ニュース収集フローの統合テスト
- [ ] 銘柄予測生成フローの統合テスト
- [ ] アクション保存の統合テスト
- [ ] 精度更新の統合テスト

### E2Eテスト

- [ ] 銘柄予測生成のE2Eテスト
- [ ] 予測履歴表示のE2Eテスト

## 実装優先度

**最高**: Phase 1, Phase 2, Phase 4, Phase 5（核心機能）
**高**: Phase 3, Phase 6（必須機能）
**中**: Phase 7, Phase 8（拡張機能）

## 注意事項

- ニュースソースの信頼性と著作権への配慮
- RSSフィードのレート制限対応
- LLM APIのレート制限とコスト管理
- 連想チェーンの可視化の分かりやすさ
- 予測精度の追跡の自動化
- エラーハンドリング（ニュース収集失敗、LLM APIエラー等）
- ユーザーへの注意喚起（予測は参考情報であること）

