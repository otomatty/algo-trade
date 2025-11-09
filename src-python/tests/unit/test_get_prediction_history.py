"""
Unit tests for get_prediction_history script.
"""
import pytest
import sqlite3
import json
import sys
from pathlib import Path
from datetime import datetime, timedelta
from unittest.mock import patch
from io import StringIO

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from database.connection import get_connection
from database.schema import create_all_tables


@pytest.mark.unit
class TestGetPredictionHistory:
    """Test cases for get_prediction_history script."""
    
    def test_get_prediction_history_success(self, temp_db):
        """Test successful history retrieval."""
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        
        # Insert test predictions
        job_id = 'test-job-123'
        prediction_id1 = 'test-prediction-1'
        prediction_id2 = 'test-prediction-2'
        
        cursor.execute("""
            INSERT INTO stock_predictions (
                prediction_id, job_id, symbol, name, predicted_direction,
                confidence_score, rationale, recommended_action, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            prediction_id1,
            job_id,
            'AAPL',
            'Apple Inc.',
            'up',
            0.85,
            'Test rationale 1',
            'buy',
            datetime.now().isoformat()
        ))
        
        cursor.execute("""
            INSERT INTO stock_predictions (
                prediction_id, job_id, symbol, name, predicted_direction,
                confidence_score, rationale, recommended_action, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            prediction_id2,
            job_id,
            'MSFT',
            'Microsoft Corp.',
            'down',
            0.75,
            'Test rationale 2',
            'sell',
            (datetime.now() - timedelta(days=1)).isoformat()
        ))
        conn.commit()
        
        input_data = {
            'limit': 10
        }
        
        from scripts.get_prediction_history import main
        
        with patch('sys.stdin', StringIO(json.dumps(input_data))), \
             patch('sys.stdout', new_callable=StringIO) as mock_stdout, \
             patch('scripts.get_prediction_history.get_connection', return_value=conn):
            
            main()
            
            output = json.loads(mock_stdout.getvalue())
            assert output['success'] is True
            assert 'predictions' in output['data']
            assert len(output['data']['predictions']) == 2
    
    def test_get_prediction_history_with_filters(self, temp_db):
        """Test history retrieval with filters."""
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        
        job_id = 'test-job-456'
        prediction_id = 'test-prediction-filter'
        
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
            'limit': 10,
            'symbol': 'AAPL'
        }
        
        from scripts.get_prediction_history import main
        
        with patch('sys.stdin', StringIO(json.dumps(input_data))), \
             patch('sys.stdout', new_callable=StringIO) as mock_stdout, \
             patch('scripts.get_prediction_history.get_connection', return_value=conn):
            
            main()
            
            output = json.loads(mock_stdout.getvalue())
            assert output['success'] is True
            assert len(output['data']['predictions']) == 1
            assert output['data']['predictions'][0]['symbol'] == 'AAPL'
        
        conn.close()
    
    def test_get_prediction_history_with_accuracy_stats(self, temp_db):
        """Test history retrieval with accuracy statistics."""
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        
        job_id = 'test-job-789'
        prediction_id1 = 'test-prediction-acc-1'
        prediction_id2 = 'test-prediction-acc-2'
        
        cursor.execute("""
            INSERT INTO stock_predictions (
                prediction_id, job_id, symbol, name, predicted_direction,
                confidence_score, rationale, recommended_action, 
                actual_direction, accuracy, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            prediction_id1,
            job_id,
            'AAPL',
            'Apple Inc.',
            'up',
            0.85,
            'Test rationale 1',
            'buy',
            'up',
            1,
            datetime.now().isoformat()
        ))
        
        cursor.execute("""
            INSERT INTO stock_predictions (
                prediction_id, job_id, symbol, name, predicted_direction,
                confidence_score, rationale, recommended_action,
                actual_direction, accuracy, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            prediction_id2,
            job_id,
            'MSFT',
            'Microsoft Corp.',
            'up',
            0.75,
            'Test rationale 2',
            'buy',
            'down',
            0,
            datetime.now().isoformat()
        ))
        conn.commit()
        
        input_data = {
            'limit': 10
        }
        
        from scripts.get_prediction_history import main
        
        with patch('sys.stdin', StringIO(json.dumps(input_data))), \
             patch('sys.stdout', new_callable=StringIO) as mock_stdout, \
             patch('scripts.get_prediction_history.get_connection', return_value=conn):
            
            main()
            
            output = json.loads(mock_stdout.getvalue())
            assert output['success'] is True
            assert 'accuracy_stats' in output['data']
            assert output['data']['accuracy_stats']['total_predictions'] == 2
            assert output['data']['accuracy_stats']['correct_predictions'] == 1
            assert output['data']['accuracy_stats']['accuracy_rate'] == 0.5
        
        conn.close()

