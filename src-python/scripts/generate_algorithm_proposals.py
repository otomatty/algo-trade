#!/usr/bin/env python3
"""
Script to generate algorithm proposals.
Called from Rust Tauri command.
"""
import sys
import json
import threading
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from database.connection import get_connection
from modules.algorithm_proposal.proposal_generator import ProposalGenerator
from modules.algorithm_proposal.job_manager import ProposalJobManager
from modules.llm_integration.exceptions import LLMError, ParseError
from utils.json_io import read_json_input, write_json_output, json_response


def run_proposal_generation_in_background(
    job_id: str,
    data_set_id: int,
    analysis_id: Optional[int],
    num_proposals: int,
    user_preferences: Optional[Dict[str, Any]]
):
    """Run proposal generation in background thread."""
    try:
        conn = get_connection()
        job_manager = ProposalJobManager(conn=conn)
        generator = ProposalGenerator()
        
        # Update status to analyzing
        job_manager.update_job_status(job_id, 'analyzing', 0.1, 'Fetching analysis results...')
        
        # Get analysis results if analysis_id is provided
        analysis_result = None
        if analysis_id:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT analysis_summary, technical_indicators, statistics
                FROM analysis_results
                WHERE id = ?
            """, (analysis_id,))
            
            row = cursor.fetchone()
            if row:
                analysis_summary_json, technical_indicators_json, statistics_json = row
                analysis_result = {
                    'analysis_summary': json.loads(analysis_summary_json),
                    'technical_indicators': json.loads(technical_indicators_json),
                    'statistics': json.loads(statistics_json),
                }
        
        # If no analysis result, try to get latest for data set
        if not analysis_result:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT analysis_summary, technical_indicators, statistics
                FROM analysis_results
                WHERE data_set_id = ?
                ORDER BY created_at DESC
                LIMIT 1
            """, (data_set_id,))
            
            row = cursor.fetchone()
            if row:
                analysis_summary_json, technical_indicators_json, statistics_json = row
                analysis_result = {
                    'analysis_summary': json.loads(analysis_summary_json),
                    'technical_indicators': json.loads(technical_indicators_json),
                    'statistics': json.loads(statistics_json),
                }
        
        if not analysis_result:
            job_manager.update_job_status(
                job_id,
                'failed',
                0.0,
                'No analysis results found for data set',
                error='No analysis results found for data set'
            )
            return
        
        # Update status to generating
        job_manager.update_job_status(job_id, 'generating', 0.3, 'Generating proposals with LLM...')
        
        # Generate proposals
        proposals = generator.generate_proposals(
            analysis_result,
            user_preferences,
            num_proposals
        )
        
        # Update progress
        job_manager.update_job_status(job_id, 'generating', 0.8, 'Saving proposals...')
        
        # Save proposals
        job_manager.save_proposals(job_id, proposals)
        
        # Update status to completed
        job_manager.update_job_status(
            job_id,
            'completed',
            1.0,
            f'Generated {len(proposals)} proposals',
            completed=True
        )
        
    except LLMError as e:
        conn = get_connection()
        job_manager = ProposalJobManager(conn=conn)
        job_manager.update_job_status(
            job_id,
            'failed',
            0.0,
            f'LLM API error: {str(e)}',
            error=str(e),
            completed=True
        )
    except ParseError as e:
        conn = get_connection()
        job_manager = ProposalJobManager(conn=conn)
        job_manager.update_job_status(
            job_id,
            'failed',
            0.0,
            f'Parse error: {str(e)}',
            error=str(e),
            completed=True
        )
    except Exception as e:
        conn = get_connection()
        job_manager = ProposalJobManager(conn=conn)
        job_manager.update_job_status(
            job_id,
            'failed',
            0.0,
            f'Unexpected error: {str(e)}',
            error=str(e),
            completed=True
        )


def main():
    """Main entry point."""
    try:
        # Read input from stdin
        input_data = read_json_input()
        data_set_id = input_data.get('data_set_id')
        analysis_id = input_data.get('analysis_id')
        num_proposals = input_data.get('num_proposals', 5)
        user_preferences = input_data.get('user_preferences')
        
        if not data_set_id:
            result = json_response(success=False, error="data_set_id is required")
            write_json_output(result)
            sys.exit(1)
        
        # Validate data set exists
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id FROM data_sets WHERE id = ?", (data_set_id,))
        if not cursor.fetchone():
            result = json_response(success=False, error=f"Data set with id {data_set_id} not found")
            write_json_output(result)
            sys.exit(1)
        
        # Create job
        job_manager = ProposalJobManager(conn=conn)
        job_id = job_manager.create_job(
            data_set_id,
            analysis_id,
            num_proposals,
            user_preferences
        )
        
        # Start generation in background thread
        thread = threading.Thread(
            target=run_proposal_generation_in_background,
            args=(job_id, data_set_id, analysis_id, num_proposals, user_preferences)
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

