#!/usr/bin/env python3
"""
Script to generate stock predictions.
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
from modules.stock_prediction.prediction_generator import PredictionGenerator
from modules.stock_prediction.job_manager import StockPredictionJobManager
from modules.news_collection.news_collector import NewsCollector
from modules.llm_integration.exceptions import LLMError, ParseError
from utils.json_io import read_json_input, write_json_output, json_response


def run_prediction_generation_in_background(
    job_id: str,
    news_job_id: Optional[str],
    num_predictions: int,
    user_preferences: Optional[Dict[str, Any]],
    market_trends: Optional[str]
):
    """Run prediction generation in background thread."""
    try:
        conn = get_connection()
        job_manager = StockPredictionJobManager(conn=conn)
        generator = PredictionGenerator()
        news_collector = NewsCollector(conn=conn)
        
        # Update status to analyzing
        job_manager.update_job_status(job_id, 'analyzing', 0.1, 'Fetching news...')
        
        # Get news from news_job_id if provided
        news_list = []
        if news_job_id:
            # Get news collected by this job
            # Note: We'll get all recent news since we don't have a direct link
            # In a real implementation, we might want to add a news_job_id column to market_news table
            # For now, we'll get recent news from the database
            news_list = news_collector.get_collected_news(
                limit=50,
                offset=0,
                order_by='published_at',
                order_desc=True
            )
        
        # If no news_job_id, get recent news
        if not news_list:
            news_list = news_collector.get_collected_news(
                limit=50,
                offset=0,
                order_by='published_at',
                order_desc=True
            )
        
        if not news_list:
            job_manager.update_job_status(
                job_id,
                'failed',
                0.0,
                'No news found. Please collect news first.',
                error='No news found. Please collect news first.',
                completed=True
            )
            return
        
        # Update status to generating
        job_manager.update_job_status(job_id, 'generating', 0.3, f'Generating predictions from {len(news_list)} news articles...')
        
        # Generate predictions
        predictions = generator.generate_predictions(
            news_list,
            market_trends,
            user_preferences,
            num_predictions
        )
        
        # Update progress
        job_manager.update_job_status(job_id, 'generating', 0.8, 'Saving predictions...')
        
        # Save predictions
        job_manager.save_predictions(job_id, predictions)
        
        # Update status to completed
        job_manager.update_job_status(
            job_id,
            'completed',
            1.0,
            f'Generated {len(predictions)} predictions',
            completed=True
        )
        
    except LLMError as e:
        conn = get_connection()
        job_manager = StockPredictionJobManager(conn=conn)
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
        job_manager = StockPredictionJobManager(conn=conn)
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
        job_manager = StockPredictionJobManager(conn=conn)
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
        news_job_id = input_data.get('news_job_id')
        num_predictions = input_data.get('num_predictions', 5)
        user_preferences = input_data.get('user_preferences')
        market_trends = input_data.get('market_trends')
        
        # Create job
        conn = get_connection()
        job_manager = StockPredictionJobManager(conn=conn)
        job_id = job_manager.create_job(
            news_job_id,
            num_predictions,
            user_preferences,
            market_trends
        )
        
        # Start generation in background thread
        thread = threading.Thread(
            target=run_prediction_generation_in_background,
            args=(job_id, news_job_id, num_predictions, user_preferences, market_trends)
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

