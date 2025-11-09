#!/usr/bin/env python3
"""
Script to get prediction history with filtering and accuracy statistics.
Called from Rust Tauri command.
"""
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from database.connection import get_connection
from utils.json_io import read_json_input, write_json_output, json_response


def calculate_accuracy_stats(predictions: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """Calculate accuracy statistics from predictions."""
    total = len(predictions)
    if total == 0:
        return None
    
    correct = sum(1 for p in predictions if p.get('accuracy') is True)
    accuracy_rate = correct / total if total > 0 else 0.0
    
    return {
        'total_predictions': total,
        'correct_predictions': correct,
        'accuracy_rate': accuracy_rate
    }


def main():
    """Main entry point."""
    try:
        # Read input from stdin
        input_data = read_json_input()
        limit = input_data.get('limit', 50)
        start_date = input_data.get('start_date')
        end_date = input_data.get('end_date')
        symbol = input_data.get('symbol')
        
        conn = get_connection()
        cursor = conn.cursor()
        
        # Build query with filters
        query = """
            SELECT 
                sp.prediction_id,
                sp.symbol,
                sp.predicted_direction,
                sp.created_at as predicted_at,
                sp.actual_direction,
                sp.actual_change_percent,
                sp.accuracy,
                sp.rationale as reasoning,
                pa.action as user_action
            FROM stock_predictions sp
            LEFT JOIN prediction_actions pa ON sp.prediction_id = pa.prediction_id
            WHERE 1=1
        """
        params = []
        
        if start_date:
            query += " AND DATE(sp.created_at) >= DATE(?)"
            params.append(start_date)
        
        if end_date:
            query += " AND DATE(sp.created_at) <= DATE(?)"
            params.append(end_date)
        
        if symbol:
            query += " AND sp.symbol = ?"
            params.append(symbol)
        
        query += " ORDER BY sp.created_at DESC LIMIT ?"
        params.append(limit)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        # Convert rows to dictionaries
        predictions = []
        for row in rows:
            prediction = {
                'prediction_id': row['prediction_id'],
                'symbol': row['symbol'],
                'predicted_direction': row['predicted_direction'],
                'predicted_at': row['predicted_at'],
                'reasoning': row['reasoning'] or '',
            }
            
            if row['actual_direction']:
                prediction['actual_direction'] = row['actual_direction']
            
            if row['actual_change_percent'] is not None:
                prediction['actual_change_percent'] = row['actual_change_percent']
            
            if row['accuracy'] is not None:
                prediction['accuracy'] = bool(row['accuracy'])
            
            if row['user_action']:
                prediction['user_action'] = row['user_action']
            
            predictions.append(prediction)
        
        # Calculate accuracy statistics
        accuracy_stats = calculate_accuracy_stats(predictions)
        
        result_data = {
            'predictions': predictions
        }
        
        if accuracy_stats:
            result_data['accuracy_stats'] = accuracy_stats
        
        result = json_response(success=True, data=result_data)
        write_json_output(result)
    except Exception as e:
        result = json_response(success=False, error=str(e))
        write_json_output(result)
        sys.exit(1)


if __name__ == '__main__':
    main()

