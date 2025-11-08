# データ収集 データモデル

## Pythonデータクラス

```python
@dataclass
class DataSet:
    id: int
    name: str
    symbol: Optional[str]
    start_date: str
    end_date: str
    record_count: int
    imported_at: str
```

