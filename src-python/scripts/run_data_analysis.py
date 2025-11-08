#!/usr/bin/env python3
"""
Script to run data analysis job.
Called from Rust Tauri command.
"""
import sys
import json
import uuid
import threading
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from database.connection import get_connection
from modules.data_analysis.analyzer import DataAnalyzer
from utils.json_io import read_json_input, write_json_output, json_response


def run_analysis_in_background(job_id: str, data_set_id: int):
    """Run analysis in background thread."""
    try:
        conn = get_connection()
        analyzer = DataAnalyzer(conn=conn)
        analyzer.analyze_data_set(job_id, data_set_id)
    except Exception as e:
        # Update job status to failed
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE analysis_jobs
            SET status = 'failed', progress = 0.0, error = ?, completed_at = ?
            WHERE job_id = ?
        """, (str(e), datetime.now().isoformat(), job_id))
        conn.commit()


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
        
        # Validate data set exists
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id FROM data_sets WHERE id = ?", (data_set_id,))
        if not cursor.fetchone():
            result = json_response(success=False, error=f"Data set with id {data_set_id} not found")
            write_json_output(result)
            sys.exit(1)
        
        # Generate job ID
        job_id = str(uuid.uuid4())
        
        # Create analysis job record
        cursor.execute("""
            INSERT INTO analysis_jobs (job_id, data_set_id, status, progress, message, created_at)
            VALUES (?, ?, 'pending', 0.0, 'Analysis job created', ?)
        """, (job_id, data_set_id, datetime.now().isoformat()))
        
        conn.commit()
        
        # Start analysis in background thread
        thread = threading.Thread(target=run_analysis_in_background, args=(job_id, data_set_id))
        thread.daemon = True
        thread.start()
        
        result = json_response(success=True, data={"job_id": job_id})
        write_json_output(result)
    except Exception as e:
        result = json_response(success=False, error=str(e))
        write_json_output(result)
        sys.exit(1)


if __name__ == '__main__':
    main()
