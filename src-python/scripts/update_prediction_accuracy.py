#!/usr/bin/env python3
"""
Script to update prediction accuracy with actual results.
Called from Rust Tauri command.
"""
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Optional

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from database.connection import get_connection
from utils.json_io import read_json_input, write_json_output, json_response


def calculate_accuracy(
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


def main():
    """Main entry point."""
    try:
        # Read input from stdin
        input_data = read_json_input()
        prediction_id = input_data.get('prediction_id')
        actual_price = input_data.get('actual_price')
        actual_direction = input_data.get('actual_direction')
        
        if not prediction_id:
            result = json_response(success=False, error="prediction_id is required")
            write_json_output(result)
            sys.exit(1)
        
        if actual_price is None:
            result = json_response(success=False, error="actual_price is required")
            write_json_output(result)
            sys.exit(1)
        
        if not actual_direction:
            result = json_response(success=False, error="actual_direction is required")
            write_json_output(result)
            sys.exit(1)
        
        # Validate actual_direction
        valid_directions = ['up', 'down', 'sideways']
        if actual_direction not in valid_directions:
            result = json_response(
                success=False,
                error=f"Invalid actual_direction. Must be one of: {', '.join(valid_directions)}"
            )
            write_json_output(result)
            sys.exit(1)
        
        conn = get_connection()
        cursor = conn.cursor()
        
        # Get prediction details
        cursor.execute("""
            SELECT 
                predicted_direction,
                predicted_change_percent,
                symbol
            FROM stock_predictions
            WHERE prediction_id = ?
        """, (prediction_id,))
        
        prediction = cursor.fetchone()
        
        if not prediction:
            result = json_response(success=False, error="Prediction not found")
            write_json_output(result)
            sys.exit(1)
        
        predicted_direction = prediction['predicted_direction']
        predicted_change_percent = prediction['predicted_change_percent']
        
        # Calculate actual change percent (requires original price)
        # For now, we'll use a simplified approach
        # In a real implementation, we'd need to get the price at prediction time
        actual_change_percent = 0.0  # Placeholder - would need original price
        
        # Calculate accuracy
        accuracy = calculate_accuracy(
            predicted_direction,
            actual_direction,
            predicted_change_percent,
            actual_change_percent
        )
        
        # Update prediction with accuracy data
        cursor.execute("""
            UPDATE stock_predictions
            SET 
                actual_direction = ?,
                actual_change_percent = ?,
                accuracy = ?,
                accuracy_updated_at = datetime('now')
            WHERE prediction_id = ?
        """, (actual_direction, actual_change_percent, 1 if accuracy else 0, prediction_id))
        
        conn.commit()
        
        result_data = {
            'success': True,
            'accuracy_updated': accuracy
        }
        
        result = json_response(success=True, data=result_data)
        write_json_output(result)
    except Exception as e:
        result = json_response(success=False, error=str(e))
        write_json_output(result)
        sys.exit(1)


if __name__ == '__main__':
    main()

