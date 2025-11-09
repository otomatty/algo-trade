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

### `get_data_preview`

データセットのプレビュー（OHLCVデータと統計情報）を取得します。

#### リクエスト

```typescript
interface GetDataPreviewRequest {
  data_set_id: number;
  limit?: number;  // Optional, default: 100
}

invoke('get_data_preview', {
  data_set_id: 1,
  limit: 100
})
```

#### レスポンス

```typescript
{
  data_set_id: number;
  data: Array<{
    id: number;
    data_set_id: number;
    date: string;
    open: number;
    high: number;
    low: number;
    close: number;
    volume: number;
  }>;
  statistics: {
    count: number;
    date_range: {
      start: string;
      end: string;
    };
    open: { mean: number; min: number; max: number; std: number };
    high: { mean: number; min: number; max: number; std: number };
    low: { mean: number; min: number; max: number; std: number };
    close: { mean: number; min: number; max: number; std: number };
    volume: { mean: number; min: number; max: number; std: number };
  };
}
```

#### エラー

- `data_set_id is required`: data_set_idが指定されていない場合
- `limit must be greater than 0`: limitが0以下の場合
- `Data set with id {id} not found`: 指定されたデータセットが存在しない場合
- `No data found for data set {id}`: データセットにデータが存在しない場合


