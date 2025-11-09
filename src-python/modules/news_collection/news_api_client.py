"""
News API client for market news collection.

Related Documentation:
  └─ Plan: docs/03_plans/news-collection/README.md

DEPENDENCY MAP:

Parents (Files that import this file):
  └─ src-python/modules/news_collection/news_collector.py

Dependencies (External files that this file imports):
  ├─ requests (external library)
  ├─ datetime (standard library)
  ├─ typing (standard library)
  ├─ logging (standard library)
  ├─ time (standard library)
  ├─ os (standard library)
  ├─ pathlib (standard library)
  └─ src-python/modules/news_collection.exceptions
"""
import requests
import logging
import time
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
from requests.exceptions import RequestException, Timeout

from .exceptions import APIKeyError, RateLimitError, APIError, NetworkError

# Load .env file if available
try:
    from dotenv import load_dotenv
    project_root = Path(__file__).parent.parent.parent.parent
    env_path = project_root / ".env"
    if env_path.exists():
        load_dotenv(env_path)
    else:
        load_dotenv()
except ImportError:
    # python-dotenv not installed, skip .env loading
    pass


logger = logging.getLogger(__name__)


class NewsAPIClient:
    """Client for NewsAPI (https://newsapi.org)."""
    
    BASE_URL = "https://newsapi.org/v2"
    MIN_REQUEST_INTERVAL = 1.0  # Minimum seconds between requests
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize NewsAPI client.
        
        Args:
            api_key: NewsAPI API key. If None, reads from NEWSAPI_KEY environment variable.
            
        Raises:
            APIKeyError: If API key is not provided
        """
        self.api_key = api_key or self._get_api_key_from_env()
        if not self.api_key:
            raise APIKeyError("NewsAPI key is required. Set NEWSAPI_KEY environment variable or pass api_key parameter.")
        
        self.session = requests.Session()
        self.last_request_time = 0
    
    def _get_api_key_from_env(self) -> Optional[str]:
        """Get API key from environment variable."""
        return os.getenv('NEWSAPI_KEY')
    
    def fetch_news(
        self,
        keywords: Optional[List[str]] = None,
        max_articles: int = 50,
        language: str = 'en',
        sort_by: str = 'publishedAt'
    ) -> List[Dict[str, Any]]:
        """
        Fetch news articles from NewsAPI.
        
        Args:
            keywords: List of keywords to search for (optional)
            max_articles: Maximum number of articles to fetch (default: 50, max: 100)
            language: Language code (default: 'en')
            sort_by: Sort order ('relevancy', 'popularity', 'publishedAt')
            
        Returns:
            List of news dictionaries with keys: title, content, source, url, published_at
            
        Raises:
            APIError: If API call fails
            RateLimitError: If rate limit is exceeded
            NetworkError: If network request fails
        """
        self._check_rate_limit()
        
        try:
            params = {
                'apiKey': self.api_key,
                'language': language,
                'sortBy': sort_by,
                'pageSize': min(max_articles, 100)  # API limit is 100
            }
            
            # Add search query if keywords provided
            if keywords:
                query = ' OR '.join(keywords)
                params['q'] = query
            
            # Use 'everything' endpoint for keyword search, 'top-headlines' for general news
            if keywords:
                endpoint = f'{self.BASE_URL}/everything'
            else:
                endpoint = f'{self.BASE_URL}/top-headlines'
                params['category'] = 'business'  # Focus on business news
            
            response = self.session.get(endpoint, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            # Check for API errors
            if data.get('status') == 'error':
                error_message = data.get('message', 'Unknown API error')
                code = data.get('code')
                
                if code == 'rateLimited':
                    raise RateLimitError(f"NewsAPI rate limit exceeded: {error_message}")
                else:
                    raise APIError(f"NewsAPI error: {error_message}", status_code=response.status_code)
            
            # Parse articles
            articles = data.get('articles', [])
            news_list = []
            
            for article in articles:
                try:
                    # Extract fields
                    title = article.get('title', '').strip()
                    if not title or title == '[Removed]':
                        continue
                    
                    content = article.get('content', article.get('description', '')).strip()
                    url = article.get('url', '').strip()
                    source_name = article.get('source', {}).get('name', 'unknown')
                    published_at = article.get('publishedAt', '')
                    
                    # Parse date
                    if published_at:
                        try:
                            # NewsAPI returns ISO 8601 format
                            dt = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
                            published_at = dt.isoformat()
                        except Exception:
                            logger.warning(f"Could not parse date: {published_at}")
                            published_at = datetime.now().isoformat()
                    else:
                        published_at = datetime.now().isoformat()
                    
                    news_item = {
                        'title': title,
                        'content': content,
                        'source': source_name.lower().replace(' ', '_'),
                        'url': url,
                        'published_at': published_at
                    }
                    
                    news_list.append(news_item)
                except Exception as e:
                    logger.error(f"Error processing article: {str(e)}")
                    continue
            
            logger.info(f"Fetched {len(news_list)} articles from NewsAPI")
            return news_list
            
        except RateLimitError:
            raise
        except APIError:
            raise
        except Timeout:
            raise NetworkError("Request to NewsAPI timed out")
        except RequestException as e:
            raise NetworkError(f"Network error while fetching from NewsAPI: {str(e)}")
        except Exception as e:
            raise APIError(f"Unexpected error while fetching from NewsAPI: {str(e)}")
    
    def _check_rate_limit(self) -> None:
        """Check and enforce rate limiting."""
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        if time_since_last_request < self.MIN_REQUEST_INTERVAL:
            sleep_time = self.MIN_REQUEST_INTERVAL - time_since_last_request
            time.sleep(sleep_time)
        self.last_request_time = time.time()

