# 技術スタック決定

## 決定日
2025-01-01

## 決定内容

### アーキテクチャ
- **フロントエンド**: Tauri 2.0 + React 19 + TypeScript + Mantine UI
- **バックエンド**: Rust (Tauriコマンド) + Python (データ分析・LLM連携)
- **通信方式**: RustコマンドからPythonスクリプトを実行する方式

### 選択理由

#### Pythonバックエンドを採用した理由
1. **データ分析ライブラリの豊富さ**: Pandas, NumPy, TA-Lib等の実績あるライブラリが利用可能
2. **LLM APIクライアント**: OpenAI, Anthropicの公式Pythonライブラリが充実
3. **計画ドキュメントとの整合性**: 既存の計画ドキュメントがPythonベースで設計されている

#### Rust + Pythonハイブリッド方式を採用した理由
1. **Tauri 2.0の制約**: PyTauriの直接統合が困難
2. **パフォーマンス**: RustでTauriコマンドを実装し、重い処理はPythonで実行
3. **柔軟性**: Pythonの豊富なエコシステムを活用しつつ、Tauriの利点を維持

### 実装方式

#### Rustコマンド → Pythonスクリプト実行
```rust
// Rust側: Tauriコマンド
#[tauri::command]
async fn import_ohlcv_data(file_path: String) -> Result<DataSet, String> {
    // Pythonスクリプトを実行
    let output = Command::new("python3")
        .arg("src-python/scripts/import_ohlcv.py")
        .arg(&file_path)
        .output()
        .await?;
    
    // JSONレスポンスをパース
    let result: DataSet = serde_json::from_slice(&output.stdout)?;
    Ok(result)
}
```

#### Python側: スクリプトベース
- `src-python/` ディレクトリにPythonコードを配置
- 各機能ごとにモジュール化
- JSON形式でRustと通信

### ディレクトリ構造
```
algo-trade/
├── src/                    # React フロントエンド
├── src-tauri/              # Rust バックエンド
└── src-python/             # Python バックエンド
    ├── scripts/             # 実行可能スクリプト
    ├── modules/             # 機能モジュール
    │   ├── data_collection/
    │   ├── data_analysis/
    │   ├── llm_integration/
    │   └── ...
    ├── database/            # データベース管理
    └── requirements.txt     # Python依存関係
```

### データベース
- **SQLite**: ローカルデータベースとして使用
- **マイグレーション**: Python側で管理（Alembic等を検討）

### 型定義の共有
- **TypeScript型定義**: `src/types/` に配置
- **Python型定義**: Pydanticを使用して型安全性を確保
- **Rust型定義**: Serdeを使用してJSONシリアライゼーション

## 次のステップ
1. プロジェクト構造の整備（src-python/ ディレクトリ作成）
2. Python依存関係の定義（requirements.txt）
3. RustコマンドからPythonスクリプト実行の基盤実装
4. データベーススキーマの統一設計

