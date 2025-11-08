"""
Unit tests for proposal job manager.
"""
import pytest
import sqlite3
import json
from pathlib import Path
import sys
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from modules.algorithm_proposal.job_manager import ProposalJobManager


@pytest.mark.unit
class TestProposalJobManager:
    """Test cases for ProposalJobManager class."""
    
    @pytest.fixture
    def job_manager(self, temp_db):
        """Create ProposalJobManager instance."""
        conn = sqlite3.connect(temp_db)
        return ProposalJobManager(conn=conn)
    
    def test_create_job_success(self, job_manager, temp_db):
        """Test successful job creation."""
        job_id = job_manager.create_job(
            data_set_id=1,
            analysis_id=2,
            num_proposals=5,
            user_preferences={'risk_tolerance': 'medium'}
        )
        
        assert job_id is not None
        assert len(job_id) > 0
        
        # Verify job was created in database
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT job_id, data_set_id, analysis_id, num_proposals, status
            FROM proposal_generation_jobs
            WHERE job_id = ?
        """, (job_id,))
        
        row = cursor.fetchone()
        assert row is not None
        assert row[0] == job_id
        assert row[1] == 1
        assert row[2] == 2
        assert row[3] == 5
        assert row[4] == 'pending'
    
    def test_update_job_status(self, job_manager, temp_db):
        """Test job status update."""
        # Create job first
        job_id = job_manager.create_job(
            data_set_id=1,
            analysis_id=None,
            num_proposals=5
        )
        
        # Update status
        job_manager.update_job_status(
            job_id,
            'generating',
            0.5,
            'Generating proposals...'
        )
        
        # Verify update
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT status, progress, message
            FROM proposal_generation_jobs
            WHERE job_id = ?
        """, (job_id,))
        
        row = cursor.fetchone()
        assert row[0] == 'generating'
        assert row[1] == 0.5
        assert row[2] == 'Generating proposals...'
    
    def test_update_job_status_completed(self, job_manager, temp_db):
        """Test job status update with completed flag."""
        job_id = job_manager.create_job(
            data_set_id=1,
            analysis_id=None,
            num_proposals=5
        )
        
        job_manager.update_job_status(
            job_id,
            'completed',
            1.0,
            'Completed',
            completed=True
        )
        
        # Verify completed_at is set
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT status, progress, completed_at
            FROM proposal_generation_jobs
            WHERE job_id = ?
        """, (job_id,))
        
        row = cursor.fetchone()
        assert row[0] == 'completed'
        assert row[1] == 1.0
        assert row[2] is not None
    
    def test_save_proposals(self, job_manager, temp_db):
        """Test saving proposals to database."""
        job_id = job_manager.create_job(
            data_set_id=1,
            analysis_id=None,
            num_proposals=2
        )
        
        proposals = [
            {
                'proposal_id': 'prop-1',
                'name': 'Algorithm 1',
                'description': 'Description 1',
                'rationale': 'Rationale 1',
                'definition': {'triggers': [], 'actions': []},
                'confidence_score': 0.8,
            },
            {
                'proposal_id': 'prop-2',
                'name': 'Algorithm 2',
                'description': 'Description 2',
                'rationale': 'Rationale 2',
                'definition': {'triggers': [], 'actions': []},
                'confidence_score': 0.9,
            },
        ]
        
        job_manager.save_proposals(job_id, proposals)
        
        # Verify proposals were saved
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT proposal_id, name, description, confidence_score
            FROM algorithm_proposals
            WHERE job_id = ?
            ORDER BY confidence_score DESC
        """, (job_id,))
        
        rows = cursor.fetchall()
        assert len(rows) == 2
        assert rows[0][0] == 'prop-2'  # Higher confidence first
        assert rows[0][1] == 'Algorithm 2'
        assert rows[1][0] == 'prop-1'
        assert rows[1][1] == 'Algorithm 1'

