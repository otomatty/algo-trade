#!/usr/bin/env python3
"""
Script to initialize the database.
Should be run once at application startup.
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from database.connection import init_database


def main():
    """Main entry point."""
    try:
        init_database()
        print("Database initialized successfully")
    except Exception as e:
        print(f"Error initializing database: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()

