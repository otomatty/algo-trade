# テスト実行コマンドガイド

## 概要

このプロジェクトでは、Python（pytest）とTypeScript（Bun test）の2種類のテストがあります。

## セットアップ

### Pythonテスト環境のセットアップ

まず、Pythonの依存関係をインストールしてください：

```bash
cd src-python
pip install -r requirements.txt
```

または、仮想環境を使用する場合：

```bash
cd src-python
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# または
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

## TypeScript/Reactテスト（Bun）

### すべてのテストを実行
```bash
bun run test
# または
bun run test:ts
```

### ウォッチモード（ファイル変更時に自動実行）
```bash
bun run test:ts:watch
```

### カバレッジ付きで実行
```bash
bun run test:ts:coverage
```

### 特定のテストファイルを実行
```bash
bun test src/pages/DataManagement/DataImportForm.test.tsx
```

### 特定のテストを実行（パターンマッチ）
```bash
bun test --test-name-pattern "should import CSV"
```

## Pythonテスト（pytest）

### すべてのテストを実行
```bash
bun run test:python
```

### 単体テストのみ実行
```bash
bun run test:python:unit
```

### 統合テストのみ実行
```bash
bun run test:python:integration
```

### カバレッジ付きで実行
```bash
bun run test:python:cov
```

### 詳細出力で実行
```bash
bun run test:python:verbose
```

### 特定のテストファイルを実行

#### CSVインポーターのテスト
```bash
bun run test:python:csv
```

#### APIクライアントのテスト
```bash
bun run test:python:api
```

#### データコレクターのテスト
```bash
bun run test:python:collector
```

#### データベース操作のテスト
```bash
bun run test:python:db
```

#### データ収集フローの統合テスト
```bash
bun run test:python:flow
```

### 特定のテストクラスを実行
```bash
cd src-python && python3 -m pytest tests/unit/test_csv_importer.py::TestCSVImporter
```

### 特定のテスト関数を実行
```bash
cd src-python && python3 -m pytest tests/unit/test_csv_importer.py::TestCSVImporter::test_import_csv_success
```

### すべてのテストを実行
```bash
bun run test
# または
bun run test:ts
```

### ウォッチモード（ファイル変更時に自動実行）
```bash
bun run test:ts:watch
```

### カバレッジ付きで実行
```bash
bun run test:ts:coverage
```

### 特定のテストファイルを実行
```bash
bun test src/pages/DataManagement/DataImportForm.test.tsx
```

### 特定のテストを実行（パターンマッチ）
```bash
bun test --test-name-pattern "should import CSV"
```

## Pythonテスト（pytest）

### すべてのテストを実行
```bash
bun run test:python
```

### 単体テストのみ実行
```bash
bun run test:python:unit
```

### 統合テストのみ実行
```bash
bun run test:python:integration
```

### カバレッジ付きで実行
```bash
bun run test:python:cov
```

### 詳細出力で実行
```bash
bun run test:python:verbose
```

### 特定のテストファイルを実行

#### CSVインポーターのテスト
```bash
bun run test:python:csv
```

#### APIクライアントのテスト
```bash
bun run test:python:api
```

#### データコレクターのテスト
```bash
bun run test:python:collector
```

#### データベース操作のテスト
```bash
bun run test:python:db
```

#### データ収集フローの統合テスト
```bash
bun run test:python:flow
```

### 特定のテストクラスを実行
```bash
cd src-python && python3 -m pytest tests/unit/test_csv_importer.py::TestCSVImporter
```

### 特定のテスト関数を実行
```bash
cd src-python && python3 -m pytest tests/unit/test_csv_importer.py::TestCSVImporter::test_import_csv_success
```

## すべてのテストを実行

### PythonとTypeScriptの両方を実行
```bash
bun run test:all
```

## テストの構造

### TypeScriptテスト
```
src/
├── pages/
│   └── DataManagement/
│       ├── DataImportForm.test.tsx
│       ├── DataManagement.test.tsx
│       └── DataManagement.additional.test.tsx
└── types/
    └── data.test.ts
```

### Pythonテスト
```
src-python/
├── tests/
│   ├── unit/              # 単体テスト
│   │   ├── test_csv_importer.py
│   │   ├── test_api_clients.py
│   │   ├── test_data_collector.py
│   │   ├── test_database_schema.py
│   │   └── test_database_operations.py
│   └── integration/       # 統合テスト
│       └── test_data_collection_flow.py
```

## 注意事項

- Pythonテストは一時データベースを使用します（`conftest.py`の`temp_db`フィクスチャ）
- APIクライアントのテストはモックを使用します（実際のAPI呼び出しは行いません）
- TypeScriptテストは`bun-types`パッケージが必要です
- Pythonテストは`pytest-mock`パッケージが必要です

