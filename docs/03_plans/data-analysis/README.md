# データ解析機能 実装計画

## 概要

株価データのトレンド分析、テクニカル指標計算を行う機能です。解析結果はアルゴリズム提案の入力として使用されます。

## 関連ドキュメント

- **要件定義**: `docs/01_issues/open/2025_11/20251101_01_trend-association-algorithm-platform.md` (SCREEN-006)
- **仕様書**: `src/pages/DataAnalysis/DataAnalysis.spec.md` (作成予定)
- **テスト**: `src/pages/DataAnalysis/DataAnalysis.test.tsx` (作成予定)

## 実装フェーズ

### Phase 1: 解析ジョブ実行UI

**目標**: データ解析ジョブの実行UIを実装

**タスク**:
- [ ] データセット選択UIの実装
- [ ] 解析実行ボタンの実装
- [ ] `run_data_analysis()` Tauriコマンドの実装（バックエンド）
- [ ] ジョブ開始処理の実装

**技術スタック**:
- React 19.x
- TypeScript 5.x
- Mantine UI
- Tauri invoke API

**依存関係**:
- データ管理機能

### Phase 2: 解析エンジン実装（バックエンド）

**目標**: データ解析エンジンの実装

**タスク**:
- [ ] トレンド分析ロジックの実装
- [ ] テクニカル指標計算の実装（RSI, MACD等）
- [ ] 統計情報計算の実装
- [ ] 解析結果の構造化

**技術スタック**:
- Python 3.10+
- Pandas, NumPy
- TA-Lib
- PyTauri

**依存関係**:
- Phase 1完了

### Phase 3: 進捗表示機能

**目標**: 解析ジョブの進捗を表示

**タスク**:
- [ ] `get_analysis_status()` Tauriコマンドの実装
- [ ] ジョブ管理システムの実装（バックエンド）
- [ ] ポーリング機能の実装（フロントエンド）
- [ ] 進捗バーの実装

**技術スタック**:
- Python threading / asyncio
- React useEffect / setInterval
- Mantine Progress

**依存関係**:
- Phase 2完了

### Phase 4: 解析結果表示

**目標**: 解析結果を分かりやすく表示

**タスク**:
- [ ] `get_analysis_results()` Tauriコマンドの実装
- [ ] 解析結果サマリーコンポーネントの実装
- [ ] トレンド分析結果の表示
- [ ] テクニカル指標の表示
- [ ] 統計情報の表示

**技術スタック**:
- Mantine Card, Table
- Tauri invoke API

**依存関係**:
- Phase 3完了

### Phase 5: 結果可視化

**目標**: 解析結果をチャートで可視化

**タスク**:
- [ ] トレンドチャートの実装
- [ ] テクニカル指標チャートの実装
- [ ] チャートライブラリの統合

**技術スタック**:
- ECharts / Lightweight Charts
- React chart components

**依存関係**:
- Phase 4完了

### Phase 6: アルゴリズム提案への遷移

**目標**: 解析結果からアルゴリズム提案画面への遷移

**タスク**:
- [ ] 遷移ボタンの実装
- [ ] 解析結果IDの受け渡し
- [ ] ナビゲーション統合

**技術スタック**:
- React Router (またはTauriのナビゲーション)

**依存関係**:
- Phase 4完了
- アルゴリズム提案機能

## 技術的な詳細

### コンポーネント構造

```
DataAnalysis/
├── DataAnalysis.tsx           # メインコンポーネント
├── AnalysisJobForm.tsx        # 解析ジョブ実行フォーム
├── AnalysisProgress.tsx        # 進捗表示
├── AnalysisResults.tsx        # 解析結果表示
├── TrendAnalysis.tsx          # トレンド分析結果
├── TechnicalIndicators.tsx     # テクニカル指標
├── Statistics.tsx             # 統計情報
└── DataAnalysis.spec.md      # 仕様書
```

### 状態管理

```typescript
interface DataAnalysisState {
  dataSetId: number | null;
  jobId: string | null;
  status: 'idle' | 'running' | 'completed' | 'error';
  progress: number;
  results: AnalysisResult | null;
  loading: boolean;
  error: string | null;
}
```

### 解析結果構造

```typescript
interface AnalysisResult {
  job_id: string;
  data_set_id: number;
  analysis_summary: {
    trend_direction: 'upward' | 'downward' | 'sideways';
    volatility_level: 'low' | 'medium' | 'high';
    dominant_patterns: string[];
  };
  technical_indicators: {
    rsi: RSIResult;
    macd: MACDResult;
    // その他の指標...
  };
  statistics: {
    price_range: { min: number; max: number; current: number };
    volume_average: number;
    price_change_percent: number;
  };
}
```

### テクニカル指標実装

```python
class TechnicalAnalyzer:
    def calculate_rsi(self, data, period=14):
        # RSI計算
        pass
    
    def calculate_macd(self, data):
        # MACD計算
        pass
    
    def analyze_trend(self, data):
        # トレンド分析
        pass
```

### API連携

- `run_data_analysis(data_set_id)`: データ解析実行開始
- `get_analysis_status(job_id)`: 進捗状況取得
- `get_analysis_results(job_id)`: 解析結果取得
- `get_data_list()`: データセット一覧取得

## テスト計画

### 単体テスト

- [ ] AnalysisJobFormコンポーネントのテスト
- [ ] AnalysisResultsコンポーネントのテスト
- [ ] テクニカル指標計算のテスト
- [ ] トレンド分析ロジックのテスト

### 統合テスト

- [ ] データ解析フローの統合テスト
- [ ] ジョブ管理の統合テスト
- [ ] 結果取得と表示の統合テスト

### E2Eテスト

- [ ] データ解析実行のE2Eテスト
- [ ] 解析結果表示のE2Eテスト

## 実装優先度

**最高**: Phase 1, Phase 2, Phase 3（核心機能）
**高**: Phase 4（必須機能）
**中**: Phase 5, Phase 6（可視化・遷移機能）

## 注意事項

- 大量データの解析時のパフォーマンス最適化
- メモリ使用量の管理
- テクニカル指標計算の精度
- エラーハンドリング（データ不足、計算エラー等）
- 解析結果のキャッシュ機能（再計算の回避）

