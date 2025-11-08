"""
Unit tests for select_algorithm script.
"""
import pytest
import sqlite3
import json
import sys
from pathlib import Path
from datetime import datetime
from unittest.mock import patch, mock_open
from io import StringIO

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from database.connection import get_connection
from database.schema import create_all_tables


@pytest.mark.unit
class TestSelectAlgorithm:
    """Test cases for select_algorithm script."""
    
    def test_select_algorithm_success(self, temp_db):
        """Test successful algorithm selection."""
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        
        # Insert test proposal
        proposal_id = 'test-proposal-123'
        job_id = 'test-job-123'
        definition_json = json.dumps({
            'triggers': [{'type': 'rsi', 'condition': {'operator': 'lt', 'value': 30}}],
            'actions': [{'type': 'buy', 'parameters': {'percentage': 10}}]
        })
        
        cursor.execute("""
            INSERT INTO algorithm_proposals (
                proposal_id, job_id, name, description, rationale,
                definition, confidence_score, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            proposal_id,
            job_id,
            'Test Algorithm',
            'Test Description',
            'Test Rationale',
            definition_json,
            0.75,
            datetime.now().isoformat()
        ))
        conn.commit()
        
        # Mock stdin input
        input_data = {
            'proposal_id': proposal_id,
            'custom_name': None
        }
        
        # Import and run the script logic
        from scripts.select_algorithm import main
        
        with patch('sys.stdin', StringIO(json.dumps(input_data))), \
             patch('sys.stdout', new_callable=StringIO) as mock_stdout, \
             patch('scripts.select_algorithm.get_connection', return_value=conn):
            
            main()
            
            output = json.loads(mock_stdout.getvalue())
            assert output['success'] is True
            assert 'algorithm_id' in output['data']
            assert output['data']['name'] == 'Test Algorithm'
            assert output['data']['proposal_id'] == proposal_id
        
        # Verify algorithm was inserted
        cursor.execute("SELECT id, name, description, definition, proposal_id FROM algorithms WHERE proposal_id = ?", (proposal_id,))
        algorithm = cursor.fetchone()
        assert algorithm is not None
        assert algorithm[1] == 'Test Algorithm'
        assert algorithm[2] == 'Test Description'
        assert algorithm[4] == proposal_id
        
        conn.close()
    
    def test_select_algorithm_with_custom_name(self, temp_db):
        """Test algorithm selection with custom name."""
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        
        # Insert test proposal
        proposal_id = 'test-proposal-456'
        job_id = 'test-job-456'
        definition_json = json.dumps({
            'triggers': [{'type': 'rsi', 'condition': {'operator': 'lt', 'value': 30}}],
            'actions': [{'type': 'buy', 'parameters': {'percentage': 10}}]
        })
        
        cursor.execute("""
            INSERT INTO algorithm_proposals (
                proposal_id, job_id, name, description, rationale,
                definition, confidence_score, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            proposal_id,
            job_id,
            'Original Name',
            'Test Description',
            'Test Rationale',
            definition_json,
            0.75,
            datetime.now().isoformat()
        ))
        conn.commit()
        
        # Mock stdin input with custom name
        input_data = {
            'proposal_id': proposal_id,
            'custom_name': 'My Custom Algorithm'
        }
        
        from scripts.select_algorithm import main
        
        with patch('sys.stdin', StringIO(json.dumps(input_data))), \
             patch('sys.stdout', new_callable=StringIO) as mock_stdout, \
             patch('scripts.select_algorithm.get_connection', return_value=conn):
            
            main()
            
            output = json.loads(mock_stdout.getvalue())
            assert output['success'] is True
            assert output['data']['name'] == 'My Custom Algorithm'
        
        # Verify algorithm was inserted with custom name
        cursor.execute("SELECT name FROM algorithms WHERE proposal_id = ?", (proposal_id,))
        algorithm = cursor.fetchone()
        assert algorithm[0] == 'My Custom Algorithm'
        
        conn.close()
    
    def test_select_algorithm_proposal_not_found(self, temp_db):
        """Test algorithm selection with non-existent proposal."""
        conn = sqlite3.connect(temp_db)
        
        # Mock stdin input with non-existent proposal_id
        input_data = {
            'proposal_id': 'non-existent-proposal',
            'custom_name': None
        }
        
        from scripts.select_algorithm import main
        
        with patch('sys.stdin', StringIO(json.dumps(input_data))), \
             patch('sys.stdout', new_callable=StringIO) as mock_stdout, \
             patch('scripts.select_algorithm.get_connection', return_value=conn):
            
            main()
            
            output = json.loads(mock_stdout.getvalue())
            assert output['success'] is False
            assert 'Proposal not found' in output['error']
        
        conn.close()
    
    def test_select_algorithm_missing_proposal_id(self, temp_db):
        """Test algorithm selection with missing proposal_id."""
        conn = sqlite3.connect(temp_db)
        
        # Mock stdin input without proposal_id
        input_data = {
            'custom_name': 'Test Name'
        }
        
        from scripts.select_algorithm import main
        
        with patch('sys.stdin', StringIO(json.dumps(input_data))), \
             patch('sys.stdout', new_callable=StringIO) as mock_stdout, \
             patch('scripts.select_algorithm.get_connection', return_value=conn):
            
            main()
            
            output = json.loads(mock_stdout.getvalue())
            assert output['success'] is False
            assert 'proposal_id is required' in output['error']
        
        conn.close()

