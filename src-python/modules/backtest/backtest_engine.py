"""
Backtest engine module.

Related Documentation:
  └─ Plan: docs/03_plans/backtest/README.md

DEPENDENCY MAP:

Parents (Files that import this file):
  └─ src-python/scripts/run_backtest.py

Dependencies (External files that this file imports):
  ├─ pandas
  ├─ typing (standard library)
  ├─ src-python/modules/backtest/algorithm_parser
  ├─ src-python/modules/backtest/signal_generator
  ├─ src-python/modules/backtest/trade_simulator
  └─ src-python/modules/backtest/performance_calculator
"""
import pandas as pd
from typing import Dict, Any, Optional
from modules.backtest.algorithm_parser import AlgorithmParser
from modules.backtest.signal_generator import SignalGenerator
from modules.backtest.trade_simulator import TradeSimulator
from modules.backtest.performance_calculator import PerformanceCalculator


class BacktestEngine:
    """Main backtest engine."""
    
    def __init__(
        self,
        algorithm: Dict[str, Any],
        data: pd.DataFrame,
        start_date: str,
        end_date: str,
        initial_capital: float = 100000.0
    ):
        """
        Initialize backtest engine.
        
        Args:
            algorithm: Algorithm definition
            data: DataFrame with OHLCV data
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            initial_capital: Initial capital for backtesting
        """
        self.algorithm = algorithm
        self.data = data
        self.start_date = start_date
        self.end_date = end_date
        self.initial_capital = initial_capital
        
        self.algorithm_parser = AlgorithmParser()
        self.signal_generator = SignalGenerator()
        self.trade_simulator = TradeSimulator(initial_capital)
        self.performance_calculator = PerformanceCalculator(initial_capital)
    
    def run(self) -> Dict[str, Any]:
        """
        Run backtest.
        
        Returns:
            Dict with backtest results
        """
        # 1. Filter data by date range
        filtered_data = self._filter_data()
        
        if filtered_data.empty:
            raise ValueError(f"No data available for date range {self.start_date} to {self.end_date}")
        
        # 2. Parse algorithm
        parsed_algorithm = self.algorithm_parser.parse_algorithm(self.algorithm)
        
        # 3. Generate signals
        signals_df = self.signal_generator.generate_signals(filtered_data, parsed_algorithm)
        
        # 4. Simulate trades
        trades = self.trade_simulator.simulate_trades(signals_df, parsed_algorithm)
        
        # 5. Calculate performance
        performance = self.performance_calculator.calculate_performance(trades)
        
        # 6. Calculate equity curve
        dates = filtered_data['date'].tolist()
        equity_curve = self.performance_calculator.calculate_equity_curve(trades, dates)
        
        return {
            'trades': trades,
            'performance': performance,
            'equity_curve': equity_curve
        }
    
    def _filter_data(self) -> pd.DataFrame:
        """
        Filter data by date range.
        
        Returns:
            Filtered DataFrame
        """
        if self.data.empty:
            return pd.DataFrame()
        
        # Ensure date column is datetime
        if not pd.api.types.is_datetime64_any_dtype(self.data['date']):
            self.data['date'] = pd.to_datetime(self.data['date'])
        
        # Filter by date range
        mask = (self.data['date'] >= self.start_date) & (self.data['date'] <= self.end_date)
        filtered = self.data[mask].copy()
        
        return filtered

