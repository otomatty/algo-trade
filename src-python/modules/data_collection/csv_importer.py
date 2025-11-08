"""
CSV importer for OHLCV data.
"""
import pandas as pd
import json
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

from database.connection import get_connection
from utils.json_io import json_response
import sqlite3
from typing import Optional


class CSVImporter:
    """CSV importer for OHLCV data."""
    
    REQUIRED_COLUMNS = ['date', 'open', 'high', 'low', 'close', 'volume']
    DATE_FORMATS = ['%Y-%m-%d', '%Y/%m/%d', '%Y-%m-%d %H:%M:%S']
    
    def __init__(self, conn: Optional[sqlite3.Connection] = None):
        """
        Initialize CSV importer.
        
        Args:
            conn: Optional database connection. If None, uses get_connection().
        """
        self.conn = conn if conn is not None else get_connection()
    
    def import_csv(self, file_path: str, name: Optional[str] = None) -> Dict[str, Any]:
        """
        Import OHLCV data from CSV file.
        
        Args:
            file_path: Path to CSV file
            name: Optional name for the dataset
            
        Returns:
            Dict with success status and data_set_id or error message
        """
        try:
            # Read CSV
            df = pd.read_csv(file_path, encoding='utf-8')
            
            # Validate columns
            self._validate_columns(df)
            
            # Validate and normalize data
            df = self._normalize_data(df)
            
            # Generate dataset name if not provided
            if not name:
                name = f"Dataset_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Save to database
            data_set_id = self._save_to_database(df, name, file_path)
            
            return json_response(
                success=True,
                data={
                    "data_set_id": data_set_id,
                    "name": name,
                    "record_count": len(df)
                }
            )
        except Exception as e:
            return json_response(
                success=False,
                error=str(e)
            )
    
    def _validate_columns(self, df: pd.DataFrame) -> None:
        """Validate that required columns exist."""
        missing_columns = set(self.REQUIRED_COLUMNS) - set(df.columns.str.lower())
        if missing_columns:
            raise ValueError(
                f"Missing required columns: {', '.join(missing_columns)}. "
                f"Found columns: {', '.join(df.columns)}"
            )
    
    def _normalize_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Normalize data types and formats."""
        # Normalize column names to lowercase
        df.columns = df.columns.str.lower()
        
        # Parse date column
        df['date'] = pd.to_datetime(df['date'], format='mixed', errors='coerce')
        if df['date'].isna().any():
            raise ValueError("Invalid date format. Supported formats: YYYY-MM-DD, YYYY/MM/DD")
        
        # Convert to string format for storage
        df['date'] = df['date'].dt.strftime('%Y-%m-%d')
        
        # Validate numeric columns
        numeric_columns = ['open', 'high', 'low', 'close', 'volume']
        for col in numeric_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            if df[col].isna().any():
                raise ValueError(f"Invalid numeric values in column: {col}")
        
        # Validate OHLC relationships
        invalid_rows = (
            (df['high'] < df['low']) |
            (df['high'] < df['open']) |
            (df['high'] < df['close']) |
            (df['low'] > df['open']) |
            (df['low'] > df['close'])
        )
        if invalid_rows.any():
            raise ValueError(f"Invalid OHLC relationships found in {invalid_rows.sum()} rows")
        
        # Sort by date
        df = df.sort_values('date').reset_index(drop=True)
        
        # Remove duplicates
        df = df.drop_duplicates(subset=['date'], keep='last')
        
        return df
    
    def _save_to_database(self, df: pd.DataFrame, name: str, source_path: str) -> int:
        """Save data to database."""
        cursor = self.conn.cursor()
        
        try:
            # Insert dataset
            start_date = df['date'].min()
            end_date = df['date'].max()
            record_count = len(df)
            imported_at = datetime.now().isoformat()
            
            cursor.execute("""
                INSERT INTO data_sets (name, start_date, end_date, record_count, imported_at, source)
                VALUES (?, ?, ?, ?, ?, 'csv')
            """, (name, start_date, end_date, record_count, imported_at))
            
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

