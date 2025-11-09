#!/usr/bin/env python3
"""
Script to get stock predictions for a job.
Called from Rust Tauri command.
"""
import sys
import json
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.stock_prediction.job_manager import StockPredictionJobManager
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
        
        job_manager = StockPredictionJobManager()
        predictions = job_manager.get_predictions(job_id)
        
        result_data = {
            'job_id': job_id,
            'predictions': predictions
        }
        
        result = json_response(success=True, data=result_data)
        write_json_output(result)
    except Exception as e:
        result = json_response(success=False, error=str(e))
        write_json_output(result)
        sys.exit(1)


if __name__ == '__main__':
    main()

