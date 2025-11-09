#!/usr/bin/env python3
"""
Script to get data collection schedules.
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

from modules.data_collection.scheduler import DataCollectionScheduler
from utils.json_io import read_json_input, write_json_output, json_response

logger = logging.getLogger(__name__)


def main():
    """Main entry point."""
    try:
        # Read input from stdin (optional)
        try:
            input_data = read_json_input()
        except:
            input_data = {}
        
        enabled_only = input_data.get('enabled_only', False)
        schedule_id = input_data.get('schedule_id')
        
        scheduler = DataCollectionScheduler.get_instance()
        scheduler.start()
        
        if schedule_id:
            # Get single schedule
            schedule = scheduler.get_schedule(schedule_id)
            if not schedule:
                result = json_response(success=False, error=f"Schedule {schedule_id} not found")
                write_json_output(result)
                sys.exit(1)
            
            result = json_response(success=True, data={'schedule': schedule})
        else:
            # Get all schedules
            schedules = scheduler.get_all_schedules(enabled_only=enabled_only)
            result = json_response(success=True, data={'schedules': schedules})
        
        # Write result to stdout
        write_json_output(result)
        
    except Exception as e:
        logger.exception("Error in get_data_collection_schedules")
        result = json_response(success=False, error=str(e))
        write_json_output(result)
        sys.exit(1)


if __name__ == '__main__':
    main()

