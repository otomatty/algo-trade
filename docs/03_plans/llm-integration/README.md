# LLM連携（バックエンド）実装計画

## 概要

OpenAI API / Anthropic APIを使用したLLM連携機能の実装計画です。アルゴリズム提案生成と銘柄予測生成の両方で使用されます。

## 関連ドキュメント

- **要件定義**: `docs/01_issues/open/2025_11/20251101_01_trend-association-algorithm-platform.md`
- **依存機能**:
  - アルゴリズム提案機能 (`docs/03_plans/algorithm-proposal/`)
  - 銘柄予測機能 (`docs/03_plans/stock-prediction/`)

## 実装フェーズ

### Phase 1: LLM APIクライアント基盤

**目標**: LLM APIへの接続基盤を実装

**タスク**:
- [ ] OpenAI APIクライアントの実装
- [ ] Anthropic APIクライアントの実装
- [ ] APIキー管理機能の実装
- [ ] エラーハンドリングの実装
- [ ] リトライ機構の実装

**技術スタック**:
- Python 3.10+
- openai (Python library)
- anthropic (Python library)
- python-dotenv (環境変数管理)

**依存関係**:
- なし（基盤機能）

### Phase 2: プロンプトエンジニアリング

**目標**: 効果的なプロンプトテンプレートの設計・実装

**タスク**:
- [ ] アルゴリズム提案用プロンプトの設計
- [ ] 銘柄予測用プロンプトの設計
- [ ] プロンプトテンプレートシステムの実装
- [ ] プロンプト最適化のテスト

**技術スタック**:
- Python string templates
- JSON schema validation

**依存関係**:
- Phase 1完了

### Phase 3: レスポンスパース処理

**目標**: LLMからのレスポンスを構造化データに変換

**タスク**:
- [ ] JSONレスポンスパーサーの実装
- [ ] スキーマバリデーションの実装
- [ ] エラーハンドリング（不正なJSON等）
- [ ] フォールバック処理の実装

**技術スタック**:
- Python json
- pydantic (データバリデーション)

**依存関係**:
- Phase 2完了

### Phase 4: ストリーミング対応（オプション）

**目標**: ストリーミングレスポンスの対応（将来拡張）

**タスク**:
- [ ] ストリーミングAPIクライアントの実装
- [ ] チャンク処理の実装
- [ ] フロントエンドへのストリーミング転送

**技術スタック**:
- Python asyncio
- Server-Sent Events (SSE)

**依存関係**:
- Phase 3完了
- 低優先度（将来実装）

### Phase 5: コスト管理・最適化

**目標**: LLM APIのコスト管理と最適化

**タスク**:
- [ ] トークン数計算の実装
- [ ] コスト追跡機能の実装
- [ ] プロンプト最適化（トークン削減）
- [ ] キャッシュ機能の実装（同じ入力の場合）

**技術スタック**:
- tiktoken (トークン数計算)
- SQLite (コストログ)

**依存関係**:
- Phase 3完了

## 技術的な詳細

### APIクライアント設計

```python
class LLMClient:
    def __init__(self, provider: str, api_key: str):
        self.provider = provider
        self.api_key = api_key
        self.client = self._create_client()
    
    def generate_algorithm_proposals(self, analysis_results, user_preferences):
        prompt = self._build_algorithm_prompt(analysis_results, user_preferences)
        response = self._call_api(prompt)
        return self._parse_algorithm_response(response)
    
    def generate_stock_predictions(self, news, market_trends):
        prompt = self._build_prediction_prompt(news, market_trends)
        response = self._call_api(prompt)
        return self._parse_prediction_response(response)
```

### プロンプトテンプレート管理

```python
class PromptTemplate:
    def __init__(self, template_path: str):
        self.template = self._load_template(template_path)
    
    def render(self, **kwargs) -> str:
        return self.template.format(**kwargs)
    
    def validate_input(self, **kwargs) -> bool:
        # 必須パラメータの検証
        pass
```

### エラーハンドリング

```python
class LLMError(Exception):
    pass

class APIKeyError(LLMError):
    pass

class RateLimitError(LLMError):
    pass

class ParseError(LLMError):
    pass

def handle_llm_error(error):
    # エラータイプに応じた処理
    if isinstance(error, RateLimitError):
        # リトライ処理
        pass
    elif isinstance(error, ParseError):
        # フォールバック処理
        pass
```

### リトライ機構

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10)
)
def call_llm_api(prompt):
    # LLM API呼び出し
    pass
```

### APIキー管理

```python
import os
from cryptography.fernet import Fernet

class APIKeyManager:
    def __init__(self):
        self.encryption_key = self._get_encryption_key()
        self.cipher = Fernet(self.encryption_key)
    
    def save_api_key(self, provider: str, api_key: str):
        encrypted_key = self.cipher.encrypt(api_key.encode())
        # 安全な場所に保存（OSのキーチェーン等）
        pass
    
    def get_api_key(self, provider: str) -> str:
        # 暗号化されたキーを取得・復号
        pass
```

## テスト計画

### 単体テスト

- [ ] LLM APIクライアントのテスト（モック）
- [ ] プロンプトテンプレートのテスト
- [ ] レスポンスパーサーのテスト
- [ ] エラーハンドリングのテスト
- [ ] リトライ機構のテスト

### 統合テスト

- [ ] 実際のLLM APIとの統合テスト（テスト環境）
- [ ] エンドツーエンドのフローテスト

## 実装優先度

**最高**: Phase 1, Phase 2, Phase 3（必須機能）
**中**: Phase 5（コスト管理）
**低**: Phase 4（ストリーミング対応）

## 注意事項

- APIキーの安全な管理（暗号化、OSキーチェーン使用）
- レート制限への対応（リトライ、キューイング）
- コスト管理（トークン数追跡、予算アラート）
- プロンプトの最適化（トークン削減、精度向上）
- エラーハンドリングの堅牢性
- レスポンスパースの堅牢性（不正なJSON対応）
- プライバシーへの配慮（送信データの最小化）

