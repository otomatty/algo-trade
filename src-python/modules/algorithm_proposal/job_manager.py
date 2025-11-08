"""
Job manager for proposal generation jobs.

Related Documentation:
  ├─ Plan: docs/03_plans/algorithm-proposal/README.md
  └─ Data Model: docs/03_plans/algorithm-proposal/data-model.md

DEPENDENCY MAP:

Parents (Files that import this file):
  └─ src-python/scripts/generate_algorithm_proposals.py

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


class ProposalJobManager:
    """Manages proposal generation jobs."""
    
    def __init__(self, conn: Optional[sqlite3.Connection] = None):
        """
        Initialize job manager.
        
        Args:
            conn: Database connection (optional, will create new if not provided)
        """
        self.conn = conn
    
    def create_job(
        self,
        data_set_id: int,
        analysis_id: Optional[int],
        num_proposals: int,
        user_preferences: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Create a new proposal generation job.
        
        Args:
            data_set_id: Data set ID
            analysis_id: Analysis result ID (optional)
            num_proposals: Number of proposals to generate
            user_preferences: User preferences dictionary (optional)
            
        Returns:
            Job ID
        """
        if not self.conn:
            self.conn = get_connection()
        
        job_id = str(uuid.uuid4())
        cursor = self.conn.cursor()
        
        user_preferences_json = json.dumps(user_preferences) if user_preferences else None
        
        cursor.execute("""
            INSERT INTO proposal_generation_jobs (
                job_id, data_set_id, analysis_id, num_proposals,
                user_preferences, status, progress, message, created_at
            )
            VALUES (?, ?, ?, ?, ?, 'pending', 0.0, 'Job created', ?)
        """, (
            job_id,
            data_set_id,
            analysis_id,
            num_proposals,
            user_preferences_json,
            datetime.now().isoformat()
        ))
        
        self.conn.commit()
        logger.info(f"Created proposal generation job: {job_id}")
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
        Update job status.
        
        Args:
            job_id: Job ID
            status: Job status ('pending' | 'analyzing' | 'generating' | 'completed' | 'failed')
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
                UPDATE proposal_generation_jobs
                SET status = ?, progress = ?, message = ?, error = ?, completed_at = ?
                WHERE job_id = ?
            """, (status, progress, message, error, datetime.now().isoformat(), job_id))
        else:
            cursor.execute("""
                UPDATE proposal_generation_jobs
                SET status = ?, progress = ?, message = ?, error = ?
                WHERE job_id = ?
            """, (status, progress, message, error, job_id))
        
        self.conn.commit()
        logger.debug(f"Updated job {job_id}: status={status}, progress={progress}")
    
    def save_proposals(
        self,
        job_id: str,
        proposals: List[Dict[str, Any]]
    ):
        """
        Save proposals to database.
        
        Args:
            job_id: Job ID
            proposals: List of proposal dictionaries
        """
        if not self.conn:
            self.conn = get_connection()
        
        cursor = self.conn.cursor()
        
        for proposal in proposals:
            proposal_id = proposal.get('proposal_id', str(uuid.uuid4()))
            name = proposal.get('name', '')
            description = proposal.get('description', '')
            rationale = proposal.get('rationale', '')
            expected_performance = proposal.get('expected_performance')
            definition = proposal.get('definition', {})
            confidence_score = proposal.get('confidence_score')
            
            cursor.execute("""
                INSERT INTO algorithm_proposals (
                    proposal_id, job_id, name, description, rationale,
                    expected_performance, definition, confidence_score, created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                proposal_id,
                job_id,
                name,
                description,
                rationale,
                json.dumps(expected_performance) if expected_performance else None,
                json.dumps(definition),
                confidence_score,
                datetime.now().isoformat()
            ))
        
        self.conn.commit()
        logger.info(f"Saved {len(proposals)} proposals for job {job_id}")

