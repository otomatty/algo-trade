#!/usr/bin/env python3
"""
Script to collect market news from RSS feeds and/or NewsAPI.
Called from Rust Tauri command.
"""
import sys
import json
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.news_collection.news_collector import NewsCollector
from modules.news_collection.job_manager import NewsCollectionJobManager
from utils.json_io import read_json_input, write_json_output, json_response

logger = logging.getLogger(__name__)


def main():
    """Main entry point."""
    try:
        # Read input from stdin
        input_data = read_json_input()
        logger.info(f"Received input: {json.dumps(input_data, indent=2)}")
        
        use_rss = input_data.get('use_rss', True)
        use_api = input_data.get('use_api', False)
        api_key = input_data.get('api_key')
        keywords = input_data.get('keywords')  # List of strings
        max_articles = input_data.get('max_articles', 50)
        
        logger.info(f"Configuration: use_rss={use_rss}, use_api={use_api}, has_api_key={bool(api_key)}")
        
        # Validate API key if using API
        if use_api and not api_key:
            # Check environment variable
            import os
            api_key = os.getenv('NEWSAPI_KEY')
            if not api_key:
                error_msg = "API key is required when use_api is True. Set NEWSAPI_KEY environment variable or pass api_key parameter."
                logger.error(error_msg)
                result = json_response(success=False, error=error_msg)
                write_json_output(result)
                sys.exit(1)
        
        # Create job
        job_manager = NewsCollectionJobManager()
        job_id = job_manager.create_job(
            use_rss=use_rss,
            use_api=use_api,
            api_key=api_key,
            keywords=keywords,
            max_articles=max_articles
        )
        logger.info(f"Created job: {job_id}")
        
        # Update job status to running
        job_manager.update_job_status(
            job_id=job_id,
            status='running',
            progress=0.1,
            message='Starting news collection...'
        )
        
        # Collect news
        collector = NewsCollector()
        result = collector.collect_news(
            use_rss=use_rss,
            use_api=use_api,
            api_key=api_key,
            keywords=keywords,
            max_articles=max_articles
        )
        
        logger.info(f"Collection result: success={result.get('success')}, error={result.get('error')}")
        
        if result.get('success'):
            # Update job status to completed
            data = result.get('data', {})
            job_manager.update_job_status(
                job_id=job_id,
                status='completed',
                progress=1.0,
                message='News collection completed',
                collected_count=data.get('collected_count', 0),
                skipped_count=data.get('skipped_count', 0),
                completed=True
            )
            
            logger.info(f"Job completed: collected={data.get('collected_count')}, skipped={data.get('skipped_count')}")
            
            # Return result with job_id
            result['data']['job_id'] = job_id
            write_json_output(result)
        else:
            # Update job status to failed
            error_message = result.get('error', 'Unknown error')
            logger.error(f"Job failed: {error_message}")
            job_manager.update_job_status(
                job_id=job_id,
                status='failed',
                progress=0.0,
                message='News collection failed',
                error=error_message,
                completed=True
            )
            
            result['data'] = {'job_id': job_id}
            write_json_output(result)
            sys.exit(1)
            
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        logger.error(error_msg, exc_info=True)
        result = json_response(success=False, error=error_msg)
        write_json_output(result)
        sys.exit(1)


if __name__ == '__main__':
    main()

