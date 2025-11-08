#!/usr/bin/env python3
"""
Script to collect OHLCV data from external API.
Called from Rust Tauri command.
"""
import sys
import json
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.data_collection.data_collector import DataCollector
from utils.json_io import read_json_input, write_json_output


def main():
    """Main entry point."""
    try:
        # Read input from stdin
        input_data = read_json_input()
        source = input_data.get('source')
        symbol = input_data.get('symbol')
        start_date = input_data.get('start_date')
        end_date = input_data.get('end_date')
        name = input_data.get('name')
        api_key = input_data.get('api_key')
        
        # Validate required fields
        if not source:
            result = {"success": False, "error": "source is required"}
            write_json_output(result)
            sys.exit(1)
        if not symbol:
            result = {"success": False, "error": "symbol is required"}
            write_json_output(result)
            sys.exit(1)
        if not start_date:
            result = {"success": False, "error": "start_date is required"}
            write_json_output(result)
            sys.exit(1)
        if not end_date:
            result = {"success": False, "error": "end_date is required"}
            write_json_output(result)
            sys.exit(1)
        
        # Collect data
        collector = DataCollector()
        result = collector.collect_from_api(
            source=source,
            symbol=symbol,
            start_date=start_date,
            end_date=end_date,
            name=name,
            api_key=api_key
        )
        
        # Write result to stdout
        write_json_output(result)
        
        if not result.get('success'):
            sys.exit(1)
    except Exception as e:
        result = {
            "success": False,
            "error": str(e)
        }
        write_json_output(result)
        sys.exit(1)


if __name__ == '__main__':
    main()

