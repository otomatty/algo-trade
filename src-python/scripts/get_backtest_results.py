#!/usr/bin/env python3
"""
Script to get backtest results.
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
        # Read input from stdin
        input_data = read_json_input()
        job_id = input_data.get('job_id')
        
        if not job_id:
            result = json_response(success=False, error="job_id is required")
            write_json_output(result)
            sys.exit(1)
        
        conn = get_connection()
        cursor = conn.cursor()
        
        # Get backtest result
        cursor.execute("""
            SELECT job_id, algorithm_id, start_date, end_date,
                   total_return, sharpe_ratio, max_drawdown, win_rate,
                   total_trades, average_profit, average_loss, created_at
            FROM backtest_results
            WHERE job_id = ?
        """, (job_id,))
        
        result_row = cursor.fetchone()
        
        if not result_row:
            result = json_response(success=False, error=f"Backtest results for job {job_id} not found")
            write_json_output(result)
            sys.exit(1)
        
        (job_id_db, algorithm_id, start_date, end_date,
         total_return, sharpe_ratio, max_drawdown, win_rate,
         total_trades, average_profit, average_loss, created_at) = result_row
        
        # Get trades
        cursor.execute("""
            SELECT entry_date, exit_date, entry_price, exit_price,
                   quantity, profit, profit_rate
            FROM backtest_trades
            WHERE job_id = ?
            ORDER BY entry_date ASC
        """, (job_id,))
        
        trade_rows = cursor.fetchall()
        trades = []
        for trade_row in trade_rows:
            (entry_date, exit_date, entry_price, exit_price,
             quantity, profit, profit_rate) = trade_row
            trades.append({
                'entry_date': entry_date,
                'exit_date': exit_date,
                'entry_price': entry_price,
                'exit_price': exit_price,
                'quantity': quantity,
                'profit': profit,
                'profit_rate': profit_rate
            })
        
        # Get equity curve
        cursor.execute("""
            SELECT date, equity
            FROM backtest_equity_curve
            WHERE job_id = ?
            ORDER BY date ASC
        """, (job_id,))
        
        equity_rows = cursor.fetchall()
        equity_curve = []
        for equity_row in equity_rows:
            date, equity = equity_row
            equity_curve.append({
                'date': date,
                'equity': equity
            })
        
        result_data = {
            'job_id': job_id_db,
            'algorithm_id': algorithm_id,
            'start_date': start_date,
            'end_date': end_date,
            'performance': {
                'total_return': total_return,
                'sharpe_ratio': sharpe_ratio,
                'max_drawdown': max_drawdown,
                'win_rate': win_rate,
                'total_trades': total_trades,
                'average_profit': average_profit,
                'average_loss': average_loss
            },
            'trades': trades,
            'equity_curve': equity_curve
        }
        
        result = json_response(success=True, data=result_data)
        write_json_output(result)
    except Exception as e:
        result = json_response(success=False, error=str(e))
        write_json_output(result)
        sys.exit(1)


if __name__ == '__main__':
    main()

