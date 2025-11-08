#!/usr/bin/env python3
"""
Script to import OHLCV data from CSV file.
Called from Rust Tauri command.
"""
import sys
import json
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.data_collection.csv_importer import CSVImporter
from utils.json_io import read_json_input, write_json_output


def main():
    """Main entry point."""
    try:
        # Read input from stdin
        input_data = read_json_input()
        file_path = input_data.get('file_path')
        name = input_data.get('name')
        
        if not file_path:
            result = {
                "success": False,
                "error": "file_path is required"
            }
            write_json_output(result)
            sys.exit(1)
        
        # Import CSV
        importer = CSVImporter()
        result = importer.import_csv(file_path, name)
        
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

