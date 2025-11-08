# アルゴリズム提案機能 実装計画

## 概要

LLMがデータ解析結果を基にアルゴリズムを提案し、ユーザーが選択する機能です。本機能はプラットフォームの核心機能の一つです。

## 関連ドキュメント

- **要件定義**: `docs/01_issues/open/2025_11/20251101_01_trend-association-algorithm-platform.md` (SCREEN-002)
- **仕様書**: `src/pages/AlgorithmProposal/AlgorithmProposal.spec.md` ✅ **完了**
- **テスト**: `src/pages/AlgorithmProposal/AlgorithmProposal.test.tsx` ✅ **完了**
- **実装ガイドライン**: `docs/03_plans/algorithm-proposal/IMPLEMENTATION_GUIDE.md` - 詳細な実装手順と既存パターンの参照方法

## 実装フェーズ

### Phase 1: 基本UI構築 ✅ **完了** (2025年11月8日)

**目標**: アルゴリズム提案画面の基本レイアウトを実装

**タスク**:
- [x] 提案生成ボタンとフォームの実装 (`ProposalGenerationForm.tsx`)
- [x] 進捗表示コンポーネントの実装 (`ProgressIndicator.tsx` - 基本構造のみ)
- [x] 提案一覧表示エリアの実装 (`ProposalList.tsx` - 空の状態表示)
- [x] ローディング状態の表示
- [x] 仕様書の作成 (`AlgorithmProposal.spec.md`)
- [x] テストファイルの作成 (`AlgorithmProposal.test.tsx` - 10テストケース、全て通過)

**実装ファイル**:
- `src/pages/AlgorithmProposal/AlgorithmProposal.tsx` ✅
- `src/pages/AlgorithmProposal/ProposalGenerationForm.tsx` ✅
- `src/pages/AlgorithmProposal/ProposalList.tsx` ✅
- `src/pages/AlgorithmProposal/ProgressIndicator.tsx` ✅
- `src/pages/AlgorithmProposal/AlgorithmProposal.spec.md` ✅
- `src/pages/AlgorithmProposal/AlgorithmProposal.test.tsx` ✅

**実装状況**:
- データセット選択機能: ✅ 実装完了
- ユーザー設定入力機能（リスク許容度、取引頻度、好みの指標）: ✅ 実装完了
- 提案数指定機能: ✅ 実装完了
- 提案生成ボタン: ✅ UI実装完了（Phase 3まで無効化）
- エラーハンドリング: ✅ 実装完了
- ローディング状態表示: ✅ 実装完了

**技術スタック**:
- React 19.x
- TypeScript 5.x
- Mantine UI
- Zustand

**依存関係**:
- なし

### Phase 2: データ解析結果取得

**目標**: データ解析結果を取得し、LLMへの入力として準備

**タスク**:
- [ ] `get_analysis_results()` Tauriコマンドの実装（バックエンド）
- [ ] データ解析結果の表示コンポーネント
- [ ] データセット選択機能の実装

**技術スタック**:
- Tauri invoke API
- Zustand store

**依存関係**:
- Phase 1完了
- バックエンド: データ解析機能実装

### Phase 3: LLM連携（バックエンド）

**目標**: LLM APIを使用してアルゴリズム提案を生成

**タスク**:
- [ ] `generate_algorithm_proposals()` Tauriコマンドの実装
- [ ] LLM APIクライアントの実装（OpenAI / Anthropic）
- [ ] プロンプトエンジニアリングの実装
- [ ] レスポンスパース処理の実装
- [ ] エラーハンドリングの実装

**技術スタック**:
- Python 3.10+
- OpenAI API / Anthropic API
- PyTauri

**依存関係**:
- Phase 2完了
- LLM APIキーの設定

### Phase 4: 提案生成ジョブ管理

**目標**: 非同期ジョブの管理と進捗追跡

**タスク**:
- [ ] `get_proposal_generation_status()` Tauriコマンドの実装
- [ ] ジョブ管理システムの実装（バックエンド）
- [ ] ポーリング機能の実装（フロントエンド）
- [ ] 進捗バーの実装

**技術スタック**:
- Python threading / asyncio
- React useEffect / setInterval

**依存関係**:
- Phase 3完了

### Phase 5: 提案一覧表示

**目標**: 生成されたアルゴリズム提案を一覧表示

**タスク**:
- [ ] `get_algorithm_proposals()` Tauriコマンドの実装
- [ ] 提案カードコンポーネントの作成
- [ ] 提案詳細モーダルの実装
- [ ] 説明・根拠の表示

**技術スタック**:
- Mantine Card, Modal
- React Markdown (説明の表示)

**依存関係**:
- Phase 4完了

### Phase 6: アルゴリズム選択機能

**目標**: ユーザーが提案アルゴリズムを選択して保存

**タスク**:
- [ ] `select_algorithm()` Tauriコマンドの実装
- [ ] 選択UIの実装（チェックボックス/ラジオボタン）
- [ ] 選択確認ダイアログの実装
- [ ] 選択後のナビゲーション

**技術スタック**:
- Mantine Checkbox / Radio
- Mantine Dialog

**依存関係**:
- Phase 5完了

## 技術的な詳細

### コンポーネント構造

```
AlgorithmProposal/
├── AlgorithmProposal.tsx        # メインコンポーネント
├── ProposalGenerationForm.tsx   # 提案生成フォーム
├── ProposalList.tsx            # 提案一覧
├── ProposalCard.tsx            # 提案カード
├── ProposalDetailModal.tsx     # 提案詳細モーダル
├── ProgressIndicator.tsx       # 進捗表示
└── AlgorithmProposal.spec.md   # 仕様書
```

### 状態管理

```typescript
interface AlgorithmProposalState {
  dataSetId: number | null;
  analysisId: number | null;
  jobId: string | null;
  status: 'idle' | 'generating' | 'completed' | 'error';
  progress: number;
  proposals: AlgorithmProposal[];
  selectedProposalId: string | null;
  loading: boolean;
  error: string | null;
}
```

### LLMプロンプト設計

```python
prompt_template = """
以下のデータ解析結果を基に、最適なトレードアルゴリズムを提案してください。

【データ解析結果】
{analysis_results}

【ユーザー設定】
- リスク許容度: {risk_tolerance}
- 取引頻度: {trading_frequency}
- 好みの指標: {preferred_indicators}

【出力形式】
JSON形式で以下の構造で出力してください：
{
  "proposals": [
    {
      "name": "アルゴリズム名",
      "description": "説明",
      "rationale": "提案理由",
      "definition": {
        "triggers": [...],
        "actions": [...]
      },
      "confidence_score": 0.0-1.0
    }
  ]
}
"""
```

### API連携

- `generate_algorithm_proposals(params)`: アルゴリズム提案生成開始
- `get_proposal_generation_status(job_id)`: 進捗状況取得
- `get_algorithm_proposals(job_id)`: 提案一覧取得
- `select_algorithm(proposal_id)`: アルゴリズム選択
- `get_analysis_results(analysis_id)`: データ解析結果取得

## テスト計画

### 単体テスト

- [ ] ProposalGenerationFormコンポーネントのテスト
- [ ] ProposalListコンポーネントのテスト
- [ ] ProposalCardコンポーネントのテスト
- [ ] LLM APIクライアントのテスト（モック）

### 統合テスト

- [ ] 提案生成フローの統合テスト
- [ ] ジョブ管理の統合テスト
- [ ] エラーハンドリングのテスト

### E2Eテスト

- [ ] アルゴリズム提案生成のE2Eテスト
- [ ] アルゴリズム選択のE2Eテスト

## 実装優先度

**最高**: Phase 1, Phase 2, Phase 3（核心機能）
**高**: Phase 4, Phase 5（必須機能）
**中**: Phase 6（選択機能）

## 注意事項

- LLM APIのレート制限とコスト管理
- プロンプトエンジニアリングの最適化
- レスポンスパースの堅牢性（JSON形式の検証）
- タイムアウト処理とリトライ機構
- ユーザーへの進捗フィードバック
- エラーメッセージの分かりやすさ

