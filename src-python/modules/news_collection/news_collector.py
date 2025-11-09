"""
News collector that orchestrates RSS and API news collection.

Related Documentation:
  └─ Plan: docs/03_plans/news-collection/README.md

DEPENDENCY MAP:

Parents (Files that import this file):
  └─ src-python/scripts/collect_market_news.py

Dependencies (External files that this file imports):
  ├─ sqlite3 (standard library)
  ├─ json (standard library)
  ├─ datetime (standard library)
  ├─ typing (standard library)
  ├─ logging (standard library)
  ├─ src-python/modules/news_collection.rss_parser
  ├─ src-python/modules/news_collection.news_api_client
  ├─ src-python/modules/news_collection.exceptions
  └─ src-python/database.connection
"""
import sqlite3
import json
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional

from .rss_parser import RSSFeedParser
from .news_api_client import NewsAPIClient
from .exceptions import NewsCollectionError, DatabaseError
from database.connection import get_connection
from utils.json_io import json_response


logger = logging.getLogger(__name__)


class NewsCollector:
    """Collects news from RSS feeds and APIs and saves to database."""
    
    def __init__(self, conn: Optional[sqlite3.Connection] = None):
        """
        Initialize news collector.
        
        Args:
            conn: Optional database connection. If None, uses get_connection().
        """
        self.conn = conn if conn is not None else get_connection()
        self.rss_parser = RSSFeedParser()
        self.api_client = None  # Lazy initialization
    
    def collect_news(
        self,
        use_rss: bool = True,
        use_api: bool = False,
        api_key: Optional[str] = None,
        keywords: Optional[List[str]] = None,
        max_articles: int = 50
    ) -> Dict[str, Any]:
        """
        Collect news from RSS feeds and/or NewsAPI.
        
        Args:
            use_rss: Whether to collect from RSS feeds (default: True)
            use_api: Whether to collect from NewsAPI (default: False)
            api_key: NewsAPI key (required if use_api=True)
            keywords: Keywords for NewsAPI search (optional)
            max_articles: Maximum articles from NewsAPI (default: 50)
            
        Returns:
            Dict with success status, collected_count, and skipped_count
        """
        all_news = []
        errors = []
        
        try:
            # Collect from RSS feeds
            if use_rss:
                try:
                    logger.info("Collecting news from RSS feeds...")
                    rss_news = self.rss_parser.parse_feeds()
                    all_news.extend(rss_news)
                    logger.info(f"Collected {len(rss_news)} items from RSS feeds")
                except Exception as e:
                    error_msg = f"Failed to collect from RSS feeds: {str(e)}"
                    logger.error(error_msg)
                    errors.append(error_msg)
                    # Continue with API collection even if RSS fails
            
            # Collect from NewsAPI
            if use_api:
                try:
                    if not self.api_client:
                        if not api_key:
                            # Try to get from environment
                            import os
                            api_key = os.getenv('NEWSAPI_KEY')
                            if not api_key:
                                raise NewsCollectionError("API key is required for NewsAPI collection. Set NEWSAPI_KEY environment variable or pass api_key parameter.")
                        self.api_client = NewsAPIClient(api_key)
                    
                    logger.info("Collecting news from NewsAPI...")
                    api_news = self.api_client.fetch_news(
                        keywords=keywords,
                        max_articles=max_articles
                    )
                    all_news.extend(api_news)
                    logger.info(f"Collected {len(api_news)} items from NewsAPI")
                except Exception as e:
                    error_msg = f"Failed to collect from NewsAPI: {str(e)}"
                    logger.error(error_msg)
                    errors.append(error_msg)
                    # Continue with saving even if API fails
            
            if not all_news:
                error_message = "No news items collected"
                if errors:
                    error_message += f". Errors: {'; '.join(errors)}"
                return json_response(
                    success=False,
                    error=error_message
                )
            
            # Save to database
            logger.info(f"Saving {len(all_news)} news items to database...")
            result = self._save_to_database(all_news)
            
            # If we have errors but still collected some news, include warnings
            if errors and result['saved_count'] > 0:
                logger.warning(f"Collected {result['saved_count']} items but encountered errors: {'; '.join(errors)}")
            
            return json_response(
                success=True,
                data={
                    "collected_count": result['saved_count'],
                    "skipped_count": result['skipped_count'],
                    "total_processed": len(all_news),
                    "warnings": errors if errors else None
                }
            )
            
        except Exception as e:
            error_msg = f"News collection failed: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return json_response(
                success=False,
                error=error_msg
            )
    
    def _save_to_database(self, news_items: List[Dict[str, Any]]) -> Dict[str, int]:
        """
        Save news items to database with duplicate checking.
        
        Args:
            news_items: List of news dictionaries
            
        Returns:
            Dict with 'saved_count' and 'skipped_count'
        """
        cursor = self.conn.cursor()
        saved_count = 0
        skipped_count = 0
        
        try:
            collected_at = datetime.now().isoformat()
            
            for news_item in news_items:
                try:
                    title = news_item.get('title', '')
                    content = news_item.get('content', '')
                    source = news_item.get('source', 'unknown')
                    url = news_item.get('url', '')
                    published_at = news_item.get('published_at', collected_at)
                    keywords = news_item.get('keywords')  # Optional
                    sentiment = news_item.get('sentiment')  # Optional, for future use
                    
                    # Validate required fields
                    if not title or not url:
                        logger.warning(f"Skipping news item without title or URL")
                        skipped_count += 1
                        continue
                    
                    # Check for duplicates (URL-based)
                    cursor.execute("SELECT id FROM market_news WHERE url = ?", (url,))
                    if cursor.fetchone():
                        logger.debug(f"Skipping duplicate news: {url}")
                        skipped_count += 1
                        continue
                    
                    # Convert keywords to JSON if provided
                    keywords_json = json.dumps(keywords) if keywords else None
                    
                    # Insert news item
                    cursor.execute("""
                        INSERT INTO market_news (
                            title, content, source, url, published_at,
                            collected_at, keywords, sentiment
                        )
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        title,
                        content,
                        source,
                        url,
                        published_at,
                        collected_at,
                        keywords_json,
                        sentiment
                    ))
                    
                    saved_count += 1
                    
                except sqlite3.IntegrityError as e:
                    # Handle UNIQUE constraint violation (duplicate URL)
                    logger.debug(f"Duplicate news item (URL constraint): {url}")
                    skipped_count += 1
                except Exception as e:
                    logger.error(f"Error saving news item: {str(e)}")
                    skipped_count += 1
                    continue
            
            self.conn.commit()
            logger.info(f"Saved {saved_count} news items, skipped {skipped_count} duplicates")
            
            return {
                'saved_count': saved_count,
                'skipped_count': skipped_count
            }
            
        except Exception as e:
            self.conn.rollback()
            raise DatabaseError(f"Failed to save news to database: {str(e)}")
    
    def get_collected_news(
        self,
        limit: int = 100,
        offset: int = 0,
        source: Optional[str] = None,
        order_by: str = 'published_at',
        order_desc: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Get collected news from database.
        
        Args:
            limit: Maximum number of news items to return (default: 100)
            offset: Offset for pagination (default: 0)
            source: Filter by source (optional)
            order_by: Field to order by (default: 'published_at')
            order_desc: Whether to order descending (default: True)
            
        Returns:
            List of news dictionaries
        """
        cursor = self.conn.cursor()
        
        # Build query
        query = "SELECT id, title, content, source, url, published_at, collected_at, keywords, sentiment FROM market_news"
        params = []
        
        if source:
            query += " WHERE source = ?"
            params.append(source)
        
        # Validate order_by field
        valid_order_fields = ['published_at', 'collected_at', 'id']
        if order_by not in valid_order_fields:
            order_by = 'published_at'
        
        query += f" ORDER BY {order_by} {'DESC' if order_desc else 'ASC'}"
        query += " LIMIT ? OFFSET ?"
        params.extend([limit, offset])
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        news_list = []
        for row in rows:
            news_item = {
                'id': row[0],
                'title': row[1],
                'content': row[2],
                'source': row[3],
                'url': row[4],
                'published_at': row[5],
                'collected_at': row[6],
                'keywords': json.loads(row[7]) if row[7] else None,
                'sentiment': row[8]
            }
            news_list.append(news_item)
        
        return news_list

