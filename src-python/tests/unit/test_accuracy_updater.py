"""
Unit tests for accuracy_updater module.
"""
import pytest
import sqlite3
import sys
from pathlib import Path
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from modules.stock_prediction.accuracy_updater import AccuracyUpdater
from database.connection import get_connection
from database.schema import create_all_tables


@pytest.mark.unit
class TestAccuracyUpdater:
    """Test cases for AccuracyUpdater class."""
    
    def test_get_predictions_needing_update(self, temp_db):
        """Test getting predictions that need accuracy updates."""
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        
        job_id = 'test-job-123'
        prediction_id = 'test-prediction-123'
        
        # Insert prediction without accuracy
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
            (datetime.now() - timedelta(days=10)).isoformat()
        ))
        conn.commit()
        
        updater = AccuracyUpdater(conn)
        predictions = updater.get_predictions_needing_update(days_old=7)
        
        assert len(predictions) == 1
        assert predictions[0]['prediction_id'] == prediction_id
        
        conn.close()
    
    def test_calculate_accuracy_correct(self):
        """Test accuracy calculation for correct prediction."""
        updater = AccuracyUpdater()
        
        # Same direction
        assert updater.calculate_accuracy('up', 'up', None, 5.0) is True
        
        # Both positive change
        assert updater.calculate_accuracy('up', 'down', 5.0, 3.0) is True
        
        # Both negative change
        assert updater.calculate_accuracy('down', 'up', -5.0, -3.0) is True
    
    def test_calculate_accuracy_incorrect(self):
        """Test accuracy calculation for incorrect prediction."""
        updater = AccuracyUpdater()
        
        # Different directions, no change percent
        assert updater.calculate_accuracy('up', 'down', None, 5.0) is False
        
        # Different directions, opposite change signs
        assert updater.calculate_accuracy('up', 'down', 5.0, -3.0) is False
    
    def test_update_prediction_accuracy(self, temp_db):
        """Test updating a single prediction's accuracy."""
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        
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
        conn.commit()
        
        updater = AccuracyUpdater(conn)
        success = updater.update_prediction_accuracy(
            prediction_id,
            150.0,
            'up',
            5.0
        )
        
        assert success is True
        
        # Verify update
        cursor.execute("""
            SELECT actual_direction, accuracy, accuracy_updated_at
            FROM stock_predictions
            WHERE prediction_id = ?
        """, (prediction_id,))
        prediction = cursor.fetchone()
        assert prediction[0] == 'up'
        assert prediction[1] == 1  # Correct
        assert prediction[2] is not None
        
        conn.close()
    
    def test_batch_update_accuracy(self, temp_db):
        """Test batch updating accuracy for multiple predictions."""
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        
        job_id = 'test-job-789'
        prediction_id1 = 'test-prediction-batch-1'
        prediction_id2 = 'test-prediction-batch-2'
        
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
            (datetime.now() - timedelta(days=10)).isoformat()
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
            (datetime.now() - timedelta(days=10)).isoformat()
        ))
        conn.commit()
        
        updater = AccuracyUpdater(conn)
        
        # Mock fetch_actual_price to return None (not implemented)
        with patch.object(updater, 'fetch_actual_price', return_value=None):
            stats = updater.batch_update_accuracy(days_old=7, limit=10)
            
            assert stats['total_predictions'] == 2
            assert stats['updated_count'] == 0  # None returned from fetch
            assert stats['failed_count'] == 2
        
        conn.close()

