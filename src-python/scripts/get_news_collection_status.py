#!/usr/bin/env python3
"""
Script to get news collection job status.
Called from Rust Tauri command.
"""
import sys
import json
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.news_collection.job_manager import NewsCollectionJobManager
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
        
        job_manager = NewsCollectionJobManager()
        job_status = job_manager.get_job_status(job_id)
        
        if not job_status:
            result = json_response(success=False, error=f"Job {job_id} not found")
            write_json_output(result)
            sys.exit(1)
        
        result = json_response(success=True, data=job_status)
        write_json_output(result)
    except Exception as e:
        result = json_response(success=False, error=str(e))
        write_json_output(result)
        sys.exit(1)


if __name__ == '__main__':
    main()

