"""
Accuracy updater module for batch processing prediction accuracy.
Can be used with APScheduler for automatic updates.

Related Documentation:
  └─ Plan: docs/03_plans/stock-prediction/README.md

DEPENDENCY MAP:

Parents (Files that import this file):
  └─ src-python/scripts/ (batch processing scripts)

Dependencies (External files that this file imports):
  ├─ sqlite3 (standard library)
  ├─ datetime (standard library)
  ├─ typing (standard library)
  ├─ logging (standard library)
  └─ src-python/database.connection
"""
import sqlite3
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

from database.connection import get_connection


logger = logging.getLogger(__name__)


class AccuracyUpdater:
    """Updates prediction accuracy by fetching actual prices from external APIs."""
    
    def __init__(self, conn: Optional[sqlite3.Connection] = None):
        """
        Initialize accuracy updater.
        
        Args:
            conn: Database connection (optional, will create new if not provided)
        """
        self.conn = conn
    
    def get_predictions_needing_update(
        self,
        days_old: int = 7,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Get predictions that need accuracy updates.
        
        Args:
            days_old: Minimum age of predictions to update (in days)
            limit: Maximum number of predictions to return
        
        Returns:
            List of prediction dictionaries
        """
        if not self.conn:
            self.conn = get_connection()
        
        cursor = self.conn.cursor()
        
        cutoff_date = (datetime.now() - timedelta(days=days_old)).isoformat()
        
        query = """
            SELECT 
                prediction_id,
                symbol,
                predicted_direction,
                predicted_change_percent,
                created_at,
                time_horizon
            FROM stock_predictions
            WHERE accuracy IS NULL
            AND DATE(created_at) <= DATE(?)
            ORDER BY created_at ASC
        """
        
        params = [cutoff_date]
        
        if limit:
            query += " LIMIT ?"
            params.append(limit)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        predictions = []
        for row in rows:
            predictions.append({
                'prediction_id': row['prediction_id'],
                'symbol': row['symbol'],
                'predicted_direction': row['predicted_direction'],
                'predicted_change_percent': row['predicted_change_percent'],
                'created_at': row['created_at'],
                'time_horizon': row['time_horizon']
            })
        
        return predictions
    
    def fetch_actual_price(self, symbol: str, date: str) -> Optional[float]:
        """
        Fetch actual price for a symbol at a given date.
        
        This is a placeholder implementation. In production, this would:
        1. Query external API (Yahoo Finance, Alpha Vantage, etc.)
        2. Get price data for the symbol at the specified date
        3. Return the closing price
        
        Args:
            symbol: Stock symbol
            date: Date string (ISO format)
        
        Returns:
            Actual price or None if not available
        """
        # TODO: Implement actual API call
        # For now, return None to indicate not implemented
        logger.warning(f"fetch_actual_price not implemented for {symbol} at {date}")
        return None
    
    def calculate_accuracy(
        self,
        predicted_direction: str,
        actual_direction: str,
        predicted_change_percent: Optional[float],
        actual_change_percent: float
    ) -> bool:
        """
        Calculate if prediction was accurate.
        
        Args:
            predicted_direction: 'up' | 'down' | 'sideways'
            actual_direction: 'up' | 'down' | 'sideways'
            predicted_change_percent: Optional predicted change percentage
            actual_change_percent: Actual change percentage
        
        Returns:
            True if prediction was accurate, False otherwise
        """
        # Simple direction-based accuracy
        if predicted_direction == actual_direction:
            return True
        
        # If predicted change percent is available, use threshold-based accuracy
        if predicted_change_percent is not None:
            # Consider accurate if both are positive or both are negative
            if (predicted_change_percent > 0 and actual_change_percent > 0) or \
               (predicted_change_percent < 0 and actual_change_percent < 0):
                return True
        
        return False
    
    def update_prediction_accuracy(
        self,
        prediction_id: str,
        actual_price: float,
        actual_direction: str,
        actual_change_percent: float
    ) -> bool:
        """
        Update a single prediction's accuracy.
        
        Args:
            prediction_id: Prediction ID
            actual_price: Actual price
            actual_direction: Actual direction ('up' | 'down' | 'sideways')
            actual_change_percent: Actual change percentage
        
        Returns:
            True if accuracy was updated, False otherwise
        """
        if not self.conn:
            self.conn = get_connection()
        
        cursor = self.conn.cursor()
        
        # Get prediction details
        cursor.execute("""
            SELECT 
                predicted_direction,
                predicted_change_percent
            FROM stock_predictions
            WHERE prediction_id = ?
        """, (prediction_id,))
        
        prediction = cursor.fetchone()
        
        if not prediction:
            logger.error(f"Prediction not found: {prediction_id}")
            return False
        
        predicted_direction = prediction['predicted_direction']
        predicted_change_percent = prediction['predicted_change_percent']
        
        # Calculate accuracy
        accuracy = self.calculate_accuracy(
            predicted_direction,
            actual_direction,
            predicted_change_percent,
            actual_change_percent
        )
        
        # Update prediction
        cursor.execute("""
            UPDATE stock_predictions
            SET 
                actual_direction = ?,
                actual_change_percent = ?,
                accuracy = ?,
                accuracy_updated_at = datetime('now')
            WHERE prediction_id = ?
        """, (actual_direction, actual_change_percent, 1 if accuracy else 0, prediction_id))
        
        self.conn.commit()
        
        logger.info(
            f"Updated accuracy for prediction {prediction_id}: "
            f"predicted={predicted_direction}, actual={actual_direction}, "
            f"accuracy={accuracy}"
        )
        
        return True
    
    def batch_update_accuracy(
        self,
        days_old: int = 7,
        limit: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Batch update accuracy for multiple predictions.
        
        Args:
            days_old: Minimum age of predictions to update (in days)
            limit: Maximum number of predictions to update
        
        Returns:
            Dictionary with update statistics
        """
        predictions = self.get_predictions_needing_update(days_old, limit)
        
        updated_count = 0
        failed_count = 0
        
        for prediction in predictions:
            try:
                # Fetch actual price (placeholder - would need real API)
                actual_price = self.fetch_actual_price(
                    prediction['symbol'],
                    prediction['created_at']
                )
                
                if actual_price is None:
                    logger.warning(
                        f"Could not fetch actual price for {prediction['symbol']} "
                        f"at {prediction['created_at']}"
                    )
                    failed_count += 1
                    continue
                
                # Calculate actual direction and change percent
                # This is simplified - would need original price at prediction time
                actual_direction = 'up'  # Placeholder
                actual_change_percent = 0.0  # Placeholder
                
                # Update accuracy
                success = self.update_prediction_accuracy(
                    prediction['prediction_id'],
                    actual_price,
                    actual_direction,
                    actual_change_percent
                )
                
                if success:
                    updated_count += 1
                else:
                    failed_count += 1
                    
            except Exception as e:
                logger.error(
                    f"Error updating accuracy for prediction {prediction['prediction_id']}: {e}"
                )
                failed_count += 1
        
        return {
            'total_predictions': len(predictions),
            'updated_count': updated_count,
            'failed_count': failed_count
        }

