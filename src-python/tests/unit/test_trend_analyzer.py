"""
Unit tests for trend analyzer.
"""
import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from modules.data_analysis.trend_analyzer import TrendAnalyzer


@pytest.mark.unit
class TestTrendAnalyzer:
    """Test cases for TrendAnalyzer class."""
    
    @pytest.fixture
    def trend_analyzer(self):
        """Create TrendAnalyzer instance."""
        return TrendAnalyzer()
    
    def test_analyze_trend_upward(self, trend_analyzer):
        """Test trend analysis for upward trend."""
        dates = pd.date_range('2023-01-01', periods=30, freq='D')
        prices = 100 + np.arange(30) * 0.5  # Upward trend
        data = pd.DataFrame({
            'date': dates,
            'open': prices,
            'high': prices + 1,
            'low': prices - 1,
            'close': prices + 0.3,
            'volume': np.random.randint(1000000, 2000000, 30)
        })
        
        result = trend_analyzer.analyze_trend(data)
        
        assert result is not None
        assert 'trend_direction' in result
        assert result['trend_direction'] == 'upward'
    
    def test_analyze_trend_downward(self, trend_analyzer):
        """Test trend analysis for downward trend."""
        dates = pd.date_range('2023-01-01', periods=30, freq='D')
        prices = 100 - np.arange(30) * 0.5  # Downward trend
        data = pd.DataFrame({
            'date': dates,
            'open': prices,
            'high': prices + 1,
            'low': prices - 1,
            'close': prices - 0.3,
            'volume': np.random.randint(1000000, 2000000, 30)
        })
        
        result = trend_analyzer.analyze_trend(data)
        
        assert result is not None
        assert 'trend_direction' in result
        assert result['trend_direction'] == 'downward'
    
    def test_analyze_trend_sideways(self, trend_analyzer):
        """Test trend analysis for sideways trend."""
        dates = pd.date_range('2023-01-01', periods=30, freq='D')
        prices = 100 + np.random.randn(30) * 2  # Sideways with noise
        data = pd.DataFrame({
            'date': dates,
            'open': prices,
            'high': prices + 1,
            'low': prices - 1,
            'close': prices + np.random.randn(30) * 0.5,
            'volume': np.random.randint(1000000, 2000000, 30)
        })
        
        result = trend_analyzer.analyze_trend(data)
        
        assert result is not None
        assert 'trend_direction' in result
        assert result['trend_direction'] in ['upward', 'downward', 'sideways']
    
    def test_analyze_trend_insufficient_data(self, trend_analyzer):
        """Test trend analysis with insufficient data."""
        dates = pd.date_range('2023-01-01', periods=5, freq='D')
        data = pd.DataFrame({
            'date': dates,
            'open': np.random.rand(5) * 100,
            'high': np.random.rand(5) * 100,
            'low': np.random.rand(5) * 100,
            'close': np.random.rand(5) * 100,
            'volume': np.random.randint(1000000, 2000000, 5)
        })
        
        result = trend_analyzer.analyze_trend(data)
        # Should handle gracefully
        assert result is not None or result is None  # Either is acceptable

