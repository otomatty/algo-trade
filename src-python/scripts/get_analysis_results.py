#!/usr/bin/env python3
"""
Script to get analysis results.
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
            SELECT job_id, data_set_id, analysis_summary, technical_indicators, statistics
            FROM analysis_results
            WHERE job_id = ?
        """, (job_id,))
        
        row = cursor.fetchone()
        
        if not row:
            result = json_response(success=False, error=f"Analysis results for job {job_id} not found")
            write_json_output(result)
            sys.exit(1)
        
        job_id_db, data_set_id, analysis_summary_json, technical_indicators_json, statistics_json = row
        
        result_data = {
            'job_id': job_id_db,
            'data_set_id': data_set_id,
            'analysis_summary': json.loads(analysis_summary_json),
            'technical_indicators': json.loads(technical_indicators_json),
            'statistics': json.loads(statistics_json)
        }
        
        result = json_response(success=True, data=result_data)
        write_json_output(result)
    except Exception as e:
        result = json_response(success=False, error=str(e))
        write_json_output(result)
        sys.exit(1)


if __name__ == '__main__':
    main()

