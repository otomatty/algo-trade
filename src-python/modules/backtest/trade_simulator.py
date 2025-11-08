"""
Trade simulator module for backtest engine.

Related Documentation:
  └─ Plan: docs/03_plans/backtest/README.md

DEPENDENCY MAP:

Parents (Files that import this file):
  └─ src-python/modules/backtest/backtest_engine.py

Dependencies (External files that this file imports):
  ├─ pandas
  ├─ typing (standard library)
  └─ datetime (standard library)
"""
import pandas as pd
from typing import List, Dict, Any, Optional
from datetime import datetime


class TradeSimulator:
    """Simulate trades based on signals."""
    
    def __init__(self, initial_capital: float = 100000.0):
        """
        Initialize trade simulator.
        
        Args:
            initial_capital: Initial capital for backtesting
        """
        self.initial_capital = initial_capital
    
    def simulate_trades(
        self,
        signals_df: pd.DataFrame,
        algorithm: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Simulate trades based on signals.
        
        Args:
            signals_df: DataFrame with signals (columns: date, open, high, low, close, volume, signal)
            algorithm: Algorithm definition with actions
        
        Returns:
            List of trade dictionaries
        """
        trades = []
        position = None  # {'entry_date', 'entry_price', 'quantity'}
        capital = self.initial_capital
        
        actions = algorithm.get('actions', [])
        if not actions:
            return trades
        
        action = actions[0]  # Use first action for now
        action_type = action.get('type', 'hold')
        parameters = action.get('parameters', {})
        
        for idx, row in signals_df.iterrows():
            signal = row['signal']
            date = row['date']
            close_price = row['close']
            
            if signal == 'buy' and position is None:
                # Enter position
                quantity = self._calculate_quantity(capital, close_price, parameters)
                if quantity > 0:
                    position = {
                        'entry_date': date,
                        'entry_price': close_price,
                        'quantity': quantity
                    }
                    capital -= quantity * close_price
            
            elif signal == 'sell' and position is not None:
                # Exit position
                exit_price = close_price
                profit = (exit_price - position['entry_price']) * position['quantity']
                profit_rate = (profit / (position['entry_price'] * position['quantity'])) * 100
                
                trade = {
                    'entry_date': position['entry_date'],
                    'exit_date': date,
                    'entry_price': position['entry_price'],
                    'exit_price': exit_price,
                    'quantity': position['quantity'],
                    'profit': round(profit, 2),
                    'profit_rate': round(profit_rate, 2)
                }
                trades.append(trade)
                
                capital += position['quantity'] * exit_price
                position = None
        
        # Close any open position at the end
        if position is not None:
            last_row = signals_df.iloc[-1]
            exit_price = last_row['close']
            profit = (exit_price - position['entry_price']) * position['quantity']
            profit_rate = (profit / (position['entry_price'] * position['quantity'])) * 100
            
            trade = {
                'entry_date': position['entry_date'],
                'exit_date': last_row['date'],
                'entry_price': position['entry_price'],
                'exit_price': exit_price,
                'quantity': position['quantity'],
                'profit': round(profit, 2),
                'profit_rate': round(profit_rate, 2)
            }
            trades.append(trade)
        
        return trades
    
    def _calculate_quantity(
        self,
        capital: float,
        price: float,
        parameters: Dict[str, Any]
    ) -> float:
        """
        Calculate quantity to buy based on capital and parameters.
        
        Args:
            capital: Available capital
            price: Current price
            parameters: Action parameters
        
        Returns:
            Quantity to buy
        """
        # Use percentage if specified, otherwise use all capital
        percentage = parameters.get('percentage', 100.0)
        quantity_percentage = percentage / 100.0
        
        available_capital = capital * quantity_percentage
        quantity = available_capital / price
        
        # Round down to avoid fractional shares
        return int(quantity)

