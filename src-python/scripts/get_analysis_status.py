#!/usr/bin/env python3
"""
Script to get analysis job status.
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
        
        cursor.execute("""
            SELECT status, progress, message, error, completed_at
            FROM analysis_jobs
            WHERE job_id = ?
        """, (job_id,))
        
        row = cursor.fetchone()
        
        if not row:
            result = json_response(success=False, error=f"Job with id {job_id} not found")
            write_json_output(result)
            sys.exit(1)
        
        status, progress, message, error, completed_at = row
        
        result_data = {
            'status': status,
            'progress': progress,
            'message': message or '',
        }
        
        if error:
            result_data['error'] = error
        
        result = json_response(success=True, data=result_data)
        write_json_output(result)
    except Exception as e:
        result = json_response(success=False, error=str(e))
        write_json_output(result)
        sys.exit(1)


if __name__ == '__main__':
    main()

