"""
Unit tests for database operations (get_data_list, delete_data_set).
"""
import pytest
import sqlite3
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from database.connection import get_connection
from database.schema import create_all_tables


@pytest.mark.unit
class TestDatabaseOperations:
    """Test cases for database operations."""
    
    def test_get_data_list_empty(self, temp_db):
        """Test getting empty data list."""
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, name, symbol, start_date, end_date, record_count, imported_at, source, created_at
            FROM data_sets
            ORDER BY created_at DESC
        """)
        
        rows = cursor.fetchall()
        assert len(rows) == 0
        
        conn.close()
    
    def test_get_data_list_with_data(self, temp_db):
        """Test getting data list with data."""
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        
        # Insert test data
        cursor.execute("""
            INSERT INTO data_sets (name, symbol, start_date, end_date, record_count, imported_at, source, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            'Test Dataset',
            'AAPL',
            '2023-01-01',
            '2023-12-31',
            252,
            datetime.now().isoformat(),
            'csv',
            datetime.now().isoformat()
        ))
        data_set_id = cursor.lastrowid
        
        # Insert OHLCV data
        cursor.execute("""
            INSERT INTO ohlcv_data (data_set_id, date, open, high, low, close, volume)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (data_set_id, '2023-01-01', 100.0, 105.0, 99.0, 103.0, 1000000))
        
        conn.commit()
        
        # Query data list with row_factory for dict-like access
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, name, symbol, start_date, end_date, record_count, imported_at, source, created_at
            FROM data_sets
            ORDER BY created_at DESC
        """)
        
        rows = cursor.fetchall()
        assert len(rows) == 1
        assert rows[0]['name'] == 'Test Dataset'
        assert rows[0]['symbol'] == 'AAPL'
        assert rows[0]['record_count'] == 252
        
        conn.close()
    
    def test_delete_data_set_success(self, temp_db):
        """Test successful data set deletion."""
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        
        # Insert test data
        cursor.execute("""
            INSERT INTO data_sets (name, symbol, start_date, end_date, record_count, imported_at, source, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            'Test Dataset',
            'AAPL',
            '2023-01-01',
            '2023-12-31',
            252,
            datetime.now().isoformat(),
            'csv',
            datetime.now().isoformat()
        ))
        data_set_id = cursor.lastrowid
        
        # Insert OHLCV data
        cursor.execute("""
            INSERT INTO ohlcv_data (data_set_id, date, open, high, low, close, volume)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (data_set_id, '2023-01-01', 100.0, 105.0, 99.0, 103.0, 1000000))
        
        conn.commit()
        
        # Delete OHLCV data first
        cursor.execute("DELETE FROM ohlcv_data WHERE data_set_id = ?", (data_set_id,))
        
        # Delete data set
        cursor.execute("DELETE FROM data_sets WHERE id = ?", (data_set_id,))
        conn.commit()
        
        # Verify deletion
        cursor.execute("SELECT COUNT(*) FROM data_sets WHERE id = ?", (data_set_id,))
        count = cursor.fetchone()[0]
        assert count == 0
        
        cursor.execute("SELECT COUNT(*) FROM ohlcv_data WHERE data_set_id = ?", (data_set_id,))
        count = cursor.fetchone()[0]
        assert count == 0
        
        conn.close()
    
    def test_delete_data_set_cascade(self, temp_db):
        """Test that OHLCV data is deleted when data set is deleted (CASCADE)."""
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        
        # Enable foreign key constraints
        cursor.execute("PRAGMA foreign_keys = ON")
        
        # Insert test data
        cursor.execute("""
            INSERT INTO data_sets (name, symbol, start_date, end_date, record_count, imported_at, source, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            'Test Dataset',
            'AAPL',
            '2023-01-01',
            '2023-12-31',
            252,
            datetime.now().isoformat(),
            'csv',
            datetime.now().isoformat()
        ))
        data_set_id = cursor.lastrowid
        
        # Insert OHLCV data
        cursor.execute("""
            INSERT INTO ohlcv_data (data_set_id, date, open, high, low, close, volume)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (data_set_id, '2023-01-01', 100.0, 105.0, 99.0, 103.0, 1000000))
        
        conn.commit()
        
        # Delete data set (should cascade to OHLCV data)
        cursor.execute("DELETE FROM data_sets WHERE id = ?", (data_set_id,))
        conn.commit()
        
        # Verify OHLCV data is also deleted
        cursor.execute("SELECT COUNT(*) FROM ohlcv_data WHERE data_set_id = ?", (data_set_id,))
        count = cursor.fetchone()[0]
        assert count == 0
        
        conn.close()
    
    def test_delete_data_set_not_found(self, temp_db):
        """Test deletion of non-existent data set."""
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        
        # Try to delete non-existent data set
        cursor.execute("DELETE FROM data_sets WHERE id = ?", (999,))
        conn.commit()
        
        # Should not raise error, but rowcount should be 0
        assert cursor.rowcount == 0
        
        conn.close()

