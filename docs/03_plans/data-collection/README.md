# データ収集（バックエンド）実装計画

## 概要

外部APIやCSVファイルから株価データ（OHLCV）を収集するバックエンド機能の実装計画です。

## 関連ドキュメント

- **要件定義**: `docs/01_issues/open/2025_11/20251101_01_trend-association-algorithm-platform.md`
- **依存機能**: データ管理機能 (`docs/03_plans/data-management/`)

## 実装フェーズ

### Phase 1: CSVインポート処理

**目標**: CSVファイルからOHLCVデータをインポート

**タスク**:
- [ ] CSVパーサーの実装
- [ ] データバリデーションの実装
- [ ] データ正規化処理の実装
- [ ] データベース保存処理の実装
- [ ] エラーハンドリングの実装

**技術スタック**:
- Python 3.10+
- Pandas
- SQLite
- PyTauri

**依存関係**:
- なし（最初に実装）

### Phase 2: 外部API連携基盤

**目標**: 外部APIへの接続基盤を実装

**タスク**:
- [ ] HTTPクライアントの実装
- [ ] API認証処理の実装
- [ ] レート制限対応の実装
- [ ] エラーハンドリングの実装
- [ ] リトライ機構の実装

**技術スタック**:
- Python 3.10+
- requests / httpx
- PyTauri

**依存関係**:
- Phase 1完了

### Phase 3: 主要データソース実装

**目標**: 主要なデータソース（Yahoo Finance等）の実装

**タスク**:
- [ ] Yahoo Finance APIクライアントの実装
- [ ] Alpha Vantage APIクライアントの実装（オプション）
- [ ] その他主要データソースの実装
- [ ] データ形式の統一処理

**技術スタック**:
- yfinance (Yahoo Finance)
- requests / httpx

**依存関係**:
- Phase 2完了

### Phase 4: 自動収集スケジューラー

**目標**: 定期的なデータ収集の自動化

**タスク**:
- [ ] スケジューラー実装（APScheduler等）
- [ ] スケジュール設定の保存・読み込み
- [ ] ジョブ管理機能の実装
- [ ] エラー通知機能の実装

**技術スタック**:
- APScheduler
- SQLite

**依存関係**:
- Phase 3完了

### Phase 5: データ更新・差分管理

**目標**: 既存データの更新と差分管理

**タスク**:
- [ ] データ更新チェック機能の実装
- [ ] 差分データの取得・適用処理
- [ ] データ整合性チェック機能の実装

**技術スタック**:
- Pandas
- SQLite

**依存関係**:
- Phase 4完了

## 技術的な詳細

### CSVパーサー設計

```python
class CSVImporter:
    def __init__(self):
        self.required_columns = ['date', 'open', 'high', 'low', 'close', 'volume']
        self.date_formats = ['%Y-%m-%d', '%Y/%m/%d']
    
    def import_csv(self, file_path: str, name: str = None) -> int:
        # 1. CSV読み込み
        df = pd.read_csv(file_path)
        
        # 2. バリデーション
        self._validate_columns(df)
        self._validate_data(df)
        
        # 3. データ正規化
        df = self._normalize_data(df)
        
        # 4. データベース保存
        data_set_id = self._save_to_database(df, name)
        
        return data_set_id
    
    def _validate_columns(self, df):
        # 必須カラムのチェック
        pass
    
    def _validate_data(self, df):
        # データ型、範囲のチェック
        pass
    
    def _normalize_data(self, df):
        # 日付形式の統一、データ型の変換
        pass
```

### APIクライアント設計

```python
class DataSourceClient:
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.session = requests.Session()
    
    def fetch_ohlcv(self, symbol: str, start_date: str, end_date: str):
        # API呼び出し
        response = self._make_request(symbol, start_date, end_date)
        # データ変換
        df = self._parse_response(response)
        return df
    
    def _make_request(self, symbol, start_date, end_date):
        # レート制限チェック
        self._check_rate_limit()
        # API呼び出し
        pass
```

### スケジューラー設計

```python
from apscheduler.schedulers.background import BackgroundScheduler

class DataCollectionScheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
    
    def schedule_collection(self, config: CollectionConfig):
        # スケジュール登録
        self.scheduler.add_job(
            self._collect_data,
            trigger=config.trigger,
            args=[config],
            id=config.job_id
        )
    
    def _collect_data(self, config: CollectionConfig):
        # データ収集実行
        pass
```

### データベーススキーマ

```sql
CREATE TABLE data_sets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    symbol TEXT,
    start_date TEXT,
    end_date TEXT,
    record_count INTEGER,
    imported_at TEXT,
    source TEXT -- 'csv' | 'api' | 'manual'
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

## テスト計画

### 単体テスト

- [ ] CSVパーサーのテスト
- [ ] データバリデーションのテスト
- [ ] APIクライアントのテスト（モック）
- [ ] スケジューラーのテスト

### 統合テスト

- [ ] CSVインポートフローの統合テスト
- [ ] APIデータ収集の統合テスト
- [ ] スケジューラーの統合テスト

## 実装優先度

**最高**: Phase 1, Phase 2（必須機能）
**高**: Phase 3（主要データソース）
**中**: Phase 4, Phase 5（自動化・最適化）

## 注意事項

- CSVファイルのエンコーディング対応（UTF-8, Shift-JIS等）
- データバリデーションの堅牢性
- APIレート制限への対応
- エラーハンドリング（ネットワークエラー、APIエラー等）
- データ整合性の保証
- 大量データの処理パフォーマンス
- スケジューラーの安定性

