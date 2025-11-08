# アルゴリズム提案機能 実装ガイドライン

## 概要

本ドキュメントは、アルゴリズム提案機能の実装方法を詳しく解説します。既存のデータ解析機能の実装パターンを参考にしながら、段階的に実装を進めます。

## 関連ドキュメント

- **実装計画**: `docs/03_plans/algorithm-proposal/README.md`
- **API仕様**: `docs/03_plans/algorithm-proposal/api-spec.md`
- **データモデル**: `docs/03_plans/algorithm-proposal/data-model.md`
- **LLM連携**: `docs/03_plans/llm-integration/README.md`
- **参考実装**: `src/pages/DataAnalysis/` (データ解析機能)

## 実装の前提条件

### ✅ 完了している機能

1. **データ解析機能** (83%完了)
   - ジョブ管理システムの実装パターン
   - 進捗表示の実装パターン
   - Tauriコマンドの実装パターン
   - 参考ファイル: `src-python/scripts/run_data_analysis.py`, `get_analysis_status.py`, `get_analysis_results.py`

2. **LLM連携基盤** (60%完了、Phase 1-3完了)
   - LLM APIクライアント（OpenAI/Anthropic）
   - プロンプト生成ロジック
   - レスポンスパース処理
   - 参考ファイル: `src-python/modules/llm_integration/`

3. **データベーススキーマ**
   - `proposal_generation_jobs` テーブル（既に定義済み）
   - `algorithm_proposals` テーブル（既に定義済み）
   - 参考ファイル: `src-python/database/schema.py`

## 実装手順（Phase別）

### Phase 1: 基本UI構築 ✅ **完了** (2025年11月8日)

#### 実装ファイル

**フロントエンド:**
- `src/pages/AlgorithmProposal/AlgorithmProposal.tsx` - メインコンポーネント ✅
- `src/pages/AlgorithmProposal/ProposalGenerationForm.tsx` - 提案生成フォーム ✅
- `src/pages/AlgorithmProposal/ProposalList.tsx` - 提案一覧（初期は空） ✅
- `src/pages/AlgorithmProposal/ProgressIndicator.tsx` - 進捗表示（Phase 4で使用） ✅
- `src/pages/AlgorithmProposal/AlgorithmProposal.spec.md` - 仕様書 ✅
- `src/pages/AlgorithmProposal/AlgorithmProposal.test.tsx` - テストファイル ✅

**参考実装:**
- `src/pages/DataAnalysis/DataAnalysis.tsx` - メインコンポーネントの構造
- `src/pages/DataAnalysis/AnalysisJobForm.tsx` - フォームの実装パターン

#### 実装内容

1. **基本レイアウト**
   ```typescript
   // AlgorithmProposal.tsx の基本構造
   export function AlgorithmProposal() {
     return (
       <Container>
         <Title>アルゴリズム提案</Title>
         <ProposalGenerationForm />
         <ProposalList proposals={[]} />
       </Container>
     );
   }
   ```

2. **提案生成フォーム**
   - データセット選択（既存のデータセット一覧から選択）
   - ユーザー設定入力（リスク許容度、取引頻度、好みの指標）
   - 提案数指定（デフォルト: 5）
   - 生成ボタン（Phase 3まで無効化）

3. **状態管理（Zustand）**
   ```typescript
   // stores/algorithmProposalStore.ts
   interface AlgorithmProposalState {
     dataSetId: number | null;
     analysisId: number | null;
     jobId: string | null;
     status: 'idle' | 'generating' | 'completed' | 'error';
     progress: number;
     proposals: AlgorithmProposal[];
     userPreferences: UserPreferences;
     loading: boolean;
     error: string | null;
   }
   ```

#### テスト

- `src/pages/AlgorithmProposal/AlgorithmProposal.test.tsx`
- `src/pages/AlgorithmProposal/ProposalGenerationForm.test.tsx`

**参考**: `src/pages/DataAnalysis/DataAnalysis.test.tsx`, `AnalysisJobForm.test.tsx`

---

### Phase 2: データ解析結果取得

#### 実装ファイル

**バックエンド:**
- `src-python/scripts/get_analysis_results.py` - 既に実装済み（データ解析機能で使用）
- 新規実装不要（既存のTauriコマンドを再利用）

**フロントエンド:**
- `src/pages/AlgorithmProposal/ProposalGenerationForm.tsx` - データセット選択時に解析結果を取得
- `src/pages/AlgorithmProposal/AnalysisResultDisplay.tsx` - 解析結果の表示コンポーネント（オプション）

#### 実装内容

1. **データセット選択時の処理**
   ```typescript
   const handleDataSetChange = async (dataSetId: number) => {
     // 最新の解析結果を取得
     const analysisResults = await getLatestAnalysisResults(dataSetId);
     setAnalysisId(analysisResults?.id || null);
   };
   ```

2. **解析結果の表示**
   - 既存の `AnalysisResults.tsx` を参考に、簡易版を表示
   - または、解析結果のサマリーのみ表示

#### 注意事項

- `get_analysis_results()` Tauriコマンドは既に実装済み
- データセットに解析結果がない場合は、ユーザーに解析を促す

---

### Phase 3: LLM連携（バックエンド）

#### 実装ファイル

**バックエンド:**
- `src-python/scripts/generate_algorithm_proposals.py` - 提案生成スクリプト
- `src-python/modules/algorithm_proposal/` - アルゴリズム提案モジュール（新規作成）
  - `proposal_generator.py` - 提案生成ロジック
  - `job_manager.py` - ジョブ管理ロジック

**Rust:**
- `src-tauri/src/lib.rs` - `generate_algorithm_proposals` Tauriコマンド追加

#### 実装内容

1. **提案生成スクリプト** (`generate_algorithm_proposals.py`)
   ```python
   # データ解析機能の run_data_analysis.py を参考に実装
   def main():
       input_data = read_json_input()
       data_set_id = input_data.get('data_set_id')
       analysis_id = input_data.get('analysis_id')
       num_proposals = input_data.get('num_proposals', 5)
       user_preferences = input_data.get('user_preferences', {})
       
       # ジョブID生成
       job_id = str(uuid.uuid4())
       
       # ジョブレコード作成
       create_proposal_job(job_id, data_set_id, analysis_id, ...)
       
       # バックグラウンドスレッドで実行
       thread = threading.Thread(
           target=run_proposal_generation_in_background,
           args=(job_id, data_set_id, analysis_id, ...)
       )
       thread.start()
       
       return json_response(success=True, data={"job_id": job_id})
   ```

2. **提案生成ロジック** (`proposal_generator.py`)
   ```python
   from modules.llm_integration import (
       APIKeyManager,
       OpenAIClient,
       AnthropicClient,
       PromptBuilder,
       ResponseParser,
       FallbackHandler
   )
   
   class ProposalGenerator:
       def __init__(self):
           self.api_key_manager = APIKeyManager()
           # OpenAIまたはAnthropicを選択（設定可能に）
           self.llm_client = self._create_llm_client()
           self.prompt_builder = PromptBuilder()
           self.response_parser = ResponseParser()
           self.fallback_handler = FallbackHandler()
       
       def generate_proposals(
           self,
           analysis_result: Dict[str, Any],
           user_preferences: Dict[str, Any],
           num_proposals: int = 5
       ) -> List[Dict[str, Any]]:
           # 1. プロンプト生成
           prompt = self.prompt_builder.build_algorithm_proposal_prompt(
               analysis_result,
               user_preferences,
               num_proposals
           )
           
           # 2. LLM API呼び出し
           response_text = self.llm_client.generate(prompt)
           
           # 3. レスポンスパース（フォールバック付き）
           proposals = self.fallback_handler.parse_with_fallback(
               response_text,
               "algorithm_proposal"
           )
           
           return proposals
   ```

3. **ジョブ管理** (`job_manager.py`)
   ```python
   # データ解析機能の analyzer.py を参考に実装
   class ProposalJobManager:
       def update_job_status(
           self,
           job_id: str,
           status: str,
           progress: float,
           message: str
       ):
           # proposal_generation_jobs テーブルを更新
           pass
       
       def save_proposals(
           self,
           job_id: str,
           proposals: List[Dict[str, Any]]
       ):
           # algorithm_proposals テーブルに保存
           pass
   ```

4. **Tauriコマンド追加** (`src-tauri/src/lib.rs`)
   ```rust
   #[tauri::command]
   async fn generate_algorithm_proposals(
       data_set_id: i32,
       analysis_id: Option<i32>,
       num_proposals: Option<i32>,
       user_preferences: Option<serde_json::Value>,
   ) -> Result<serde_json::Value, String> {
       // run_data_analysis コマンドと同様の実装パターン
       let script_path = get_python_script_path("generate_algorithm_proposals.py")?;
       // ... Pythonスクリプト実行
   }
   ```

#### 実装パターン

**既存のデータ解析機能を参考:**
- `src-python/scripts/run_data_analysis.py` - ジョブ管理パターン
- `src-python/modules/data_analysis/analyzer.py` - 進捗更新パターン
- `src-tauri/src/lib.rs` の `run_data_analysis` - Tauriコマンド実装パターン

#### テスト

- `src-python/tests/unit/test_proposal_generator.py`
- `src-python/tests/integration/test_proposal_generation.py`

---

### Phase 4: 提案生成ジョブ管理

#### 実装ファイル

**バックエンド:**
- `src-python/scripts/get_proposal_generation_status.py` - ジョブ状態取得スクリプト

**Rust:**
- `src-tauri/src/lib.rs` - `get_proposal_generation_status` Tauriコマンド追加

**フロントエンド:**
- `src/pages/AlgorithmProposal/ProgressIndicator.tsx` - 進捗表示コンポーネント

#### 実装内容

1. **ジョブ状態取得スクリプト**
   ```python
   # get_analysis_status.py を参考に実装
   def main():
       input_data = read_json_input()
       job_id = input_data.get('job_id')
       
       conn = get_connection()
       cursor = conn.cursor()
       
       cursor.execute("""
           SELECT status, progress, message, error, completed_at
           FROM proposal_generation_jobs
           WHERE job_id = ?
       """, (job_id,))
       
       # ... 既存パターンと同様
   ```

2. **進捗表示コンポーネント**
   ```typescript
   // AnalysisProgress.tsx を参考に実装
   export function ProposalProgress({ jobId, onCompleted, onError }) {
     const [status, setStatus] = useState<'pending' | 'analyzing' | 'generating' | 'completed' | 'failed'>('pending');
     const [progress, setProgress] = useState(0);
     
     useEffect(() => {
       const interval = setInterval(async () => {
         const response = await invoke('get_proposal_generation_status', { job_id: jobId });
         setStatus(response.status);
         setProgress(response.progress);
         
         if (response.status === 'completed' || response.status === 'failed') {
           clearInterval(interval);
         }
       }, 2000); // 2秒間隔でポーリング
       
       return () => clearInterval(interval);
     }, [jobId]);
     
     // ... 既存パターンと同様
   }
   ```

#### 実装パターン

**既存のデータ解析機能を参考:**
- `src-python/scripts/get_analysis_status.py` - ジョブ状態取得パターン
- `src/pages/DataAnalysis/AnalysisProgress.tsx` - 進捗表示パターン

---

### Phase 5: 提案一覧表示

#### 実装ファイル

**バックエンド:**
- `src-python/scripts/get_algorithm_proposals.py` - 提案一覧取得スクリプト

**Rust:**
- `src-tauri/src/lib.rs` - `get_algorithm_proposals` Tauriコマンド追加

**フロントエンド:**
- `src/pages/AlgorithmProposal/ProposalList.tsx` - 提案一覧コンポーネント
- `src/pages/AlgorithmProposal/ProposalCard.tsx` - 提案カードコンポーネント
- `src/pages/AlgorithmProposal/ProposalDetailModal.tsx` - 提案詳細モーダル

#### 実装内容

1. **提案一覧取得スクリプト**
   ```python
   # get_analysis_results.py を参考に実装
   def main():
       input_data = read_json_input()
       job_id = input_data.get('job_id')
       
       conn = get_connection()
       cursor = conn.cursor()
       
       # ジョブが完了しているか確認
       cursor.execute("SELECT status FROM proposal_generation_jobs WHERE job_id = ?", (job_id,))
       job_status = cursor.fetchone()
       
       if not job_status or job_status[0] != 'completed':
           return json_response(success=False, error="Job not completed")
       
       # 提案一覧を取得
       cursor.execute("""
           SELECT proposal_id, name, description, rationale, 
                  expected_performance, definition, confidence_score
           FROM algorithm_proposals
           WHERE job_id = ?
           ORDER BY confidence_score DESC
       """, (job_id,))
       
       proposals = []
       for row in cursor.fetchall():
           proposals.append({
               "proposal_id": row[0],
               "name": row[1],
               "description": row[2],
               "rationale": row[3],
               "expected_performance": json.loads(row[4]) if row[4] else None,
               "definition": json.loads(row[5]),
               "confidence_score": row[6]
           })
       
       return json_response(success=True, data={"proposals": proposals})
   ```

2. **提案カードコンポーネント**
   ```typescript
   // Mantine Cardを使用
   export function ProposalCard({ proposal }: { proposal: AlgorithmProposal }) {
     return (
       <Card>
         <Title order={4}>{proposal.name}</Title>
         <Text>{proposal.description}</Text>
         <Badge color={getConfidenceColor(proposal.confidence_score)}>
           信頼度: {(proposal.confidence_score * 100).toFixed(0)}%
         </Badge>
         <Button onClick={() => openDetailModal(proposal)}>詳細を見る</Button>
       </Card>
     );
   }
   ```

---

### Phase 6: アルゴリズム選択機能

#### 実装ファイル

**バックエンド:**
- `src-python/scripts/select_algorithm.py` - アルゴリズム選択スクリプト

**Rust:**
- `src-tauri/src/lib.rs` - `select_algorithm` Tauriコマンド追加

**フロントエンド:**
- `src/pages/AlgorithmProposal/ProposalCard.tsx` - 選択UI追加
- `src/pages/AlgorithmProposal/SelectAlgorithmDialog.tsx` - 選択確認ダイアログ

#### 実装内容

1. **アルゴリズム選択スクリプト**
   ```python
   def main():
       input_data = read_json_input()
       proposal_id = input_data.get('proposal_id')
       custom_name = input_data.get('custom_name')
       
       conn = get_connection()
       cursor = conn.cursor()
       
       # 提案を取得
       cursor.execute("""
           SELECT name, definition, job_id
           FROM algorithm_proposals
           WHERE proposal_id = ?
       """, (proposal_id,))
       
       proposal = cursor.fetchone()
       if not proposal:
           return json_response(success=False, error="Proposal not found")
       
       # algorithms テーブルに保存
       algorithm_name = custom_name or proposal[0]
       cursor.execute("""
           INSERT INTO algorithms (name, definition, proposal_id, created_at)
           VALUES (?, ?, ?, ?)
       """, (algorithm_name, proposal[1], proposal_id, datetime.now().isoformat()))
       
       algo_id = cursor.lastrowid
       conn.commit()
       
       return json_response(success=True, data={"algo_id": algo_id})
   ```

## 実装のベストプラクティス

### 1. 既存パターンの再利用

- **ジョブ管理**: `run_data_analysis.py` のパターンをそのまま使用
- **進捗表示**: `AnalysisProgress.tsx` のパターンを参考に実装
- **Tauriコマンド**: `src-tauri/src/lib.rs` の既存コマンドを参考に実装

### 2. エラーハンドリング

- LLM API呼び出しエラー: `LLMError` 例外を使用
- データベースエラー: 適切なエラーメッセージを返す
- パースエラー: `FallbackHandler` を使用してリカバリを試みる

### 3. テスト戦略

- **単体テスト**: 各モジュールを個別にテスト
- **統合テスト**: エンドツーエンドのフローをテスト
- **モック**: LLM API呼び出しはモックを使用（実際のAPIを呼ばない）

### 4. パフォーマンス

- ジョブはバックグラウンドスレッドで実行
- 進捗ポーリングは2秒間隔（推奨）
- LLM API呼び出しのタイムアウト: 60秒

## 実装チェックリスト

### Phase 1: 基本UI構築 ✅ **完了** (2025年11月8日)
- [x] `AlgorithmProposal.tsx` 作成
- [x] `ProposalGenerationForm.tsx` 作成
- [x] `ProposalList.tsx` 作成（初期は空）
- [x] `ProgressIndicator.tsx` 作成（基本構造のみ）
- [x] `AlgorithmProposal.spec.md` 作成
- [x] `AlgorithmProposal.test.tsx` 作成（10テストケース、全て通過）
- [x] DEPENDENCY MAPコメント追加
- [x] テスト実行・確認完了

### Phase 2: データ解析結果取得 ✅ **完了** (2025年11月8日)
- [x] `get_latest_analysis_results.py` 作成
- [x] Tauriコマンド `get_latest_analysis_results` 追加
- [x] `ProposalGenerationForm.tsx` でデータセット選択時に解析結果を取得
- [x] テスト追加（4テストケース、全て通過）

### Phase 3: LLM連携（バックエンド） ✅ **完了** (2025年11月8日)
- [x] `generate_algorithm_proposals.py` 作成
- [x] `proposal_generator.py` 作成
- [x] `job_manager.py` 作成
- [x] Tauriコマンド `generate_algorithm_proposals` 追加
- [x] テストファイル作成（proposal_generator: 4テストケース、job_manager: 3テストケース、全て通過）

### Phase 4: 提案生成ジョブ管理 ✅ **完了** (2025年11月8日)
- [x] `get_proposal_generation_status.py` 作成
- [x] Tauriコマンド `get_proposal_generation_status` 追加
- [x] `ProgressIndicator.tsx` 実装（ポーリング機能含む）
- [x] テスト追加（ProgressIndicator: 4テストケース、get_proposal_generation_status: 4テストケース、全て通過）

### Phase 5: 提案一覧表示 ✅ **完了** (2025年11月8日)
- [x] `get_algorithm_proposals.py` 作成
- [x] Tauriコマンド `get_algorithm_proposals` 追加
- [x] `ProposalCard.tsx` 実装
- [x] `ProposalDetailModal.tsx` 実装
- [x] `ProposalList.tsx` 実装完了
- [x] `AlgorithmProposal.tsx` でジョブ完了時に提案を取得して表示
- [x] `react-markdown`依存関係追加
- [x] テスト追加（ProposalCard: 9テストケース、ProposalList: 4テストケース、ProposalDetailModal: 10テストケース、get_algorithm_proposals: 3テストケース、全て通過）

### Phase 6: アルゴリズム選択機能 ✅ **完了** (2025年11月8日)
- [x] `select_algorithm.py` 作成
- [x] Tauriコマンド `select_algorithm` 追加
- [x] 選択UI実装（`SelectAlgorithmDialog.tsx`）
- [x] `ProposalList.tsx`に選択機能統合
- [x] テスト追加（バックエンド: 4テストケース、フロントエンド: SelectAlgorithmDialog 11テストケース、ProposalList 3テストケース追加）

## 注意事項

1. **LLM APIキーの設定**: `.env` ファイルに `OPENAI_API_KEY` または `ANTHROPIC_API_KEY` を設定
2. **データベーススキーマ**: 既に定義済みなので、マイグレーション不要
3. **型定義**: `src/types/algorithm.ts` に既に定義済み
4. **プロンプトテンプレート**: `src-python/modules/llm_integration/templates/algorithm_proposal.txt` を使用

## 参考実装ファイル一覧

### バックエンド
- `src-python/scripts/run_data_analysis.py` - ジョブ実行パターン
- `src-python/scripts/get_analysis_status.py` - ジョブ状態取得パターン
- `src-python/scripts/get_analysis_results.py` - 結果取得パターン
- `src-python/modules/data_analysis/analyzer.py` - 進捗更新パターン

### フロントエンド
- `src/pages/DataAnalysis/DataAnalysis.tsx` - メインコンポーネント構造
- `src/pages/DataAnalysis/AnalysisJobForm.tsx` - フォーム実装パターン
- `src/pages/DataAnalysis/AnalysisProgress.tsx` - 進捗表示パターン
- `src/pages/DataAnalysis/AnalysisResults.tsx` - 結果表示パターン

### LLM連携
- `src-python/modules/llm_integration/prompt_builder.py` - プロンプト生成
- `src-python/modules/llm_integration/response_parser.py` - レスポンスパース
- `src-python/modules/llm_integration/fallback_handler.py` - フォールバック処理

## 次のステップ

1. Phase 1から順番に実装を開始
2. 各Phaseでテストを実装
3. 既存のデータ解析機能のパターンを参考にしながら実装
4. LLM連携モジュールを活用して提案生成を実装

