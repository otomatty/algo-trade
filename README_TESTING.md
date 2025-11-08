# テストガイド

## テスト環境

このプロジェクトでは以下のテストフレームワークを使用しています：

- **Python**: pytest
- **TypeScript/React**: Bun テストフレームワーク
- **Rust**: Rust標準テストフレームワーク

## テストの実行

### Pythonバックエンドのテスト

```bash
# すべてのテストを実行
bun run test:python

# カバレッジ付きで実行
bun run test:python:cov

# 特定のテストファイルを実行
cd src-python && pytest tests/unit/test_csv_importer.py

# 特定のテストクラスを実行
cd src-python && pytest tests/unit/test_csv_importer.py::TestCSVImporter
```

### TypeScriptフロントエンドのテスト

```bash
# すべてのテストを実行
bun run test

# 特定のテストファイルを実行
bun test src/pages/DataManagement/DataManagement.test.tsx
```

### Rustバックエンドのテスト

```bash
cd src-tauri
cargo test
```

## テスト構造

```
src-python/
├── tests/
│   ├── unit/              # 単体テスト
│   │   ├── test_csv_importer.py
│   │   └── test_database_schema.py
│   ├── integration/       # 統合テスト
│   │   └── test_data_collection_flow.py
│   └── conftest.py        # pytest設定とフィクスチャ

src/
├── pages/
│   └── DataManagement/
│       ├── DataManagement.test.tsx
│       └── DataImportForm.test.tsx
└── types/
    └── data.test.ts

src-tauri/
└── tests/
    └── integration_test.rs
```

## テストカバレッジ

現在のテストカバレッジ：

- ✅ CSVインポート処理
- ✅ データベーススキーマ
- ✅ データ収集フロー（統合テスト）
- ✅ DataManagementコンポーネント
- ✅ DataImportFormコンポーネント
- ✅ 型定義

## テストの追加

新しい機能を実装する際は、以下の順序でテストを追加してください：

1. **単体テスト**: 個別の関数・クラスのテスト
2. **統合テスト**: 複数コンポーネント間の連携テスト
3. **E2Eテスト**: エンドツーエンドのフローテスト

## 注意事項

- Pythonテストは一時データベースを使用します（`conftest.py`の`temp_db`フィクスチャ）
- Tauriコマンドのテストはモックを使用します
- テストデータは`conftest.py`のフィクスチャで管理します

