#!/usr/bin/env python3
"""
Script to run backtest job.
Called from Rust Tauri command.
"""
import sys
import json
import uuid
import threading
import pandas as pd
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from database.connection import get_connection
from modules.backtest.backtest_engine import BacktestEngine
from modules.backtest.job_manager import BacktestJobManager
from utils.json_io import read_json_input, write_json_output, json_response


def run_backtest_in_background(
    job_id: str,
    algorithm_id: int,
    start_date: str,
    end_date: str,
    data_set_id: Optional[int]
):
    """Run backtest in background thread."""
    conn = get_connection()
    job_manager = BacktestJobManager(conn=conn)
    
    try:
        # Update job status to running
        job_manager.update_job_status(job_id, 'running', 0.1, 'Loading algorithm...')
        
        # Load algorithm from database
        cursor = conn.cursor()
        cursor.execute("""
            SELECT name, description, definition
            FROM algorithms
            WHERE id = ?
        """, (algorithm_id,))
        
        algorithm_row = cursor.fetchone()
        if not algorithm_row:
            raise ValueError(f"Algorithm with id {algorithm_id} not found")
        
        algorithm_name, algorithm_description, definition_json = algorithm_row
        algorithm_definition = json.loads(definition_json)
        
        job_manager.update_job_status(job_id, 'running', 0.2, 'Loading data...')
        
        # Load OHLCV data
        if data_set_id:
            cursor.execute("""
                SELECT date, open, high, low, close, volume
                FROM ohlcv_data
                WHERE data_set_id = ?
                ORDER BY date ASC
            """, (data_set_id,))
        else:
            # If no data_set_id, get data from all data sets (for now, use first available)
            cursor.execute("""
                SELECT date, open, high, low, close, volume
                FROM ohlcv_data
                ORDER BY date ASC
            """)
        
        rows = cursor.fetchall()
        if not rows:
            raise ValueError("No OHLCV data available")
        
        data = pd.DataFrame(rows, columns=['date', 'open', 'high', 'low', 'close', 'volume'])
        
        job_manager.update_job_status(job_id, 'running', 0.3, 'Running backtest...')
        
        # Run backtest
        engine = BacktestEngine(
            algorithm=algorithm_definition,
            data=data,
            start_date=start_date,
            end_date=end_date
        )
        
        results = engine.run()
        
        job_manager.update_job_status(job_id, 'running', 0.9, 'Saving results...')
        
        # Save results
        job_manager.save_results(
            job_id=job_id,
            algorithm_id=algorithm_id,
            start_date=start_date,
            end_date=end_date,
            performance=results['performance'],
            trades=results['trades'],
            equity_curve=results['equity_curve']
        )
        
        job_manager.update_job_status(
            job_id,
            'completed',
            1.0,
            'Backtest completed successfully',
            completed=True
        )
    except Exception as e:
        # Update job status to failed
        job_manager.update_job_status(
            job_id,
            'failed',
            0.0,
            f'Backtest failed: {str(e)}',
            error=str(e),
            completed=True
        )


def main():
    """Main entry point."""
    try:
        # Read input from stdin
        input_data = read_json_input()
        algorithm_ids = input_data.get('algorithm_ids', [])
        start_date = input_data.get('start_date')
        end_date = input_data.get('end_date')
        data_set_id = input_data.get('data_set_id')
        
        if not algorithm_ids:
            result = json_response(success=False, error="algorithm_ids is required")
            write_json_output(result)
            sys.exit(1)
        
        if not start_date or not end_date:
            result = json_response(success=False, error="start_date and end_date are required")
            write_json_output(result)
            sys.exit(1)
        
        # Validate algorithm exists
        conn = get_connection()
        cursor = conn.cursor()
        
        # For now, run backtest for first algorithm only
        # TODO: Support multiple algorithms
        algorithm_id = algorithm_ids[0]
        
        cursor.execute("SELECT id FROM algorithms WHERE id = ?", (algorithm_id,))
        if not cursor.fetchone():
            result = json_response(success=False, error=f"Algorithm with id {algorithm_id} not found")
            write_json_output(result)
            sys.exit(1)
        
        # Validate data set if provided
        if data_set_id:
            cursor.execute("SELECT id FROM data_sets WHERE id = ?", (data_set_id,))
            if not cursor.fetchone():
                result = json_response(success=False, error=f"Data set with id {data_set_id} not found")
                write_json_output(result)
                sys.exit(1)
        
        # Create job
        job_manager = BacktestJobManager(conn=conn)
        job_id = job_manager.create_job(
            algorithm_id=algorithm_id,
            start_date=start_date,
            end_date=end_date,
            data_set_id=data_set_id
        )
        
        # Start backtest in background thread
        thread = threading.Thread(
            target=run_backtest_in_background,
            args=(job_id, algorithm_id, start_date, end_date, data_set_id)
        )
        thread.daemon = True
        thread.start()
        
        result = json_response(success=True, data={"job_id": job_id})
        write_json_output(result)
    except Exception as e:
        result = json_response(success=False, error=str(e))
        write_json_output(result)
        sys.exit(1)


if __name__ == '__main__':
    main()

