# データ管理機能 データモデル詳細

## TypeScript型定義

```typescript
interface DataSet {
  id: number;
  name: string;
  symbol?: string;
  start_date: string;
  end_date: string;
  record_count: number;
  imported_at: string;
}

interface OHLCVData {
  date: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
}
```

## データベーススキーマ

```sql
CREATE TABLE data_sets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    symbol TEXT,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    record_count INTEGER,
    imported_at TEXT NOT NULL
);

CREATE TABLE ohlcv_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data_set_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    open REAL NOT NULL,
    high REAL NOT NULL,
    low REAL NOT NULL,
    close REAL NOT NULL,
    volume INTEGER NOT NULL,
    FOREIGN KEY (data_set_id) REFERENCES data_sets(id)
);
```

