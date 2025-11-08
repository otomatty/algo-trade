#!/usr/bin/env python3
"""
Script to get backtest results summary for multiple algorithms.
Called from Rust Tauri command.

This script retrieves the latest backtest result for each specified algorithm.
If algorithm_ids is not provided, it returns the latest result for all algorithms.
"""
import sys
import json
from pathlib import Path
from typing import Optional, List, Dict, Any

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from database.connection import get_connection
from utils.json_io import read_json_input, write_json_output, json_response


def main():
    """Main entry point."""
    try:
        # Read input from stdin
        input_data = read_json_input()
        algorithm_ids = input_data.get('algorithm_ids')  # Optional list of algorithm IDs
        limit = input_data.get('limit', 10)  # Optional limit (default: 10)
        
        conn = get_connection()
        cursor = conn.cursor()
        
        results = []
        
        if algorithm_ids and len(algorithm_ids) > 0:
            # Get latest backtest result for each specified algorithm
            placeholders = ','.join(['?'] * len(algorithm_ids))
            cursor.execute(f"""
                SELECT 
                    br.job_id,
                    br.algorithm_id,
                    a.name as algorithm_name,
                    br.start_date,
                    br.end_date,
                    br.total_return,
                    br.sharpe_ratio,
                    br.max_drawdown,
                    br.win_rate,
                    br.total_trades,
                    br.average_profit,
                    br.average_loss,
                    br.created_at
                FROM backtest_results br
                INNER JOIN algorithms a ON br.algorithm_id = a.id
                WHERE br.algorithm_id IN ({placeholders})
                ORDER BY br.algorithm_id, br.created_at DESC
            """, algorithm_ids)
            
            # Group by algorithm_id and get the latest result for each
            algorithm_results: Dict[int, Optional[tuple]] = {}
            for row in cursor.fetchall():
                algorithm_id = row[1]
                if algorithm_id not in algorithm_results:
                    algorithm_results[algorithm_id] = row
            
            # Convert to list format
            for row in algorithm_results.values():
                if row:
                    (job_id, algorithm_id, algorithm_name, start_date, end_date,
                     total_return, sharpe_ratio, max_drawdown, win_rate,
                     total_trades, average_profit, average_loss, created_at) = row
                    
                    result = {
                        'job_id': job_id,
                        'algorithm_id': algorithm_id,
                        'algorithm_name': algorithm_name,
                        'start_date': start_date,
                        'end_date': end_date,
                        'completed_at': created_at,  # Use created_at as completed_at
                        'performance': {
                            'total_return': total_return,
                            'sharpe_ratio': sharpe_ratio,
                            'max_drawdown': max_drawdown,
                            'win_rate': win_rate,
                            'total_trades': total_trades,
                            'average_profit': average_profit,
                            'average_loss': average_loss
                        }
                    }
                    results.append(result)
        else:
            # Get latest backtest result for all algorithms
            # Use a subquery to get the latest created_at for each algorithm
            cursor.execute("""
                SELECT 
                    br.job_id,
                    br.algorithm_id,
                    a.name as algorithm_name,
                    br.start_date,
                    br.end_date,
                    br.total_return,
                    br.sharpe_ratio,
                    br.max_drawdown,
                    br.win_rate,
                    br.total_trades,
                    br.average_profit,
                    br.average_loss,
                    br.created_at
                FROM backtest_results br
                INNER JOIN algorithms a ON br.algorithm_id = a.id
                INNER JOIN (
                    SELECT algorithm_id, MAX(created_at) as max_created_at
                    FROM backtest_results
                    GROUP BY algorithm_id
                ) latest ON br.algorithm_id = latest.algorithm_id 
                    AND br.created_at = latest.max_created_at
                ORDER BY br.algorithm_id
                LIMIT ?
            """, (limit,))
            
            # Convert to list format
            for row in cursor.fetchall():
                (job_id, algorithm_id, algorithm_name, start_date, end_date,
                 total_return, sharpe_ratio, max_drawdown, win_rate,
                 total_trades, average_profit, average_loss, created_at) = row
                
                result = {
                    'job_id': job_id,
                    'algorithm_id': algorithm_id,
                    'algorithm_name': algorithm_name,
                    'start_date': start_date,
                    'end_date': end_date,
                    'completed_at': created_at,  # Use created_at as completed_at
                    'performance': {
                        'total_return': total_return,
                        'sharpe_ratio': sharpe_ratio,
                        'max_drawdown': max_drawdown,
                        'win_rate': win_rate,
                        'total_trades': total_trades,
                        'average_profit': average_profit,
                        'average_loss': average_loss
                    }
                }
                results.append(result)
        
        result_data = {
            'results': results
        }
        
        result = json_response(success=True, data=result_data)
        write_json_output(result)
    except Exception as e:
        result = json_response(success=False, error=str(e))
        write_json_output(result)
        sys.exit(1)


if __name__ == '__main__':
    main()

