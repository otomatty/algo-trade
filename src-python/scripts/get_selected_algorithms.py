#!/usr/bin/env python3
"""
Script to get selected algorithms from algorithms table.
Called from Rust Tauri command.
"""
import sys
import json
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from database.connection import get_connection
from utils.json_io import read_json_input, write_json_output, json_response


def main():
    """Main entry point."""
    try:
        # Read input from stdin (no input required for this command)
        input_data = read_json_input()
        
        conn = get_connection()
        cursor = conn.cursor()
        
        # Get all algorithms from algorithms table, ordered by created_at DESC
        cursor.execute("""
            SELECT id, name, description, definition, proposal_id, created_at, updated_at
            FROM algorithms
            ORDER BY created_at DESC
        """)
        
        rows = cursor.fetchall()
        
        algorithms = []
        for row in rows:
            algo_id, name, description, definition_json, proposal_id, created_at, updated_at = row
            
            algorithm = {
                'id': algo_id,
                'name': name,
                'description': description,
                'definition': json.loads(definition_json),
                'proposal_id': proposal_id,
                'created_at': created_at,
                'updated_at': updated_at,
            }
            
            algorithms.append(algorithm)
        
        result_data = {
            'algorithms': algorithms
        }
        
        result = json_response(success=True, data=result_data)
        write_json_output(result)
    except Exception as e:
        result = json_response(success=False, error=str(e))
        write_json_output(result)
        sys.exit(1)


if __name__ == '__main__':
    main()

