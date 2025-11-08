"""
Database connection management.
"""
import sqlite3
import os
from pathlib import Path
from typing import Optional


def get_db_path() -> str:
    """
    Get the path to the SQLite database file.
    """
    # Use app data directory for production, local for development
    if os.getenv("TAURI_ENV") == "production":
        # In production, use Tauri's app data directory
        app_data_dir = os.getenv("APPDATA") or os.getenv("HOME")
        db_dir = Path(app_data_dir) / "algo-trade"
        db_dir.mkdir(parents=True, exist_ok=True)
        return str(db_dir / "algo_trade.db")
    else:
        # In development, use project root
        project_root = Path(__file__).parent.parent.parent
        db_path = project_root / "algo_trade.db"
        return str(db_path)


def get_connection() -> sqlite3.Connection:
    """
    Get a database connection.
    """
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Enable column access by name
    return conn


def init_database() -> None:
    """
    Initialize the database with all required tables.
    This should be called once at application startup.
    """
    from .schema import create_all_tables
    
    conn = get_connection()
    try:
        create_all_tables(conn)
        conn.commit()
    finally:
        conn.close()

