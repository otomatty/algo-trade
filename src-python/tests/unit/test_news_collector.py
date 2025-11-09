"""
Unit tests for news collector.
"""
import pytest
import sqlite3
import sys
from pathlib import Path
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from modules.news_collection.news_collector import NewsCollector
from modules.news_collection.exceptions import NewsCollectionError


@pytest.mark.unit
class TestNewsCollector:
    """Test cases for NewsCollector class."""
    
    @pytest.fixture
    def collector(self, temp_db):
        """Create NewsCollector instance."""
        conn = sqlite3.connect(temp_db)
        return NewsCollector(conn=conn)
    
    def test_collect_news_rss_only(self, collector, mocker):
        """Test news collection from RSS only."""
        # Mock RSS parser
        mock_rss_news = [
            {
                'title': 'RSS News',
                'content': 'RSS content',
                'source': 'yahoo',
                'url': 'https://example.com/rss/1',
                'published_at': '2024-01-01T12:00:00'
            }
        ]
        
        mocker.patch.object(collector.rss_parser, 'parse_feeds', return_value=mock_rss_news)
        
        result = collector.collect_news(use_rss=True, use_api=False)
        
        assert result['success'] is True
        assert result['data']['collected_count'] == 1
        assert result['data']['skipped_count'] == 0
    
    def test_collect_news_api_only(self, collector, mocker):
        """Test news collection from API only."""
        # Mock API client
        mock_api_news = [
            {
                'title': 'API News',
                'content': 'API content',
                'source': 'newsapi',
                'url': 'https://example.com/api/1',
                'published_at': '2024-01-01T12:00:00'
            }
        ]
        
        mock_api_client = Mock()
        mock_api_client.fetch_news.return_value = mock_api_news
        
        collector.api_client = mock_api_client
        
        result = collector.collect_news(use_rss=False, use_api=True, api_key='test_key')
        
        assert result['success'] is True
        assert result['data']['collected_count'] == 1
    
    def test_collect_news_duplicate_prevention(self, collector, mocker):
        """Test duplicate news prevention."""
        mock_news = [
            {
                'title': 'Duplicate News',
                'content': 'Content',
                'source': 'yahoo',
                'url': 'https://example.com/news/1',
                'published_at': '2024-01-01T12:00:00'
            }
        ]
        
        mocker.patch.object(collector.rss_parser, 'parse_feeds', return_value=mock_news)
        
        # First collection
        result1 = collector.collect_news(use_rss=True, use_api=False)
        assert result1['success'] is True
        assert result1['data']['collected_count'] == 1
        
        # Second collection (should skip duplicate)
        result2 = collector.collect_news(use_rss=True, use_api=False)
        assert result2['success'] is True
        assert result2['data']['collected_count'] == 0
        assert result2['data']['skipped_count'] == 1
    
    def test_get_collected_news(self, collector, mocker):
        """Test getting collected news."""
        # Insert test data
        conn = collector.conn
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO market_news (title, content, source, url, published_at, collected_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            'Test News',
            'Test content',
            'test_source',
            'https://example.com/news/1',
            '2024-01-01T12:00:00',
            '2024-01-01T13:00:00'
        ))
        conn.commit()
        
        news_list = collector.get_collected_news(limit=10)
        
        assert len(news_list) == 1
        assert news_list[0]['title'] == 'Test News'
        assert news_list[0]['source'] == 'test_source'
    
    def test_get_collected_news_with_filter(self, collector):
        """Test getting collected news with source filter."""
        # Insert test data
        conn = collector.conn
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO market_news (title, content, source, url, published_at, collected_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            'Yahoo News',
            'Content',
            'yahoo',
            'https://example.com/yahoo/1',
            '2024-01-01T12:00:00',
            '2024-01-01T13:00:00'
        ))
        cursor.execute("""
            INSERT INTO market_news (title, content, source, url, published_at, collected_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            'Reuters News',
            'Content',
            'reuters',
            'https://example.com/reuters/1',
            '2024-01-01T12:00:00',
            '2024-01-01T13:00:00'
        ))
        conn.commit()
        
        news_list = collector.get_collected_news(source='yahoo')
        
        assert len(news_list) == 1
        assert news_list[0]['source'] == 'yahoo'

