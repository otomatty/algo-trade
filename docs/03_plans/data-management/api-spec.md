# データ管理機能 API仕様書

## 概要

データ管理機能で使用するTauriコマンドの詳細仕様です。

## Tauriコマンド一覧

### `import_ohlcv_data`

CSVファイルからOHLCVデータをインポートします。

#### リクエスト

```typescript
interface ImportOHLCVDataRequest {
  file_path: string;
  name?: string;
}

invoke('import_ohlcv_data', {
  file_path: '/path/to/data.csv',
  name: 'My Dataset'
})
```

#### レスポンス

```typescript
{
  success: boolean;
  message: string;
  data_set_id?: number;
}
```

### `get_data_list`

データセット一覧を取得します。

#### リクエスト

引数なし

#### レスポンス

```typescript
{
  data_list: Array<{
    id: number;
    name: string;
    symbol?: string;
    start_date: string;
    end_date: string;
    record_count: number;
    imported_at: string;
  }>;
}
```

### `delete_data_set`

データセットを削除します。

#### リクエスト

```typescript
interface DeleteDataSetRequest {
  data_set_id: number;
}
```

#### レスポンス

```typescript
{
  success: boolean;
  message?: string;
}
```

