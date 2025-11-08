"""
Job manager for backtest jobs.

Related Documentation:
  └─ Plan: docs/03_plans/backtest/README.md

DEPENDENCY MAP:

Parents (Files that import this file):
  └─ src-python/scripts/run_backtest.py

Dependencies (External files that this file imports):
  ├─ sqlite3 (standard library)
  ├─ json (standard library)
  ├─ datetime (standard library)
  ├─ typing (standard library)
  ├─ logging (standard library)
  └─ src-python/database.connection
"""
import sqlite3
import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional, List

from database.connection import get_connection


logger = logging.getLogger(__name__)


class BacktestJobManager:
    """Manages backtest jobs."""
    
    def __init__(self, conn: Optional[sqlite3.Connection] = None):
        """
        Initialize job manager.
        
        Args:
            conn: Database connection (optional, will create new if not provided)
        """
        self.conn = conn
    
    def create_job(
        self,
        algorithm_id: int,
        start_date: str,
        end_date: str,
        data_set_id: Optional[int] = None
    ) -> str:
        """
        Create a new backtest job.
        
        Args:
            algorithm_id: Algorithm ID
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            data_set_id: Data set ID (optional)
            
        Returns:
            Job ID
        """
        if not self.conn:
            self.conn = get_connection()
        
        import uuid
        job_id = str(uuid.uuid4())
        cursor = self.conn.cursor()
        
        cursor.execute("""
            INSERT INTO backtest_jobs (
                job_id, algorithm_id, start_date, end_date, data_set_id,
                status, progress, message, created_at
            )
            VALUES (?, ?, ?, ?, ?, 'pending', 0.0, 'Job created', ?)
        """, (
            job_id,
            algorithm_id,
            start_date,
            end_date,
            data_set_id,
            datetime.now().isoformat()
        ))
        
        self.conn.commit()
        logger.info(f"Created backtest job: {job_id}")
        return job_id
    
    def update_job_status(
        self,
        job_id: str,
        status: str,
        progress: float,
        message: str,
        error: Optional[str] = None,
        completed: bool = False
    ):
        """
        Update backtest job status.
        
        Args:
            job_id: Job ID
            status: Job status ('pending', 'running', 'completed', 'failed')
            progress: Progress (0.0 to 1.0)
            message: Status message
            error: Error message (optional)
            completed: Whether job is completed
        """
        if not self.conn:
            self.conn = get_connection()
        
        cursor = self.conn.cursor()
        
        if completed:
            cursor.execute("""
                UPDATE backtest_jobs
                SET status = ?, progress = ?, message = ?, error = ?, completed_at = ?
                WHERE job_id = ?
            """, (status, progress, message, error, datetime.now().isoformat(), job_id))
        else:
            cursor.execute("""
                UPDATE backtest_jobs
                SET status = ?, progress = ?, message = ?, error = ?
                WHERE job_id = ?
            """, (status, progress, message, error, job_id))
        
        self.conn.commit()
        logger.debug(f"Updated backtest job {job_id}: {status} ({progress:.1%})")
    
    def save_results(
        self,
        job_id: str,
        algorithm_id: int,
        start_date: str,
        end_date: str,
        performance: Dict[str, Any],
        trades: List[Dict[str, Any]],
        equity_curve: List[Dict[str, Any]]
    ):
        """
        Save backtest results to database.
        
        Args:
            job_id: Job ID
            algorithm_id: Algorithm ID
            start_date: Start date
            end_date: End date
            performance: Performance metrics
            trades: List of trades
            equity_curve: Equity curve data
        """
        if not self.conn:
            self.conn = get_connection()
        
        cursor = self.conn.cursor()
        
        # Save performance metrics to backtest_results
        cursor.execute("""
            INSERT INTO backtest_results (
                job_id, algorithm_id, start_date, end_date,
                total_return, sharpe_ratio, max_drawdown, win_rate,
                total_trades, average_profit, average_loss, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            job_id,
            algorithm_id,
            start_date,
            end_date,
            performance.get('total_return', 0.0),
            performance.get('sharpe_ratio', 0.0),
            performance.get('max_drawdown', 0.0),
            performance.get('win_rate', 0.0),
            performance.get('total_trades', 0),
            performance.get('average_profit', 0.0),
            performance.get('average_loss', 0.0),
            datetime.now().isoformat()
        ))
        
        # Save trades
        for trade in trades:
            cursor.execute("""
                INSERT INTO backtest_trades (
                    job_id, entry_date, exit_date, entry_price, exit_price,
                    quantity, profit, profit_rate
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                job_id,
                trade['entry_date'],
                trade['exit_date'],
                trade['entry_price'],
                trade['exit_price'],
                trade['quantity'],
                trade['profit'],
                trade['profit_rate']
            ))
        
        # Save equity curve
        for point in equity_curve:
            cursor.execute("""
                INSERT INTO backtest_equity_curve (
                    job_id, date, equity
                )
                VALUES (?, ?, ?)
            """, (
                job_id,
                point['date'],
                point['equity']
            ))
        
        self.conn.commit()
        logger.info(f"Saved backtest results for job {job_id}")

