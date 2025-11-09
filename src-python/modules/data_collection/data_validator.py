"""
Data validator for checking data integrity.

Related Documentation:
  └─ Plan: docs/03_plans/data-collection/README.md

DEPENDENCY MAP:

Parents (Files that import this file):
  └─ src-python/scripts/check_data_integrity.py

Dependencies (External files that this file imports):
  ├─ sqlite3 (standard library)
  ├─ pandas (external)
  ├─ datetime (standard library)
  ├─ typing (standard library)
  ├─ logging (standard library)
  └─ src-python/database.connection
"""
import sqlite3
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import pandas as pd

from database.connection import get_connection

logger = logging.getLogger(__name__)


class DataValidator:
    """Validates data integrity."""
    
    def __init__(self, conn: Optional[sqlite3.Connection] = None):
        """
        Initialize data validator.
        
        Args:
            conn: Database connection (optional, will create new if not provided)
        """
        self.conn = conn if conn is not None else get_connection()
    
    def check_integrity(self, data_set_id: int) -> Dict[str, Any]:
        """
        Check data integrity for a dataset.
        
        Args:
            data_set_id: Dataset ID
            
        Returns:
            Dict with integrity check results:
            - valid: bool
            - issues: List[str]
            - statistics: Dict
        """
        cursor = self.conn.cursor()
        
        # Get all data
        cursor.execute("""
            SELECT date, open, high, low, close, volume
            FROM ohlcv_data
            WHERE data_set_id = ?
            ORDER BY date
        """, (data_set_id,))
        
        rows = cursor.fetchall()
        
        if not rows:
            return {
                'valid': False,
                'issues': ['No data found'],
                'statistics': {}
            }
        
        # Convert to DataFrame
        df = pd.DataFrame(rows, columns=['date', 'open', 'high', 'low', 'close', 'volume'])
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')
        
        issues = []
        
        # Check 1: Date continuity
        date_continuity_issues = self._check_date_continuity(df)
        issues.extend(date_continuity_issues)
        
        # Check 2: Price validity
        price_issues = self._check_price_validity(df)
        issues.extend(price_issues)
        
        # Check 3: Duplicates
        duplicate_issues = self._check_duplicates(data_set_id)
        issues.extend(duplicate_issues)
        
        # Check 4: Volume validity
        volume_issues = self._check_volume_validity(df)
        issues.extend(volume_issues)
        
        # Statistics
        statistics = {
            'total_records': len(df),
            'date_range': {
                'start': df['date'].min().strftime('%Y-%m-%d'),
                'end': df['date'].max().strftime('%Y-%m-%d')
            },
            'gaps': len(date_continuity_issues),
            'price_issues': len(price_issues),
            'duplicates': len(duplicate_issues),
            'volume_issues': len(volume_issues)
        }
        
        return {
            'valid': len(issues) == 0,
            'issues': issues,
            'statistics': statistics
        }
    
    def _check_date_continuity(self, df: pd.DataFrame) -> List[str]:
        """Check for gaps in date sequence."""
        issues = []
        
        if len(df) < 2:
            return issues
        
        df_sorted = df.sort_values('date')
        date_diff = df_sorted['date'].diff()
        
        # Check for gaps larger than expected (more than 3 days, accounting for weekends)
        for idx, diff in enumerate(date_diff):
            if pd.isna(diff):
                continue
            
            days = diff.days
            if days > 3:  # More than 3 days gap
                prev_date = df_sorted.iloc[idx - 1]['date']
                curr_date = df_sorted.iloc[idx]['date']
                issues.append(f"Date gap detected: {prev_date.strftime('%Y-%m-%d')} to {curr_date.strftime('%Y-%m-%d')} ({days} days)")
        
        return issues
    
    def _check_price_validity(self, df: pd.DataFrame) -> List[str]:
        """Check price data validity."""
        issues = []
        
        # Check: high >= low
        invalid_hl = df[df['high'] < df['low']]
        if len(invalid_hl) > 0:
            issues.append(f"Found {len(invalid_hl)} records where high < low")
        
        # Check: open and close within high-low range
        invalid_range = df[
            (df['open'] < df['low']) | (df['open'] > df['high']) |
            (df['close'] < df['low']) | (df['close'] > df['high'])
        ]
        if len(invalid_range) > 0:
            issues.append(f"Found {len(invalid_range)} records where open/close outside high-low range")
        
        # Check: negative prices
        negative_prices = df[
            (df['open'] < 0) | (df['high'] < 0) | (df['low'] < 0) | (df['close'] < 0)
        ]
        if len(negative_prices) > 0:
            issues.append(f"Found {len(negative_prices)} records with negative prices")
        
        # Check: extreme price changes (more than 50% change)
        price_changes = df['close'].pct_change().abs()
        extreme_changes = df[price_changes > 0.5]
        if len(extreme_changes) > 0:
            issues.append(f"Found {len(extreme_changes)} records with extreme price changes (>50%)")
        
        return issues
    
    def _check_duplicates(self, data_set_id: int) -> List[str]:
        """Check for duplicate dates."""
        cursor = self.conn.cursor()
        
        cursor.execute("""
            SELECT date, COUNT(*) as count
            FROM ohlcv_data
            WHERE data_set_id = ?
            GROUP BY date
            HAVING COUNT(*) > 1
        """, (data_set_id,))
        
        duplicates = cursor.fetchall()
        
        if duplicates:
            return [f"Found {len(duplicates)} duplicate dates"]
        
        return []
    
    def _check_volume_validity(self, df: pd.DataFrame) -> List[str]:
        """Check volume data validity."""
        issues = []
        
        # Check: negative volume
        negative_volume = df[df['volume'] < 0]
        if len(negative_volume) > 0:
            issues.append(f"Found {len(negative_volume)} records with negative volume")
        
        return issues

