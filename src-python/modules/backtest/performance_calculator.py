"""
Performance calculator module for backtest engine.

Related Documentation:
  └─ Plan: docs/03_plans/backtest/README.md

DEPENDENCY MAP:

Parents (Files that import this file):
  └─ src-python/modules/backtest/backtest_engine.py

Dependencies (External files that this file imports):
  ├─ typing (standard library)
  └─ numpy
"""
from typing import List, Dict, Any
import numpy as np


class PerformanceCalculator:
    """Calculate performance metrics from trades."""
    
    def __init__(self, initial_capital: float = 100000.0, risk_free_rate: float = 0.0):
        """
        Initialize performance calculator.
        
        Args:
            initial_capital: Initial capital
            risk_free_rate: Risk-free rate for Sharpe ratio calculation (default: 0.0)
        """
        self.initial_capital = initial_capital
        self.risk_free_rate = risk_free_rate
    
    def calculate_performance(self, trades: List[Dict[str, Any]]) -> Dict[str, float]:
        """
        Calculate performance metrics from trades.
        
        Args:
            trades: List of trade dictionaries
        
        Returns:
            Dict with performance metrics
        """
        if not trades:
            return {
                'total_return': 0.0,
                'sharpe_ratio': 0.0,
                'max_drawdown': 0.0,
                'win_rate': 0.0,
                'total_trades': 0,
                'average_profit': 0.0,
                'average_loss': 0.0
            }
        
        # Calculate total return
        total_profit = sum(trade['profit'] for trade in trades)
        total_return = (total_profit / self.initial_capital) * 100
        
        # Calculate win rate
        winning_trades = [t for t in trades if t['profit'] > 0]
        losing_trades = [t for t in trades if t['profit'] < 0]
        win_rate = (len(winning_trades) / len(trades)) * 100 if trades else 0.0
        
        # Calculate average profit and loss
        average_profit = np.mean([t['profit'] for t in winning_trades]) if winning_trades else 0.0
        average_loss = np.mean([t['profit'] for t in losing_trades]) if losing_trades else 0.0
        
        # Calculate Sharpe ratio (simplified)
        returns = [t['profit_rate'] / 100.0 for t in trades]
        if len(returns) > 1:
            mean_return = np.mean(returns)
            std_return = np.std(returns)
            sharpe_ratio = (mean_return - self.risk_free_rate) / std_return if std_return > 0 else 0.0
        else:
            sharpe_ratio = 0.0
        
        # Calculate max drawdown (simplified - based on trade profits)
        cumulative_profit = 0.0
        peak = 0.0
        max_drawdown = 0.0
        
        for trade in trades:
            cumulative_profit += trade['profit']
            if cumulative_profit > peak:
                peak = cumulative_profit
            drawdown = peak - cumulative_profit
            if drawdown > max_drawdown:
                max_drawdown = drawdown
        
        max_drawdown_percent = (max_drawdown / self.initial_capital) * 100 if self.initial_capital > 0 else 0.0
        
        return {
            'total_return': round(total_return, 2),
            'sharpe_ratio': round(sharpe_ratio, 2),
            'max_drawdown': round(max_drawdown_percent, 2),
            'win_rate': round(win_rate, 2),
            'total_trades': len(trades),
            'average_profit': round(average_profit, 2),
            'average_loss': round(average_loss, 2)
        }
    
    def calculate_equity_curve(
        self,
        trades: List[Dict[str, Any]],
        dates: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Calculate equity curve over time.
        
        Args:
            trades: List of trade dictionaries
            dates: List of dates in the backtest period
        
        Returns:
            List of equity points (date, equity)
        """
        equity_curve = []
        capital = self.initial_capital
        
        # Create a map of trades by exit date
        trades_by_date = {}
        for trade in trades:
            exit_date = trade['exit_date']
            if exit_date not in trades_by_date:
                trades_by_date[exit_date] = []
            trades_by_date[exit_date].append(trade)
        
        # Track open positions
        open_positions = {}  # {entry_date: trade}
        
        for date in dates:
            # Close positions that exit on this date
            if date in trades_by_date:
                for trade in trades_by_date[date]:
                    capital += trade['quantity'] * trade['exit_price']
            
            # Add equity point
            equity_curve.append({
                'date': date,
                'equity': round(capital, 2)
            })
        
        return equity_curve

