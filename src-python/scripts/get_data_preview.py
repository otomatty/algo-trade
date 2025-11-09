#!/usr/bin/env python3
"""
Script to get data preview for a data set.
Called from Rust Tauri command.
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
from database.connection import get_connection
from utils.json_io import read_json_input, write_json_output, json_response


def main():
    """Main entry point."""
    try:
        input_data = read_json_input()
        data_set_id = input_data.get('data_set_id')
        limit = input_data.get('limit', 100)
        
        if not data_set_id:
            result = json_response(success=False, error="data_set_id is required")
            write_json_output(result)
            sys.exit(1)
        
        if limit < 1:
            result = json_response(success=False, error="limit must be greater than 0")
            write_json_output(result)
            sys.exit(1)
        
        conn = get_connection()
        cursor = conn.cursor()
        
        # Check if data set exists
        cursor.execute("SELECT id, name FROM data_sets WHERE id = ?", (data_set_id,))
        data_set = cursor.fetchone()
        
        if not data_set:
            result = json_response(success=False, error=f"Data set with id {data_set_id} not found")
            write_json_output(result)
            sys.exit(1)
        
        # Get OHLCV data
        cursor.execute("""
            SELECT id, data_set_id, date, open, high, low, close, volume
            FROM ohlcv_data
            WHERE data_set_id = ?
            ORDER BY date ASC
            LIMIT ?
        """, (data_set_id, limit))
        
        rows = cursor.fetchall()
        
        if not rows:
            result = json_response(success=False, error=f"No data found for data set {data_set_id}")
            write_json_output(result)
            sys.exit(1)
        
        # Convert to list of dictionaries
        data = []
        for row in rows:
            data.append({
                "id": row["id"],
                "data_set_id": row["data_set_id"],
                "date": row["date"],
                "open": row["open"],
                "high": row["high"],
                "low": row["low"],
                "close": row["close"],
                "volume": int(row["volume"])
            })
        
        # Calculate statistics using Pandas
        df = pd.DataFrame(data)
        
        # Get date range
        date_range = {
            "start": df["date"].min(),
            "end": df["date"].max()
        }
        
        # Calculate statistics for each column
        statistics = {
            "count": len(df),
            "date_range": date_range,
            "open": {
                "mean": float(df["open"].mean()),
                "min": float(df["open"].min()),
                "max": float(df["open"].max()),
                "std": float(df["open"].std())
            },
            "high": {
                "mean": float(df["high"].mean()),
                "min": float(df["high"].min()),
                "max": float(df["high"].max()),
                "std": float(df["high"].std())
            },
            "low": {
                "mean": float(df["low"].mean()),
                "min": float(df["low"].min()),
                "max": float(df["low"].max()),
                "std": float(df["low"].std())
            },
            "close": {
                "mean": float(df["close"].mean()),
                "min": float(df["close"].min()),
                "max": float(df["close"].max()),
                "std": float(df["close"].std())
            },
            "volume": {
                "mean": float(df["volume"].mean()),
                "min": float(df["volume"].min()),
                "max": float(df["volume"].max()),
                "std": float(df["volume"].std())
            }
        }
        
        result = json_response(success=True, data={
            "data_set_id": data_set_id,
            "data": data,
            "statistics": statistics
        })
        write_json_output(result)
    except Exception as e:
        result = json_response(success=False, error=str(e))
        write_json_output(result)
        sys.exit(1)


if __name__ == '__main__':
    main()

