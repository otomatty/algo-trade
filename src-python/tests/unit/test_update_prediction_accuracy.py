"""
Unit tests for update_prediction_accuracy script.
"""
import pytest
import sqlite3
import json
import sys
from pathlib import Path
from datetime import datetime
from unittest.mock import patch
from io import StringIO

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from database.connection import get_connection
from database.schema import create_all_tables


@pytest.mark.unit
class TestUpdatePredictionAccuracy:
    """Test cases for update_prediction_accuracy script."""
    
    def test_update_prediction_accuracy_success(self, temp_db):
        """Test successful accuracy update."""
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        
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
        
        input_data = {
            'prediction_id': prediction_id,
            'actual_price': 150.0,
            'actual_direction': 'up'
        }
        
        from scripts.update_prediction_accuracy import main
        
        with patch('sys.stdin', StringIO(json.dumps(input_data))), \
             patch('sys.stdout', new_callable=StringIO) as mock_stdout, \
             patch('scripts.update_prediction_accuracy.get_connection', return_value=conn):
            
            main()
            
            output = json.loads(mock_stdout.getvalue())
            assert output['success'] is True
            assert 'accuracy_updated' in output['data']
        
        # Verify accuracy was updated
        cursor.execute("""
            SELECT actual_direction, accuracy, accuracy_updated_at
            FROM stock_predictions
            WHERE prediction_id = ?
        """, (prediction_id,))
        prediction = cursor.fetchone()
        assert prediction[0] == 'up'
        assert prediction[1] is not None
        assert prediction[2] is not None
        
        conn.close()
    
    def test_update_prediction_accuracy_prediction_not_found(self, temp_db):
        """Test accuracy update with non-existent prediction."""
        conn = sqlite3.connect(temp_db)
        
        input_data = {
            'prediction_id': 'non-existent-prediction',
            'actual_price': 150.0,
            'actual_direction': 'up'
        }
        
        from scripts.update_prediction_accuracy import main
        
        with patch('sys.stdin', StringIO(json.dumps(input_data))), \
             patch('sys.stdout', new_callable=StringIO) as mock_stdout, \
             patch('scripts.update_prediction_accuracy.get_connection', return_value=conn):
            
            with pytest.raises(SystemExit):
                main()
            
            output = json.loads(mock_stdout.getvalue())
            assert output['success'] is False
            assert 'Prediction not found' in output['error']
        
        conn.close()
    
    def test_update_prediction_accuracy_invalid_direction(self, temp_db):
        """Test accuracy update with invalid direction."""
        conn = sqlite3.connect(temp_db)
        
        input_data = {
            'prediction_id': 'test-prediction',
            'actual_price': 150.0,
            'actual_direction': 'invalid-direction'
        }
        
        from scripts.update_prediction_accuracy import main
        
        with patch('sys.stdin', StringIO(json.dumps(input_data))), \
             patch('sys.stdout', new_callable=StringIO) as mock_stdout, \
             patch('scripts.update_prediction_accuracy.get_connection', return_value=conn):
            
            with pytest.raises(SystemExit):
                main()
            
            output = json.loads(mock_stdout.getvalue())
            assert output['success'] is False
            assert 'Invalid actual_direction' in output['error']
        
        conn.close()
    
    def test_update_prediction_accuracy_missing_required_fields(self, temp_db):
        """Test accuracy update with missing required fields."""
        conn = sqlite3.connect(temp_db)
        
        # Test missing prediction_id
        input_data = {
            'actual_price': 150.0,
            'actual_direction': 'up'
        }
        
        from scripts.update_prediction_accuracy import main
        
        with patch('sys.stdin', StringIO(json.dumps(input_data))), \
             patch('sys.stdout', new_callable=StringIO) as mock_stdout, \
             patch('scripts.update_prediction_accuracy.get_connection', return_value=conn):
            
            with pytest.raises(SystemExit):
                main()
            
            output = json.loads(mock_stdout.getvalue())
            assert output['success'] is False
            assert 'prediction_id is required' in output['error']
        
        conn.close()

