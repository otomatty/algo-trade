"""
Pytest configuration and fixtures.
"""
import pytest
import tempfile
import os
import sqlite3
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from database.connection import get_connection
from database.schema import create_all_tables


@pytest.fixture
def temp_db():
    """Create a temporary database for testing."""
    # Create temporary database file
    fd, db_path = tempfile.mkstemp(suffix='.db')
    os.close(fd)
    
    # Override database path
    original_get_db_path = None
    try:
        from database import connection
        
        # Store original function
        original_get_db_path = connection.get_db_path
        
        # Override to use temp database
        def get_test_db_path():
            return db_path
        
        connection.get_db_path = get_test_db_path
        
        # Initialize database
        conn = sqlite3.connect(db_path)
        create_all_tables(conn)
        conn.close()
        
        yield db_path
    finally:
        # Restore original function
        if original_get_db_path:
            connection.get_db_path = original_get_db_path
        
        # Clean up
        if os.path.exists(db_path):
            os.unlink(db_path)


@pytest.fixture
def sample_csv_data():
    """Sample CSV data for testing."""
    return """date,open,high,low,close,volume
2023-01-01,100.0,105.0,99.0,103.0,1000000
2023-01-02,103.0,108.0,102.0,106.0,1200000
2023-01-03,106.0,110.0,105.0,108.0,1100000
2023-01-04,108.0,112.0,107.0,110.0,1300000
2023-01-05,110.0,115.0,109.0,113.0,1400000"""


@pytest.fixture
def sample_csv_file(sample_csv_data, tmp_path):
    """Create a temporary CSV file for testing."""
    csv_file = tmp_path / "test_data.csv"
    csv_file.write_text(sample_csv_data)
    return str(csv_file)

