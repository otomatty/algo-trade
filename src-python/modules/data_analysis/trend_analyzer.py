"""
Trend analysis module.

Related Documentation:
  ├─ Spec: src-python/modules/data_analysis/analyzer.spec.md
  └─ Plan: docs/03_plans/data-analysis/README.md
"""
import pandas as pd
import numpy as np
from typing import Dict, Optional


class TrendAnalyzer:
    """Analyze price trends from OHLCV data."""
    
    def analyze_trend(self, data: pd.DataFrame) -> Optional[Dict]:
        """
        Analyze trend direction from OHLCV data.
        
        Args:
            data: DataFrame with OHLCV data
        
        Returns:
            Dict with 'trend_direction' and 'volatility_level' or None if insufficient data
        """
        if len(data) < 2:
            return None
        
        close_prices = data['close'].values
        high_prices = data['high'].values
        low_prices = data['low'].values
        
        # Calculate moving averages
        sma_20 = self._calculate_sma(close_prices, min(20, len(close_prices)))
        sma_50 = self._calculate_sma(close_prices, min(50, len(close_prices)))
        
        # Determine trend direction
        trend_direction = self._determine_trend_direction(close_prices, sma_20, sma_50)
        
        # Calculate volatility
        volatility_level = self._calculate_volatility(close_prices)
        
        # Identify dominant patterns (simplified)
        dominant_patterns = self._identify_patterns(close_prices, high_prices, low_prices)
        
        return {
            'trend_direction': trend_direction,
            'volatility_level': volatility_level,
            'dominant_patterns': dominant_patterns
        }
    
    def _calculate_sma(self, prices: np.ndarray, period: int) -> np.ndarray:
        """Calculate Simple Moving Average."""
        if len(prices) < period:
            return np.array([])
        
        sma = np.zeros(len(prices) - period + 1)
        for i in range(len(sma)):
            sma[i] = np.mean(prices[i:i + period])
        
        return sma
    
    def _determine_trend_direction(self, prices: np.ndarray, sma_20: np.ndarray, sma_50: np.ndarray) -> str:
        """Determine trend direction based on price and moving averages."""
        if len(prices) < 2:
            return 'sideways'
        
        # Compare first and last prices
        price_change = (prices[-1] - prices[0]) / prices[0]
        
        # Check moving average slopes
        sma_20_slope = 0
        if len(sma_20) >= 2:
            sma_20_slope = (sma_20[-1] - sma_20[0]) / sma_20[0]
        
        sma_50_slope = 0
        if len(sma_50) >= 2:
            sma_50_slope = (sma_50[-1] - sma_50[0]) / sma_50[0]
        
        # Determine trend
        if price_change > 0.02 and sma_20_slope > 0:
            return 'upward'
        elif price_change < -0.02 and sma_20_slope < 0:
            return 'downward'
        else:
            return 'sideways'
    
    def _calculate_volatility(self, prices: np.ndarray) -> str:
        """Calculate volatility level."""
        if len(prices) < 2:
            return 'low'
        
        returns = np.diff(prices) / prices[:-1]
        volatility = np.std(returns)
        
        if volatility > 0.03:  # 3% daily volatility threshold
            return 'high'
        elif volatility > 0.015:  # 1.5% daily volatility threshold
            return 'medium'
        else:
            return 'low'
    
    def _identify_patterns(self, close: np.ndarray, high: np.ndarray, low: np.ndarray) -> list:
        """Identify dominant price patterns."""
        patterns = []
        
        if len(close) < 5:
            return patterns
        
        # Check for higher highs and higher lows (uptrend pattern)
        recent_highs = high[-5:]
        recent_lows = low[-5:]
        
        if len(recent_highs) >= 3 and recent_highs[-1] > recent_highs[-3]:
            patterns.append('higher_highs')
        
        if len(recent_lows) >= 3 and recent_lows[-1] > recent_lows[-3]:
            patterns.append('higher_lows')
        
        # Check for lower highs and lower lows (downtrend pattern)
        if len(recent_highs) >= 3 and recent_highs[-1] < recent_highs[-3]:
            patterns.append('lower_highs')
        
        if len(recent_lows) >= 3 and recent_lows[-1] < recent_lows[-3]:
            patterns.append('lower_lows')
        
        return patterns

