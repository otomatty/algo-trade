"""
Custom exception classes for news collection.

Related Documentation:
  └─ Plan: docs/03_plans/news-collection/README.md
"""


class NewsCollectionError(Exception):
    """Base exception class for all news collection-related errors."""
    pass


class RSSParseError(NewsCollectionError):
    """Raised when RSS feed parsing fails."""
    pass


class APIKeyError(NewsCollectionError):
    """Raised when API key is missing or invalid."""
    pass


class RateLimitError(NewsCollectionError):
    """Raised when API rate limit is exceeded."""
    pass


class APIError(NewsCollectionError):
    """Raised when API call fails."""
    
    def __init__(self, message: str, status_code: int = None, response_body: str = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_body = response_body


class NetworkError(NewsCollectionError):
    """Raised when network request fails."""
    pass


class DatabaseError(NewsCollectionError):
    """Raised when database operation fails."""
    pass

