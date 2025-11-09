#!/usr/bin/env python3
"""
Script to get collected news from database.
Called from Rust Tauri command.
"""
import sys
import json
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.news_collection.news_collector import NewsCollector
from utils.json_io import read_json_input, write_json_output, json_response


def main():
    """Main entry point."""
    try:
        # Read input from stdin
        input_data = read_json_input()
        
        limit = input_data.get('limit', 100)
        offset = input_data.get('offset', 0)
        source = input_data.get('source')  # Optional
        order_by = input_data.get('order_by', 'published_at')
        order_desc = input_data.get('order_desc', True)
        
        collector = NewsCollector()
        news_list = collector.get_collected_news(
            limit=limit,
            offset=offset,
            source=source,
            order_by=order_by,
            order_desc=order_desc
        )
        
        result = json_response(success=True, data=news_list)
        write_json_output(result)
    except Exception as e:
        result = json_response(success=False, error=str(e))
        write_json_output(result)
        sys.exit(1)


if __name__ == '__main__':
    main()

