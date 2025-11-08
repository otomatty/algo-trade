"""
Unit tests for main analyzer.
"""
import pytest
import pandas as pd
import numpy as np
import sqlite3
from pathlib import Path
import sys
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from modules.data_analysis.analyzer import DataAnalyzer


@pytest.mark.unit
class TestDataAnalyzer:
    """Test cases for DataAnalyzer class."""
    
    @pytest.fixture
    def analyzer(self, temp_db):
        """Create DataAnalyzer instance."""
        conn = sqlite3.connect(temp_db)
        return DataAnalyzer(conn=conn)
    
    @pytest.fixture
    def sample_ohlcv_data(self):
        """Create sample OHLCV data."""
        dates = pd.date_range('2023-01-01', periods=30, freq='D')
        prices = 100 + np.arange(30) * 0.5
        return pd.DataFrame({
            'date': dates.strftime('%Y-%m-%d'),
            'open': prices,
            'high': prices + 1,
            'low': prices - 1,
            'close': prices + 0.3,
            'volume': np.random.randint(1000000, 2000000, 30)
        })
    
    def test_analyze_data_set_success(self, analyzer, temp_db, sample_ohlcv_data):
        """Test successful data analysis."""
        # First create a data set
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO data_sets (name, symbol, start_date, end_date, record_count, imported_at, source)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, ('Test Dataset', 'TEST', '2023-01-01', '2023-01-30', 30, datetime.now().isoformat(), 'csv'))
        
        data_set_id = cursor.lastrowid
        
        # Insert OHLCV data
        for _, row in sample_ohlcv_data.iterrows():
            cursor.execute("""
                INSERT INTO ohlcv_data (data_set_id, date, open, high, low, close, volume)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (data_set_id, row['date'], row['open'], row['high'], row['low'], row['close'], row['volume']))
        
        conn.commit()
        
        # Create job
        job_id = 'test-job-123'
        cursor.execute("""
            INSERT INTO analysis_jobs (job_id, data_set_id, status, progress, message, created_at)
            VALUES (?, ?, 'pending', 0.0, 'Test job', ?)
        """, (job_id, data_set_id, datetime.now().isoformat()))
        conn.commit()
        
        # Run analysis
        result = analyzer.analyze_data_set(job_id, data_set_id)
        
        assert result['success'] is True
        assert 'analysis_summary' in result['data']
        assert 'technical_indicators' in result['data']
        assert 'statistics' in result['data']
        
        # Check that results were saved to database
        cursor.execute("SELECT * FROM analysis_results WHERE job_id = ?", (job_id,))
        saved_result = cursor.fetchone()
        assert saved_result is not None
        
        # Check that job status was updated
        cursor.execute("SELECT status FROM analysis_jobs WHERE job_id = ?", (job_id,))
        job_status = cursor.fetchone()[0]
        assert job_status == 'completed'
    
    def test_analyze_data_set_invalid_data_set(self, analyzer, temp_db):
        """Test analysis with invalid data set ID."""
        job_id = 'test-job-456'
        result = analyzer.analyze_data_set(job_id, 99999)  # Non-existent data set
        
        assert result['success'] is False
        assert 'error' in result
    
    def test_analyze_data_set_insufficient_data(self, analyzer, temp_db):
        """Test analysis with insufficient data."""
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        
        # Create data set with only 5 data points (insufficient for RSI/MACD)
        cursor.execute("""
            INSERT INTO data_sets (name, symbol, start_date, end_date, record_count, imported_at, source)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, ('Small Dataset', 'SMALL', '2023-01-01', '2023-01-05', 5, datetime.now().isoformat(), 'csv'))
        
        data_set_id = cursor.lastrowid
        
        # Insert minimal OHLCV data
        for i in range(5):
            cursor.execute("""
                INSERT INTO ohlcv_data (data_set_id, date, open, high, low, close, volume)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (data_set_id, f'2023-01-{i+1:02d}', 100.0, 105.0, 99.0, 103.0, 1000000))
        
        conn.commit()
        
        job_id = 'test-job-789'
        cursor.execute("""
            INSERT INTO analysis_jobs (job_id, data_set_id, status, progress, message, created_at)
            VALUES (?, ?, 'pending', 0.0, 'Test job', ?)
        """, (job_id, data_set_id, datetime.now().isoformat()))
        conn.commit()
        
        # Run analysis - should handle gracefully
        result = analyzer.analyze_data_set(job_id, data_set_id)
        
        # Should either succeed with partial results or fail gracefully
        assert result is not None

