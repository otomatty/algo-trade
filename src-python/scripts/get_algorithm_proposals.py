#!/usr/bin/env python3
"""
Script to get algorithm proposals for a job.
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
        job_id = input_data.get('job_id')
        
        if not job_id:
            result = json_response(success=False, error="job_id is required")
            write_json_output(result)
            sys.exit(1)
        
        conn = get_connection()
        cursor = conn.cursor()
        
        # Get proposals for the job, ordered by confidence_score DESC
        cursor.execute("""
            SELECT proposal_id, job_id, name, description, rationale,
                   expected_performance, definition, confidence_score, created_at
            FROM algorithm_proposals
            WHERE job_id = ?
            ORDER BY confidence_score DESC
        """, (job_id,))
        
        rows = cursor.fetchall()
        
        proposals = []
        for row in rows:
            proposal_id, job_id_db, name, description, rationale, expected_performance_json, definition_json, confidence_score, created_at = row
            
            proposal = {
                'proposal_id': proposal_id,
                'job_id': job_id_db,
                'name': name,
                'description': description,
                'rationale': rationale,
                'definition': json.loads(definition_json),
                'confidence_score': confidence_score,
                'created_at': created_at,
            }
            
            if expected_performance_json:
                proposal['expected_performance'] = json.loads(expected_performance_json)
            
            proposals.append(proposal)
        
        result_data = {
            'job_id': job_id,
            'proposals': proposals
        }
        
        result = json_response(success=True, data=result_data)
        write_json_output(result)
    except Exception as e:
        result = json_response(success=False, error=str(e))
        write_json_output(result)
        sys.exit(1)


if __name__ == '__main__':
    main()

