"""
Technical indicators calculation module.

Related Documentation:
  ├─ Spec: src-python/modules/data_analysis/analyzer.spec.md
  └─ Plan: docs/03_plans/data-analysis/README.md
"""
import pandas as pd
import numpy as np
from typing import Dict, Optional


class TechnicalIndicators:
    """Calculate technical indicators from OHLCV data."""
    
    def calculate_rsi(self, data: pd.DataFrame, period: int = 14) -> Optional[Dict]:
        """
        Calculate RSI (Relative Strength Index).
        
        Args:
            data: DataFrame with OHLCV data
            period: RSI period (default: 14)
        
        Returns:
            Dict with 'value', 'period', 'signal' or None if insufficient data
        """
        if len(data) < period + 1:
            return None
        
        # Calculate price changes
        close_prices = data['close'].values
        deltas = np.diff(close_prices)
        
        # Separate gains and losses
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)
        
        # Calculate average gain and loss using Wilder's smoothing
        avg_gain = np.mean(gains[:period])
        avg_loss = np.mean(losses[:period])
        
        for i in range(period, len(deltas)):
            avg_gain = (avg_gain * (period - 1) + gains[i]) / period
            avg_loss = (avg_loss * (period - 1) + losses[i]) / period
        
        # Calculate RS and RSI
        if avg_loss == 0:
            rsi = 100.0
        else:
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))
        
        # Determine signal
        if rsi > 70:
            signal = 'overbought'
        elif rsi < 30:
            signal = 'oversold'
        else:
            signal = 'neutral'
        
        return {
            'value': round(rsi, 2),
            'period': period,
            'signal': signal
        }
    
    def calculate_macd(self, data: pd.DataFrame, fast_period: int = 12, slow_period: int = 26, signal_period: int = 9) -> Optional[Dict]:
        """
        Calculate MACD (Moving Average Convergence Divergence).
        
        Args:
            data: DataFrame with OHLCV data
            fast_period: Fast EMA period (default: 12)
            slow_period: Slow EMA period (default: 26)
            signal_period: Signal line EMA period (default: 9)
        
        Returns:
            Dict with 'macd', 'signal', 'histogram', 'signal_type' or None if insufficient data
        """
        if len(data) < slow_period + signal_period:
            return None
        
        close_prices = data['close'].values
        
        # Calculate EMAs
        fast_ema = self._calculate_ema(close_prices, fast_period)
        slow_ema = self._calculate_ema(close_prices, slow_period)
        
        # Align EMAs - use the shorter length
        min_length = min(len(fast_ema), len(slow_ema))
        if min_length < signal_period:
            return None
        
        fast_ema_aligned = fast_ema[-min_length:]
        slow_ema_aligned = slow_ema[-min_length:]
        
        # MACD line
        macd_line = fast_ema_aligned - slow_ema_aligned
        
        # Signal line (EMA of MACD line)
        signal_line = self._calculate_ema(macd_line, signal_period)
        
        if len(signal_line) == 0:
            return None
        
        # Histogram
        histogram = macd_line[-len(signal_line):] - signal_line
        
        # Current values
        current_macd = macd_line[-1]
        current_signal = signal_line[-1]
        current_histogram = histogram[-1]
        
        # Determine signal type
        if current_macd > current_signal:
            signal_type = 'bullish'
        elif current_macd < current_signal:
            signal_type = 'bearish'
        else:
            signal_type = 'neutral'
        
        return {
            'macd': round(current_macd, 4),
            'signal': round(current_signal, 4),
            'histogram': round(current_histogram, 4),
            'signal_type': signal_type
        }
    
    def _calculate_ema(self, prices: np.ndarray, period: int) -> np.ndarray:
        """Calculate Exponential Moving Average."""
        ema = np.zeros(len(prices))
        ema[0] = prices[0]
        
        multiplier = 2 / (period + 1)
        
        for i in range(1, len(prices)):
            ema[i] = (prices[i] * multiplier) + (ema[i - 1] * (1 - multiplier))
        
        return ema[period - 1:]

