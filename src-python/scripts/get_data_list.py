#!/usr/bin/env python3
"""
Script to get list of data sets.
Called from Rust Tauri command.
"""
import sys
import json
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from database.connection import get_connection
from utils.json_io import write_json_output, json_response


def main():
    """Main entry point."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, name, symbol, start_date, end_date, record_count, imported_at, source, created_at
            FROM data_sets
            ORDER BY created_at DESC
        """)
        
        rows = cursor.fetchall()
        
        data_list = []
        for row in rows:
            data_list.append({
                "id": row["id"],
                "name": row["name"],
                "symbol": row["symbol"],
                "start_date": row["start_date"],
                "end_date": row["end_date"],
                "record_count": row["record_count"],
                "imported_at": row["imported_at"],
                "source": row["source"],
                "created_at": row["created_at"]
            })
        
        result = json_response(success=True, data={"data_list": data_list})
        write_json_output(result)
    except Exception as e:
        result = json_response(success=False, error=str(e))
        write_json_output(result)
        sys.exit(1)


if __name__ == '__main__':
    main()

