"""
Unit tests for save_prediction_action script.
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
class TestSavePredictionAction:
    """Test cases for save_prediction_action script."""
    
    def test_save_prediction_action_success(self, temp_db):
        """Test successful action save."""
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        
        # Insert test prediction
        prediction_id = 'test-prediction-123'
        job_id = 'test-job-123'
        
        cursor.execute("""
            INSERT INTO stock_predictions (
                prediction_id, job_id, symbol, name, predicted_direction,
                confidence_score, rationale, recommended_action, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            prediction_id,
            job_id,
            'AAPL',
            'Apple Inc.',
            'up',
            0.85,
            'Test rationale',
            'buy',
            datetime.now().isoformat()
        ))
        conn.commit()
        
        # Mock stdin input
        input_data = {
            'prediction_id': prediction_id,
            'action': 'buy',
            'notes': 'Test notes'
        }
        
        from scripts.save_prediction_action import main
        
        with patch('sys.stdin', StringIO(json.dumps(input_data))), \
             patch('sys.stdout', new_callable=StringIO) as mock_stdout, \
             patch('scripts.save_prediction_action.get_connection', return_value=conn):
            
            main()
            
            output = json.loads(mock_stdout.getvalue())
            assert output['success'] is True
            assert 'action_id' in output['data']
            assert output['data']['prediction_id'] == prediction_id
            assert output['data']['action'] == 'buy'
        
        # Verify action was inserted
        cursor.execute("""
            SELECT id, prediction_id, action, notes 
            FROM prediction_actions 
            WHERE prediction_id = ?
        """, (prediction_id,))
        action = cursor.fetchone()
        assert action is not None
        assert action[2] == 'buy'
        assert action[3] == 'Test notes'
        
        conn.close()
    
    def test_save_prediction_action_update_existing(self, temp_db):
        """Test updating existing action."""
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        
        # Insert test prediction
        prediction_id = 'test-prediction-456'
        job_id = 'test-job-456'
        
        cursor.execute("""
            INSERT INTO stock_predictions (
                prediction_id, job_id, symbol, name, predicted_direction,
                confidence_score, rationale, recommended_action, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            prediction_id,
            job_id,
            'MSFT',
            'Microsoft Corp.',
            'up',
            0.80,
            'Test rationale',
            'buy',
            datetime.now().isoformat()
        ))
        
        # Insert existing action
        cursor.execute("""
            INSERT INTO prediction_actions (prediction_id, action, notes, created_at)
            VALUES (?, ?, ?, ?)
        """, (prediction_id, 'hold', 'Old notes', datetime.now().isoformat()))
        conn.commit()
        
        # Mock stdin input to update action
        input_data = {
            'prediction_id': prediction_id,
            'action': 'buy',
            'notes': 'Updated notes'
        }
        
        from scripts.save_prediction_action import main
        
        with patch('sys.stdin', StringIO(json.dumps(input_data))), \
             patch('sys.stdout', new_callable=StringIO) as mock_stdout, \
             patch('scripts.save_prediction_action.get_connection', return_value=conn):
            
            main()
            
            output = json.loads(mock_stdout.getvalue())
            assert output['success'] is True
        
        # Verify action was updated
        cursor.execute("""
            SELECT action, notes FROM prediction_actions WHERE prediction_id = ?
        """, (prediction_id,))
        action = cursor.fetchone()
        assert action[0] == 'buy'
        assert action[1] == 'Updated notes'
        
        conn.close()
    
    def test_save_prediction_action_prediction_not_found(self, temp_db):
        """Test action save with non-existent prediction."""
        conn = sqlite3.connect(temp_db)
        
        input_data = {
            'prediction_id': 'non-existent-prediction',
            'action': 'buy'
        }
        
        from scripts.save_prediction_action import main
        
        with patch('sys.stdin', StringIO(json.dumps(input_data))), \
             patch('sys.stdout', new_callable=StringIO) as mock_stdout, \
             patch('scripts.save_prediction_action.get_connection', return_value=conn):
            
            with pytest.raises(SystemExit):
                main()
            
            output = json.loads(mock_stdout.getvalue())
            assert output['success'] is False
            assert 'Prediction not found' in output['error']
        
        conn.close()
    
    def test_save_prediction_action_invalid_action(self, temp_db):
        """Test action save with invalid action."""
        conn = sqlite3.connect(temp_db)
        
        input_data = {
            'prediction_id': 'test-prediction',
            'action': 'invalid-action'
        }
        
        from scripts.save_prediction_action import main
        
        with patch('sys.stdin', StringIO(json.dumps(input_data))), \
             patch('sys.stdout', new_callable=StringIO) as mock_stdout, \
             patch('scripts.save_prediction_action.get_connection', return_value=conn):
            
            with pytest.raises(SystemExit):
                main()
            
            output = json.loads(mock_stdout.getvalue())
            assert output['success'] is False
            assert 'Invalid action' in output['error']
        
        conn.close()
    
    def test_save_prediction_action_missing_required_fields(self, temp_db):
        """Test action save with missing required fields."""
        conn = sqlite3.connect(temp_db)
        
        # Test missing prediction_id
        input_data = {
            'action': 'buy'
        }
        
        from scripts.save_prediction_action import main
        
        with patch('sys.stdin', StringIO(json.dumps(input_data))), \
             patch('sys.stdout', new_callable=StringIO) as mock_stdout, \
             patch('scripts.save_prediction_action.get_connection', return_value=conn):
            
            with pytest.raises(SystemExit):
                main()
            
            output = json.loads(mock_stdout.getvalue())
            assert output['success'] is False
            assert 'prediction_id is required' in output['error']
        
        # Test missing action
        input_data = {
            'prediction_id': 'test-prediction'
        }
        
        with patch('sys.stdin', StringIO(json.dumps(input_data))), \
             patch('sys.stdout', new_callable=StringIO) as mock_stdout, \
             patch('scripts.save_prediction_action.get_connection', return_value=conn):
            
            with pytest.raises(SystemExit):
                main()
            
            output = json.loads(mock_stdout.getvalue())
            assert output['success'] is False
            assert 'action is required' in output['error']
        
        conn.close()

