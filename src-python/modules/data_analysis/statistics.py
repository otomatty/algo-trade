"""
Statistics calculation module.

Related Documentation:
  ├─ Spec: src-python/modules/data_analysis/analyzer.spec.md
  └─ Plan: docs/03_plans/data-analysis/README.md
"""
import pandas as pd
import numpy as np
from typing import Dict, Optional


class StatisticsCalculator:
    """Calculate statistics from OHLCV data."""
    
    def calculate(self, data: pd.DataFrame) -> Optional[Dict]:
        """
        Calculate statistics from OHLCV data.
        
        Args:
            data: DataFrame with OHLCV data
        
        Returns:
            Dict with 'price_range', 'volume_average', 'price_change_percent' or None if empty
        """
        if len(data) == 0:
            return None
        
        close_prices = data['close'].values
        volumes = data['volume'].values
        
        # Price range
        price_range = {
            'min': float(np.min(close_prices)),
            'max': float(np.max(close_prices)),
            'current': float(close_prices[-1])
        }
        
        # Average volume
        volume_average = float(np.mean(volumes))
        
        # Price change percentage
        if len(close_prices) > 1:
            price_change_percent = ((close_prices[-1] - close_prices[0]) / close_prices[0]) * 100
        else:
            price_change_percent = 0.0
        
        return {
            'price_range': price_range,
            'volume_average': round(volume_average, 2),
            'price_change_percent': round(price_change_percent, 2)
        }

