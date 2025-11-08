#!/usr/bin/env python3
"""
Script to select an algorithm proposal and save it to algorithms table.
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
        # Read input from stdin
        input_data = read_json_input()
        proposal_id = input_data.get('proposal_id')
        custom_name = input_data.get('custom_name')
        
        if not proposal_id:
            result = json_response(success=False, error="proposal_id is required")
            write_json_output(result)
            sys.exit(1)
        
        conn = get_connection()
        cursor = conn.cursor()
        
        # Get proposal from algorithm_proposals table
        cursor.execute("""
            SELECT name, description, definition, proposal_id
            FROM algorithm_proposals
            WHERE proposal_id = ?
        """, (proposal_id,))
        
        proposal = cursor.fetchone()
        
        if not proposal:
            result = json_response(success=False, error="Proposal not found")
            write_json_output(result)
            sys.exit(1)
        
        proposal_name, proposal_description, definition_json, proposal_id_db = proposal
        
        # Use custom_name if provided, otherwise use proposal name
        algorithm_name = custom_name if custom_name else proposal_name
        
        # Insert into algorithms table
        cursor.execute("""
            INSERT INTO algorithms (name, description, definition, proposal_id, created_at, updated_at)
            VALUES (?, ?, ?, ?, datetime('now'), datetime('now'))
        """, (algorithm_name, proposal_description, definition_json, proposal_id_db))
        
        algorithm_id = cursor.lastrowid
        conn.commit()
        
        result_data = {
            'algorithm_id': algorithm_id,
            'name': algorithm_name,
            'proposal_id': proposal_id_db
        }
        
        result = json_response(success=True, data=result_data)
        write_json_output(result)
    except Exception as e:
        result = json_response(success=False, error=str(e))
        write_json_output(result)
        sys.exit(1)


if __name__ == '__main__':
    main()

