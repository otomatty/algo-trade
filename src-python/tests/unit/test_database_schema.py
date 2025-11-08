"""
Unit tests for database schema.
"""
import pytest
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from database.schema import create_all_tables
from database.connection import get_connection


@pytest.mark.unit
class TestDatabaseSchema:
    """Test cases for database schema."""
    
    def test_create_all_tables(self, temp_db):
        """Test that all tables are created."""
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        
        create_all_tables(conn)
        
        # Check that all expected tables exist
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name NOT LIKE 'sqlite_%'
            ORDER BY name
        """)
        tables = [row[0] for row in cursor.fetchall()]
        
        expected_tables = [
            'algorithm_proposals',
            'algorithms',
            'analysis_jobs',
            'analysis_results',
            'backtest_equity_curve',
            'backtest_jobs',
            'backtest_results',
            'backtest_trades',
            'data_sets',
            'market_news',
            'ohlcv_data',
            'proposal_generation_jobs'
        ]
        
        for table in expected_tables:
            assert table in tables, f"Table {table} not found"
        
        conn.close()
    
    def test_data_sets_table_structure(self, temp_db):
        """Test data_sets table structure."""
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        
        create_all_tables(conn)
        
        cursor.execute("PRAGMA table_info(data_sets)")
        columns = {row[1]: row[2] for row in cursor.fetchall()}
        
        assert 'id' in columns
        assert 'name' in columns
        assert 'symbol' in columns
        assert 'start_date' in columns
        assert 'end_date' in columns
        assert 'record_count' in columns
        assert 'imported_at' in columns
        assert 'source' in columns
        
        conn.close()
    
    def test_ohlcv_data_table_structure(self, temp_db):
        """Test ohlcv_data table structure."""
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        
        create_all_tables(conn)
        
        cursor.execute("PRAGMA table_info(ohlcv_data)")
        columns = {row[1]: row[2] for row in cursor.fetchall()}
        
        assert 'id' in columns
        assert 'data_set_id' in columns
        assert 'date' in columns
        assert 'open' in columns
        assert 'high' in columns
        assert 'low' in columns
        assert 'close' in columns
        assert 'volume' in columns
        
        conn.close()
    
    def test_foreign_key_constraints(self, temp_db):
        """Test foreign key constraints."""
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        
        create_all_tables(conn)
        
        # Enable foreign key constraints
        cursor.execute("PRAGMA foreign_keys = ON")
        
        # Try to insert OHLCV data without valid data_set_id
        with pytest.raises(sqlite3.IntegrityError):
            cursor.execute("""
                INSERT INTO ohlcv_data 
                (data_set_id, date, open, high, low, close, volume)
                VALUES (999, '2023-01-01', 100.0, 105.0, 99.0, 103.0, 1000000)
            """)
            conn.commit()
        
        conn.close()

