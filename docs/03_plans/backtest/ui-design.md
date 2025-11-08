# バックテスト機能 UI/UX設計書

## 概要

バックテスト機能のUI/UX設計詳細です。設定画面と結果表示画面の2つで構成されます。

## 画面レイアウト設計

### バックテスト設定画面

```
┌─────────────────────────────────────────────────────────┐
│ Backtest Settings                                            │
├─────────────────────────────────────────────────────────┤
│                                                          │
│ ┌────────────────────────────────────────────────────┐ │
│ │ Algorithm Selection                                │ │
│ │ [ ] Algorithm 1                                    │ │
│ │ [ ] Algorithm 2                                    │ │
│ │ [ ] Algorithm 3                                    │ │
│ └────────────────────────────────────────────────────┘ │
│                                                          │
│ ┌────────────────────────────────────────────────────┐ │
│ │ Date Range                                         │ │
│ │ Start: [2023-01-01]                               │ │
│ │ End:   [2023-12-31]                               │ │
│ └────────────────────────────────────────────────────┘ │
│                                                          │
│ ┌────────────────────────────────────────────────────┐ │
│ │ Data Set                                           │ │
│ │ [Select Data Set ▼]                                │ │
│ └────────────────────────────────────────────────────┘ │
│                                                          │
│ [Run Backtest]                                          │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### バックテスト結果画面

```
┌─────────────────────────────────────────────────────────┐
│ Backtest Results                                        │
├─────────────────────────────────────────────────────────┤
│                                                          │
│ ┌────────────────────────────────────────────────────┐ │
│ │ Performance Metrics                                │ │
│ │ Total Return: +15.2%                               │ │
│ │ Sharpe Ratio: 1.23                                 │ │
│ │ Max Drawdown: -8.5%                                │ │
│ │ Win Rate: 65.0%                                    │ │
│ └────────────────────────────────────────────────────┘ │
│                                                          │
│ ┌────────────────────────────────────────────────────┐ │
│ │ Equity Curve Chart                                 │ │
│ │ [Chart Area]                                       │ │
│ └────────────────────────────────────────────────────┘ │
│                                                          │
│ ┌────────────────────────────────────────────────────┐ │
│ │ Trade History                                      │ │
│ │ [Table]                                            │ │
│ └────────────────────────────────────────────────────┘ │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## コンポーネント構造

```
BacktestSettings/
├── BacktestSettings.tsx
├── AlgorithmSelector.tsx
├── DateRangePicker.tsx
└── DataSetSelector.tsx

BacktestResults/
├── BacktestResults.tsx
├── PerformanceMetrics.tsx
├── TradeHistory.tsx
└── EquityChart.tsx
```

## 状態管理

```typescript
interface BacktestSettingsState {
  selectedAlgorithmIds: number[];
  startDate: string;
  endDate: string;
  dataSetId: number | null;
}

interface BacktestResultsState {
  jobId: string | null;
  status: 'idle' | 'running' | 'completed' | 'error';
  progress: number;
  results: BacktestResult | null;
}
```

