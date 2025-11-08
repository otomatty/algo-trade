# LLM連携 API仕様

## 内部API

LLM連携は主にバックエンド内部で使用されます。

### LLMClient

```python
class LLMClient:
    def generate_algorithm_proposals(self, analysis_results, user_preferences) -> List[AlgorithmProposal]:
        pass
    
    def generate_stock_predictions(self, news, market_trends) -> List[StockPrediction]:
        pass
```

## 設定

### APIキー管理

- 環境変数または設定ファイルから読み込み
- 暗号化して保存

