"""
Job manager for news collection jobs.

Related Documentation:
  └─ Plan: docs/03_plans/news-collection/README.md

DEPENDENCY MAP:

Parents (Files that import this file):
  └─ src-python/scripts/collect_market_news.py

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
from typing import Dict, Any, List, Optional

from database.connection import get_connection


logger = logging.getLogger(__name__)


class NewsCollectionJobManager:
    """Manages news collection jobs."""
    
    def __init__(self, conn: Optional[sqlite3.Connection] = None):
        """
        Initialize job manager.
        
        Args:
            conn: Database connection (optional, will create new if not provided)
        """
        self.conn = conn
    
    def create_job(
        self,
        use_rss: bool = True,
        use_api: bool = False,
        api_key: Optional[str] = None,
        keywords: Optional[List[str]] = None,
        max_articles: int = 50
    ) -> str:
        """
        Create a new news collection job.
        
        Args:
            use_rss: Whether to collect from RSS feeds (default: True)
            use_api: Whether to collect from NewsAPI (default: False)
            api_key: NewsAPI key (required if use_api=True)
            keywords: Keywords for NewsAPI search (optional)
            max_articles: Maximum articles from NewsAPI (default: 50)
            
        Returns:
            Job ID
        """
        if not self.conn:
            self.conn = get_connection()
        
        job_id = str(uuid.uuid4())
        cursor = self.conn.cursor()
        
        keywords_json = json.dumps(keywords) if keywords else None
        
        cursor.execute("""
            INSERT INTO news_collection_jobs (
                job_id, use_rss, use_api, api_key, keywords, max_articles,
                status, progress, message, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, 'pending', 0.0, 'Job created', ?)
        """, (
            job_id,
            1 if use_rss else 0,
            1 if use_api else 0,
            api_key,
            keywords_json,
            max_articles,
            datetime.now().isoformat()
        ))
        
        self.conn.commit()
        logger.info(f"Created news collection job: {job_id}")
        return job_id
    
    def update_job_status(
        self,
        job_id: str,
        status: str,
        progress: float,
        message: str,
        error: Optional[str] = None,
        collected_count: Optional[int] = None,
        skipped_count: Optional[int] = None,
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
            collected_count: Number of news items collected (optional)
            skipped_count: Number of news items skipped (optional)
            completed: Whether job is completed
        """
        if not self.conn:
            self.conn = get_connection()
        
        cursor = self.conn.cursor()
        
        update_fields = ["status = ?", "progress = ?", "message = ?", "error = ?"]
        update_values = [status, progress, message, error]
        
        if collected_count is not None:
            update_fields.append("collected_count = ?")
            update_values.append(collected_count)
        
        if skipped_count is not None:
            update_fields.append("skipped_count = ?")
            update_values.append(skipped_count)
        
        if completed:
            update_fields.append("completed_at = ?")
            update_values.append(datetime.now().isoformat())
        
        update_values.append(job_id)
        
        query = f"""
            UPDATE news_collection_jobs
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
            SELECT job_id, use_rss, use_api, status, progress, message, error,
                   collected_count, skipped_count, created_at, completed_at
            FROM news_collection_jobs
            WHERE job_id = ?
        """, (job_id,))
        
        row = cursor.fetchone()
        if not row:
            return None
        
        return {
            'job_id': row[0],
            'use_rss': bool(row[1]),
            'use_api': bool(row[2]),
            'status': row[3],
            'progress': row[4],
            'message': row[5],
            'error': row[6],
            'collected_count': row[7],
            'skipped_count': row[8],
            'created_at': row[9],
            'completed_at': row[10]
        }

