# データ管理機能 実装計画

## 概要

株価データ（OHLCV）のインポート、外部APIからの自動収集設定、データセット管理を行う機能です。

## 関連ドキュメント

- **要件定義**: `docs/01_issues/open/2025_11/20251101_01_trend-association-algorithm-platform.md` (SCREEN-005)
- **仕様書**: `src/pages/DataManagement/DataManagement.spec.md` (作成予定)
- **テスト**: `src/pages/DataManagement/DataManagement.test.tsx` (作成予定)

## 実装フェーズ

### Phase 1: CSVインポート機能

**目標**: CSVファイルから株価データをインポート

**タスク**:
- [ ] ファイル選択UIの実装
- [ ] `import_ohlcv_data()` Tauriコマンドの実装（バックエンド）
- [ ] CSVパース処理の実装
- [ ] データバリデーションの実装
- [ ] インポート進捗表示の実装
- [ ] エラーハンドリングの実装

**技術スタック**:
- React 19.x
- TypeScript 5.x
- Mantine UI (FileInput)
- Python (Pandas)
- PyTauri

**依存関係**:
- なし（最初に実装する機能の一つ）

### Phase 2: データセット一覧表示

**目標**: インポート済みデータセットの一覧表示

**タスク**:
- [ ] `get_data_list()` Tauriコマンドの実装
- [ ] データセット一覧テーブルの実装
- [ ] データセット情報カードの実装
- [ ] ソート・フィルタ機能の実装

**技術スタック**:
- Mantine Table
- Tauri invoke API

**依存関係**:
- Phase 1完了

### Phase 3: データ削除機能

**目標**: データセットの削除機能

**タスク**:
- [ ] 削除ボタンの実装
- [ ] 削除確認ダイアログの実装
- [ ] データベースからの削除処理（バックエンド）
- [ ] 削除後の一覧更新

**技術スタック**:
- Mantine Dialog
- SQLite

**依存関係**:
- Phase 2完了

### Phase 4: 外部API自動収集設定

**目標**: 外部APIからの自動データ収集設定

**タスク**:
- [ ] `configure_data_collection()` Tauriコマンドの実装
- [ ] API設定フォームの実装
- [ ] スケジュール設定の実装
- [ ] 設定保存機能の実装

**技術スタック**:
- Mantine Form
- Python scheduler (APScheduler等)

**依存関係**:
- Phase 2完了
- データ収集機能（バックエンド）

### Phase 5: データプレビュー機能

**目標**: データセットの内容をプレビュー表示

**タスク**:
- [ ] データプレビューモーダルの実装
- [ ] データテーブル表示の実装
- [ ] 基本統計情報の表示

**技術スタック**:
- Mantine Modal, Table
- Pandas (統計計算)

**依存関係**:
- Phase 2完了

## 技術的な詳細

### コンポーネント構造

```
DataManagement/
├── DataManagement.tsx         # メインコンポーネント
├── DataImportForm.tsx         # CSVインポートフォーム
├── DataSetList.tsx            # データセット一覧
├── DataSetCard.tsx            # データセットカード
├── DataPreviewModal.tsx       # データプレビューモーダル
├── APIConfigForm.tsx          # API設定フォーム
└── DataManagement.spec.md     # 仕様書
```

### 状態管理

```typescript
interface DataManagementState {
  dataSets: DataSet[];
  selectedDataSetId: number | null;
  importProgress: number;
  importing: boolean;
  error: string | null;
}
```

### CSV形式要件

```typescript
interface CSVFormat {
  requiredColumns: ['date', 'open', 'high', 'low', 'close', 'volume'];
  dateFormats: ['YYYY-MM-DD', 'YYYY/MM/DD'];
  encoding: 'UTF-8';
}
```

### API連携

- `import_ohlcv_data(file_path, name?)`: CSVファイルインポート
- `get_data_list()`: データセット一覧取得
- `delete_data_set(data_set_id)`: データセット削除
- `configure_data_collection(config)`: 自動収集設定
- `get_data_preview(data_set_id, limit?)`: データプレビュー取得

## テスト計画

### 単体テスト

- [ ] DataImportFormコンポーネントのテスト
- [ ] DataSetListコンポーネントのテスト
- [ ] CSVパース処理のテスト
- [ ] データバリデーションのテスト

### 統合テスト

- [ ] CSVインポートフローの統合テスト
- [ ] データ削除の統合テスト
- [ ] エラーハンドリングのテスト

### E2Eテスト

- [ ] CSVインポートのE2Eテスト
- [ ] データセット管理のE2Eテスト

## 実装優先度

**最高**: Phase 1, Phase 2（必須機能）
**高**: Phase 3（削除機能）
**中**: Phase 4, Phase 5（拡張機能）

## 注意事項

- CSVファイルのエンコーディング対応（UTF-8, Shift-JIS等）
- 大量データのインポート時のパフォーマンス
- データバリデーションの堅牢性
- ファイルサイズ制限の設定
- エラーメッセージの分かりやすさ
- データベースの整合性管理

