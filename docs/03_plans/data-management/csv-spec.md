# CSV形式仕様

## 必須カラム

- `date`: 日付 (YYYY-MM-DD または YYYY/MM/DD)
- `open`: 始値
- `high`: 高値
- `low`: 安値
- `close`: 終値
- `volume`: 出来高

## 例

```csv
date,open,high,low,close,volume
2023-01-01,100.0,105.0,99.0,103.0,1000000
2023-01-02,103.0,108.0,102.0,106.0,1200000
```

## バリデーション

- 日付形式の検証
- 数値の範囲チェック（価格 > 0, 出来高 >= 0）
- データの整合性（high >= low, high >= open, high >= close等）

