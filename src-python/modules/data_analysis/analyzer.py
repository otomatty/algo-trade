"""
Main data analyzer module.

Related Documentation:
  ├─ Spec: src-python/modules/data_analysis/analyzer.spec.md
  └─ Plan: docs/03_plans/data-analysis/README.md
"""
import sqlite3
import json
from datetime import datetime
from typing import Dict, Optional
import pandas as pd

from modules.data_analysis.technical_indicators import TechnicalIndicators
from modules.data_analysis.trend_analyzer import TrendAnalyzer
from modules.data_analysis.statistics import StatisticsCalculator


class DataAnalyzer:
    """Main data analyzer that orchestrates all analysis components."""
    
    def __init__(self, conn: Optional[sqlite3.Connection] = None):
        """
        Initialize DataAnalyzer.
        
        Args:
            conn: Database connection (optional, will create new if not provided)
        """
        self.conn = conn
        self.technical_indicators = TechnicalIndicators()
        self.trend_analyzer = TrendAnalyzer()
        self.statistics_calculator = StatisticsCalculator()
    
    def analyze_data_set(self, job_id: str, data_set_id: int) -> Dict:
        """
        Analyze a data set and save results.
        
        Args:
            job_id: Analysis job ID
            data_set_id: Data set ID to analyze
        
        Returns:
            Dict with 'success' and 'data' or 'error'
        """
        try:
            # Update job status to running
            self._update_job_status(job_id, 'running', 0.1, 'Loading data...')
            
            # Load OHLCV data
            data = self._load_ohlcv_data(data_set_id)
            if data is None or len(data) == 0:
                self._update_job_status(job_id, 'failed', 0.0, 'No data found')
                return {'success': False, 'error': f'No data found for data set {data_set_id}'}
            
            self._update_job_status(job_id, 'running', 0.3, 'Calculating technical indicators...')
            
            # Calculate technical indicators
            rsi = self.technical_indicators.calculate_rsi(data)
            macd = self.technical_indicators.calculate_macd(data)
            
            technical_indicators = {}
            if rsi:
                technical_indicators['rsi'] = rsi
            if macd:
                technical_indicators['macd'] = macd
            
            self._update_job_status(job_id, 'running', 0.6, 'Analyzing trends...')
            
            # Analyze trends
            trend_analysis = self.trend_analyzer.analyze_trend(data)
            if not trend_analysis:
                trend_analysis = {
                    'trend_direction': 'sideways',
                    'volatility_level': 'medium',
                    'dominant_patterns': []
                }
            
            self._update_job_status(job_id, 'running', 0.8, 'Calculating statistics...')
            
            # Calculate statistics
            statistics = self.statistics_calculator.calculate(data)
            if not statistics:
                statistics = {
                    'price_range': {'min': 0, 'max': 0, 'current': 0},
                    'volume_average': 0,
                    'price_change_percent': 0
                }
            
            # Structure results
            analysis_summary = {
                'trend_direction': trend_analysis['trend_direction'],
                'volatility_level': trend_analysis['volatility_level'],
                'dominant_patterns': trend_analysis['dominant_patterns']
            }
            
            results = {
                'analysis_summary': analysis_summary,
                'technical_indicators': technical_indicators,
                'statistics': statistics
            }
            
            self._update_job_status(job_id, 'running', 0.9, 'Saving results...')
            
            # Save results to database
            self._save_results(job_id, data_set_id, results)
            
            # Update job status to completed
            self._update_job_status(job_id, 'completed', 1.0, 'Analysis completed', completed=True)
            
            return {
                'success': True,
                'data': results
            }
            
        except Exception as e:
            self._update_job_status(job_id, 'failed', 0.0, f'Analysis failed: {str(e)}')
            return {
                'success': False,
                'error': str(e)
            }
    
    def _load_ohlcv_data(self, data_set_id: int) -> Optional[pd.DataFrame]:
        """Load OHLCV data from database."""
        if not self.conn:
            from database.connection import get_connection
            self.conn = get_connection()
        
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT date, open, high, low, close, volume
            FROM ohlcv_data
            WHERE data_set_id = ?
            ORDER BY date ASC
        """, (data_set_id,))
        
        rows = cursor.fetchall()
        if not rows:
            return None
        
        data = pd.DataFrame(rows, columns=['date', 'open', 'high', 'low', 'close', 'volume'])
        return data
    
    def _update_job_status(self, job_id: str, status: str, progress: float, message: str, completed: bool = False):
        """Update analysis job status."""
        if not self.conn:
            from database.connection import get_connection
            self.conn = get_connection()
        
        cursor = self.conn.cursor()
        
        if completed:
            cursor.execute("""
                UPDATE analysis_jobs
                SET status = ?, progress = ?, message = ?, completed_at = ?
                WHERE job_id = ?
            """, (status, progress, message, datetime.now().isoformat(), job_id))
        else:
            cursor.execute("""
                UPDATE analysis_jobs
                SET status = ?, progress = ?, message = ?
                WHERE job_id = ?
            """, (status, progress, message, job_id))
        
        self.conn.commit()
    
    def _save_results(self, job_id: str, data_set_id: int, results: Dict):
        """Save analysis results to database."""
        if not self.conn:
            from database.connection import get_connection
            self.conn = get_connection()
        
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO analysis_results (job_id, data_set_id, analysis_summary, technical_indicators, statistics, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            job_id,
            data_set_id,
            json.dumps(results['analysis_summary']),
            json.dumps(results['technical_indicators']),
            json.dumps(results['statistics']),
            datetime.now().isoformat()
        ))
        
        self.conn.commit()

