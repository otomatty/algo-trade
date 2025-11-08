# データ収集 API仕様

## 内部API

データ収集は主にバックエンド内部で使用されます。

### CSVImporter

```python
class CSVImporter:
    def import_csv(self, file_path: str, name: str = None) -> int:
        pass
```

### DataSourceClient

```python
class DataSourceClient:
    def fetch_ohlcv(self, symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
        pass
```

