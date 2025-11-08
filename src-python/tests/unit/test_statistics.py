"""
Unit tests for statistics calculation.
"""
import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from modules.data_analysis.statistics import StatisticsCalculator


@pytest.mark.unit
class TestStatisticsCalculator:
    """Test cases for StatisticsCalculator class."""
    
    @pytest.fixture
    def statistics_calculator(self):
        """Create StatisticsCalculator instance."""
        return StatisticsCalculator()
    
    @pytest.fixture
    def sample_data(self):
        """Create sample OHLCV data."""
        dates = pd.date_range('2023-01-01', periods=30, freq='D')
        prices = 100 + np.arange(30) * 0.5
        return pd.DataFrame({
            'date': dates,
            'open': prices,
            'high': prices + 1,
            'low': prices - 1,
            'close': prices + 0.3,
            'volume': np.random.randint(1000000, 2000000, 30)
        })
    
    def test_calculate_statistics_valid_data(self, statistics_calculator, sample_data):
        """Test statistics calculation with valid data."""
        result = statistics_calculator.calculate(sample_data)
        
        assert result is not None
        assert 'price_range' in result
        assert 'volume_average' in result
        assert 'price_change_percent' in result
        
        assert 'min' in result['price_range']
        assert 'max' in result['price_range']
        assert 'current' in result['price_range']
        
        assert result['price_range']['min'] <= result['price_range']['max']
        assert result['price_range']['current'] >= result['price_range']['min']
        assert result['price_range']['current'] <= result['price_range']['max']
        assert result['volume_average'] > 0
    
    def test_calculate_statistics_empty_data(self, statistics_calculator):
        """Test statistics calculation with empty data."""
        empty_data = pd.DataFrame(columns=['date', 'open', 'high', 'low', 'close', 'volume'])
        
        result = statistics_calculator.calculate(empty_data)
        assert result is None
    
    def test_calculate_statistics_single_point(self, statistics_calculator):
        """Test statistics calculation with single data point."""
        single_data = pd.DataFrame({
            'date': ['2023-01-01'],
            'open': [100.0],
            'high': [105.0],
            'low': [99.0],
            'close': [103.0],
            'volume': [1000000]
        })
        
        result = statistics_calculator.calculate(single_data)
        assert result is not None
        assert result['price_range']['min'] == result['price_range']['max']
        assert result['price_change_percent'] == 0.0
    
    def test_calculate_price_change_percent(self, statistics_calculator):
        """Test price change percentage calculation."""
        dates = pd.date_range('2023-01-01', periods=10, freq='D')
        # Start at 100, end at 110 (10% increase)
        prices = np.linspace(100, 110, 10)
        data = pd.DataFrame({
            'date': dates,
            'open': prices,
            'high': prices + 1,
            'low': prices - 1,
            'close': prices,
            'volume': np.random.randint(1000000, 2000000, 10)
        })
        
        result = statistics_calculator.calculate(data)
        assert result is not None
        # Should be approximately 10% (allowing for floating point precision)
        assert abs(result['price_change_percent'] - 10.0) < 1.0

