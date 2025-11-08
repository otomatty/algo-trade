"""
Integration tests for data collection flow.
"""
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from modules.data_collection.csv_importer import CSVImporter
from database.connection import get_connection
import sqlite3


@pytest.mark.integration
class TestDataCollectionFlow:
    """Integration tests for data collection flow."""
    
    def test_csv_import_to_database(self, sample_csv_file, temp_db):
        """Test complete CSV import flow."""
        import sqlite3
        conn = sqlite3.connect(temp_db)
        importer = CSVImporter(conn=conn)
        result = importer.import_csv(sample_csv_file, "Integration Test Dataset")
        
        assert result['success'] is True
        data_set_id = result['data']['data_set_id']
        
        # Verify data in database
        conn = sqlite3.connect(temp_db)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Check data_set
        cursor.execute("SELECT * FROM data_sets WHERE id = ?", (data_set_id,))
        data_set = cursor.fetchone()
        assert data_set is not None
        assert data_set['name'] == "Integration Test Dataset"
        assert data_set['record_count'] == 5
        
        # Check OHLCV data
        cursor.execute("SELECT COUNT(*) FROM ohlcv_data WHERE data_set_id = ?", (data_set_id,))
        count = cursor.fetchone()[0]
        assert count == 5
        
        # Verify data integrity
        cursor.execute("""
            SELECT date, open, high, low, close, volume 
            FROM ohlcv_data 
            WHERE data_set_id = ? 
            ORDER BY date
        """, (data_set_id,))
        rows = cursor.fetchall()
        
        assert len(rows) == 5
        assert rows[0]['date'] == '2023-01-01'
        assert rows[0]['open'] == 100.0
        assert rows[0]['close'] == 103.0
        
        conn.close()
    
    def test_duplicate_date_handling(self, sample_csv_file, temp_db):
        """Test handling of duplicate dates in CSV."""
        # Add duplicate date to CSV
        duplicate_csv = """date,open,high,low,close,volume
2023-01-01,100.0,105.0,99.0,103.0,1000000
2023-01-01,102.0,107.0,101.0,105.0,1100000
2023-01-02,103.0,108.0,102.0,106.0,1200000"""
        
        import tempfile
        import sqlite3
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write(duplicate_csv)
            csv_path = f.name
        
        try:
            conn = sqlite3.connect(temp_db)
            importer = CSVImporter(conn=conn)
            result = importer.import_csv(csv_path, "Duplicate Test")
            
            assert result['success'] is True
            data_set_id = result['data']['data_set_id']
            
            # Verify only one record per date (last one kept)
            conn = sqlite3.connect(temp_db)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM ohlcv_data WHERE data_set_id = ?", (data_set_id,))
            count = cursor.fetchone()[0]
            assert count == 2  # Should have 2 unique dates
            
            # Verify last duplicate is kept
            cursor.execute("""
                SELECT close FROM ohlcv_data 
                WHERE data_set_id = ? AND date = '2023-01-01'
            """, (data_set_id,))
            close_price = cursor.fetchone()['close']
            assert close_price == 105.0  # Last duplicate value
            
            conn.close()
        finally:
            import os
            os.unlink(csv_path)

