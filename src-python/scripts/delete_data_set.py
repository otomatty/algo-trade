#!/usr/bin/env python3
"""
Script to delete a data set.
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
        input_data = read_json_input()
        data_set_id = input_data.get('data_set_id')
        
        if not data_set_id:
            result = json_response(success=False, error="data_set_id is required")
            write_json_output(result)
            sys.exit(1)
        
        conn = get_connection()
        cursor = conn.cursor()
        
        # Delete OHLCV data first (CASCADE should handle this, but explicit is better)
        cursor.execute("DELETE FROM ohlcv_data WHERE data_set_id = ?", (data_set_id,))
        
        # Delete data set
        cursor.execute("DELETE FROM data_sets WHERE id = ?", (data_set_id,))
        
        if cursor.rowcount == 0:
            result = json_response(success=False, error=f"Data set with id {data_set_id} not found")
            write_json_output(result)
            sys.exit(1)
        
        conn.commit()
        
        result = json_response(success=True, data={"message": "Data set deleted successfully"})
        write_json_output(result)
    except Exception as e:
        result = json_response(success=False, error=str(e))
        write_json_output(result)
        sys.exit(1)


if __name__ == '__main__':
    main()

