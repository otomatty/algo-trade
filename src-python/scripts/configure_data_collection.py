#!/usr/bin/env python3
"""
Script to configure data collection schedules.
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
        # Read input from stdin
        input_data = read_json_input()
        logger.info(f"Received input: {json.dumps(input_data, indent=2)}")
        
        action = input_data.get('action')  # 'create', 'update', 'delete'
        
        if action == 'create':
            # Create new schedule
            name = input_data.get('name')
            source = input_data.get('source')
            symbol = input_data.get('symbol')
            cron_expression = input_data.get('cron_expression')
            start_date = input_data.get('start_date')
            end_date = input_data.get('end_date')
            api_key = input_data.get('api_key')
            data_set_name = input_data.get('data_set_name')
            enabled = input_data.get('enabled', True)
            
            # Validate required fields
            if not name:
                result = json_response(success=False, error="name is required")
                write_json_output(result)
                sys.exit(1)
            if not source:
                result = json_response(success=False, error="source is required")
                write_json_output(result)
                sys.exit(1)
            if not symbol:
                result = json_response(success=False, error="symbol is required")
                write_json_output(result)
                sys.exit(1)
            if not cron_expression:
                result = json_response(success=False, error="cron_expression is required")
                write_json_output(result)
                sys.exit(1)
            
            scheduler = DataCollectionScheduler.get_instance()
            scheduler.start()
            
            schedule_id = scheduler.add_schedule(
                name=name,
                source=source,
                symbol=symbol,
                cron_expression=cron_expression,
                start_date=start_date,
                end_date=end_date,
                api_key=api_key,
                data_set_name=data_set_name,
                enabled=enabled
            )
            
            result = json_response(
                success=True,
                data={'schedule_id': schedule_id}
            )
            
        elif action == 'update':
            # Update existing schedule
            schedule_id = input_data.get('schedule_id')
            if not schedule_id:
                result = json_response(success=False, error="schedule_id is required")
                write_json_output(result)
                sys.exit(1)
            
            scheduler = DataCollectionScheduler.get_instance()
            scheduler.start()
            
            updated = scheduler.update_schedule(
                schedule_id=schedule_id,
                name=input_data.get('name'),
                cron_expression=input_data.get('cron_expression'),
                enabled=input_data.get('enabled'),
                source=input_data.get('source'),
                symbol=input_data.get('symbol'),
                start_date=input_data.get('start_date'),
                end_date=input_data.get('end_date'),
                api_key=input_data.get('api_key'),
                data_set_name=input_data.get('data_set_name')
            )
            
            if not updated:
                result = json_response(success=False, error=f"Schedule {schedule_id} not found")
                write_json_output(result)
                sys.exit(1)
            
            result = json_response(success=True, data={'schedule_id': schedule_id})
            
        elif action == 'delete':
            # Delete schedule
            schedule_id = input_data.get('schedule_id')
            if not schedule_id:
                result = json_response(success=False, error="schedule_id is required")
                write_json_output(result)
                sys.exit(1)
            
            scheduler = DataCollectionScheduler.get_instance()
            scheduler.start()
            
            deleted = scheduler.delete_schedule(schedule_id)
            
            if not deleted:
                result = json_response(success=False, error=f"Schedule {schedule_id} not found")
                write_json_output(result)
                sys.exit(1)
            
            result = json_response(success=True, data={'schedule_id': schedule_id})
            
        else:
            result = json_response(success=False, error=f"Unknown action: {action}")
            write_json_output(result)
            sys.exit(1)
        
        # Write result to stdout
        write_json_output(result)
        
    except Exception as e:
        logger.exception("Error in configure_data_collection")
        result = json_response(success=False, error=str(e))
        write_json_output(result)
        sys.exit(1)


if __name__ == '__main__':
    main()

