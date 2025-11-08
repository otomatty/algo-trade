# アルゴリズム提案機能 LLMプロンプト設計

## 概要

アルゴリズム提案生成に使用するLLMプロンプトの設計詳細です。

## 関連ドキュメント

- **実装計画**: `docs/03_plans/algorithm-proposal/README.md`
- **LLM連携**: `docs/03_plans/llm-integration/README.md`

## プロンプトテンプレート

### 基本プロンプト

```python
ALGORITHM_PROPOSAL_PROMPT = """
あなたは経験豊富なアルゴリズムトレーディングの専門家です。
以下のデータ解析結果を基に、最適なトレードアルゴリズムを提案してください。

## データ解析結果

{analysis_results_summary}

### トレンド分析
- 方向: {trend_direction}
- ボラティリティ: {volatility_level}
- 主要パターン: {dominant_patterns}

### テクニカル指標
{technical_indicators_summary}

### 統計情報
- 価格範囲: {price_min} - {price_max}
- 現在価格: {current_price}
- 価格変動率: {price_change_percent}%
- 平均出来高: {volume_average}

## ユーザー設定

- リスク許容度: {risk_tolerance}
- 取引頻度: {trading_frequency}
- 好みの指標: {preferred_indicators}

## 要件

1. データ解析結果に基づいて、実用的なアルゴリズムを{num_proposals}個提案してください
2. 各アルゴリズムには以下の情報を含めてください:
   - 明確な名前
   - 詳細な説明
   - 提案理由（データ解析結果との関連性）
   - 具体的なトリガー条件とアクション
   - 期待されるパフォーマンス（可能な範囲で）
   - 信頼度スコア（0.0-1.0）

3. ユーザーのリスク許容度と取引頻度を考慮してください
4. 好みの指標がある場合は、それを優先的に使用してください

## 出力形式

以下のJSON形式で出力してください:

{{
  "proposals": [
    {{
      "name": "アルゴリズム名",
      "description": "アルゴリズムの詳細な説明（日本語、200-300文字程度）",
      "rationale": "なぜこのアルゴリズムが提案されたかの根拠（データ解析結果との関連性を含む）",
      "expected_performance": {{
        "expected_return": 数値（%）、
        "risk_level": "low" | "medium" | "high"
      }},
      "definition": {{
        "triggers": [
          {{
            "type": "rsi" | "macd" | "price" | "volume" | "moving_average",
            "condition": {{
              "operator": "gt" | "lt" | "gte" | "lte" | "eq" | "between" | "cross_above" | "cross_below",
              "value": 数値 または [数値, 数値],
              "period": 数値（オプション）
            }},
            "logical_operator": "AND" | "OR"（複数トリガーがある場合）
          }}
        ],
        "actions": [
          {{
            "type": "buy" | "sell" | "hold",
            "parameters": {{
              "quantity": 数値（オプション）,
              "percentage": 数値（オプション、%）,
              "stop_loss": 数値（オプション、%）,
              "take_profit": 数値（オプション、%）
            }},
            "execution_type": "market" | "limit" | "stop"
          }}
        ]
      }},
      "confidence_score": 0.0-1.0の数値
    }}
  ]
}}
"""
```

## プロンプト変数

### analysis_results_summary

データ解析結果のサマリーを生成する関数:

```python
def format_analysis_summary(analysis_result: AnalysisResult) -> str:
    return f"""
トレンド方向: {analysis_result.analysis_summary.trend_direction}
ボラティリティレベル: {analysis_result.analysis_summary.volatility_level}
主要パターン: {', '.join(analysis_result.analysis_summary.dominant_patterns)}

RSI: {analysis_result.technical_indicators.rsi.current} ({analysis_result.technical_indicators.rsi.signal})
MACD: {analysis_result.technical_indicators.macd.current} (トレンド: {analysis_result.technical_indicators.macd.trend})

価格範囲: {analysis_result.statistics.price_range.min} - {analysis_result.statistics.price_range.max}
現在価格: {analysis_result.statistics.price_range.current}
価格変動率: {analysis_result.statistics.price_change_percent}%
"""
```

### technical_indicators_summary

テクニカル指標のサマリーを生成:

```python
def format_technical_indicators(indicators: TechnicalIndicators) -> str:
    lines = []
    
    if hasattr(indicators, 'rsi'):
        lines.append(f"RSI: {indicators.rsi.current} (平均: {indicators.rsi.average}, シグナル: {indicators.rsi.signal})")
    
    if hasattr(indicators, 'macd'):
        lines.append(f"MACD: {indicators.macd.current} (シグナル: {indicators.macd.signal_line}, ヒストグラム: {indicators.macd.histogram}, トレンド: {indicators.macd.trend})")
    
    # その他の指標...
    
    return '\n'.join(lines)
```

## プロンプト生成関数

```python
from typing import Dict, Any

def build_algorithm_proposal_prompt(
    analysis_result: AnalysisResult,
    user_preferences: UserPreferences,
    num_proposals: int = 5
) -> str:
    """
    アルゴリズム提案用のプロンプトを生成
    """
    analysis_summary = format_analysis_summary(analysis_result)
    technical_summary = format_technical_indicators(analysis_result.technical_indicators)
    
    preferred_indicators_str = ', '.join(user_preferences.preferred_indicators) if user_preferences.preferred_indicators else 'なし'
    
    prompt = ALGORITHM_PROPOSAL_PROMPT.format(
        analysis_results_summary=analysis_summary,
        trend_direction=analysis_result.analysis_summary.trend_direction,
        volatility_level=analysis_result.analysis_summary.volatility_level,
        dominant_patterns=', '.join(analysis_result.analysis_summary.dominant_patterns),
        technical_indicators_summary=technical_summary,
        price_min=analysis_result.statistics.price_range.min,
        price_max=analysis_result.statistics.price_range.max,
        current_price=analysis_result.statistics.price_range.current,
        price_change_percent=analysis_result.statistics.price_change_percent,
        volume_average=analysis_result.statistics.volume_average,
        risk_tolerance=user_preferences.risk_tolerance or 'medium',
        trading_frequency=user_preferences.trading_frequency or 'medium',
        preferred_indicators=preferred_indicators_str,
        num_proposals=num_proposals
    )
    
    return prompt
```

## プロンプト最適化のポイント

### 1. コンテキストの明確化

- データ解析結果を構造化して提示
- 重要な数値は強調
- 不要な情報は除外

### 2. 出力形式の明確化

- JSONスキーマを明示
- 必須フィールドとオプションフィールドを区別
- 型と値の範囲を明記

### 3. ユーザー設定の反映

- リスク許容度に応じたアルゴリズムの調整
- 取引頻度に応じたトリガー条件の設定
- 好みの指標の優先使用

### 4. エラー防止

- JSON形式の厳密な指定
- 数値の範囲指定
- 必須フィールドの明示

## レスポンス検証

```python
import json
from typing import List, Dict, Any
from pydantic import BaseModel, ValidationError

class AlgorithmProposalResponse(BaseModel):
    proposals: List[Dict[str, Any]]

def validate_llm_response(response_text: str) -> List[Dict[str, Any]]:
    """
    LLMレスポンスを検証
    """
    try:
        # JSONパース
        data = json.loads(response_text)
        
        # スキーマ検証
        validated = AlgorithmProposalResponse(**data)
        
        # 各提案の検証
        for proposal in validated.proposals:
            # 必須フィールドのチェック
            required_fields = ['name', 'description', 'rationale', 'definition']
            for field in required_fields:
                if field not in proposal:
                    raise ValueError(f"Missing required field: {field}")
            
            # 信頼度スコアの範囲チェック
            if 'confidence_score' in proposal:
                score = proposal['confidence_score']
                if not (0.0 <= score <= 1.0):
                    raise ValueError(f"Invalid confidence_score: {score}")
        
        return validated.proposals
        
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {e}")
    except ValidationError as e:
        raise ValueError(f"Validation error: {e}")
```

## プロンプトバージョン管理

```python
PROMPT_VERSIONS = {
    "1.0": ALGORITHM_PROPOSAL_PROMPT,
    # 将来のバージョン追加
}

def get_prompt(version: str = "1.0") -> str:
    return PROMPT_VERSIONS.get(version, PROMPT_VERSIONS["1.0"])
```

## 注意事項

- プロンプトの長さに注意（トークン数の制限）
- 重要な情報はプロンプトの前半に配置
- 出力形式の例をプロンプトに含める（Few-shot learning）
- プロンプトのバージョン管理を適切に行う
- A/Bテストでプロンプトの効果を検証

