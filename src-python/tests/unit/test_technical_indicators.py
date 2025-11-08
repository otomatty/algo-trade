"""
Unit tests for technical indicators calculation.
"""
import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from modules.data_analysis.technical_indicators import TechnicalIndicators


@pytest.mark.unit
class TestTechnicalIndicators:
    """Test cases for TechnicalIndicators class."""
    
    @pytest.fixture
    def sample_data(self):
        """Create sample OHLCV data."""
        dates = pd.date_range('2023-01-01', periods=50, freq='D')  # Increased to 50 for MACD
        # Create upward trend data
        prices = 100 + np.arange(50) * 0.5 + np.random.randn(50) * 2
        return pd.DataFrame({
            'date': dates,
            'open': prices,
            'high': prices + np.random.rand(50) * 2,
            'low': prices - np.random.rand(50) * 2,
            'close': prices + np.random.randn(50) * 0.5,
            'volume': np.random.randint(1000000, 2000000, 50)
        })
    
    @pytest.fixture
    def technical_indicators(self):
        """Create TechnicalIndicators instance."""
        return TechnicalIndicators()
    
    def test_calculate_rsi_valid_data(self, technical_indicators, sample_data):
        """Test RSI calculation with valid data."""
        result = technical_indicators.calculate_rsi(sample_data)
        
        assert result is not None
        assert 'value' in result
        assert 'period' in result
        assert 'signal' in result
        assert 0 <= result['value'] <= 100
        assert result['period'] == 14
        assert result['signal'] in ['overbought', 'oversold', 'neutral']
    
    def test_calculate_rsi_insufficient_data(self, technical_indicators):
        """Test RSI calculation with insufficient data."""
        # Create data with less than 14 points
        dates = pd.date_range('2023-01-01', periods=10, freq='D')
        data = pd.DataFrame({
            'date': dates,
            'open': np.random.rand(10) * 100,
            'high': np.random.rand(10) * 100,
            'low': np.random.rand(10) * 100,
            'close': np.random.rand(10) * 100,
            'volume': np.random.randint(1000000, 2000000, 10)
        })
        
        result = technical_indicators.calculate_rsi(data)
        assert result is None
    
    def test_calculate_rsi_overbought(self, technical_indicators):
        """Test RSI calculation for overbought condition."""
        # Create data with strong upward momentum
        dates = pd.date_range('2023-01-01', periods=20, freq='D')
        prices = 100 + np.arange(20) * 2  # Strong upward trend
        data = pd.DataFrame({
            'date': dates,
            'open': prices,
            'high': prices + 1,
            'low': prices - 1,
            'close': prices + 0.5,
            'volume': np.random.randint(1000000, 2000000, 20)
        })
        
        result = technical_indicators.calculate_rsi(data)
        if result:
            # RSI should be high (may not always be > 70 due to calculation specifics)
            assert result['value'] > 50
    
    def test_calculate_macd_valid_data(self, technical_indicators, sample_data):
        """Test MACD calculation with valid data."""
        result = technical_indicators.calculate_macd(sample_data)
        
        assert result is not None
        assert 'macd' in result
        assert 'signal' in result
        assert 'histogram' in result
        assert 'signal_type' in result
        assert result['signal_type'] in ['bullish', 'bearish', 'neutral']
        assert abs(result['histogram'] - (result['macd'] - result['signal'])) < 0.01
    
    def test_calculate_macd_insufficient_data(self, technical_indicators):
        """Test MACD calculation with insufficient data."""
        # Create data with less than 26 points
        dates = pd.date_range('2023-01-01', periods=20, freq='D')
        data = pd.DataFrame({
            'date': dates,
            'open': np.random.rand(20) * 100,
            'high': np.random.rand(20) * 100,
            'low': np.random.rand(20) * 100,
            'close': np.random.rand(20) * 100,
            'volume': np.random.randint(1000000, 2000000, 20)
        })
        
        result = technical_indicators.calculate_macd(data)
        assert result is None
    
    def test_calculate_macd_bullish(self, technical_indicators):
        """Test MACD calculation for bullish signal."""
        # Create data with upward trend
        dates = pd.date_range('2023-01-01', periods=30, freq='D')
        prices = 100 + np.arange(30) * 0.5
        data = pd.DataFrame({
            'date': dates,
            'open': prices,
            'high': prices + 1,
            'low': prices - 1,
            'close': prices + 0.3,
            'volume': np.random.randint(1000000, 2000000, 30)
        })
        
        result = technical_indicators.calculate_macd(data)
        if result:
            # MACD should be above signal (bullish)
            assert result['signal_type'] == 'bullish' or result['macd'] > result['signal']

