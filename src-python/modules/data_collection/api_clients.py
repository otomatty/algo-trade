"""
API clients for external data sources.
"""
import pandas as pd
import requests
from requests.exceptions import RequestException
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import time
import json

from utils.json_io import json_response


class DataSourceClient:
    """Base class for data source clients."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.session = requests.Session()
        self.last_request_time = 0
        self.min_request_interval = 1.0  # Minimum seconds between requests
    
    def fetch_ohlcv(self, symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
        """
        Fetch OHLCV data.
        
        Args:
            symbol: Stock symbol
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            
        Returns:
            DataFrame with OHLCV data
        """
        raise NotImplementedError
    
    def _check_rate_limit(self) -> None:
        """Check and enforce rate limiting."""
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        if time_since_last_request < self.min_request_interval:
            time.sleep(self.min_request_interval - time_since_last_request)
        self.last_request_time = time.time()


class YahooFinanceClient(DataSourceClient):
    """Yahoo Finance API client using yfinance library."""
    
    def __init__(self):
        super().__init__()
        try:
            import yfinance as yf
            self.yf = yf
        except ImportError:
            raise ImportError("yfinance is required. Install with: pip install yfinance")
    
    def fetch_ohlcv(self, symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
        """Fetch OHLCV data from Yahoo Finance."""
        self._check_rate_limit()
        
        try:
            ticker = self.yf.Ticker(symbol)
            df = ticker.history(start=start_date, end=end_date)
            
            if df.empty:
                raise ValueError(f"No data found for symbol {symbol} in date range {start_date} to {end_date}")
            
            # Rename columns to match our schema
            df = df.reset_index()
            df['date'] = df['Date'].dt.strftime('%Y-%m-%d')
            df = df.rename(columns={
                'Open': 'open',
                'High': 'high',
                'Low': 'low',
                'Close': 'close',
                'Volume': 'volume'
            })
            
            # Select and reorder columns
            df = df[['date', 'open', 'high', 'low', 'close', 'volume']]
            
            return df
        except Exception as e:
            raise Exception(f"Failed to fetch data from Yahoo Finance: {str(e)}")


class AlphaVantageClient(DataSourceClient):
    """Alpha Vantage API client."""
    
    BASE_URL = "https://www.alphavantage.co/query"
    MIN_REQUEST_INTERVAL = 12.0  # 5 calls per minute = 12 seconds between calls
    
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.min_request_interval = self.MIN_REQUEST_INTERVAL
    
    def fetch_ohlcv(self, symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
        """Fetch OHLCV data from Alpha Vantage."""
        self._check_rate_limit()
        
        if not self.api_key:
            raise ValueError("API key is required for Alpha Vantage")
        
        try:
            params = {
                'function': 'TIME_SERIES_DAILY',
                'symbol': symbol,
                'apikey': self.api_key,
                'outputsize': 'full',
                'datatype': 'json'
            }
            
            response = self.session.get(self.BASE_URL, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            # Check for API errors
            if 'Error Message' in data:
                raise ValueError(f"Alpha Vantage API error: {data['Error Message']}")
            if 'Note' in data:
                raise ValueError(f"Alpha Vantage rate limit: {data['Note']}")
            
            # Parse time series data
            time_series_key = 'Time Series (Daily)'
            if time_series_key not in data:
                raise ValueError(f"Unexpected response format from Alpha Vantage")
            
            time_series = data[time_series_key]
            
            # Convert to DataFrame
            records = []
            for date_str, values in time_series.items():
                date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                if start_date <= date_str <= end_date:
                    records.append({
                        'date': date_str,
                        'open': float(values['1. open']),
                        'high': float(values['2. high']),
                        'low': float(values['3. low']),
                        'close': float(values['4. close']),
                        'volume': int(values['5. volume'])
                    })
            
            if not records:
                raise ValueError(f"No data found for symbol {symbol} in date range {start_date} to {end_date}")
            
            df = pd.DataFrame(records)
            df = df.sort_values('date').reset_index(drop=True)
            
            return df
        except RequestException as e:
            raise Exception(f"Network error while fetching from Alpha Vantage: {str(e)}")
        except Exception as e:
            raise Exception(f"Failed to fetch data from Alpha Vantage: {str(e)}")
