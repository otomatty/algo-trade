"""
RSS feed parser for market news collection.

Related Documentation:
  └─ Plan: docs/03_plans/news-collection/README.md

DEPENDENCY MAP:

Parents (Files that import this file):
  └─ src-python/modules/news_collection/news_collector.py

Dependencies (External files that this file imports):
  ├─ feedparser (external library)
  ├─ datetime (standard library)
  ├─ typing (standard library)
  ├─ logging (standard library)
  ├─ ssl (standard library)
  └─ src-python/modules/news_collection.exceptions
"""
import feedparser
import logging
import ssl
from datetime import datetime
from typing import List, Dict, Any, Optional
from urllib.parse import urlparse

from .exceptions import RSSParseError, NetworkError


logger = logging.getLogger(__name__)


class RSSFeedParser:
    """Parser for RSS feeds from various news sources."""
    
    # Default RSS feed sources
    DEFAULT_FEEDS = [
        'https://feeds.finance.yahoo.com/rss/2.0/headline',
        'https://feeds.reuters.com/reuters/businessNews',
        'https://feeds.bloomberg.com/markets/news.rss',
    ]
    
    def __init__(self, feed_urls: Optional[List[str]] = None):
        """
        Initialize RSS feed parser.
        
        Args:
            feed_urls: List of RSS feed URLs. If None, uses default feeds.
        """
        self.feed_urls = feed_urls if feed_urls else self.DEFAULT_FEEDS
    
    def parse_feeds(self) -> List[Dict[str, Any]]:
        """
        Parse all configured RSS feeds and return news items.
        
        Returns:
            List of news dictionaries with keys: title, content, source, url, published_at
        """
        all_news = []
        
        for feed_url in self.feed_urls:
            try:
                news_items = self._parse_feed(feed_url)
                all_news.extend(news_items)
                logger.info(f"Parsed {len(news_items)} items from {feed_url}")
            except Exception as e:
                logger.error(f"Failed to parse feed {feed_url}: {str(e)}")
                # Continue with other feeds even if one fails
                continue
        
        logger.info(f"Total news items parsed: {len(all_news)}")
        return all_news
    
    def _parse_feed(self, feed_url: str) -> List[Dict[str, Any]]:
        """
        Parse a single RSS feed.
        
        Args:
            feed_url: RSS feed URL
            
        Returns:
            List of news dictionaries
            
        Raises:
            RSSParseError: If parsing fails
            NetworkError: If network request fails
        """
        try:
            # Disable SSL verification for feedparser (development only)
            # feedparser uses urllib internally, so we need to patch SSL context
            original_ssl_context = ssl._create_default_https_context
            ssl._create_default_https_context = ssl._create_unverified_context
            
            try:
                feed = feedparser.parse(feed_url)
            finally:
                # Restore original SSL context
                ssl._create_default_https_context = original_ssl_context
            
            # Check for feed parsing errors
            if feed.bozo and feed.bozo_exception:
                raise RSSParseError(f"Failed to parse RSS feed: {feed.bozo_exception}")
            
            news_list = []
            source = self._extract_source(feed_url)
            
            for entry in feed.entries:
                try:
                    # Extract title
                    title = entry.get('title', '').strip()
                    if not title:
                        logger.warning(f"Skipping entry without title from {feed_url}")
                        continue
                    
                    # Extract content/summary
                    content = entry.get('summary', entry.get('description', '')).strip()
                    
                    # Extract URL
                    url = entry.get('link', '').strip()
                    if not url:
                        logger.warning(f"Skipping entry without URL: {title}")
                        continue
                    
                    # Parse published date
                    published_at = self._parse_date(entry.get('published', entry.get('updated', '')))
                    if not published_at:
                        # Use current time if date parsing fails
                        published_at = datetime.now().isoformat()
                        logger.warning(f"Could not parse date for entry: {title}, using current time")
                    
                    news_item = {
                        'title': title,
                        'content': content,
                        'source': source,
                        'url': url,
                        'published_at': published_at
                    }
                    
                    news_list.append(news_item)
                except Exception as e:
                    logger.error(f"Error processing entry from {feed_url}: {str(e)}")
                    continue
            
            return news_list
            
        except RSSParseError:
            raise
        except Exception as e:
            raise NetworkError(f"Network error while fetching RSS feed {feed_url}: {str(e)}")
    
    def _extract_source(self, feed_url: str) -> str:
        """
        Extract source name from feed URL.
        
        Args:
            feed_url: RSS feed URL
            
        Returns:
            Source name (e.g., 'yahoo', 'reuters', 'bloomberg')
        """
        parsed = urlparse(feed_url)
        domain = parsed.netloc.lower()
        
        if 'yahoo' in domain:
            return 'yahoo'
        elif 'reuters' in domain:
            return 'reuters'
        elif 'bloomberg' in domain:
            return 'bloomberg'
        else:
            # Extract domain name as source
            return domain.split('.')[0] if domain else 'unknown'
    
    def _parse_date(self, date_str: str) -> Optional[str]:
        """
        Parse date string from RSS feed to ISO format.
        
        Args:
            date_str: Date string from RSS feed
            
        Returns:
            ISO format date string (YYYY-MM-DDTHH:MM:SS) or None if parsing fails
        """
        if not date_str:
            return None
        
        try:
            # feedparser provides parsed date in time.struct_time format
            # We need to parse the string ourselves
            from email.utils import parsedate_to_datetime
            
            dt = parsedate_to_datetime(date_str)
            return dt.isoformat()
        except Exception:
            # Try alternative parsing methods
            try:
                # Try common date formats
                for fmt in ['%a, %d %b %Y %H:%M:%S %z', '%a, %d %b %Y %H:%M:%S %Z', '%Y-%m-%d %H:%M:%S']:
                    try:
                        dt = datetime.strptime(date_str, fmt)
                        return dt.isoformat()
                    except ValueError:
                        continue
            except Exception:
                pass
            
            logger.warning(f"Could not parse date: {date_str}")
            return None

