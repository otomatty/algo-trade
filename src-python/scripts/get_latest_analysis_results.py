#!/usr/bin/env python3
"""
Script to get latest analysis results for a data set.
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
        data_set_id = input_data.get('data_set_id')
        
        if not data_set_id:
            result = json_response(success=False, error="data_set_id is required")
            write_json_output(result)
            sys.exit(1)
        
        conn = get_connection()
        cursor = conn.cursor()
        
        # Validate data set exists
        cursor.execute("SELECT id FROM data_sets WHERE id = ?", (data_set_id,))
        if not cursor.fetchone():
            result = json_response(success=False, error=f"Data set with id {data_set_id} not found")
            write_json_output(result)
            sys.exit(1)
        
        # Get latest analysis result for this data set
        # Order by created_at DESC to get the most recent one
        cursor.execute("""
            SELECT job_id, data_set_id, analysis_summary, technical_indicators, statistics, created_at
            FROM analysis_results
            WHERE data_set_id = ?
            ORDER BY created_at DESC
            LIMIT 1
        """, (data_set_id,))
        
        row = cursor.fetchone()
        
        if not row:
            result = json_response(success=False, error=f"No analysis results found for data set {data_set_id}")
            write_json_output(result)
            sys.exit(1)
        
        job_id_db, data_set_id_db, analysis_summary_json, technical_indicators_json, statistics_json, created_at = row
        
        result_data = {
            'job_id': job_id_db,
            'data_set_id': data_set_id_db,
            'analysis_summary': json.loads(analysis_summary_json),
            'technical_indicators': json.loads(technical_indicators_json),
            'statistics': json.loads(statistics_json),
            'created_at': created_at
        }
        
        result = json_response(success=True, data=result_data)
        write_json_output(result)
    except Exception as e:
        result = json_response(success=False, error=str(e))
        write_json_output(result)
        sys.exit(1)


if __name__ == '__main__':
    main()

