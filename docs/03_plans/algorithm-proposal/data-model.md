# アルゴリズム提案機能 データモデル詳細

## 概要

アルゴリズム提案機能で使用するデータモデルの詳細定義です。

## 関連ドキュメント

- **実装計画**: `docs/03_plans/algorithm-proposal/README.md`
- **API仕様**: `docs/03_plans/algorithm-proposal/api-spec.md`

## TypeScript型定義

### コア型定義

```typescript
// アルゴリズム提案
interface AlgorithmProposal {
  proposal_id: string;
  name: string;
  description: string;
  rationale: string;
  expected_performance?: ExpectedPerformance;
  definition: AlgorithmDefinition;
  confidence_score?: number;
}

// 期待パフォーマンス
interface ExpectedPerformance {
  expected_return?: number;
  risk_level?: 'low' | 'medium' | 'high';
}

// アルゴリズム定義
interface AlgorithmDefinition {
  triggers: TriggerDefinition[];
  actions: ActionDefinition[];
}

// トリガー定義
interface TriggerDefinition {
  type: 'rsi' | 'macd' | 'price' | 'volume' | 'moving_average' | string;
  condition: TriggerCondition;
  logical_operator?: 'AND' | 'OR';  // 複数トリガー間の論理演算子
}

interface TriggerCondition {
  operator: 'gt' | 'lt' | 'gte' | 'lte' | 'eq' | 'between' | 'cross_above' | 'cross_below';
  value: number | [number, number];
  period?: number;
  indicator?: string;
}

// アクション定義
interface ActionDefinition {
  type: 'buy' | 'sell' | 'hold';
  parameters: ActionParameters;
  execution_type?: 'market' | 'limit' | 'stop';
}

interface ActionParameters {
  quantity?: number;
  percentage?: number;
  stop_loss?: number;
  take_profit?: number;
  limit_price?: number;
}

// ユーザー設定
interface UserPreferences {
  risk_tolerance?: 'low' | 'medium' | 'high';
  trading_frequency?: 'low' | 'medium' | 'high';
  preferred_indicators?: string[];
}

// ジョブ状態
interface ProposalGenerationStatus {
  status: 'pending' | 'analyzing' | 'generating' | 'completed' | 'failed';
  progress: number;
  message: string;
  error?: string;
}
```

### 状態管理型定義

```typescript
// Zustand Store State
interface AlgorithmProposalState {
  dataSetId: number | null;
  analysisId: number | null;
  jobId: string | null;
  status: 'idle' | 'generating' | 'completed' | 'error';
  progress: number;
  proposals: AlgorithmProposal[];
  selectedProposalId: string | null;
  userPreferences: UserPreferences;
  loading: boolean;
  error: string | null;
}

// Zustand Store Actions
interface AlgorithmProposalActions {
  setDataSetId: (id: number | null) => void;
  setAnalysisId: (id: number | null) => void;
  setUserPreferences: (preferences: UserPreferences) => void;
  generateProposals: () => Promise<void>;
  pollStatus: () => Promise<void>;
  fetchProposals: () => Promise<void>;
  selectProposal: (proposalId: string, customName?: string) => Promise<void>;
  clearError: () => void;
}
```

## Pythonデータクラス定義

```python
from dataclasses import dataclass
from typing import Optional, List, Dict, Any, Literal
from enum import Enum

class RiskTolerance(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class TradingFrequency(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

@dataclass
class UserPreferences:
    risk_tolerance: Optional[RiskTolerance] = None
    trading_frequency: Optional[TradingFrequency] = None
    preferred_indicators: Optional[List[str]] = None

@dataclass
class ExpectedPerformance:
    expected_return: Optional[float] = None
    risk_level: Optional[Literal["low", "medium", "high"]] = None

@dataclass
class TriggerCondition:
    operator: str
    value: float | tuple[float, float]
    period: Optional[int] = None
    indicator: Optional[str] = None

@dataclass
class TriggerDefinition:
    type: str
    condition: TriggerCondition
    logical_operator: Optional[Literal["AND", "OR"]] = None

@dataclass
class ActionParameters:
    quantity: Optional[float] = None
    percentage: Optional[float] = None
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None
    limit_price: Optional[float] = None

@dataclass
class ActionDefinition:
    type: Literal["buy", "sell", "hold"]
    parameters: ActionParameters
    execution_type: Optional[Literal["market", "limit", "stop"]] = None

@dataclass
class AlgorithmDefinition:
    triggers: List[TriggerDefinition]
    actions: List[ActionDefinition]

@dataclass
class AlgorithmProposal:
    proposal_id: str
    name: str
    description: str
    rationale: str
    expected_performance: Optional[ExpectedPerformance] = None
    definition: AlgorithmDefinition = None
    confidence_score: Optional[float] = None
```

## データベーススキーマ

### algorithm_proposals テーブル

```sql
CREATE TABLE algorithm_proposals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    proposal_id TEXT UNIQUE NOT NULL,
    job_id TEXT NOT NULL,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    rationale TEXT NOT NULL,
    expected_performance TEXT,  -- JSON形式
    definition TEXT NOT NULL,   -- JSON形式
    confidence_score REAL,
    created_at TEXT NOT NULL,
    FOREIGN KEY (job_id) REFERENCES proposal_generation_jobs(job_id)
);

CREATE INDEX idx_algorithm_proposals_job_id ON algorithm_proposals(job_id);
CREATE INDEX idx_algorithm_proposals_proposal_id ON algorithm_proposals(proposal_id);
```

### proposal_generation_jobs テーブル

```sql
CREATE TABLE proposal_generation_jobs (
    job_id TEXT PRIMARY KEY,
    data_set_id INTEGER NOT NULL,
    analysis_id INTEGER,
    num_proposals INTEGER,
    user_preferences TEXT,  -- JSON形式
    status TEXT NOT NULL,
    progress REAL DEFAULT 0.0,
    message TEXT,
    error TEXT,
    created_at TEXT NOT NULL,
    completed_at TEXT,
    FOREIGN KEY (data_set_id) REFERENCES data_sets(id),
    FOREIGN KEY (analysis_id) REFERENCES analysis_results(id)
);

CREATE INDEX idx_proposal_jobs_status ON proposal_generation_jobs(status);
CREATE INDEX idx_proposal_jobs_created_at ON proposal_generation_jobs(created_at);
```

## データフロー図

```
┌─────────────┐
│  Frontend   │
│  Form       │
└──────┬──────┘
       │
       │ invoke('generate_algorithm_proposals')
       ▼
┌─────────────┐
│  Backend    │
│  PyTauri    │
└──────┬──────┘
       │
       │ 1. データ解析結果取得
       │ 2. LLM API呼び出し
       │ 3. レスポンスパース
       │ 4. データベース保存
       ▼
┌─────────────┐
│  SQLite DB  │
│  proposals  │
└─────────────┘

┌─────────────┐
│  Frontend   │
│  Polling    │
└──────┬──────┘
       │
       │ invoke('get_proposal_generation_status')
       ▼
┌─────────────┐
│  Backend    │
│  Job Status │
└─────────────┘

┌─────────────┐
│  Frontend   │
│  Display    │
└──────┬──────┘
       │
       │ invoke('get_algorithm_proposals')
       ▼
┌─────────────┐
│  Backend    │
│  PyTauri    │
└──────┬──────┘
       │
       │ SELECT * FROM algorithm_proposals
       ▼
┌─────────────┐
│SQLite DB│
└─────────┘
```

## データ変換

### フロントエンド → バックエンド

```typescript
// 提案生成リクエスト
const request: GenerateAlgorithmProposalsRequest = {
  data_set_id: 1,
  num_proposals: 5,
  user_preferences: {
    risk_tolerance: 'medium',
    trading_frequency: 'high',
    preferred_indicators: ['RSI', 'MACD']
  }
};
```

### バックエンド → フロントエンド

```python
# Python → TypeScript
def format_proposal(proposal: AlgorithmProposal) -> Dict[str, Any]:
    return {
        "proposal_id": proposal.proposal_id,
        "name": proposal.name,
        "description": proposal.description,
        "rationale": proposal.rationale,
        "expected_performance": {
            "expected_return": proposal.expected_performance.expected_return,
            "risk_level": proposal.expected_performance.risk_level
        } if proposal.expected_performance else None,
        "definition": {
            "triggers": [format_trigger(t) for t in proposal.definition.triggers],
            "actions": [format_action(a) for a in proposal.definition.actions]
        },
        "confidence_score": proposal.confidence_score
    }
```

## LLMレスポンスパース

```python
import json
from typing import List

def parse_llm_response(response_text: str) -> List[AlgorithmProposal]:
    """
    LLMからのJSONレスポンスをパースしてAlgorithmProposalリストに変換
    """
    try:
        data = json.loads(response_text)
        proposals = []
        
        for proposal_data in data.get("proposals", []):
            proposal = AlgorithmProposal(
                proposal_id=generate_proposal_id(),
                name=proposal_data["name"],
                description=proposal_data["description"],
                rationale=proposal_data["rationale"],
                expected_performance=ExpectedPerformance(
                    expected_return=proposal_data.get("expected_performance", {}).get("expected_return"),
                    risk_level=proposal_data.get("expected_performance", {}).get("risk_level")
                ) if proposal_data.get("expected_performance") else None,
                definition=parse_algorithm_definition(proposal_data["definition"]),
                confidence_score=proposal_data.get("confidence_score")
            )
            proposals.append(proposal)
        
        return proposals
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON response: {e}")
    except KeyError as e:
        raise ValueError(f"Missing required field: {e}")
```

## 注意事項

- プロposal_idは一意な文字列として生成（UUID推奨）
- JSON形式のデータ（`definition`, `expected_performance`）は文字列として保存
- 信頼度スコアは0.0～1.0の範囲で正規化
- LLMレスポンスのパース時はエラーハンドリングを適切に実装
- データベースのインデックスを適切に設定してパフォーマンスを最適化

