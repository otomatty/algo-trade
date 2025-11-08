#!/usr/bin/env python3
"""
Script to delete an algorithm from algorithms table.
Called from Rust Tauri command.

This script deletes an algorithm and optionally its related backtest results.
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
        # Read input from stdin
        input_data = read_json_input()
        algo_id = input_data.get('algo_id')
        
        if not algo_id:
            result = json_response(success=False, error="algo_id is required")
            write_json_output(result)
            sys.exit(1)
        
        conn = get_connection()
        cursor = conn.cursor()
        
        # Check if algorithm exists
        cursor.execute("SELECT id FROM algorithms WHERE id = ?", (algo_id,))
        algorithm = cursor.fetchone()
        
        if not algorithm:
            result = json_response(success=False, error=f"Algorithm with id {algo_id} not found")
            write_json_output(result)
            sys.exit(1)
        
        # Delete related backtest jobs (cascade will handle backtest_results, backtest_trades, backtest_equity_curve)
        cursor.execute("DELETE FROM backtest_jobs WHERE algorithm_id = ?", (algo_id,))
        
        # Delete the algorithm
        cursor.execute("DELETE FROM algorithms WHERE id = ?", (algo_id,))
        
        conn.commit()
        
        result_data = {
            'success': True,
            'message': f'Algorithm {algo_id} deleted successfully'
        }
        
        result = json_response(success=True, data=result_data)
        write_json_output(result)
    except Exception as e:
        result = json_response(success=False, error=str(e))
        write_json_output(result)
        sys.exit(1)


if __name__ == '__main__':
    main()

