# ダッシュボード機能 データモデル詳細

## 概要

ダッシュボード機能で使用するデータモデルの詳細定義です。

## 関連ドキュメント

- **実装計画**: `docs/03_plans/dashboard/README.md`
- **API仕様**: `docs/03_plans/dashboard/api-spec.md`

## TypeScript型定義

### コア型定義

```typescript
// アルゴリズム
interface Algorithm {
  id: number;
  name: string;
  description?: string;
  proposal_id?: string;
  created_at: string;
  updated_at: string;
  definition: AlgorithmDefinition;
}

// アルゴリズム定義
interface AlgorithmDefinition {
  triggers: TriggerDefinition[];
  actions: ActionDefinition[];
}

// トリガー定義
interface TriggerDefinition {
  type: 'rsi' | 'macd' | 'price' | 'volume' | string;
  condition: TriggerCondition;
}

interface TriggerCondition {
  operator: 'gt' | 'lt' | 'gte' | 'lte' | 'eq' | 'between';
  value: number | [number, number];
  period?: number;
}

// アクション定義
interface ActionDefinition {
  type: 'buy' | 'sell' | 'hold';
  parameters: ActionParameters;
}

interface ActionParameters {
  quantity?: number;
  percentage?: number;
  stop_loss?: number;
  take_profit?: number;
}

// バックテスト結果サマリー
interface BacktestResultSummary {
  job_id: string;
  algorithm_id: number;
  algorithm_name: string;
  start_date: string;
  end_date: string;
  completed_at: string;
  performance: PerformanceMetrics;
}

// パフォーマンス指標
interface PerformanceMetrics {
  total_return: number;        // 総リターン率 (%)
  sharpe_ratio: number;        // シャープレシオ
  max_drawdown: number;        // 最大ドローダウン (%)
  win_rate: number;            // 勝率 (%)
  total_trades: number;        // 総取引数
  average_profit: number;      // 平均利益
  average_loss: number;        // 平均損失
}
```

### 状態管理型定義

```typescript
// Zustand Store State
interface DashboardState {
  algorithms: Algorithm[];
  backtestResults: BacktestResultSummary[];
  loading: boolean;
  error: string | null;
  selectedAlgorithmId: number | null;
}

// Zustand Store Actions
interface DashboardActions {
  fetchAlgorithms: () => Promise<void>;
  fetchBacktestResults: (algorithmIds?: number[]) => Promise<void>;
  deleteAlgorithm: (algorithmId: number) => Promise<void>;
  setSelectedAlgorithmId: (id: number | null) => void;
  clearError: () => void;
}
```

## Pythonデータクラス定義

```python
from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from datetime import datetime

@dataclass
class Algorithm:
    id: int
    name: str
    description: Optional[str]
    proposal_id: Optional[str]
    created_at: str
    updated_at: str
    definition: Dict[str, Any]

@dataclass
class PerformanceMetrics:
    total_return: float
    sharpe_ratio: float
    max_drawdown: float
    win_rate: float
    total_trades: int
    average_profit: float
    average_loss: float

@dataclass
class BacktestResultSummary:
    job_id: str
    algorithm_id: int
    algorithm_name: str
    start_date: str
    end_date: str
    completed_at: str
    performance: PerformanceMetrics
```

## データベーススキーマ

### algorithms テーブル

```sql
CREATE TABLE algorithms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    proposal_id TEXT,
    definition TEXT NOT NULL,  -- JSON形式
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (proposal_id) REFERENCES algorithm_proposals(id)
);

CREATE INDEX idx_algorithms_created_at ON algorithms(created_at);
CREATE INDEX idx_algorithms_proposal_id ON algorithms(proposal_id);
```

### backtest_results テーブル

```sql
CREATE TABLE backtest_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id TEXT UNIQUE NOT NULL,
    algorithm_id INTEGER NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    total_return REAL,
    sharpe_ratio REAL,
    max_drawdown REAL,
    win_rate REAL,
    total_trades INTEGER,
    average_profit REAL,
    average_loss REAL,
    completed_at TEXT NOT NULL,
    FOREIGN KEY (algorithm_id) REFERENCES algorithms(id)
);

CREATE INDEX idx_backtest_results_algorithm_id ON backtest_results(algorithm_id);
CREATE INDEX idx_backtest_results_completed_at ON backtest_results(completed_at);
```

## データフロー図

```
┌─────────────┐
│  Frontend   │
│  Dashboard  │
└──────┬──────┘
       │
       │ invoke('get_selected_algorithms')
       ▼
┌─────────────┐
│  Backend    │
│  PyTauri    │
└──────┬──────┘
       │
       │ SELECT * FROM algorithms
       ▼
┌─────────────┐
│  SQLite DB  │
│  algorithms │
└─────────────┘

┌─────────────┐
│  Frontend   │
│  Dashboard  │
└──────┬──────┘
       │
       │ invoke('get_backtest_results')
       ▼
┌─────────────┐
│  Backend    │
│  PyTauri    │
└──────┬──────┘
       │
       │ SELECT * FROM backtest_results
       │ WHERE algorithm_id IN (...)
       ▼
┌─────────────┐
│  SQLite DB  │
│backtest_    │
│  results    │
└─────────────┘
```

## データ変換

### フロントエンド → バックエンド

```typescript
// アルゴリズム削除リクエスト
const request: DeleteAlgorithmRequest = {
  algo_id: algorithm.id
};
```

### バックエンド → フロントエンド

```python
# Python → TypeScript
def format_algorithm(algorithm: Algorithm) -> Dict[str, Any]:
    return {
        "id": algorithm.id,
        "name": algorithm.name,
        "description": algorithm.description,
        "proposal_id": algorithm.proposal_id,
        "created_at": algorithm.created_at.isoformat(),
        "updated_at": algorithm.updated_at.isoformat(),
        "definition": json.loads(algorithm.definition)
    }
```

## 注意事項

- 日付はISO 8601形式（`YYYY-MM-DDTHH:mm:ss.sssZ`）で統一
- JSON形式のデータ（`definition`）は文字列として保存し、取得時にパース
- 数値の精度に注意（特にパフォーマンス指標）
- データベースのインデックスを適切に設定してパフォーマンスを最適化

