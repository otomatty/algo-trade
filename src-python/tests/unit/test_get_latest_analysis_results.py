"""
Unit tests for get_latest_analysis_results script.
"""
import pytest
import json
import sqlite3
from pathlib import Path
import sys
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from scripts.get_latest_analysis_results import main
from utils.json_io import read_json_input, write_json_output
from io import StringIO


@pytest.mark.unit
class TestGetLatestAnalysisResults:
    """Test cases for get_latest_analysis_results script."""
    
    def test_get_latest_analysis_results_success(self, temp_db, monkeypatch):
        """Test successful retrieval of latest analysis results."""
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        
        # Create data set
        cursor.execute("""
            INSERT INTO data_sets (name, symbol, start_date, end_date, record_count, imported_at, source)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, ('Test Dataset', 'TEST', '2023-01-01', '2023-01-30', 30, datetime.now().isoformat(), 'csv'))
        data_set_id = cursor.lastrowid
        
        # Create first analysis job and result
        job_id_1 = 'test-job-1'
        cursor.execute("""
            INSERT INTO analysis_jobs (job_id, data_set_id, status, progress, message, created_at, completed_at)
            VALUES (?, ?, 'completed', 1.0, 'Completed', ?, ?)
        """, (job_id_1, data_set_id, datetime.now().isoformat(), datetime.now().isoformat()))
        
        result_1 = {
            'trend_direction': 'upward',
            'volatility_level': 'medium',
            'dominant_patterns': ['uptrend']
        }
        indicators_1 = {'RSI': 60.0, 'MACD': 0.5}
        statistics_1 = {'price_range': {'min': 100, 'max': 150, 'current': 140}}
        
        cursor.execute("""
            INSERT INTO analysis_results (job_id, data_set_id, analysis_summary, technical_indicators, statistics, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (job_id_1, data_set_id, json.dumps(result_1), json.dumps(indicators_1), json.dumps(statistics_1), datetime.now().isoformat()))
        
        # Create second analysis job and result (newer)
        job_id_2 = 'test-job-2'
        cursor.execute("""
            INSERT INTO analysis_jobs (job_id, data_set_id, status, progress, message, created_at, completed_at)
            VALUES (?, ?, 'completed', 1.0, 'Completed', ?, ?)
        """, (job_id_2, data_set_id, datetime.now().isoformat(), datetime.now().isoformat()))
        
        result_2 = {
            'trend_direction': 'downward',
            'volatility_level': 'high',
            'dominant_patterns': ['downtrend']
        }
        indicators_2 = {'RSI': 40.0, 'MACD': -0.3}
        statistics_2 = {'price_range': {'min': 100, 'max': 150, 'current': 120}}
        
        cursor.execute("""
            INSERT INTO analysis_results (job_id, data_set_id, analysis_summary, technical_indicators, statistics, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (job_id_2, data_set_id, json.dumps(result_2), json.dumps(indicators_2), json.dumps(statistics_2), datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
        
        # Mock stdin/stdout
        input_data = {'data_set_id': data_set_id}
        input_json = json.dumps(input_data)
        
        stdin_mock = StringIO(input_json)
        stdout_mock = StringIO()
        
        # Mock sys.stdin and sys.stdout
        monkeypatch.setattr('sys.stdin', stdin_mock)
        monkeypatch.setattr('sys.stdout', stdout_mock)
        
        # Mock get_connection to return temp_db
        def mock_get_connection():
            return sqlite3.connect(temp_db)
        
        monkeypatch.setattr('scripts.get_latest_analysis_results.get_connection', mock_get_connection)
        
        # Run script
        main()
        
        # Check output
        stdout_mock.seek(0)
        output = json.loads(stdout_mock.read())
        
        assert output['success'] is True
        assert 'data' in output
        assert output['data']['job_id'] == job_id_2  # Should return latest (job_id_2)
        assert output['data']['data_set_id'] == data_set_id
        assert output['data']['analysis_summary']['trend_direction'] == 'downward'
        assert output['data']['technical_indicators']['RSI'] == 40.0
    
    def test_get_latest_analysis_results_no_results(self, temp_db, monkeypatch):
        """Test when no analysis results exist for data set."""
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        
        # Create data set
        cursor.execute("""
            INSERT INTO data_sets (name, symbol, start_date, end_date, record_count, imported_at, source)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, ('Test Dataset', 'TEST', '2023-01-01', '2023-01-30', 30, datetime.now().isoformat(), 'csv'))
        data_set_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        # Mock stdin/stdout
        input_data = {'data_set_id': data_set_id}
        input_json = json.dumps(input_data)
        
        stdin_mock = StringIO(input_json)
        stdout_mock = StringIO()
        
        monkeypatch.setattr('sys.stdin', stdin_mock)
        monkeypatch.setattr('sys.stdout', stdout_mock)
        
        def mock_get_connection():
            return sqlite3.connect(temp_db)
        
        monkeypatch.setattr('scripts.get_latest_analysis_results.get_connection', mock_get_connection)
        
        # Run script
        main()
        
        # Check output
        stdout_mock.seek(0)
        output = json.loads(stdout_mock.read())
        
        assert output['success'] is False
        assert 'error' in output
        assert 'not found' in output['error'].lower()
    
    def test_get_latest_analysis_results_missing_data_set_id(self, monkeypatch):
        """Test when data_set_id is missing."""
        input_data = {}
        input_json = json.dumps(input_data)
        
        stdin_mock = StringIO(input_json)
        stdout_mock = StringIO()
        
        monkeypatch.setattr('sys.stdin', stdin_mock)
        monkeypatch.setattr('sys.stdout', stdout_mock)
        
        # Run script
        main()
        
        # Check output
        stdout_mock.seek(0)
        output = json.loads(stdout_mock.read())
        
        assert output['success'] is False
        assert 'error' in output
        assert 'data_set_id' in output['error'].lower()
    
    def test_get_latest_analysis_results_invalid_data_set_id(self, temp_db, monkeypatch):
        """Test when data_set_id does not exist."""
        # Mock stdin/stdout
        input_data = {'data_set_id': 99999}
        input_json = json.dumps(input_data)
        
        stdin_mock = StringIO(input_json)
        stdout_mock = StringIO()
        
        monkeypatch.setattr('sys.stdin', stdin_mock)
        monkeypatch.setattr('sys.stdout', stdout_mock)
        
        def mock_get_connection():
            return sqlite3.connect(temp_db)
        
        monkeypatch.setattr('scripts.get_latest_analysis_results.get_connection', mock_get_connection)
        
        # Run script
        main()
        
        # Check output
        stdout_mock.seek(0)
        output = json.loads(stdout_mock.read())
        
        assert output['success'] is False
        assert 'error' in output

