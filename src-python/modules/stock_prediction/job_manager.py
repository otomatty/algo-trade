"""
Job manager for stock prediction generation jobs.

Related Documentation:
  ├─ Plan: docs/03_plans/stock-prediction/README.md
  └─ Data Model: docs/03_plans/stock-prediction/data-model.md

DEPENDENCY MAP:

Parents (Files that import this file):
  └─ src-python/scripts/generate_stock_predictions.py

Dependencies (External files that this file imports):
  ├─ sqlite3 (standard library)
  ├─ json (standard library)
  ├─ datetime (standard library)
  ├─ typing (standard library)
  ├─ logging (standard library)
  ├─ uuid (standard library)
  └─ src-python/database.connection
"""
import sqlite3
import json
import logging
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional

from database.connection import get_connection


logger = logging.getLogger(__name__)


class StockPredictionJobManager:
    """Manages stock prediction generation jobs."""
    
    def __init__(self, conn: Optional[sqlite3.Connection] = None):
        """
        Initialize job manager.
        
        Args:
            conn: Database connection (optional, will create new if not provided)
        """
        self.conn = conn
    
    def create_job(
        self,
        news_job_id: Optional[str],
        num_predictions: int,
        user_preferences: Optional[Dict[str, Any]] = None,
        market_trends: Optional[str] = None
    ) -> str:
        """
        Create a new stock prediction generation job.
        
        Args:
            news_job_id: News collection job ID (optional)
            num_predictions: Number of predictions to generate
            user_preferences: User preferences dictionary (optional)
            market_trends: Market trends information (optional)
            
        Returns:
            Job ID
        """
        if not self.conn:
            self.conn = get_connection()
        
        job_id = str(uuid.uuid4())
        cursor = self.conn.cursor()
        
        user_preferences_json = json.dumps(user_preferences) if user_preferences else None
        
        cursor.execute("""
            INSERT INTO stock_prediction_jobs (
                job_id, news_job_id, num_predictions,
                user_preferences, market_trends, status, progress, message, created_at
            )
            VALUES (?, ?, ?, ?, ?, 'pending', 0.0, 'Job created', ?)
        """, (
            job_id,
            news_job_id,
            num_predictions,
            user_preferences_json,
            market_trends,
            datetime.now().isoformat()
        ))
        
        self.conn.commit()
        logger.info(f"Created stock prediction generation job: {job_id}")
        return job_id
    
    def update_job_status(
        self,
        job_id: str,
        status: str,
        progress: float,
        message: str,
        error: Optional[str] = None,
        completed: bool = False
    ):
        """
        Update job status.
        
        Args:
            job_id: Job ID
            status: Job status ('pending' | 'analyzing' | 'generating' | 'completed' | 'failed')
            progress: Progress (0.0 to 1.0)
            message: Status message
            error: Error message (optional)
            completed: Whether job is completed
        """
        if not self.conn:
            self.conn = get_connection()
        
        cursor = self.conn.cursor()
        
        if completed:
            cursor.execute("""
                UPDATE stock_prediction_jobs
                SET status = ?, progress = ?, message = ?, error = ?, completed_at = ?
                WHERE job_id = ?
            """, (status, progress, message, error, datetime.now().isoformat(), job_id))
        else:
            cursor.execute("""
                UPDATE stock_prediction_jobs
                SET status = ?, progress = ?, message = ?, error = ?
                WHERE job_id = ?
            """, (status, progress, message, error, job_id))
        
        self.conn.commit()
        logger.debug(f"Updated job {job_id}: status={status}, progress={progress}")
    
    def get_job_status(self, job_id: str) -> Optional[Dict[str, Any]]:
        """
        Get job status.
        
        Args:
            job_id: Job ID
            
        Returns:
            Job status dictionary or None if not found
        """
        if not self.conn:
            self.conn = get_connection()
        
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT job_id, news_job_id, num_predictions, user_preferences, market_trends,
                   status, progress, message, error, created_at, completed_at
            FROM stock_prediction_jobs
            WHERE job_id = ?
        """, (job_id,))
        
        row = cursor.fetchone()
        if not row:
            return None
        
        return {
            'job_id': row[0],
            'news_job_id': row[1],
            'num_predictions': row[2],
            'user_preferences': json.loads(row[3]) if row[3] else None,
            'market_trends': row[4],
            'status': row[5],
            'progress': row[6],
            'message': row[7],
            'error': row[8],
            'created_at': row[9],
            'completed_at': row[10]
        }
    
    def save_predictions(
        self,
        job_id: str,
        predictions: List[Dict[str, Any]]
    ):
        """
        Save predictions to database.
        
        Args:
            job_id: Job ID
            predictions: List of prediction dictionaries
        """
        if not self.conn:
            self.conn = get_connection()
        
        cursor = self.conn.cursor()
        
        for prediction in predictions:
            prediction_id = prediction.get('prediction_id', str(uuid.uuid4()))
            symbol = prediction.get('symbol', '')
            name = prediction.get('name', '')
            predicted_direction = prediction.get('predicted_direction', 'sideways')
            predicted_change_percent = prediction.get('predicted_change_percent', 0.0)
            confidence_score = prediction.get('confidence_score', 0.0)
            rationale = prediction.get('rationale') or prediction.get('reasoning', '')
            association_chain = prediction.get('association_chain', [])
            recommended_action = prediction.get('recommended_action') or prediction.get('suggested_action', 'watch')
            risk_factors = prediction.get('risk_factors', [])
            time_horizon = prediction.get('time_horizon')
            
            cursor.execute("""
                INSERT INTO stock_predictions (
                    prediction_id, job_id, symbol, name, predicted_direction,
                    predicted_change_percent, confidence_score, rationale,
                    association_chain, recommended_action, risk_factors, time_horizon, created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                prediction_id,
                job_id,
                symbol,
                name,
                predicted_direction,
                predicted_change_percent,
                confidence_score,
                rationale,
                json.dumps(association_chain) if association_chain else None,
                recommended_action,
                json.dumps(risk_factors) if risk_factors else None,
                time_horizon,
                datetime.now().isoformat()
            ))
        
        self.conn.commit()
        logger.info(f"Saved {len(predictions)} predictions for job {job_id}")
    
    def get_predictions(self, job_id: str) -> List[Dict[str, Any]]:
        """
        Get predictions for a job.
        
        Args:
            job_id: Job ID
            
        Returns:
            List of prediction dictionaries
        """
        if not self.conn:
            self.conn = get_connection()
        
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT prediction_id, symbol, name, predicted_direction,
                   predicted_change_percent, confidence_score, rationale,
                   association_chain, recommended_action, risk_factors, time_horizon, created_at
            FROM stock_predictions
            WHERE job_id = ?
            ORDER BY created_at ASC
        """, (job_id,))
        
        predictions = []
        for row in cursor.fetchall():
            prediction = {
                'prediction_id': row[0],
                'symbol': row[1],
                'name': row[2],
                'predicted_direction': row[3],
                'predicted_change_percent': row[4],
                'confidence_score': row[5],
                'rationale': row[6],
                'reasoning': row[6],  # Alias for compatibility
                'association_chain': json.loads(row[7]) if row[7] else [],
                'recommended_action': row[8],
                'suggested_action': row[8],  # Alias for compatibility
                'risk_factors': json.loads(row[9]) if row[9] else [],
                'time_horizon': row[10],
                'created_at': row[11]
            }
            predictions.append(prediction)
        
        return predictions

