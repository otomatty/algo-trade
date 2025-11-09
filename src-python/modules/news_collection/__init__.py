"""
News collection module.

Related Documentation:
  └─ Plan: docs/03_plans/news-collection/README.md
"""

from .rss_parser import RSSFeedParser
from .news_api_client import NewsAPIClient
from .news_collector import NewsCollector
from .job_manager import NewsCollectionJobManager
from .exceptions import (
    NewsCollectionError,
    RSSParseError,
    APIKeyError,
    RateLimitError,
    APIError,
    NetworkError,
    DatabaseError
)

__all__ = [
    'RSSFeedParser',
    'NewsAPIClient',
    'NewsCollector',
    'NewsCollectionJobManager',
    'NewsCollectionError',
    'RSSParseError',
    'APIKeyError',
    'RateLimitError',
    'APIError',
    'NetworkError',
    'DatabaseError',
]

