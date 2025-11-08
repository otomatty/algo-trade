# pytest テストガイド

## 概要

このプロジェクトでは、Pythonのテストに**pytest**を使用しています。pytestのベストプラクティスに従ってテストを実装しています。

## pytestの特徴

- **フィクスチャ**: `@pytest.fixture`デコレータを使用したテストデータの共有
- **マーカー**: `@pytest.mark`を使用したテストの分類
- **mocker**: `pytest-mock`の`mocker`フィクスチャを使用したモック（`unittest.mock`の代わり）

## テストの実行

### すべてのテストを実行
```bash
cd src-python
pytest
```

### 単体テストのみ実行
```bash
cd src-python
pytest -m unit
```

### 統合テストのみ実行
```bash
cd src-python
pytest -m integration
```

### カバレッジ付きで実行
```bash
cd src-python
pytest --cov=. --cov-report=html
```

### 特定のテストファイルを実行
```bash
cd src-python
pytest tests/unit/test_csv_importer.py
```

### 特定のテストクラスを実行
```bash
cd src-python
pytest tests/unit/test_csv_importer.py::TestCSVImporter
```

### 特定のテスト関数を実行
```bash
cd src-python
pytest tests/unit/test_csv_importer.py::TestCSVImporter::test_import_csv_success
```

## テストマーカー

- `@pytest.mark.unit`: 単体テスト
- `@pytest.mark.integration`: 統合テスト
- `@pytest.mark.slow`: 実行に時間がかかるテスト

## モックの使用

`unittest.mock`の代わりに`pytest-mock`の`mocker`フィクスチャを使用します：

```python
def test_example(mocker):
    # モックの作成
    mock_obj = mocker.patch('module.Class')
    mock_instance = mocker.MagicMock()
    mock_obj.return_value = mock_instance
    
    # テストの実行
    # ...
```

## フィクスチャ

`conftest.py`で定義されたフィクスチャ：

- `temp_db`: 一時データベースを作成（テスト後に自動削除）
- `sample_csv_data`: サンプルCSVデータ
- `sample_csv_file`: サンプルCSVファイル（一時ファイル）

## テストの構造

```
src-python/
├── tests/
│   ├── conftest.py          # pytest設定とフィクスチャ
│   ├── unit/                # 単体テスト
│   │   ├── test_csv_importer.py
│   │   ├── test_api_clients.py
│   │   ├── test_data_collector.py
│   │   ├── test_database_schema.py
│   │   └── test_database_operations.py
│   └── integration/         # 統合テスト
│       └── test_data_collection_flow.py
└── pytest.ini               # pytest設定ファイル
```

## 注意事項

- テストは一時データベースを使用します（`temp_db`フィクスチャ）
- APIクライアントのテストはモックを使用します（実際のAPI呼び出しは行いません）
- `CSVImporter`と`DataCollector`はテスト用に`conn`パラメータを受け取れるように実装されています

