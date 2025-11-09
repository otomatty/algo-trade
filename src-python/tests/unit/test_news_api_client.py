"""
Unit tests for NewsAPI client.
"""
import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from modules.news_collection.news_api_client import NewsAPIClient
from modules.news_collection.exceptions import APIKeyError, RateLimitError, APIError


@pytest.mark.unit
class TestNewsAPIClient:
    """Test cases for NewsAPIClient class."""
    
    def test_init_without_api_key(self):
        """Test initialization without API key."""
        with patch.dict('os.environ', {}, clear=True):
            with pytest.raises(APIKeyError):
                NewsAPIClient()
    
    def test_init_with_api_key(self):
        """Test initialization with API key."""
        client = NewsAPIClient(api_key='test_key')
        assert client.api_key == 'test_key'
    
    def test_fetch_news_success(self, mocker):
        """Test successful news fetch."""
        mock_response = Mock()
        mock_response.json.return_value = {
            'status': 'ok',
            'articles': [
                {
                    'title': 'Test News',
                    'content': 'Test content',
                    'url': 'https://example.com/news/1',
                    'source': {'name': 'Test Source'},
                    'publishedAt': '2024-01-01T12:00:00Z'
                }
            ]
        }
        mock_response.raise_for_status = Mock()
        
        mock_session = Mock()
        mock_session.get.return_value = mock_response
        
        client = NewsAPIClient(api_key='test_key')
        client.session = mock_session
        
        news_list = client.fetch_news()
        
        assert len(news_list) == 1
        assert news_list[0]['title'] == 'Test News'
        assert news_list[0]['source'] == 'test_source'
    
    def test_fetch_news_with_keywords(self, mocker):
        """Test news fetch with keywords."""
        mock_response = Mock()
        mock_response.json.return_value = {
            'status': 'ok',
            'articles': []
        }
        mock_response.raise_for_status = Mock()
        
        mock_session = Mock()
        mock_session.get.return_value = mock_response
        
        client = NewsAPIClient(api_key='test_key')
        client.session = mock_session
        
        news_list = client.fetch_news(keywords=['stock', 'market'])
        
        # Verify API was called with correct parameters
        call_args = mock_session.get.call_args
        assert 'q' in call_args[1]['params']
        assert call_args[1]['params']['q'] == 'stock OR market'
    
    def test_fetch_news_rate_limit_error(self, mocker):
        """Test rate limit error handling."""
        mock_response = Mock()
        mock_response.json.return_value = {
            'status': 'error',
            'code': 'rateLimited',
            'message': 'Rate limit exceeded'
        }
        mock_response.raise_for_status = Mock()
        
        mock_session = Mock()
        mock_session.get.return_value = mock_response
        
        client = NewsAPIClient(api_key='test_key')
        client.session = mock_session
        
        with pytest.raises(RateLimitError):
            client.fetch_news()
    
    def test_fetch_news_api_error(self, mocker):
        """Test API error handling."""
        mock_response = Mock()
        mock_response.json.return_value = {
            'status': 'error',
            'code': 'apiKeyInvalid',
            'message': 'Invalid API key'
        }
        mock_response.raise_for_status = Mock()
        
        mock_session = Mock()
        mock_session.get.return_value = mock_response
        
        client = NewsAPIClient(api_key='test_key')
        client.session = mock_session
        
        with pytest.raises(APIError):
            client.fetch_news()

