#!/usr/bin/env python3
"""
Script to check data integrity.
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

from modules.data_collection.data_validator import DataValidator
from utils.json_io import read_json_input, write_json_output, json_response

logger = logging.getLogger(__name__)


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
        
        validator = DataValidator()
        result = validator.check_integrity(data_set_id)
        
        # Write result to stdout
        write_json_output(json_response(success=True, data=result))
        
    except Exception as e:
        logger.exception("Error in check_data_integrity")
        result = json_response(success=False, error=str(e))
        write_json_output(result)
        sys.exit(1)


if __name__ == '__main__':
    main()

