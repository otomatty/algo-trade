"""
Unit tests for CSV importer.
"""
import pytest
import pandas as pd
import sqlite3
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from modules.data_collection.csv_importer import CSVImporter


@pytest.mark.unit
class TestCSVImporter:
    """Test cases for CSVImporter class."""
    
    def test_validate_columns_valid(self, sample_csv_data, tmp_path):
        """Test column validation with valid CSV."""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text(sample_csv_data)
        
        importer = CSVImporter()
        df = pd.read_csv(csv_file)
        
        # Should not raise
        importer._validate_columns(df)
    
    def test_validate_columns_missing(self, tmp_path):
        """Test column validation with missing columns."""
        invalid_csv = """date,open,high,low,close
2023-01-01,100.0,105.0,99.0,103.0"""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text(invalid_csv)
        
        importer = CSVImporter()
        df = pd.read_csv(csv_file)
        
        with pytest.raises(ValueError, match="Missing required columns"):
            importer._validate_columns(df)
    
    def test_normalize_data_valid(self, sample_csv_data, tmp_path):
        """Test data normalization with valid data."""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text(sample_csv_data)
        
        importer = CSVImporter()
        df = pd.read_csv(csv_file)
        df.columns = df.columns.str.lower()
        
        normalized = importer._normalize_data(df)
        
        assert len(normalized) == 5
        assert 'date' in normalized.columns
        assert normalized['date'].dtype == 'object'  # String after normalization
        assert all(col in normalized.columns for col in ['open', 'high', 'low', 'close', 'volume'])
    
    def test_normalize_data_invalid_ohlc(self, tmp_path):
        """Test data normalization with invalid OHLC relationships."""
        invalid_csv = """date,open,high,low,close,volume
2023-01-01,100.0,95.0,99.0,103.0,1000000"""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text(invalid_csv)
        
        importer = CSVImporter()
        df = pd.read_csv(csv_file)
        df.columns = df.columns.str.lower()
        
        with pytest.raises(ValueError, match="Invalid OHLC relationships"):
            importer._normalize_data(df)
    
    def test_normalize_data_invalid_date(self, tmp_path):
        """Test data normalization with invalid date format."""
        invalid_csv = """date,open,high,low,close,volume
invalid-date,100.0,105.0,99.0,103.0,1000000"""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text(invalid_csv)
        
        importer = CSVImporter()
        df = pd.read_csv(csv_file)
        df.columns = df.columns.str.lower()
        
        with pytest.raises(ValueError, match="Invalid date format"):
            importer._normalize_data(df)
    
    def test_import_csv_success(self, sample_csv_file, temp_db):
        """Test successful CSV import."""
        import sqlite3
        conn = sqlite3.connect(temp_db)
        importer = CSVImporter(conn=conn)
        result = importer.import_csv(sample_csv_file, "Test Dataset")
        
        assert result['success'] is True
        assert 'data_set_id' in result['data']
        assert result['data']['record_count'] == 5
        assert result['data']['name'] == "Test Dataset"
    
    def test_import_csv_auto_name(self, sample_csv_file, temp_db):
        """Test CSV import with auto-generated name."""
        import sqlite3
        conn = sqlite3.connect(temp_db)
        importer = CSVImporter(conn=conn)
        result = importer.import_csv(sample_csv_file)
        
        assert result['success'] is True
        assert 'data_set_id' in result['data']
        assert 'name' in result['data']
        assert result['data']['name'].startswith("Dataset_")
    
    def test_import_csv_invalid_file(self, temp_db):
        """Test CSV import with non-existent file."""
        import sqlite3
        conn = sqlite3.connect(temp_db)
        importer = CSVImporter(conn=conn)
        result = importer.import_csv("/nonexistent/file.csv")
        
        assert result['success'] is False
        assert 'error' in result

