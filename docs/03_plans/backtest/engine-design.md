# バックテストエンジン設計

## 概要

バックテストエンジンの設計詳細です。

## アーキテクチャ

```python
class BacktestEngine:
    def __init__(self, algorithm, data, start_date, end_date, initial_capital=100000):
        self.algorithm = algorithm
        self.data = data
        self.start_date = start_date
        self.end_date = end_date
        self.initial_capital = initial_capital
        
    def run(self):
        # 1. データフィルタリング
        filtered_data = self._filter_data()
        
        # 2. アルゴリズム実行
        signals = self._generate_signals(filtered_data)
        
        # 3. 取引シミュレーション
        trades = self._simulate_trades(signals, filtered_data)
        
        # 4. パフォーマンス計算
        performance = self._calculate_performance(trades)
        
        # 5. 結果返却
        return BacktestResult(
            trades=trades,
            performance=performance,
            equity_curve=self._calculate_equity_curve(trades)
        )
```

## 処理フロー

1. データフィルタリング（日付範囲）
2. シグナル生成（アルゴリズム定義に基づく）
3. 取引シミュレーション（エントリー/エグジット）
4. パフォーマンス指標計算
5. 結果の生成

## パフォーマンス指標計算

- 総リターン: (最終資産 - 初期資産) / 初期資産 * 100
- シャープレシオ: (平均リターン - リスクフリーレート) / リターンの標準偏差
- 最大ドローダウン: ピークから最大下落率
- 勝率: 利益が出た取引数 / 総取引数 * 100

