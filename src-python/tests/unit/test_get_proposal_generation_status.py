"""
Unit tests for get_proposal_generation_status script.
"""
import pytest
import json
import sqlite3
from pathlib import Path
import sys
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from scripts.get_proposal_generation_status import main
from utils.json_io import read_json_input, write_json_output
from io import StringIO


@pytest.mark.unit
class TestGetProposalGenerationStatus:
    """Test cases for get_proposal_generation_status script."""
    
    def test_get_proposal_generation_status_success(self, temp_db, monkeypatch):
        """Test successful retrieval of proposal generation status."""
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        
        # Create data set
        cursor.execute("""
            INSERT INTO data_sets (name, symbol, start_date, end_date, record_count, imported_at, source)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, ('Test Dataset', 'TEST', '2023-01-01', '2023-01-30', 30, datetime.now().isoformat(), 'csv'))
        data_set_id = cursor.lastrowid
        
        # Create proposal generation job
        job_id = 'test-proposal-job-123'
        cursor.execute("""
            INSERT INTO proposal_generation_jobs (
                job_id, data_set_id, analysis_id, num_proposals,
                user_preferences, status, progress, message, created_at
            )
            VALUES (?, ?, ?, ?, ?, 'generating', 0.5, 'Generating proposals...', ?)
        """, (job_id, data_set_id, None, 5, None, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
        
        # Mock stdin/stdout
        input_data = {'job_id': job_id}
        input_json = json.dumps(input_data)
        
        stdin_mock = StringIO(input_json)
        stdout_mock = StringIO()
        
        monkeypatch.setattr('sys.stdin', stdin_mock)
        monkeypatch.setattr('sys.stdout', stdout_mock)
        
        def mock_get_connection():
            return sqlite3.connect(temp_db)
        
        monkeypatch.setattr('scripts.get_proposal_generation_status.get_connection', mock_get_connection)
        
        # Run script
        main()
        
        # Check output
        stdout_mock.seek(0)
        output = json.loads(stdout_mock.read())
        
        assert output['success'] is True
        assert 'data' in output
        assert output['data']['status'] == 'generating'
        assert output['data']['progress'] == 0.5
        assert output['data']['message'] == 'Generating proposals...'
    
    def test_get_proposal_generation_status_completed(self, temp_db, monkeypatch):
        """Test retrieval of completed job status."""
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO data_sets (name, symbol, start_date, end_date, record_count, imported_at, source)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, ('Test Dataset', 'TEST', '2023-01-01', '2023-01-30', 30, datetime.now().isoformat(), 'csv'))
        data_set_id = cursor.lastrowid
        
        job_id = 'test-proposal-job-456'
        cursor.execute("""
            INSERT INTO proposal_generation_jobs (
                job_id, data_set_id, analysis_id, num_proposals,
                user_preferences, status, progress, message, completed_at
            )
            VALUES (?, ?, ?, ?, ?, 'completed', 1.0, 'Generated 5 proposals', ?)
        """, (job_id, data_set_id, None, 5, None, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
        
        input_data = {'job_id': job_id}
        input_json = json.dumps(input_data)
        
        stdin_mock = StringIO(input_json)
        stdout_mock = StringIO()
        
        monkeypatch.setattr('sys.stdin', stdin_mock)
        monkeypatch.setattr('sys.stdout', stdout_mock)
        
        def mock_get_connection():
            return sqlite3.connect(temp_db)
        
        monkeypatch.setattr('scripts.get_proposal_generation_status.get_connection', mock_get_connection)
        
        main()
        
        stdout_mock.seek(0)
        output = json.loads(stdout_mock.read())
        
        assert output['success'] is True
        assert output['data']['status'] == 'completed'
        assert output['data']['progress'] == 1.0
    
    def test_get_proposal_generation_status_not_found(self, temp_db, monkeypatch):
        """Test when job is not found."""
        input_data = {'job_id': 'non-existent-job'}
        input_json = json.dumps(input_data)
        
        stdin_mock = StringIO(input_json)
        stdout_mock = StringIO()
        
        monkeypatch.setattr('sys.stdin', stdin_mock)
        monkeypatch.setattr('sys.stdout', stdout_mock)
        
        def mock_get_connection():
            return sqlite3.connect(temp_db)
        
        monkeypatch.setattr('scripts.get_proposal_generation_status.get_connection', mock_get_connection)
        
        with pytest.raises(SystemExit):
            main()
        
        stdout_mock.seek(0)
        output = json.loads(stdout_mock.read())
        
        assert output['success'] is False
        assert 'error' in output
        assert 'not found' in output['error'].lower()
    
    def test_get_proposal_generation_status_missing_job_id(self, monkeypatch):
        """Test when job_id is missing."""
        input_data = {}
        input_json = json.dumps(input_data)
        
        stdin_mock = StringIO(input_json)
        stdout_mock = StringIO()
        
        monkeypatch.setattr('sys.stdin', stdin_mock)
        monkeypatch.setattr('sys.stdout', stdout_mock)
        
        with pytest.raises(SystemExit):
            main()
        
        stdout_mock.seek(0)
        output = json.loads(stdout_mock.read())
        
        assert output['success'] is False
        assert 'error' in output
        assert 'job_id' in output['error'].lower()

