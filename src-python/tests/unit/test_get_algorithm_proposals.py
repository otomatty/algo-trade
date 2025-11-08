"""
Unit tests for get_algorithm_proposals script.
"""
import pytest
import json
import sqlite3
from pathlib import Path
import sys
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from scripts.get_algorithm_proposals import main
from utils.json_io import read_json_input, write_json_output
from io import StringIO


@pytest.mark.unit
class TestGetAlgorithmProposals:
    """Test cases for get_algorithm_proposals script."""
    
    def test_get_algorithm_proposals_success(self, temp_db, monkeypatch):
        """Test successful retrieval of algorithm proposals."""
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
            VALUES (?, ?, ?, ?, ?, 'completed', 1.0, 'Completed', ?)
        """, (job_id, data_set_id, None, 5, None, datetime.now().isoformat()))
        
        # Create proposals
        proposal_1 = {
            'name': 'Algorithm 1',
            'description': 'Description 1',
            'rationale': 'Rationale 1',
            'definition': {'triggers': [], 'actions': []},
            'confidence_score': 0.8,
        }
        
        proposal_2 = {
            'name': 'Algorithm 2',
            'description': 'Description 2',
            'rationale': 'Rationale 2',
            'definition': {'triggers': [], 'actions': []},
            'confidence_score': 0.9,
        }
        
        cursor.execute("""
            INSERT INTO algorithm_proposals (
                proposal_id, job_id, name, description, rationale,
                expected_performance, definition, confidence_score, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            'prop-1', job_id, proposal_1['name'], proposal_1['description'],
            proposal_1['rationale'], None, json.dumps(proposal_1['definition']),
            proposal_1['confidence_score'], datetime.now().isoformat()
        ))
        
        cursor.execute("""
            INSERT INTO algorithm_proposals (
                proposal_id, job_id, name, description, rationale,
                expected_performance, definition, confidence_score, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            'prop-2', job_id, proposal_2['name'], proposal_2['description'],
            proposal_2['rationale'], None, json.dumps(proposal_2['definition']),
            proposal_2['confidence_score'], datetime.now().isoformat()
        ))
        
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
        
        monkeypatch.setattr('scripts.get_algorithm_proposals.get_connection', mock_get_connection)
        
        # Run script
        main()
        
        # Check output
        stdout_mock.seek(0)
        output = json.loads(stdout_mock.read())
        
        assert output['success'] is True
        assert 'data' in output
        assert 'proposals' in output['data']
        assert len(output['data']['proposals']) == 2
        # Should be sorted by confidence_score DESC
        assert output['data']['proposals'][0]['confidence_score'] == 0.9
        assert output['data']['proposals'][1]['confidence_score'] == 0.8
    
    def test_get_algorithm_proposals_empty(self, temp_db, monkeypatch):
        """Test when no proposals exist for job."""
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        
        job_id = 'test-proposal-job-456'
        cursor.execute("""
            INSERT INTO proposal_generation_jobs (
                job_id, data_set_id, analysis_id, num_proposals,
                user_preferences, status, progress, message, created_at
            )
            VALUES (?, ?, ?, ?, ?, 'completed', 1.0, 'Completed', ?)
        """, (job_id, 1, None, 5, None, datetime.now().isoformat()))
        
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
        
        monkeypatch.setattr('scripts.get_algorithm_proposals.get_connection', mock_get_connection)
        
        main()
        
        stdout_mock.seek(0)
        output = json.loads(stdout_mock.read())
        
        assert output['success'] is True
        assert 'data' in output
        assert 'proposals' in output['data']
        assert len(output['data']['proposals']) == 0
    
    def test_get_algorithm_proposals_missing_job_id(self, monkeypatch):
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

