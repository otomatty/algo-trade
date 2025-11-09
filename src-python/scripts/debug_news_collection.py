#!/usr/bin/env python3
"""
Debug script to test news collection functionality.
Run this script directly to test news collection without Tauri.
"""
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Configure logging
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

from modules.news_collection.news_collector import NewsCollector
from modules.news_collection.rss_parser import RSSFeedParser
from modules.news_collection.news_api_client import NewsAPIClient

logger = logging.getLogger(__name__)


def test_rss_parser():
    """Test RSS parser."""
    print("\n=== Testing RSS Parser ===")
    try:
        parser = RSSFeedParser()
        news = parser.parse_feeds()
        print(f"✓ RSS Parser: Collected {len(news)} items")
        if news:
            print(f"  Sample: {news[0]['title'][:50]}...")
        return True
    except Exception as e:
        print(f"✗ RSS Parser failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_news_api_client():
    """Test NewsAPI client."""
    print("\n=== Testing NewsAPI Client ===")
    api_key = os.getenv('NEWSAPI_KEY')
    if not api_key:
        print("✗ NEWSAPI_KEY environment variable not set")
        return False
    
    try:
        client = NewsAPIClient(api_key=api_key)
        news = client.fetch_news(max_articles=5)
        print(f"✓ NewsAPI Client: Collected {len(news)} items")
        if news:
            print(f"  Sample: {news[0]['title'][:50]}...")
        return True
    except Exception as e:
        print(f"✗ NewsAPI Client failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_news_collector():
    """Test news collector."""
    print("\n=== Testing News Collector (RSS only) ===")
    try:
        collector = NewsCollector()
        result = collector.collect_news(use_rss=True, use_api=False)
        
        if result.get('success'):
            data = result.get('data', {})
            print(f"✓ News Collector: Collected {data.get('collected_count')} items, skipped {data.get('skipped_count')}")
            return True
        else:
            print(f"✗ News Collector failed: {result.get('error')}")
            return False
    except Exception as e:
        print(f"✗ News Collector failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("News Collection Debug Script")
    print("=" * 50)
    
    # Check environment variables
    print("\n=== Environment Variables ===")
    newsapi_key = os.getenv('NEWSAPI_KEY')
    print(f"NEWSAPI_KEY: {'✓ Set' if newsapi_key else '✗ Not set'}")
    if newsapi_key:
        print(f"  Value: {newsapi_key[:10]}...{newsapi_key[-5:]}")
    
    # Test RSS parser
    rss_ok = test_rss_parser()
    
    # Test NewsAPI client (if key is set)
    api_ok = True
    if newsapi_key:
        api_ok = test_news_api_client()
    else:
        print("\n=== Skipping NewsAPI Test (no API key) ===")
    
    # Test news collector
    collector_ok = test_news_collector()
    
    # Summary
    print("\n" + "=" * 50)
    print("Summary:")
    print(f"  RSS Parser: {'✓' if rss_ok else '✗'}")
    print(f"  NewsAPI Client: {'✓' if api_ok else '✗'}")
    print(f"  News Collector: {'✓' if collector_ok else '✗'}")
    
    if rss_ok and collector_ok:
        print("\n✓ Basic functionality is working!")
    else:
        print("\n✗ Some tests failed. Check the error messages above.")


if __name__ == '__main__':
    main()

