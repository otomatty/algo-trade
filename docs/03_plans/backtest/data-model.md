# バックテスト機能 データモデル詳細

## 概要

バックテスト機能で使用するデータモデルの詳細定義です。

## TypeScript型定義

```typescript
// バックテスト結果
interface BacktestResult {
  job_id: string;
  algorithm_id: number;
  start_date: string;
  end_date: string;
  performance: PerformanceMetrics;
  trades: Trade[];
  equity_curve: EquityPoint[];
}

// パフォーマンス指標
interface PerformanceMetrics {
  total_return: number;        // 総リターン率 (%)
  sharpe_ratio: number;        // シャープレシオ
  max_drawdown: number;         // 最大ドローダウン (%)
  win_rate: number;            // 勝率 (%)
  total_trades: number;        // 総取引数
  average_profit: number;      // 平均利益
  average_loss: number;        // 平均損失
}

// 取引
interface Trade {
  entry_date: string;
  exit_date: string;
  entry_price: number;
  exit_price: number;
  quantity: number;
  profit: number;
  profit_rate: number;
}

// 資産推移ポイント
interface EquityPoint {
  date: string;
  equity: number;
}
```

## Pythonデータクラス定義

```python
from dataclasses import dataclass
from typing import List
from datetime import datetime

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
class Trade:
    entry_date: str
    exit_date: str
    entry_price: float
    exit_price: float
    quantity: float
    profit: float
    profit_rate: float

@dataclass
class EquityPoint:
    date: str
    equity: float

@dataclass
class BacktestResult:
    job_id: str
    algorithm_id: int
    start_date: str
    end_date: str
    performance: PerformanceMetrics
    trades: List[Trade]
    equity_curve: List[EquityPoint]
```

## データベーススキーマ

```sql
CREATE TABLE backtest_jobs (
    job_id TEXT PRIMARY KEY,
    algorithm_id INTEGER NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    data_set_id INTEGER,
    status TEXT NOT NULL,
    progress REAL DEFAULT 0.0,
    message TEXT,
    error TEXT,
    created_at TEXT NOT NULL,
    completed_at TEXT,
    FOREIGN KEY (algorithm_id) REFERENCES algorithms(id),
    FOREIGN KEY (data_set_id) REFERENCES data_sets(id)
);

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
    created_at TEXT NOT NULL,
    FOREIGN KEY (job_id) REFERENCES backtest_jobs(job_id),
    FOREIGN KEY (algorithm_id) REFERENCES algorithms(id)
);

CREATE TABLE backtest_trades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id TEXT NOT NULL,
    entry_date TEXT NOT NULL,
    exit_date TEXT NOT NULL,
    entry_price REAL NOT NULL,
    exit_price REAL NOT NULL,
    quantity REAL NOT NULL,
    profit REAL NOT NULL,
    profit_rate REAL NOT NULL,
    FOREIGN KEY (job_id) REFERENCES backtest_jobs(job_id)
);

CREATE TABLE backtest_equity_curve (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id TEXT NOT NULL,
    date TEXT NOT NULL,
    equity REAL NOT NULL,
    FOREIGN KEY (job_id) REFERENCES backtest_jobs(job_id)
);

CREATE INDEX idx_backtest_jobs_status ON backtest_jobs(status);
CREATE INDEX idx_backtest_trades_job_id ON backtest_trades(job_id);
CREATE INDEX idx_backtest_equity_job_id ON backtest_equity_curve(job_id);
```

