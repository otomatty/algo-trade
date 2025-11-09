"""
Data updater for updating existing datasets with new data.

Related Documentation:
  └─ Plan: docs/03_plans/data-collection/README.md

DEPENDENCY MAP:

Parents (Files that import this file):
  └─ src-python/scripts/update_data_set.py

Dependencies (External files that this file imports):
  ├─ sqlite3 (standard library)
  ├─ pandas (external)
  ├─ datetime (standard library)
  ├─ typing (standard library)
  ├─ logging (standard library)
  ├─ src-python/database.connection
  ├─ src-python/modules/data_collection.data_collector
  └─ src-python/modules/data_collection.api_clients
"""
import sqlite3
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, Tuple
import pandas as pd

from database.connection import get_connection
from modules.data_collection.data_collector import DataCollector
from modules.data_collection.api_clients import YahooFinanceClient, AlphaVantageClient

logger = logging.getLogger(__name__)


class DataUpdater:
    """Updates existing datasets with new data."""
    
    def __init__(self, conn: Optional[sqlite3.Connection] = None):
        """
        Initialize data updater.
        
        Args:
            conn: Database connection (optional, will create new if not provided)
        """
        self.conn = conn if conn is not None else get_connection()
        self.data_collector = DataCollector(self.conn)
    
    def check_for_updates(self, data_set_id: int) -> Dict[str, Any]:
        """
        Check if a dataset needs updates.
        
        Args:
            data_set_id: Dataset ID
            
        Returns:
            Dict with update information:
            - needs_update: bool
            - latest_date: str (latest date in dataset)
            - current_date: str (current date)
            - days_behind: int (number of days behind)
        """
        cursor = self.conn.cursor()
        
        # Get dataset info
        cursor.execute("""
            SELECT symbol, source, end_date
            FROM data_sets
            WHERE id = ?
        """, (data_set_id,))
        
        row = cursor.fetchone()
        if not row:
            raise ValueError(f"Dataset {data_set_id} not found")
        
        symbol, source, end_date = row
        
        if not symbol or not source:
            return {
                'needs_update': False,
                'reason': 'Dataset does not have symbol or source information'
            }
        
        # Get latest date from OHLCV data
        cursor.execute("""
            SELECT MAX(date) FROM ohlcv_data
            WHERE data_set_id = ?
        """, (data_set_id,))
        
        latest_date_row = cursor.fetchone()
        latest_date = latest_date_row[0] if latest_date_row and latest_date_row[0] else end_date
        
        if not latest_date:
            return {
                'needs_update': False,
                'reason': 'No date information available'
            }
        
        # Calculate days behind
        latest_dt = datetime.strptime(latest_date, '%Y-%m-%d')
        current_dt = datetime.now()
        days_behind = (current_dt - latest_dt).days
        
        # Consider update needed if more than 1 day behind (to account for weekends/holidays)
        needs_update = days_behind > 1
        
        return {
            'needs_update': needs_update,
            'latest_date': latest_date,
            'current_date': current_dt.strftime('%Y-%m-%d'),
            'days_behind': days_behind,
            'symbol': symbol,
            'source': source
        }
    
    def update_dataset(
        self,
        data_set_id: int,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Update a dataset with new data.
        
        Args:
            data_set_id: Dataset ID
            start_date: Start date for update (optional, defaults to day after latest date)
            end_date: End date for update (optional, defaults to today)
            
        Returns:
            Dict with update results:
            - success: bool
            - added_count: int
            - updated_count: int
            - error: str (if failed)
        """
        try:
            # Check current state
            update_info = self.check_for_updates(data_set_id)
            
            if not update_info.get('needs_update'):
                return {
                    'success': True,
                    'added_count': 0,
                    'updated_count': 0,
                    'message': 'Dataset is up to date'
                }
            
            symbol = update_info['symbol']
            source = update_info['source']
            latest_date = update_info['latest_date']
            
            # Calculate date range
            if not start_date:
                # Start from day after latest date
                latest_dt = datetime.strptime(latest_date, '%Y-%m-%d')
                start_date = (latest_dt + timedelta(days=1)).strftime('%Y-%m-%d')
            
            if not end_date:
                end_date = datetime.now().strftime('%Y-%m-%d')
            
            # Get API key if needed
            api_key = None
            if source == 'alphavantage':
                import os
                api_key = os.getenv('ALPHAVANTAGE_API_KEY')
            
            # Fetch new data
            if source == 'yahoo':
                client = YahooFinanceClient()
            elif source == 'alphavantage':
                if not api_key:
                    raise ValueError("API key required for Alpha Vantage")
                client = AlphaVantageClient(api_key)
            else:
                raise ValueError(f"Unknown source: {source}")
            
            df = client.fetch_ohlcv(symbol, start_date, end_date)
            
            if df.empty:
                return {
                    'success': True,
                    'added_count': 0,
                    'updated_count': 0,
                    'message': 'No new data available'
                }
            
            # Apply updates
            added_count, updated_count = self._apply_updates(data_set_id, df)
            
            # Update dataset metadata
            cursor = self.conn.cursor()
            cursor.execute("""
                UPDATE data_sets
                SET end_date = ?,
                    record_count = (SELECT COUNT(*) FROM ohlcv_data WHERE data_set_id = ?),
                    updated_at = ?
                WHERE id = ?
            """, (end_date, data_set_id, datetime.now().isoformat(), data_set_id))
            
            self.conn.commit()
            
            return {
                'success': True,
                'added_count': added_count,
                'updated_count': updated_count,
                'message': f'Updated dataset: {added_count} added, {updated_count} updated'
            }
            
        except Exception as e:
            logger.exception(f"Error updating dataset {data_set_id}")
            return {
                'success': False,
                'added_count': 0,
                'updated_count': 0,
                'error': str(e)
            }
    
    def _apply_updates(self, data_set_id: int, df: pd.DataFrame) -> Tuple[int, int]:
        """
        Apply updates to database.
        
        Args:
            data_set_id: Dataset ID
            df: DataFrame with new data
            
        Returns:
            Tuple of (added_count, updated_count)
        """
        cursor = self.conn.cursor()
        added_count = 0
        updated_count = 0
        
        for _, row in df.iterrows():
            date_str = row['date']
            
            # Check if record exists
            cursor.execute("""
                SELECT id FROM ohlcv_data
                WHERE data_set_id = ? AND date = ?
            """, (data_set_id, date_str))
            
            existing = cursor.fetchone()
            
            if existing:
                # Update existing record
                cursor.execute("""
                    UPDATE ohlcv_data
                    SET open = ?, high = ?, low = ?, close = ?, volume = ?
                    WHERE id = ?
                """, (
                    float(row['open']),
                    float(row['high']),
                    float(row['low']),
                    float(row['close']),
                    int(row['volume']),
                    existing[0]
                ))
                updated_count += 1
            else:
                # Insert new record
                cursor.execute("""
                    INSERT INTO ohlcv_data
                    (data_set_id, date, open, high, low, close, volume)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    data_set_id,
                    date_str,
                    float(row['open']),
                    float(row['high']),
                    float(row['low']),
                    float(row['close']),
                    int(row['volume'])
                ))
                added_count += 1
        
        self.conn.commit()
        return added_count, updated_count

