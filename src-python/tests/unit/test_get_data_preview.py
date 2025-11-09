"""
Tests for get_data_preview.py script.
"""
import pytest
import json
import sys
from pathlib import Path
from io import StringIO
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from database.connection import get_connection
from scripts.get_data_preview import main


@pytest.fixture
def sample_data_set(temp_db):
    """Create a sample data set with OHLCV data."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create data set
    cursor.execute("""
        INSERT INTO data_sets (name, symbol, start_date, end_date, record_count, imported_at, source)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, ('Test Dataset', 'AAPL', '2023-01-01', '2023-01-05', 5, datetime.now().isoformat(), 'csv'))
    
    data_set_id = cursor.lastrowid
    
    # Insert OHLCV data
    test_data = [
        ('2023-01-01', 100.0, 105.0, 99.0, 103.0, 1000000),
        ('2023-01-02', 103.0, 108.0, 102.0, 106.0, 1200000),
        ('2023-01-03', 106.0, 110.0, 105.0, 108.0, 1100000),
        ('2023-01-04', 108.0, 112.0, 107.0, 110.0, 1300000),
        ('2023-01-05', 110.0, 115.0, 109.0, 113.0, 1400000),
    ]
    
    for date, open_price, high, low, close, volume in test_data:
        cursor.execute("""
            INSERT INTO ohlcv_data (data_set_id, date, open, high, low, close, volume)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (data_set_id, date, open_price, high, low, close, volume))
    
    conn.commit()
    conn.close()
    
    return data_set_id


def test_get_data_preview_success(sample_data_set, monkeypatch):
    """Test successful data preview retrieval."""
    input_data = {
        'data_set_id': sample_data_set,
        'limit': 100
    }
    
    stdin_mock = StringIO(json.dumps(input_data))
    stdout_mock = StringIO()
    
    monkeypatch.setattr('sys.stdin', stdin_mock)
    monkeypatch.setattr('sys.stdout', stdout_mock)
    
    main()
    
    result = json.loads(stdout_mock.getvalue())
    
    assert result['success'] is True
    assert 'data' in result['data']
    assert 'statistics' in result['data']
    assert result['data']['data_set_id'] == sample_data_set
    assert len(result['data']['data']) == 5
    assert result['data']['statistics']['count'] == 5
    assert 'date_range' in result['data']['statistics']
    assert 'open' in result['data']['statistics']
    assert 'high' in result['data']['statistics']
    assert 'low' in result['data']['statistics']
    assert 'close' in result['data']['statistics']
    assert 'volume' in result['data']['statistics']


def test_get_data_preview_with_limit(sample_data_set, monkeypatch):
    """Test data preview with limit."""
    input_data = {
        'data_set_id': sample_data_set,
        'limit': 3
    }
    
    stdin_mock = StringIO(json.dumps(input_data))
    stdout_mock = StringIO()
    
    monkeypatch.setattr('sys.stdin', stdin_mock)
    monkeypatch.setattr('sys.stdout', stdout_mock)
    
    main()
    
    result = json.loads(stdout_mock.getvalue())
    
    assert result['success'] is True
    assert len(result['data']['data']) == 3


def test_get_data_preview_default_limit(sample_data_set, monkeypatch):
    """Test data preview with default limit."""
    input_data = {
        'data_set_id': sample_data_set
    }
    
    stdin_mock = StringIO(json.dumps(input_data))
    stdout_mock = StringIO()
    
    monkeypatch.setattr('sys.stdin', stdin_mock)
    monkeypatch.setattr('sys.stdout', stdout_mock)
    
    main()
    
    result = json.loads(stdout_mock.getvalue())
    
    assert result['success'] is True
    assert len(result['data']['data']) == 5  # All data should be returned


def test_get_data_preview_nonexistent_dataset(monkeypatch):
    """Test data preview with non-existent data set."""
    input_data = {
        'data_set_id': 99999,
        'limit': 100
    }
    
    stdin_mock = StringIO(json.dumps(input_data))
    stdout_mock = StringIO()
    
    monkeypatch.setattr('sys.stdin', stdin_mock)
    monkeypatch.setattr('sys.stdout', stdout_mock)
    
    main()
    
    result = json.loads(stdout_mock.getvalue())
    
    assert result['success'] is False
    assert 'not found' in result['error'].lower()


def test_get_data_preview_missing_data_set_id(monkeypatch):
    """Test data preview without data_set_id."""
    input_data = {
        'limit': 100
    }
    
    stdin_mock = StringIO(json.dumps(input_data))
    stdout_mock = StringIO()
    
    monkeypatch.setattr('sys.stdin', stdin_mock)
    monkeypatch.setattr('sys.stdout', stdout_mock)
    
    main()
    
    result = json.loads(stdout_mock.getvalue())
    
    assert result['success'] is False
    assert 'required' in result['error'].lower()


def test_get_data_preview_invalid_limit(sample_data_set, monkeypatch):
    """Test data preview with invalid limit."""
    input_data = {
        'data_set_id': sample_data_set,
        'limit': 0
    }
    
    stdin_mock = StringIO(json.dumps(input_data))
    stdout_mock = StringIO()
    
    monkeypatch.setattr('sys.stdin', stdin_mock)
    monkeypatch.setattr('sys.stdout', stdout_mock)
    
    main()
    
    result = json.loads(stdout_mock.getvalue())
    
    assert result['success'] is False
    assert 'greater than 0' in result['error'].lower()


def test_get_data_preview_statistics(sample_data_set, monkeypatch):
    """Test that statistics are calculated correctly."""
    input_data = {
        'data_set_id': sample_data_set,
        'limit': 100
    }
    
    stdin_mock = StringIO(json.dumps(input_data))
    stdout_mock = StringIO()
    
    monkeypatch.setattr('sys.stdin', stdin_mock)
    monkeypatch.setattr('sys.stdout', stdout_mock)
    
    main()
    
    result = json.loads(stdout_mock.getvalue())
    stats = result['data']['statistics']
    
    # Check that all required statistics fields exist
    for field in ['open', 'high', 'low', 'close', 'volume']:
        assert field in stats
        assert 'mean' in stats[field]
        assert 'min' in stats[field]
        assert 'max' in stats[field]
        assert 'std' in stats[field]
    
    # Check date range
    assert 'date_range' in stats
    assert 'start' in stats['date_range']
    assert 'end' in stats['date_range']
    assert stats['date_range']['start'] == '2023-01-01'
    assert stats['date_range']['end'] == '2023-01-05'

