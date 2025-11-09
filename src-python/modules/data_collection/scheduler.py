"""
Scheduler for data collection jobs using APScheduler.

Related Documentation:
  └─ Plan: docs/03_plans/data-collection/README.md

DEPENDENCY MAP:

Parents (Files that import this file):
  └─ src-python/scripts/configure_data_collection.py

Dependencies (External files that this file imports):
  ├─ apscheduler.schedulers.background.BackgroundScheduler
  ├─ apscheduler.triggers.cron.CronTrigger
  ├─ sqlite3 (standard library)
  ├─ json (standard library)
  ├─ datetime (standard library)
  ├─ typing (standard library)
  ├─ logging (standard library)
  ├─ uuid (standard library)
  ├─ threading (standard library)
  ├─ src-python/database.connection
  ├─ src-python/modules/data_collection.job_manager
  └─ src-python/modules/data_collection.data_collector
"""
import sqlite3
import json
import logging
import uuid
import threading
from datetime import datetime
from typing import Dict, Any, List, Optional

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from database.connection import get_connection
from modules.data_collection.job_manager import DataCollectionJobManager
from modules.data_collection.data_collector import DataCollector


logger = logging.getLogger(__name__)


class DataCollectionScheduler:
    """Manages scheduled data collection jobs."""
    
    _instance: Optional['DataCollectionScheduler'] = None
    _lock = threading.Lock()
    
    def __init__(self, conn: Optional[sqlite3.Connection] = None):
        """
        Initialize scheduler.
        
        Args:
            conn: Database connection (optional, will create new if not provided)
        """
        self.conn = conn if conn else get_connection()
        self.scheduler = BackgroundScheduler()
        self.job_manager = DataCollectionJobManager(self.conn)
        self.data_collector = DataCollector(self.conn)
        self._scheduler_started = False
    
    @classmethod
    def get_instance(cls) -> 'DataCollectionScheduler':
        """Get singleton instance of scheduler."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance
    
    def start(self):
        """Start the scheduler."""
        if not self._scheduler_started:
            self.scheduler.start()
            self._scheduler_started = True
            logger.info("Data collection scheduler started")
            # Load existing schedules
            self._load_schedules()
    
    def stop(self):
        """Stop the scheduler."""
        if self._scheduler_started:
            self.scheduler.shutdown()
            self._scheduler_started = False
            logger.info("Data collection scheduler stopped")
    
    def add_schedule(
        self,
        name: str,
        source: str,
        symbol: str,
        cron_expression: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        api_key: Optional[str] = None,
        data_set_name: Optional[str] = None,
        enabled: bool = True
    ) -> str:
        """
        Add a new schedule.
        
        Args:
            name: Schedule name
            source: Data source ('yahoo' or 'alphavantage')
            symbol: Stock symbol
            cron_expression: Cron expression (e.g., '0 9 * * 1-5' for weekdays at 9 AM)
            start_date: Start date (YYYY-MM-DD, optional)
            end_date: End date (YYYY-MM-DD, optional)
            api_key: API key (required for Alpha Vantage)
            data_set_name: Optional name for the dataset
            enabled: Whether schedule is enabled
            
        Returns:
            Schedule ID
        """
        schedule_id = str(uuid.uuid4())
        cursor = self.conn.cursor()
        
        cursor.execute("""
            INSERT INTO data_collection_schedules (
                schedule_id, name, source, symbol, start_date, end_date,
                cron_expression, enabled, api_key, data_set_name,
                created_at, updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            schedule_id,
            name,
            source,
            symbol,
            start_date,
            end_date,
            cron_expression,
            1 if enabled else 0,
            api_key,
            data_set_name,
            datetime.now().isoformat(),
            datetime.now().isoformat()
        ))
        
        self.conn.commit()
        logger.info(f"Created schedule: {schedule_id} ({name})")
        
        if enabled:
            self._register_schedule(schedule_id)
        
        return schedule_id
    
    def update_schedule(
        self,
        schedule_id: str,
        name: Optional[str] = None,
        cron_expression: Optional[str] = None,
        enabled: Optional[bool] = None,
        **kwargs
    ) -> bool:
        """
        Update a schedule.
        
        Args:
            schedule_id: Schedule ID
            name: New name (optional)
            cron_expression: New cron expression (optional)
            enabled: New enabled status (optional)
            **kwargs: Other fields to update
            
        Returns:
            True if updated, False if not found
        """
        cursor = self.conn.cursor()
        
        # Get current schedule
        cursor.execute("""
            SELECT enabled FROM data_collection_schedules
            WHERE schedule_id = ?
        """, (schedule_id,))
        row = cursor.fetchone()
        if not row:
            return False
        
        was_enabled = bool(row[0])
        
        # Build update query
        update_fields = []
        update_values = []
        
        if name is not None:
            update_fields.append("name = ?")
            update_values.append(name)
        
        if cron_expression is not None:
            update_fields.append("cron_expression = ?")
            update_values.append(cron_expression)
        
        if enabled is not None:
            update_fields.append("enabled = ?")
            update_values.append(1 if enabled else 0)
        
        for key, value in kwargs.items():
            if value is not None:
                update_fields.append(f"{key} = ?")
                update_values.append(value)
        
        update_fields.append("updated_at = ?")
        update_values.append(datetime.now().isoformat())
        update_values.append(schedule_id)
        
        query = f"""
            UPDATE data_collection_schedules
            SET {', '.join(update_fields)}
            WHERE schedule_id = ?
        """
        
        cursor.execute(query, update_values)
        self.conn.commit()
        
        # Update scheduler job if needed
        if was_enabled:
            self.scheduler.remove_job(schedule_id)
        
        if enabled is not None and enabled:
            self._register_schedule(schedule_id)
        elif enabled is not None and not enabled:
            self.scheduler.remove_job(schedule_id)
        elif cron_expression is not None and was_enabled:
            self._register_schedule(schedule_id)
        
        logger.info(f"Updated schedule: {schedule_id}")
        return True
    
    def delete_schedule(self, schedule_id: str) -> bool:
        """
        Delete a schedule.
        
        Args:
            schedule_id: Schedule ID
            
        Returns:
            True if deleted, False if not found
        """
        cursor = self.conn.cursor()
        
        # Check if exists
        cursor.execute("""
            SELECT schedule_id FROM data_collection_schedules
            WHERE schedule_id = ?
        """, (schedule_id,))
        if not cursor.fetchone():
            return False
        
        # Remove from scheduler
        try:
            self.scheduler.remove_job(schedule_id)
        except Exception as e:
            logger.warning(f"Failed to remove job from scheduler: {e}")
        
        # Delete from database
        cursor.execute("""
            DELETE FROM data_collection_schedules
            WHERE schedule_id = ?
        """, (schedule_id,))
        self.conn.commit()
        
        logger.info(f"Deleted schedule: {schedule_id}")
        return True
    
    def get_schedule(self, schedule_id: str) -> Optional[Dict[str, Any]]:
        """
        Get schedule information.
        
        Args:
            schedule_id: Schedule ID
            
        Returns:
            Dict with schedule information or None if not found
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT schedule_id, name, source, symbol, start_date, end_date,
                   cron_expression, enabled, api_key, data_set_name,
                   created_at, updated_at
            FROM data_collection_schedules
            WHERE schedule_id = ?
        """, (schedule_id,))
        
        row = cursor.fetchone()
        if not row:
            return None
        
        return {
            'schedule_id': row[0],
            'name': row[1],
            'source': row[2],
            'symbol': row[3],
            'start_date': row[4],
            'end_date': row[5],
            'cron_expression': row[6],
            'enabled': bool(row[7]),
            'api_key': row[8],
            'data_set_name': row[9],
            'created_at': row[10],
            'updated_at': row[11]
        }
    
    def get_all_schedules(self, enabled_only: bool = False) -> List[Dict[str, Any]]:
        """
        Get all schedules.
        
        Args:
            enabled_only: If True, only return enabled schedules
            
        Returns:
            List of schedule dictionaries
        """
        cursor = self.conn.cursor()
        
        if enabled_only:
            cursor.execute("""
                SELECT schedule_id, name, source, symbol, start_date, end_date,
                       cron_expression, enabled, api_key, data_set_name,
                       created_at, updated_at
                FROM data_collection_schedules
                WHERE enabled = 1
                ORDER BY created_at DESC
            """)
        else:
            cursor.execute("""
                SELECT schedule_id, name, source, symbol, start_date, end_date,
                       cron_expression, enabled, api_key, data_set_name,
                       created_at, updated_at
                FROM data_collection_schedules
                ORDER BY created_at DESC
            """)
        
        rows = cursor.fetchall()
        return [
            {
                'schedule_id': row[0],
                'name': row[1],
                'source': row[2],
                'symbol': row[3],
                'start_date': row[4],
                'end_date': row[5],
                'cron_expression': row[6],
                'enabled': bool(row[7]),
                'api_key': row[8],
                'data_set_name': row[9],
                'created_at': row[10],
                'updated_at': row[11]
            }
            for row in rows
        ]
    
    def _load_schedules(self):
        """Load all enabled schedules into scheduler."""
        schedules = self.get_all_schedules(enabled_only=True)
        for schedule in schedules:
            self._register_schedule(schedule['schedule_id'])
        logger.info(f"Loaded {len(schedules)} schedules into scheduler")
    
    def _register_schedule(self, schedule_id: str):
        """Register a schedule with the scheduler."""
        schedule = self.get_schedule(schedule_id)
        if not schedule or not schedule['enabled']:
            return
        
        # Parse cron expression
        cron_parts = schedule['cron_expression'].split()
        if len(cron_parts) != 5:
            logger.error(f"Invalid cron expression: {schedule['cron_expression']}")
            return
        
        try:
            trigger = CronTrigger(
                minute=cron_parts[0],
                hour=cron_parts[1],
                day=cron_parts[2],
                month=cron_parts[3],
                day_of_week=cron_parts[4]
            )
            
            self.scheduler.add_job(
                self._execute_collection,
                trigger=trigger,
                id=schedule_id,
                args=[schedule_id],
                replace_existing=True
            )
            logger.info(f"Registered schedule: {schedule_id}")
        except Exception as e:
            logger.error(f"Failed to register schedule {schedule_id}: {e}")
    
    def _execute_collection(self, schedule_id: str):
        """Execute data collection for a schedule."""
        schedule = self.get_schedule(schedule_id)
        if not schedule or not schedule['enabled']:
            return
        
        logger.info(f"Executing scheduled collection: {schedule_id}")
        
        # Create job
        job_id = self.job_manager.create_job(
            source=schedule['source'],
            symbol=schedule['symbol'],
            start_date=schedule['start_date'] or self._get_default_start_date(),
            end_date=schedule['end_date'] or datetime.now().strftime('%Y-%m-%d'),
            name=schedule['data_set_name'],
            api_key=schedule['api_key'],
            schedule_id=schedule_id
        )
        
        # Update job status
        self.job_manager.update_job_status(
            job_id=job_id,
            status='running',
            progress=0.1,
            message='Starting data collection...'
        )
        
        try:
            # Execute collection
            result = self.data_collector.collect_from_api(
                source=schedule['source'],
                symbol=schedule['symbol'],
                start_date=schedule['start_date'] or self._get_default_start_date(),
                end_date=schedule['end_date'] or datetime.now().strftime('%Y-%m-%d'),
                name=schedule['data_set_name'],
                api_key=schedule['api_key']
            )
            
            if result.get('success'):
                data_set_id = result.get('data', {}).get('data_set_id')
                self.job_manager.update_job_status(
                    job_id=job_id,
                    status='completed',
                    progress=1.0,
                    message='Data collection completed',
                    data_set_id=data_set_id,
                    completed=True
                )
                logger.info(f"Completed scheduled collection: {schedule_id}, job: {job_id}")
            else:
                error_msg = result.get('error', 'Unknown error')
                self.job_manager.update_job_status(
                    job_id=job_id,
                    status='failed',
                    progress=0.0,
                    message='Data collection failed',
                    error=error_msg,
                    completed=True
                )
                logger.error(f"Failed scheduled collection: {schedule_id}, error: {error_msg}")
        except Exception as e:
            error_msg = str(e)
            self.job_manager.update_job_status(
                job_id=job_id,
                status='failed',
                progress=0.0,
                message='Data collection failed',
                error=error_msg,
                completed=True
            )
            logger.error(f"Exception in scheduled collection: {schedule_id}, error: {error_msg}", exc_info=True)
    
    def _get_default_start_date(self) -> str:
        """Get default start date (30 days ago)."""
        from datetime import timedelta
        return (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')

