"""
Backtest module initialization.

Related Documentation:
  └─ Plan: docs/03_plans/backtest/README.md
"""
from modules.backtest.backtest_engine import BacktestEngine
from modules.backtest.algorithm_parser import AlgorithmParser
from modules.backtest.signal_generator import SignalGenerator
from modules.backtest.trade_simulator import TradeSimulator
from modules.backtest.performance_calculator import PerformanceCalculator

__all__ = [
    'BacktestEngine',
    'AlgorithmParser',
    'SignalGenerator',
    'TradeSimulator',
    'PerformanceCalculator',
]
