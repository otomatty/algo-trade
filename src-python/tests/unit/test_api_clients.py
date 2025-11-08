"""
Unit tests for API clients.
"""
import pytest
import pandas as pd
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from modules.data_collection.api_clients import YahooFinanceClient, AlphaVantageClient


@pytest.mark.unit
class TestYahooFinanceClient:
    """Test cases for YahooFinanceClient."""
    
    def test_fetch_ohlcv_success(self, mocker):
        """Test successful data fetch from Yahoo Finance."""
        # Mock yfinance module
        mock_ticker = mocker.MagicMock()
        # Create DataFrame with Date index (as yfinance returns)
        mock_history = pd.DataFrame({
            'Open': [100.0, 103.0],
            'High': [105.0, 108.0],
            'Low': [99.0, 102.0],
            'Close': [103.0, 106.0],
            'Volume': [1000000, 1200000]
        }, index=pd.to_datetime(['2023-01-01', '2023-01-02']))
        mock_history.index.name = 'Date'  # Set index name as yfinance does
        mock_ticker.history.return_value = mock_history
        
        mock_yf = mocker.MagicMock()
        mock_yf.Ticker = mocker.Mock(return_value=mock_ticker)
        
        # Patch yfinance import in the module
        mocker.patch('modules.data_collection.api_clients.yf', mock_yf, create=True)
        
        client = YahooFinanceClient()
        client.yf = mock_yf  # Ensure mock is used
        df = client.fetch_ohlcv('AAPL', '2023-01-01', '2023-01-02')
        
        assert len(df) == 2
        assert 'date' in df.columns
        assert 'open' in df.columns
        assert 'high' in df.columns
        assert 'low' in df.columns
        assert 'close' in df.columns
        assert 'volume' in df.columns
        assert df['date'].iloc[0] == '2023-01-01'
        assert df['open'].iloc[0] == 100.0
    
    def test_fetch_ohlcv_empty(self, mocker):
        """Test handling of empty data from Yahoo Finance."""
        mock_ticker = mocker.MagicMock()
        mock_ticker.history.return_value = pd.DataFrame()
        
        mock_yf = mocker.MagicMock()
        mock_yf.Ticker = mocker.Mock(return_value=mock_ticker)
        
        mocker.patch('modules.data_collection.api_clients.yf', mock_yf, create=True)
        
        client = YahooFinanceClient()
        client.yf = mock_yf  # Ensure mock is used
        
        with pytest.raises(Exception, match="No data found"):
            client.fetch_ohlcv('INVALID', '2023-01-01', '2023-01-02')
    
    def test_fetch_ohlcv_error(self, mocker):
        """Test error handling."""
        mock_yf = mocker.MagicMock()
        mock_yf.Ticker = mocker.Mock(side_effect=Exception("Network error"))
        
        mocker.patch('modules.data_collection.api_clients.yf', mock_yf, create=True)
        
        client = YahooFinanceClient()
        client.yf = mock_yf  # Ensure mock is used
        
        with pytest.raises(Exception, match="Failed to fetch data"):
            client.fetch_ohlcv('AAPL', '2023-01-01', '2023-01-02')


@pytest.mark.unit
class TestAlphaVantageClient:
    """Test cases for AlphaVantageClient."""
    
    def test_fetch_ohlcv_success(self, mocker):
        """Test successful data fetch from Alpha Vantage."""
        mock_requests = mocker.patch('modules.data_collection.api_clients.requests')
        mock_response = mocker.Mock()
        mock_response.json.return_value = {
            'Time Series (Daily)': {
                '2023-01-01': {
                    '1. open': '100.0',
                    '2. high': '105.0',
                    '3. low': '99.0',
                    '4. close': '103.0',
                    '5. volume': '1000000'
                },
                '2023-01-02': {
                    '1. open': '103.0',
                    '2. high': '108.0',
                    '3. low': '102.0',
                    '4. close': '106.0',
                    '5. volume': '1200000'
                }
            }
        }
        mock_response.raise_for_status = mocker.Mock()
        mock_session = mocker.Mock()
        mock_session.get.return_value = mock_response
        mock_requests.Session.return_value = mock_session
        
        client = AlphaVantageClient('test_api_key')
        client.session = mock_session
        
        df = client.fetch_ohlcv('AAPL', '2023-01-01', '2023-01-02')
        
        assert len(df) == 2
        assert 'date' in df.columns
        assert df['date'].iloc[0] == '2023-01-01'
        assert df['open'].iloc[0] == 100.0
    
    def test_fetch_ohlcv_no_api_key(self):
        """Test error when API key is missing."""
        client = AlphaVantageClient(None)
        
        with pytest.raises(ValueError, match="API key is required"):
            client.fetch_ohlcv('AAPL', '2023-01-01', '2023-01-02')
    
    def test_fetch_ohlcv_api_error(self, mocker):
        """Test handling of API error response."""
        mock_requests = mocker.patch('modules.data_collection.api_clients.requests')
        mock_response = mocker.Mock()
        mock_response.json.return_value = {
            'Error Message': 'Invalid API call'
        }
        mock_response.raise_for_status = mocker.Mock()
        mock_session = mocker.Mock()
        mock_session.get.return_value = mock_response
        mock_requests.Session.return_value = mock_session
        
        client = AlphaVantageClient('test_api_key')
        client.session = mock_session
        
        # ValueError is raised but then caught and re-raised as Exception
        with pytest.raises(Exception, match="Alpha Vantage API error"):
            client.fetch_ohlcv('AAPL', '2023-01-01', '2023-01-02')
    
    def test_fetch_ohlcv_rate_limit(self, mocker):
        """Test handling of rate limit response."""
        mock_requests = mocker.patch('modules.data_collection.api_clients.requests')
        mock_response = mocker.Mock()
        mock_response.json.return_value = {
            'Note': 'Thank you for using Alpha Vantage! Our standard API call frequency is 5 calls per minute...'
        }
        mock_response.raise_for_status = mocker.Mock()
        mock_session = mocker.Mock()
        mock_session.get.return_value = mock_response
        mock_requests.Session.return_value = mock_session
        
        client = AlphaVantageClient('test_api_key')
        client.session = mock_session
        
        # ValueError is raised but then caught and re-raised as Exception
        with pytest.raises(Exception, match="Alpha Vantage rate limit"):
            client.fetch_ohlcv('AAPL', '2023-01-01', '2023-01-02')

