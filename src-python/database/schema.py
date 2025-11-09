"""
Database schema definitions for the algo-trade application.
"""
import sqlite3
from typing import List


def create_all_tables(conn: sqlite3.Connection) -> None:
    """
    Create all database tables.
    """
    tables = [
        _create_data_sets_table,
        _create_ohlcv_data_table,
        _create_market_news_table,
        _create_news_collection_jobs_table,
        _create_analysis_jobs_table,
        _create_analysis_results_table,
        _create_algorithms_table,
        _create_proposal_generation_jobs_table,
        _create_algorithm_proposals_table,
        _create_backtest_jobs_table,
        _create_backtest_results_table,
        _create_backtest_trades_table,
        _create_backtest_equity_curve_table,
        _create_stock_prediction_jobs_table,
        _create_stock_predictions_table,
    ]
    
    for create_table in tables:
        create_table(conn)
    
    # Create indexes
    _create_indexes(conn)


def _create_data_sets_table(conn: sqlite3.Connection) -> None:
    """Create data_sets table."""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS data_sets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            symbol TEXT,
            start_date TEXT,
            end_date TEXT,
            record_count INTEGER DEFAULT 0,
            imported_at TEXT NOT NULL,
            source TEXT NOT NULL,  -- 'csv' | 'api' | 'manual'
            created_at TEXT NOT NULL DEFAULT (datetime('now'))
        )
    """)


def _create_ohlcv_data_table(conn: sqlite3.Connection) -> None:
    """Create ohlcv_data table."""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS ohlcv_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_set_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            open REAL NOT NULL,
            high REAL NOT NULL,
            low REAL NOT NULL,
            close REAL NOT NULL,
            volume INTEGER NOT NULL,
            FOREIGN KEY (data_set_id) REFERENCES data_sets(id) ON DELETE CASCADE,
            UNIQUE(data_set_id, date)
        )
    """)


def _create_market_news_table(conn: sqlite3.Connection) -> None:
    """Create market_news table."""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS market_news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT,
            source TEXT NOT NULL,
            url TEXT,
            published_at TEXT NOT NULL,
            collected_at TEXT NOT NULL DEFAULT (datetime('now')),
            keywords TEXT,  -- JSON array
            sentiment TEXT,  -- 'positive' | 'neutral' | 'negative'
            UNIQUE(url)
        )
    """)


def _create_news_collection_jobs_table(conn: sqlite3.Connection) -> None:
    """Create news_collection_jobs table."""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS news_collection_jobs (
            job_id TEXT PRIMARY KEY,
            use_rss INTEGER DEFAULT 1,  -- Boolean: 1 = true, 0 = false
            use_api INTEGER DEFAULT 0,
            api_key TEXT,
            keywords TEXT,  -- JSON array
            max_articles INTEGER DEFAULT 50,
            status TEXT NOT NULL,  -- 'pending' | 'running' | 'completed' | 'failed'
            progress REAL DEFAULT 0.0,
            message TEXT,
            error TEXT,
            collected_count INTEGER DEFAULT 0,
            skipped_count INTEGER DEFAULT 0,
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            completed_at TEXT
        )
    """)


def _create_analysis_jobs_table(conn: sqlite3.Connection) -> None:
    """Create analysis_jobs table."""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS analysis_jobs (
            job_id TEXT PRIMARY KEY,
            data_set_id INTEGER NOT NULL,
            status TEXT NOT NULL,  -- 'pending' | 'running' | 'completed' | 'failed'
            progress REAL DEFAULT 0.0,
            message TEXT,
            error TEXT,
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            completed_at TEXT,
            FOREIGN KEY (data_set_id) REFERENCES data_sets(id)
        )
    """)


def _create_analysis_results_table(conn: sqlite3.Connection) -> None:
    """Create analysis_results table."""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS analysis_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id TEXT UNIQUE NOT NULL,
            data_set_id INTEGER NOT NULL,
            analysis_summary TEXT NOT NULL,  -- JSON
            technical_indicators TEXT NOT NULL,  -- JSON
            statistics TEXT NOT NULL,  -- JSON
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            FOREIGN KEY (job_id) REFERENCES analysis_jobs(job_id),
            FOREIGN KEY (data_set_id) REFERENCES data_sets(id)
        )
    """)


def _create_algorithms_table(conn: sqlite3.Connection) -> None:
    """Create algorithms table (selected algorithms)."""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS algorithms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            definition TEXT NOT NULL,  -- JSON
            proposal_id TEXT,  -- Reference to algorithm_proposals if from proposal
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            updated_at TEXT NOT NULL DEFAULT (datetime('now'))
        )
    """)


def _create_proposal_generation_jobs_table(conn: sqlite3.Connection) -> None:
    """Create proposal_generation_jobs table."""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS proposal_generation_jobs (
            job_id TEXT PRIMARY KEY,
            data_set_id INTEGER NOT NULL,
            analysis_id INTEGER,
            num_proposals INTEGER DEFAULT 5,
            user_preferences TEXT,  -- JSON
            status TEXT NOT NULL,  -- 'pending' | 'analyzing' | 'generating' | 'completed' | 'failed'
            progress REAL DEFAULT 0.0,
            message TEXT,
            error TEXT,
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            completed_at TEXT,
            FOREIGN KEY (data_set_id) REFERENCES data_sets(id),
            FOREIGN KEY (analysis_id) REFERENCES analysis_results(id)
        )
    """)


def _create_algorithm_proposals_table(conn: sqlite3.Connection) -> None:
    """Create algorithm_proposals table."""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS algorithm_proposals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            proposal_id TEXT UNIQUE NOT NULL,
            job_id TEXT NOT NULL,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            rationale TEXT NOT NULL,
            expected_performance TEXT,  -- JSON
            definition TEXT NOT NULL,  -- JSON
            confidence_score REAL,
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            FOREIGN KEY (job_id) REFERENCES proposal_generation_jobs(job_id)
        )
    """)


def _create_backtest_jobs_table(conn: sqlite3.Connection) -> None:
    """Create backtest_jobs table."""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS backtest_jobs (
            job_id TEXT PRIMARY KEY,
            algorithm_id INTEGER NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            data_set_id INTEGER,
            status TEXT NOT NULL,  -- 'pending' | 'running' | 'completed' | 'failed'
            progress REAL DEFAULT 0.0,
            message TEXT,
            error TEXT,
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            completed_at TEXT,
            FOREIGN KEY (algorithm_id) REFERENCES algorithms(id),
            FOREIGN KEY (data_set_id) REFERENCES data_sets(id)
        )
    """)


def _create_backtest_results_table(conn: sqlite3.Connection) -> None:
    """Create backtest_results table."""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS backtest_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id TEXT UNIQUE NOT NULL,
            algorithm_id INTEGER NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            total_return REAL,
            sharpe_ratio REAL,
            max_drawdown REAL,
            win_rate REAL,
            total_trades INTEGER,
            average_profit REAL,
            average_loss REAL,
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            FOREIGN KEY (job_id) REFERENCES backtest_jobs(job_id),
            FOREIGN KEY (algorithm_id) REFERENCES algorithms(id)
        )
    """)


def _create_backtest_trades_table(conn: sqlite3.Connection) -> None:
    """Create backtest_trades table."""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS backtest_trades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id TEXT NOT NULL,
            entry_date TEXT NOT NULL,
            exit_date TEXT NOT NULL,
            entry_price REAL NOT NULL,
            exit_price REAL NOT NULL,
            quantity REAL NOT NULL,
            profit REAL NOT NULL,
            profit_rate REAL NOT NULL,
            FOREIGN KEY (job_id) REFERENCES backtest_jobs(job_id)
        )
    """)


def _create_backtest_equity_curve_table(conn: sqlite3.Connection) -> None:
    """Create backtest_equity_curve table."""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS backtest_equity_curve (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id TEXT NOT NULL,
            date TEXT NOT NULL,
            equity REAL NOT NULL,
            FOREIGN KEY (job_id) REFERENCES backtest_jobs(job_id)
        )
    """)


def _create_stock_prediction_jobs_table(conn: sqlite3.Connection) -> None:
    """Create stock_prediction_jobs table."""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS stock_prediction_jobs (
            job_id TEXT PRIMARY KEY,
            news_job_id TEXT,
            num_predictions INTEGER DEFAULT 5,
            user_preferences TEXT,  -- JSON
            market_trends TEXT,  -- JSON or text
            status TEXT NOT NULL,  -- 'pending' | 'analyzing' | 'generating' | 'completed' | 'failed'
            progress REAL DEFAULT 0.0,
            message TEXT,
            error TEXT,
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            completed_at TEXT,
            FOREIGN KEY (news_job_id) REFERENCES news_collection_jobs(job_id)
        )
    """)


def _create_stock_predictions_table(conn: sqlite3.Connection) -> None:
    """Create stock_predictions table."""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS stock_predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prediction_id TEXT UNIQUE NOT NULL,
            job_id TEXT NOT NULL,
            symbol TEXT NOT NULL,
            name TEXT NOT NULL,
            predicted_direction TEXT NOT NULL,  -- 'up' | 'down' | 'sideways'
            predicted_change_percent REAL,
            confidence_score REAL,
            rationale TEXT NOT NULL,
            association_chain TEXT,  -- JSON array
            recommended_action TEXT NOT NULL,  -- 'buy' | 'sell' | 'hold' | 'watch'
            risk_factors TEXT,  -- JSON array
            time_horizon TEXT,  -- '短期' | '中期' | '長期'
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            FOREIGN KEY (job_id) REFERENCES stock_prediction_jobs(job_id)
        )
    """)


def _create_indexes(conn: sqlite3.Connection) -> None:
    """Create database indexes for performance optimization."""
    indexes = [
        # OHLCV data indexes
        "CREATE INDEX IF NOT EXISTS idx_ohlcv_data_set_id ON ohlcv_data(data_set_id)",
        "CREATE INDEX IF NOT EXISTS idx_ohlcv_date ON ohlcv_data(date)",
        
        # Market news indexes
        "CREATE INDEX IF NOT EXISTS idx_market_news_published_at ON market_news(published_at)",
        "CREATE INDEX IF NOT EXISTS idx_market_news_source ON market_news(source)",
        
        # News collection indexes
        "CREATE INDEX IF NOT EXISTS idx_news_collection_jobs_status ON news_collection_jobs(status)",
        "CREATE INDEX IF NOT EXISTS idx_news_collection_jobs_created_at ON news_collection_jobs(created_at)",
        
        # Analysis indexes
        "CREATE INDEX IF NOT EXISTS idx_analysis_jobs_status ON analysis_jobs(status)",
        "CREATE INDEX IF NOT EXISTS idx_analysis_jobs_data_set_id ON analysis_jobs(data_set_id)",
        
        # Proposal indexes
        "CREATE INDEX IF NOT EXISTS idx_proposal_jobs_status ON proposal_generation_jobs(status)",
        "CREATE INDEX IF NOT EXISTS idx_proposal_jobs_created_at ON proposal_generation_jobs(created_at)",
        "CREATE INDEX IF NOT EXISTS idx_algorithm_proposals_job_id ON algorithm_proposals(job_id)",
        "CREATE INDEX IF NOT EXISTS idx_algorithm_proposals_proposal_id ON algorithm_proposals(proposal_id)",
        
        # Backtest indexes
        "CREATE INDEX IF NOT EXISTS idx_backtest_jobs_status ON backtest_jobs(status)",
        "CREATE INDEX IF NOT EXISTS idx_backtest_jobs_algorithm_id ON backtest_jobs(algorithm_id)",
        "CREATE INDEX IF NOT EXISTS idx_backtest_trades_job_id ON backtest_trades(job_id)",
        "CREATE INDEX IF NOT EXISTS idx_backtest_equity_job_id ON backtest_equity_curve(job_id)",
        
        # Stock prediction indexes
        "CREATE INDEX IF NOT EXISTS idx_stock_prediction_jobs_status ON stock_prediction_jobs(status)",
        "CREATE INDEX IF NOT EXISTS idx_stock_prediction_jobs_created_at ON stock_prediction_jobs(created_at)",
        "CREATE INDEX IF NOT EXISTS idx_stock_prediction_jobs_news_job_id ON stock_prediction_jobs(news_job_id)",
        "CREATE INDEX IF NOT EXISTS idx_stock_predictions_job_id ON stock_predictions(job_id)",
        "CREATE INDEX IF NOT EXISTS idx_stock_predictions_prediction_id ON stock_predictions(prediction_id)",
        "CREATE INDEX IF NOT EXISTS idx_stock_predictions_symbol ON stock_predictions(symbol)",
    ]
    
    for index_sql in indexes:
        conn.execute(index_sql)

