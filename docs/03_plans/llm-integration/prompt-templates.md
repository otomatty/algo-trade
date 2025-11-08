# プロンプトテンプレート詳細

## アルゴリズム提案用

詳細は`docs/03_plans/algorithm-proposal/llm-prompt-design.md`を参照。

## 銘柄予測用

```python
STOCK_PREDICTION_PROMPT = """
以下のニュースと市場トレンドを基に、連想的に銘柄予測を行ってください。

【ニュース】
{news_summary}

【市場トレンド】
{market_trends}

【出力形式】
JSON形式で出力してください。
"""
```

