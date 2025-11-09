#!/usr/bin/env python3
"""
Script to save a user's action for a stock prediction.
Called from Rust Tauri command.
"""
import sys
import json
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from database.connection import get_connection
from utils.json_io import read_json_input, write_json_output, json_response


def main():
    """Main entry point."""
    try:
        # Read input from stdin
        input_data = read_json_input()
        prediction_id = input_data.get('prediction_id')
        action = input_data.get('action')
        notes = input_data.get('notes')
        
        if not prediction_id:
            result = json_response(success=False, error="prediction_id is required")
            write_json_output(result)
            sys.exit(1)
        
        if not action:
            result = json_response(success=False, error="action is required")
            write_json_output(result)
            sys.exit(1)
        
        # Validate action
        valid_actions = ['buy', 'sell', 'hold', 'watch', 'ignore']
        if action not in valid_actions:
            result = json_response(
                success=False,
                error=f"Invalid action. Must be one of: {', '.join(valid_actions)}"
            )
            write_json_output(result)
            sys.exit(1)
        
        conn = get_connection()
        cursor = conn.cursor()
        
        # Check if prediction exists
        cursor.execute("""
            SELECT prediction_id
            FROM stock_predictions
            WHERE prediction_id = ?
        """, (prediction_id,))
        
        prediction = cursor.fetchone()
        
        if not prediction:
            result = json_response(success=False, error="Prediction not found")
            write_json_output(result)
            sys.exit(1)
        
        # Check if action already exists (upsert behavior)
        cursor.execute("""
            SELECT id FROM prediction_actions
            WHERE prediction_id = ?
        """, (prediction_id,))
        
        existing_action = cursor.fetchone()
        
        if existing_action:
            # Update existing action
            cursor.execute("""
                UPDATE prediction_actions
                SET action = ?, notes = ?, created_at = datetime('now')
                WHERE prediction_id = ?
            """, (action, notes, prediction_id))
            action_id = existing_action['id']
        else:
            # Insert new action
            cursor.execute("""
                INSERT INTO prediction_actions (prediction_id, action, notes, created_at)
                VALUES (?, ?, ?, datetime('now'))
            """, (prediction_id, action, notes))
            action_id = cursor.lastrowid
        
        conn.commit()
        
        result_data = {
            'action_id': action_id,
            'prediction_id': prediction_id,
            'action': action
        }
        
        result = json_response(success=True, data=result_data)
        write_json_output(result)
    except Exception as e:
        result = json_response(success=False, error=str(e))
        write_json_output(result)
        sys.exit(1)


if __name__ == '__main__':
    main()

