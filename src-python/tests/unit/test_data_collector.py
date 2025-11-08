"""
Unit tests for data collector.
"""
import pytest
import pandas as pd
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from modules.data_collection.data_collector import DataCollector


@pytest.mark.unit
class TestDataCollector:
    """Test cases for DataCollector class."""
    
    def test_collect_from_api_yahoo_success(self, mocker, temp_db):
        """Test successful data collection from Yahoo Finance."""
        # Mock Yahoo Finance client
        mock_client_class = mocker.patch('modules.data_collection.data_collector.YahooFinanceClient')
        mock_client = mocker.MagicMock()
        mock_df = pd.DataFrame({
            'date': ['2023-01-01', '2023-01-02'],
            'open': [100.0, 103.0],
            'high': [105.0, 108.0],
            'low': [99.0, 102.0],
            'close': [103.0, 106.0],
            'volume': [1000000, 1200000]
        })
        mock_client.fetch_ohlcv.return_value = mock_df
        mock_client_class.return_value = mock_client
        
        conn = sqlite3.connect(temp_db)
        collector = DataCollector(conn=conn)
        result = collector.collect_from_api(
            source='yahoo',
            symbol='AAPL',
            start_date='2023-01-01',
            end_date='2023-01-02',
            name='Test Dataset'
        )
        
        assert result['success'] is True
        assert 'data_set_id' in result['data']
        assert result['data']['name'] == 'Test Dataset'
        assert result['data']['record_count'] == 2
        assert result['data']['symbol'] == 'AAPL'
    
    def test_collect_from_api_alphavantage_success(self, mocker, temp_db):
        """Test successful data collection from Alpha Vantage."""
        # Mock Alpha Vantage client
        mock_client_class = mocker.patch('modules.data_collection.data_collector.AlphaVantageClient')
        mock_client = mocker.MagicMock()
        mock_df = pd.DataFrame({
            'date': ['2023-01-01', '2023-01-02'],
            'open': [100.0, 103.0],
            'high': [105.0, 108.0],
            'low': [99.0, 102.0],
            'close': [103.0, 106.0],
            'volume': [1000000, 1200000]
        })
        mock_client.fetch_ohlcv.return_value = mock_df
        mock_client_class.return_value = mock_client
        
        conn = sqlite3.connect(temp_db)
        collector = DataCollector(conn=conn)
        result = collector.collect_from_api(
            source='alphavantage',
            symbol='AAPL',
            start_date='2023-01-01',
            end_date='2023-01-02',
            name='Test Dataset',
            api_key='test_key'
        )
        
        assert result['success'] is True
        assert 'data_set_id' in result['data']
    
    def test_collect_from_api_alphavantage_no_key(self, temp_db):
        """Test error when Alpha Vantage API key is missing."""
        conn = sqlite3.connect(temp_db)
        collector = DataCollector(conn=conn)
        result = collector.collect_from_api(
            source='alphavantage',
            symbol='AAPL',
            start_date='2023-01-01',
            end_date='2023-01-02'
        )
        
        assert result['success'] is False
        assert 'API key is required' in result['error']
    
    def test_collect_from_api_unknown_source(self, temp_db):
        """Test error for unknown data source."""
        conn = sqlite3.connect(temp_db)
        collector = DataCollector(conn=conn)
        result = collector.collect_from_api(
            source='unknown',
            symbol='AAPL',
            start_date='2023-01-01',
            end_date='2023-01-02'
        )
        
        assert result['success'] is False
        assert 'Unknown data source' in result['error']
    
    def test_collect_from_api_fetch_error(self, mocker, temp_db):
        """Test error handling when API fetch fails."""
        mock_client_class = mocker.patch('modules.data_collection.data_collector.YahooFinanceClient')
        mock_client = mocker.MagicMock()
        mock_client.fetch_ohlcv.side_effect = Exception("Network error")
        mock_client_class.return_value = mock_client
        
        conn = sqlite3.connect(temp_db)
        collector = DataCollector(conn=conn)
        result = collector.collect_from_api(
            source='yahoo',
            symbol='AAPL',
            start_date='2023-01-01',
            end_date='2023-01-02'
        )
        
        assert result['success'] is False
        assert 'error' in result
    
    def test_collect_from_api_auto_name(self, mocker, temp_db):
        """Test auto-generated dataset name."""
        mock_client_class = mocker.patch('modules.data_collection.data_collector.YahooFinanceClient')
        mock_client = mocker.MagicMock()
        mock_df = pd.DataFrame({
            'date': ['2023-01-01'],
            'open': [100.0],
            'high': [105.0],
            'low': [99.0],
            'close': [103.0],
            'volume': [1000000]
        })
        mock_client.fetch_ohlcv.return_value = mock_df
        mock_client_class.return_value = mock_client
        
        conn = sqlite3.connect(temp_db)
        collector = DataCollector(conn=conn)
        result = collector.collect_from_api(
            source='yahoo',
            symbol='AAPL',
            start_date='2023-01-01',
            end_date='2023-01-02'
        )
        
        assert result['success'] is True
        assert result['data']['name'] == 'AAPL_2023-01-01_2023-01-02'

