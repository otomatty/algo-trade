"""
Job manager for data collection jobs.

Related Documentation:
  └─ Plan: docs/03_plans/data-collection/README.md

DEPENDENCY MAP:

Parents (Files that import this file):
  ├─ src-python/modules/data_collection/scheduler.py
  └─ src-python/scripts/configure_data_collection.py

Dependencies (External files that this file imports):
  ├─ sqlite3 (standard library)
  ├─ json (standard library)
  ├─ datetime (standard library)
  ├─ typing (standard library)
  ├─ logging (standard library)
  ├─ uuid (standard library)
  └─ src-python/database.connection
"""
import sqlite3
import json
import logging
import uuid
from datetime import datetime
from typing import Dict, Any, Optional

from database.connection import get_connection


logger = logging.getLogger(__name__)


class DataCollectionJobManager:
    """Manages data collection jobs."""
    
    def __init__(self, conn: Optional[sqlite3.Connection] = None):
        """
        Initialize job manager.
        
        Args:
            conn: Database connection (optional, will create new if not provided)
        """
        self.conn = conn
    
    def create_job(
        self,
        schedule_id: Optional[str],
        source: str,
        symbol: str,
        start_date: str,
        end_date: str,
        name: Optional[str] = None,
        api_key: Optional[str] = None
    ) -> str:
        """
        Create a new data collection job.
        
        Args:
            schedule_id: Schedule ID (optional, None for manual jobs)
            source: Data source ('yahoo' or 'alphavantage')
            symbol: Stock symbol
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            name: Optional name for the dataset
            api_key: API key (required for Alpha Vantage)
            
        Returns:
            Job ID
        """
        if not self.conn:
            self.conn = get_connection()
        
        job_id = str(uuid.uuid4())
        cursor = self.conn.cursor()
        
        cursor.execute("""
            INSERT INTO data_collection_jobs (
                job_id, schedule_id, source, symbol, start_date, end_date,
                name, api_key, status, progress, message, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'pending', 0.0, 'Job created', ?)
        """, (
            job_id,
            schedule_id,
            source,
            symbol,
            start_date,
            end_date,
            name,
            api_key,
            datetime.now().isoformat()
        ))
        
        self.conn.commit()
        logger.info(f"Created data collection job: {job_id}")
        return job_id
    
    def update_job_status(
        self,
        job_id: str,
        status: str,
        progress: float,
        message: str,
        error: Optional[str] = None,
        data_set_id: Optional[int] = None,
        completed: bool = False
    ):
        """
        Update job status.
        
        Args:
            job_id: Job ID
            status: Job status ('pending' | 'running' | 'completed' | 'failed')
            progress: Progress (0.0 to 1.0)
            message: Status message
            error: Error message (optional)
            data_set_id: Created data set ID (optional)
            completed: Whether job is completed
        """
        if not self.conn:
            self.conn = get_connection()
        
        cursor = self.conn.cursor()
        
        update_fields = ["status = ?", "progress = ?", "message = ?", "error = ?"]
        update_values = [status, progress, message, error]
        
        if data_set_id is not None:
            update_fields.append("data_set_id = ?")
            update_values.append(data_set_id)
        
        if completed:
            update_fields.append("completed_at = ?")
            update_values.append(datetime.now().isoformat())
        
        update_values.append(job_id)
        
        query = f"""
            UPDATE data_collection_jobs
            SET {', '.join(update_fields)}
            WHERE job_id = ?
        """
        
        cursor.execute(query, update_values)
        self.conn.commit()
        logger.debug(f"Updated job {job_id}: status={status}, progress={progress}")
    
    def get_job_status(self, job_id: str) -> Optional[Dict[str, Any]]:
        """
        Get job status.
        
        Args:
            job_id: Job ID
            
        Returns:
            Dict with job status information or None if not found
        """
        if not self.conn:
            self.conn = get_connection()
        
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT job_id, schedule_id, source, symbol, start_date, end_date,
                   name, api_key, status, progress, message, error,
                   data_set_id, created_at, completed_at
            FROM data_collection_jobs
            WHERE job_id = ?
        """, (job_id,))
        
        row = cursor.fetchone()
        if not row:
            return None
        
        return {
            'job_id': row[0],
            'schedule_id': row[1],
            'source': row[2],
            'symbol': row[3],
            'start_date': row[4],
            'end_date': row[5],
            'name': row[6],
            'api_key': row[7],
            'status': row[8],
            'progress': row[9],
            'message': row[10],
            'error': row[11],
            'data_set_id': row[12],
            'created_at': row[13],
            'completed_at': row[14]
        }
    
    def get_jobs_by_schedule(self, schedule_id: str) -> list[Dict[str, Any]]:
        """
        Get all jobs for a schedule.
        
        Args:
            schedule_id: Schedule ID
            
        Returns:
            List of job dictionaries
        """
        if not self.conn:
            self.conn = get_connection()
        
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT job_id, schedule_id, source, symbol, start_date, end_date,
                   name, api_key, status, progress, message, error,
                   data_set_id, created_at, completed_at
            FROM data_collection_jobs
            WHERE schedule_id = ?
            ORDER BY created_at DESC
        """, (schedule_id,))
        
        rows = cursor.fetchall()
        return [
            {
                'job_id': row[0],
                'schedule_id': row[1],
                'source': row[2],
                'symbol': row[3],
                'start_date': row[4],
                'end_date': row[5],
                'name': row[6],
                'api_key': row[7],
                'status': row[8],
                'progress': row[9],
                'message': row[10],
                'error': row[11],
                'data_set_id': row[12],
                'created_at': row[13],
                'completed_at': row[14]
            }
            for row in rows
        ]
