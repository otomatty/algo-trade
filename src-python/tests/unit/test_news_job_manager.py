"""
Unit tests for news collection job manager.
"""
import pytest
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from modules.news_collection.job_manager import NewsCollectionJobManager


@pytest.mark.unit
class TestNewsCollectionJobManager:
    """Test cases for NewsCollectionJobManager class."""
    
    @pytest.fixture
    def job_manager(self, temp_db):
        """Create NewsCollectionJobManager instance."""
        conn = sqlite3.connect(temp_db)
        return NewsCollectionJobManager(conn=conn)
    
    def test_create_job_success(self, job_manager, temp_db):
        """Test successful job creation."""
        job_id = job_manager.create_job(
            use_rss=True,
            use_api=False,
            keywords=['stock', 'market'],
            max_articles=50
        )
        
        assert job_id is not None
        assert len(job_id) > 0
        
        # Verify job was created in database
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT job_id, use_rss, use_api, status, max_articles
            FROM news_collection_jobs
            WHERE job_id = ?
        """, (job_id,))
        
        row = cursor.fetchone()
        assert row is not None
        assert row[0] == job_id
        assert row[1] == 1  # use_rss = True
        assert row[2] == 0  # use_api = False
        assert row[3] == 'pending'
        assert row[4] == 50
    
    def test_update_job_status(self, job_manager, temp_db):
        """Test job status update."""
        # Create job first
        job_id = job_manager.create_job(use_rss=True, use_api=False)
        
        # Update status
        job_manager.update_job_status(
            job_id,
            'running',
            0.5,
            'Collecting news...'
        )
        
        # Verify update
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT status, progress, message
            FROM news_collection_jobs
            WHERE job_id = ?
        """, (job_id,))
        
        row = cursor.fetchone()
        assert row[0] == 'running'
        assert row[1] == 0.5
        assert row[2] == 'Collecting news...'
    
    def test_update_job_status_completed(self, job_manager, temp_db):
        """Test job status update with completion."""
        job_id = job_manager.create_job(use_rss=True, use_api=False)
        
        job_manager.update_job_status(
            job_id,
            'completed',
            1.0,
            'Collection completed',
            collected_count=10,
            skipped_count=2,
            completed=True
        )
        
        # Verify completion
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT status, progress, collected_count, skipped_count, completed_at
            FROM news_collection_jobs
            WHERE job_id = ?
        """, (job_id,))
        
        row = cursor.fetchone()
        assert row[0] == 'completed'
        assert row[1] == 1.0
        assert row[2] == 10
        assert row[3] == 2
        assert row[4] is not None
    
    def test_get_job_status(self, job_manager, temp_db):
        """Test getting job status."""
        job_id = job_manager.create_job(use_rss=True, use_api=False)
        
        status = job_manager.get_job_status(job_id)
        
        assert status is not None
        assert status['job_id'] == job_id
        assert status['status'] == 'pending'
        assert status['use_rss'] is True
        assert status['use_api'] is False
    
    def test_get_job_status_not_found(self, job_manager):
        """Test getting status for non-existent job."""
        status = job_manager.get_job_status('non-existent-id')
        
        assert status is None

