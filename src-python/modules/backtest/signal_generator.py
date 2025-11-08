"""
Signal generator module for backtest engine.

Related Documentation:
  └─ Plan: docs/03_plans/backtest/README.md

DEPENDENCY MAP:

Parents (Files that import this file):
  └─ src-python/modules/backtest/backtest_engine.py

Dependencies (External files that this file imports):
  ├─ pandas
  ├─ typing (standard library)
  ├─ src-python/modules/backtest/algorithm_parser
  └─ src-python/modules/data_analysis/technical_indicators
"""
import pandas as pd
from typing import Dict, Any, List, Optional
from modules.backtest.algorithm_parser import AlgorithmParser
from modules.data_analysis.technical_indicators import TechnicalIndicators


class SignalGenerator:
    """Generate trading signals based on algorithm definitions."""
    
    def __init__(self):
        """Initialize signal generator."""
        self.algorithm_parser = AlgorithmParser()
        self.technical_indicators = TechnicalIndicators()
    
    def generate_signals(
        self,
        data: pd.DataFrame,
        algorithm: Dict[str, Any]
    ) -> pd.DataFrame:
        """
        Generate trading signals for the given data and algorithm.
        
        Args:
            data: DataFrame with OHLCV data (columns: date, open, high, low, close, volume)
            algorithm: Parsed algorithm definition
        
        Returns:
            DataFrame with signals added (columns: date, open, high, low, close, volume, signal)
            signal values: 'buy', 'sell', 'hold', None
        """
        signals_df = data.copy()
        signals_df['signal'] = None
        
        triggers = algorithm.get('triggers', [])
        actions = algorithm.get('actions', [])
        
        if not triggers or not actions:
            return signals_df
        
        # Calculate technical indicators for all data
        indicator_values_cache = self._calculate_indicators(data)
        
        # Generate signals for each row
        for idx, row in signals_df.iterrows():
            price_data = {
                'open': row['open'],
                'high': row['high'],
                'low': row['low'],
                'close': row['close'],
                'volume': row['volume']
            }
            
            # Get indicator values up to current index
            indicator_values = self._get_indicator_values(indicator_values_cache, idx)
            
            # Evaluate triggers
            trigger_satisfied = self.algorithm_parser.evaluate_triggers(
                triggers,
                indicator_values,
                price_data
            )
            
            if trigger_satisfied:
                # Get action (use first action for now)
                action = actions[0] if actions else None
                if action:
                    signal_type = action.get('type', 'hold')
                    signals_df.at[idx, 'signal'] = signal_type
        
        return signals_df
    
    def _calculate_indicators(self, data: pd.DataFrame) -> Dict[str, List[Optional[float]]]:
        """
        Calculate technical indicators for all data points.
        
        Args:
            data: DataFrame with OHLCV data
        
        Returns:
            Dict with indicator names as keys and lists of values as values
        """
        indicators = {
            'rsi': [],
            'macd': [],
            'ma_20': [],
            'ma_50': [],
        }
        
        # Calculate RSI
        for i in range(len(data)):
            subset = data.iloc[:i+1]
            rsi_result = self.technical_indicators.calculate_rsi(subset, period=14)
            indicators['rsi'].append(rsi_result['value'] if rsi_result else None)
        
        # Calculate MACD
        for i in range(len(data)):
            subset = data.iloc[:i+1]
            macd_result = self.technical_indicators.calculate_macd(subset)
            indicators['macd'].append(macd_result['macd'] if macd_result else None)
        
        # Calculate Moving Averages
        for i in range(len(data)):
            subset = data.iloc[:i+1]
            ma_20 = subset['close'].tail(20).mean() if len(subset) >= 20 else None
            ma_50 = subset['close'].tail(50).mean() if len(subset) >= 50 else None
            indicators['ma_20'].append(ma_20)
            indicators['ma_50'].append(ma_50)
        
        return indicators
    
    def _get_indicator_values(
        self,
        indicator_cache: Dict[str, List[Optional[float]]],
        index: int
    ) -> Dict[str, float]:
        """
        Get indicator values at a specific index.
        
        Args:
            indicator_cache: Cached indicator values
            index: Index to get values for
        
        Returns:
            Dict with indicator values (None values are filtered out)
        """
        values = {}
        for indicator_name, value_list in indicator_cache.items():
            if index < len(value_list) and value_list[index] is not None:
                values[indicator_name] = value_list[index]
        return values

