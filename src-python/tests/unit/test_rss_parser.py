"""
Unit tests for RSS feed parser.
"""
import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from modules.news_collection.rss_parser import RSSFeedParser
from modules.news_collection.exceptions import RSSParseError, NetworkError


@pytest.mark.unit
class TestRSSFeedParser:
    """Test cases for RSSFeedParser class."""
    
    def test_parse_feed_success(self, mocker):
        """Test successful RSS feed parsing."""
        # Mock feedparser
        mock_feed = Mock()
        mock_feed.bozo = False
        mock_feed.entries = [
            Mock(
                title='Test News Title',
                summary='Test news content',
                link='https://example.com/news/1',
                published='Mon, 01 Jan 2024 12:00:00 +0000'
            ),
            Mock(
                title='Another News Title',
                description='Another news content',
                link='https://example.com/news/2',
                updated='Tue, 02 Jan 2024 12:00:00 +0000'
            )
        ]
        
        mocker.patch('modules.news_collection.rss_parser.feedparser.parse', return_value=mock_feed)
        
        parser = RSSFeedParser(['https://example.com/feed'])
        news_list = parser._parse_feed('https://example.com/feed')
        
        assert len(news_list) == 2
        assert news_list[0]['title'] == 'Test News Title'
        assert news_list[0]['url'] == 'https://example.com/news/1'
        assert news_list[1]['title'] == 'Another News Title'
    
    def test_parse_feed_bozo_error(self, mocker):
        """Test RSS feed parsing with bozo error."""
        mock_feed = Mock()
        mock_feed.bozo = True
        mock_feed.bozo_exception = Exception("Invalid RSS format")
        
        mocker.patch('modules.news_collection.rss_parser.feedparser.parse', return_value=mock_feed)
        
        parser = RSSFeedParser(['https://example.com/feed'])
        
        with pytest.raises(RSSParseError):
            parser._parse_feed('https://example.com/feed')
    
    def test_parse_feeds_multiple_sources(self, mocker):
        """Test parsing multiple RSS feeds."""
        mock_feed = Mock()
        mock_feed.bozo = False
        mock_feed.entries = [
            Mock(
                title='News Title',
                summary='News content',
                link='https://example.com/news/1',
                published='Mon, 01 Jan 2024 12:00:00 +0000'
            )
        ]
        
        mocker.patch('modules.news_collection.rss_parser.feedparser.parse', return_value=mock_feed)
        
        parser = RSSFeedParser(['https://feed1.com', 'https://feed2.com'])
        news_list = parser.parse_feeds()
        
        assert len(news_list) == 2  # One from each feed
    
    def test_extract_source(self):
        """Test source extraction from URL."""
        parser = RSSFeedParser()
        
        assert parser._extract_source('https://feeds.finance.yahoo.com/rss') == 'yahoo'
        assert parser._extract_source('https://feeds.reuters.com/news') == 'reuters'
        assert parser._extract_source('https://feeds.bloomberg.com/markets') == 'bloomberg'
    
    def test_parse_date_success(self):
        """Test date parsing."""
        parser = RSSFeedParser()
        
        date_str = 'Mon, 01 Jan 2024 12:00:00 +0000'
        parsed = parser._parse_date(date_str)
        
        assert parsed is not None
        assert '2024-01-01' in parsed
    
    def test_parse_date_invalid(self):
        """Test date parsing with invalid format."""
        parser = RSSFeedParser()
        
        parsed = parser._parse_date('Invalid date')
        # Should return None or current time
        assert parsed is not None  # Returns current time as fallback

