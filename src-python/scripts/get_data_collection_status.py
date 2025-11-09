#!/usr/bin/env python3
"""
Script to get data collection job status.
Called from Rust Tauri command.

Related Documentation:
  └─ Plan: docs/03_plans/data-collection/README.md
"""
import sys
import json
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.data_collection.job_manager import DataCollectionJobManager
from utils.json_io import read_json_input, write_json_output, json_response

logger = logging.getLogger(__name__)


def main():
    """Main entry point."""
    try:
        # Read input from stdin
        input_data = read_json_input()
        
        job_id = input_data.get('job_id')
        schedule_id = input_data.get('schedule_id')
        
        job_manager = DataCollectionJobManager()
        
        if job_id:
            # Get single job status
            job_status = job_manager.get_job_status(job_id)
            if not job_status:
                result = json_response(success=False, error=f"Job {job_id} not found")
                write_json_output(result)
                sys.exit(1)
            
            result = json_response(success=True, data={'job': job_status})
        elif schedule_id:
            # Get all jobs for a schedule
            jobs = job_manager.get_jobs_by_schedule(schedule_id)
            result = json_response(success=True, data={'jobs': jobs})
        else:
            result = json_response(success=False, error="job_id or schedule_id is required")
            write_json_output(result)
            sys.exit(1)
        
        # Write result to stdout
        write_json_output(result)
        
    except Exception as e:
        logger.exception("Error in get_data_collection_status")
        result = json_response(success=False, error=str(e))
        write_json_output(result)
        sys.exit(1)


if __name__ == '__main__':
    main()

