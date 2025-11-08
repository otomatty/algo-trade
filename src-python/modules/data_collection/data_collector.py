"""
Data collector that uses API clients to fetch and save data.
"""
import json
from typing import Dict, Any, Optional
from datetime import datetime

from .api_clients import YahooFinanceClient, AlphaVantageClient
from database.connection import get_connection
from utils.json_io import json_response
import sqlite3
from typing import Optional


class DataCollector:
    """Collects data from external APIs and saves to database."""
    
    def __init__(self, conn: Optional[sqlite3.Connection] = None):
        """
        Initialize data collector.
        
        Args:
            conn: Optional database connection. If None, uses get_connection().
        """
        self.conn = conn if conn is not None else get_connection()
    
    def collect_from_api(
        self,
        source: str,
        symbol: str,
        start_date: str,
        end_date: str,
        name: Optional[str] = None,
        api_key: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Collect data from external API and save to database.
        
        Args:
            source: 'yahoo' or 'alphavantage'
            symbol: Stock symbol
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            name: Optional name for the dataset
            api_key: API key (required for Alpha Vantage)
            
        Returns:
            Dict with success status and data_set_id or error message
        """
        try:
            # Get appropriate client
            if source == 'yahoo':
                client = YahooFinanceClient()
            elif source == 'alphavantage':
                if not api_key:
                    return json_response(
                        success=False,
                        error="API key is required for Alpha Vantage"
                    )
                client = AlphaVantageClient(api_key)
            else:
                return json_response(
                    success=False,
                    error=f"Unknown data source: {source}"
                )
            
            # Fetch data
            df = client.fetch_ohlcv(symbol, start_date, end_date)
            
            # Generate dataset name if not provided
            if not name:
                name = f"{symbol}_{start_date}_{end_date}"
            
            # Save to database
            data_set_id = self._save_to_database(df, name, symbol, source)
            
            return json_response(
                success=True,
                data={
                    "data_set_id": data_set_id,
                    "name": name,
                    "record_count": len(df),
                    "symbol": symbol,
                    "start_date": start_date,
                    "end_date": end_date
                }
            )
        except Exception as e:
            return json_response(
                success=False,
                error=str(e)
            )
    
    def _save_to_database(
        self,
        df,
        name: str,
        symbol: str,
        source: str
    ) -> int:
        """Save data to database."""
        cursor = self.conn.cursor()
        
        try:
            # Insert dataset
            start_date = df['date'].min()
            end_date = df['date'].max()
            record_count = len(df)
            imported_at = datetime.now().isoformat()
            
            cursor.execute("""
                INSERT INTO data_sets (name, symbol, start_date, end_date, record_count, imported_at, source)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (name, symbol, start_date, end_date, record_count, imported_at, source))
            
            data_set_id = cursor.lastrowid
            
            # Insert OHLCV data
            for _, row in df.iterrows():
                cursor.execute("""
                    INSERT INTO ohlcv_data 
                    (data_set_id, date, open, high, low, close, volume)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    data_set_id,
                    row['date'],
                    float(row['open']),
                    float(row['high']),
                    float(row['low']),
                    float(row['close']),
                    int(row['volume'])
                ))
            
            self.conn.commit()
            return data_set_id
        except Exception as e:
            self.conn.rollback()
            raise Exception(f"Failed to save to database: {str(e)}")

