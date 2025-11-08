# アルゴリズム提案機能 UI/UX設計書

## 概要

アルゴリズム提案機能のUI/UX設計詳細です。

## 関連ドキュメント

- **実装計画**: `docs/03_plans/algorithm-proposal/README.md`
- **データモデル**: `docs/03_plans/algorithm-proposal/data-model.md`

## 画面レイアウト設計

### 全体レイアウト

```
┌─────────────────────────────────────────────────────────┐
│ Header                                                   │
├─────────────────────────────────────────────────────────┤
│                                                          │
│ ┌────────────────────────────────────────────────────┐ │
│ │ Proposal Generation Form                           │ │
│ │ ┌──────────────┐ ┌──────────────┐                │ │
│ │ │ Data Set     │ │ Analysis     │                │ │
│ │ │ [Select ▼]   │ │ [Select ▼]   │                │ │
│ │ └──────────────┘ └──────────────┘                │ │
│ │ ┌──────────────────────────────────────────────┐  │ │
│ │ │ User Preferences                             │  │ │
│ │ │ Risk: [Low] [Medium] [High]                 │  │ │
│ │ │ Frequency: [Low] [Medium] [High]            │  │ │
│ │ │ Indicators: [RSI] [MACD] ...]                 │  │ │
│ │ └──────────────────────────────────────────────┘  │ │
│ │ [Generate Proposals]                               │ │
│ └────────────────────────────────────────────────────┘ │
│                                                          │
│ ┌────────────────────────────────────────────────────┐ │
│ │ Progress Indicator                                 │ │
│ │ [████████░░] 80% Analyzing data trends...         │ │
│ └────────────────────────────────────────────────────┘ │
│                                                          │
│ ┌────────────────────────────────────────────────────┐ │
│ │ Proposal List                                      │ │
│ │ ┌──────────────┐ ┌──────────────┐                │ │
│ │ │ Proposal 1   │ │ Proposal 2   │                │ │
│ │ │ Confidence:  │ │ Confidence:  │                │ │
│ │ │   0.85       │ │   0.72       │                │ │
│ │ │ [Select]     │ │ [Select]     │                │ │
│ │ └──────────────┘ └──────────────┘                │ │
│ └────────────────────────────────────────────────────┘ │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## コンポーネント構造

```
AlgorithmProposal/
├── AlgorithmProposal.tsx        # メインコンポーネント
├── ProposalGenerationForm.tsx   # 提案生成フォーム
│   ├── DataSetSelector.tsx      # データセット選択
│   ├── AnalysisSelector.tsx     # 解析結果選択
│   └── UserPreferencesForm.tsx  # ユーザー設定フォーム
├── ProgressIndicator.tsx        # 進捗表示
├── ProposalList.tsx            # 提案一覧
│   └── ProposalCard.tsx         # 提案カード
├── ProposalDetailModal.tsx     # 提案詳細モーダル
└── AlgorithmProposal.spec.md   # 仕様書
```

## コンポーネント詳細設計

### AlgorithmProposal.tsx

**役割**: アルゴリズム提案画面のメインコンテナ

**Props**: なし

**State管理**: Zustand storeを使用

```typescript
import { useEffect } from 'react';
import { useAlgorithmProposalStore } from '@/stores/algorithmProposal';
import { ProposalGenerationForm } from './ProposalGenerationForm';
import { ProgressIndicator } from './ProgressIndicator';
import { ProposalList } from './ProposalList';

export function AlgorithmProposal() {
  const {
    status,
    progress,
    proposals,
    generateProposals,
    pollStatus,
    fetchProposals
  } = useAlgorithmProposalStore();

  useEffect(() => {
    if (status === 'generating') {
      const interval = setInterval(() => {
        pollStatus();
      }, 2000);
      return () => clearInterval(interval);
    }
  }, [status, pollStatus]);

  useEffect(() => {
    if (status === 'completed') {
      fetchProposals();
    }
  }, [status, fetchProposals]);

  return (
    <Container>
      <Title order={1}>アルゴリズム提案</Title>
      
      <ProposalGenerationForm onSubmit={generateProposals} />
      
      {status === 'generating' && (
        <ProgressIndicator progress={progress} />
      )}
      
      {status === 'completed' && proposals.length > 0 && (
        <ProposalList proposals={proposals} />
      )}
    </Container>
  );
}
```

### ProposalGenerationForm.tsx

**役割**: 提案生成のフォーム

**Props**:
```typescript
interface ProposalGenerationFormProps {
  onSubmit: () => Promise<void>;
}
```

**フォーム項目**:
- データセット選択
- 解析結果選択（オプション）
- 提案数
- ユーザー設定（リスク許容度、取引頻度、好みの指標）

```typescript
import { useForm } from '@mantine/form';
import { Select, NumberInput, Radio, MultiSelect, Button } from '@mantine/core';
import { useAlgorithmProposalStore } from '@/stores/algorithmProposal';

export function ProposalGenerationForm({ onSubmit }: ProposalGenerationFormProps) {
  const { dataSets, analysisResults, userPreferences, setDataSetId, setAnalysisId, setUserPreferences } = useAlgorithmProposalStore();
  
  const form = useForm({
    initialValues: {
      dataSetId: null as number | null,
      analysisId: null as number | null,
      numProposals: 5,
      riskTolerance: 'medium' as 'low' | 'medium' | 'high',
      tradingFrequency: 'medium' as 'low' | 'medium' | 'high',
      preferredIndicators: [] as string[]
    }
  });

  const handleSubmit = async (values: typeof form.values) => {
    setDataSetId(values.dataSetId);
    setAnalysisId(values.analysisId);
    setUserPreferences({
      risk_tolerance: values.riskTolerance,
      trading_frequency: values.tradingFrequency,
      preferred_indicators: values.preferredIndicators
    });
    await onSubmit();
  };

  return (
    <form onSubmit={form.onSubmit(handleSubmit)}>
      <Select
        label="データセット"
        data={dataSets.map(ds => ({ value: String(ds.id), label: ds.name }))}
        {...form.getInputProps('dataSetId')}
        required
      />
      
      <Select
        label="解析結果（オプション）"
        data={analysisResults.map(ar => ({ value: String(ar.id), label: ar.created_at }))}
        {...form.getInputProps('analysisId')}
      />
      
      <NumberInput
        label="提案数"
        min={1}
        max={10}
        {...form.getInputProps('numProposals')}
      />
      
      <Radio.Group
        label="リスク許容度"
        {...form.getInputProps('riskTolerance')}
      >
        <Radio value="low" label="低" />
        <Radio value="medium" label="中" />
        <Radio value="high" label="高" />
      </Radio.Group>
      
      <Radio.Group
        label="取引頻度"
        {...form.getInputProps('tradingFrequency')}
      >
        <Radio value="low" label="低" />
        <Radio value="medium" label="中" />
        <Radio value="high" label="高" />
      </Radio.Group>
      
      <MultiSelect
        label="好みの指標"
        data={['RSI', 'MACD', 'Bollinger Bands', 'Moving Average']}
        {...form.getInputProps('preferredIndicators')}
      />
      
      <Button type="submit" loading={status === 'generating'}>
        提案を生成
      </Button>
    </form>
  );
}
```

### ProposalCard.tsx

**役割**: 個別の提案カード表示

**Props**:
```typescript
interface ProposalCardProps {
  proposal: AlgorithmProposal;
  onSelect: (proposalId: string) => void;
  onViewDetail: (proposal: AlgorithmProposal) => void;
}
```

```typescript
import { Card, Text, Badge, Group, Button, Progress } from '@mantine/core';

export function ProposalCard({ proposal, onSelect, onViewDetail }: ProposalCardProps) {
  return (
    <Card shadow="sm" padding="lg" radius="md" withBorder>
      <Group justify="space-between" mb="xs">
        <Text fw={500}>{proposal.name}</Text>
        {proposal.confidence_score !== undefined && (
          <Badge color={proposal.confidence_score > 0.7 ? 'green' : 'yellow'}>
            {Math.round(proposal.confidence_score * 100)}%
          </Badge>
        )}
      </Group>

      <Text size="sm" c="dimmed" mb="md" lineClamp={2}>
        {proposal.description}
      </Text>

      {proposal.confidence_score !== undefined && (
        <Progress value={proposal.confidence_score * 100} mb="md" />
      )}

      <Group justify="flex-end">
        <Button variant="light" size="xs" onClick={() => onViewDetail(proposal)}>
          詳細
        </Button>
        <Button size="xs" onClick={() => onSelect(proposal.proposal_id)}>
          選択
        </Button>
      </Group>
    </Card>
  );
}
```

### ProposalDetailModal.tsx

**役割**: 提案の詳細表示モーダル

**Props**:
```typescript
interface ProposalDetailModalProps {
  proposal: AlgorithmProposal | null;
  opened: boolean;
  onClose: () => void;
  onSelect: (proposalId: string) => void;
}
```

```typescript
import { Modal, Text, Badge, Code, Button } from '@mantine/core';
import ReactMarkdown from 'react-markdown';

export function ProposalDetailModal({ proposal, opened, onClose, onSelect }: ProposalDetailModalProps) {
  if (!proposal) return null;

  return (
    <Modal
      opened={opened}
      onClose={onClose}
      title={proposal.name}
      size="xl"
    >
      <Text fw={500} mb="md">説明</Text>
      <ReactMarkdown>{proposal.description}</ReactMarkdown>

      <Text fw={500} mt="md" mb="md">提案理由</Text>
      <ReactMarkdown>{proposal.rationale}</ReactMarkdown>

      <Text fw={500} mt="md" mb="md">アルゴリズム定義</Text>
      <Code block>{JSON.stringify(proposal.definition, null, 2)}</Code>

      {proposal.expected_performance && (
        <>
          <Text fw={500} mt="md" mb="md">期待パフォーマンス</Text>
          <Group>
            {proposal.expected_performance.expected_return !== undefined && (
              <Badge>
                期待リターン: {proposal.expected_performance.expected_return}%
              </Badge>
            )}
            {proposal.expected_performance.risk_level && (
              <Badge color={proposal.expected_performance.risk_level === 'low' ? 'green' : 'red'}>
                リスク: {proposal.expected_performance.risk_level}
              </Badge>
            )}
          </Group>
        </>
      )}

      <Group justify="flex-end" mt="xl">
        <Button variant="light" onClick={onClose}>
          閉じる
        </Button>
        <Button onClick={() => {
          onSelect(proposal.proposal_id);
          onClose();
        }}>
          このアルゴリズムを選択
        </Button>
      </Group>
    </Modal>
  );
}
```

## 状態管理設計

### Zustand Store

```typescript
import { create } from 'zustand';
import { invoke } from '@tauri-apps/api/core';
import type { AlgorithmProposal, UserPreferences } from '@/types';

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

export const useAlgorithmProposalStore = create<AlgorithmProposalState & AlgorithmProposalActions>((set, get) => ({
  dataSetId: null,
  analysisId: null,
  jobId: null,
  status: 'idle',
  progress: 0,
  proposals: [],
  selectedProposalId: null,
  userPreferences: {},
  loading: false,
  error: null,

  setDataSetId: (id) => set({ dataSetId: id }),
  setAnalysisId: (id) => set({ analysisId: id }),
  setUserPreferences: (preferences) => set({ userPreferences: preferences }),

  generateProposals: async () => {
    const { dataSetId, analysisId, userPreferences } = get();
    if (!dataSetId) {
      set({ error: 'データセットを選択してください' });
      return;
    }

    set({ loading: true, error: null, status: 'generating' });
    try {
      const response = await invoke<{ job_id: string }>('generate_algorithm_proposals', {
        data_set_id: dataSetId,
        analysis_id: analysisId,
        num_proposals: 5,
        user_preferences: userPreferences
      });
      set({ jobId: response.job_id, loading: false });
    } catch (error) {
      set({ error: String(error), loading: false, status: 'error' });
    }
  },

  pollStatus: async () => {
    const { jobId } = get();
    if (!jobId) return;

    try {
      const status = await invoke<{ status: string; progress: number; message: string }>(
        'get_proposal_generation_status',
        { job_id: jobId }
      );
      set({ progress: status.progress, status: status.status as any });
      
      if (status.status === 'completed') {
        await get().fetchProposals();
      }
    } catch (error) {
      set({ error: String(error), status: 'error' });
    }
  },

  fetchProposals: async () => {
    const { jobId } = get();
    if (!jobId) return;

    try {
      const response = await invoke<{ proposals: AlgorithmProposal[] }>(
        'get_algorithm_proposals',
        { job_id: jobId }
      );
      set({ proposals: response.proposals, status: 'completed' });
    } catch (error) {
      set({ error: String(error) });
    }
  },

  selectProposal: async (proposalId: string, customName?: string) => {
    try {
      await invoke('select_algorithm', {
        proposal_id: proposalId,
        custom_name: customName
      });
      set({ selectedProposalId: proposalId });
    } catch (error) {
      set({ error: String(error) });
    }
  },

  clearError: () => set({ error: null }),
}));
```

## ユーザーフロー図

```
[アルゴリズム提案画面]
    │
    ├─→ [データセット選択]
    │       │
    │       └─→ [解析結果選択（オプション）]
    │
    ├─→ [ユーザー設定入力]
    │       │
    │       ├─→ [リスク許容度選択]
    │       ├─→ [取引頻度選択]
    │       └─→ [好みの指標選択]
    │
    └─→ [提案生成ボタンクリック]
            │
            ├─→ [進捗表示]
            │       │
            │       └─→ [ポーリング（2秒間隔）]
            │
            └─→ [提案一覧表示]
                    │
                    ├─→ [提案詳細表示]
                    │       │
                    │       └─→ [アルゴリズム選択]
                    │
                    └─→ [直接選択]
                            │
                            └─→ [確認ダイアログ]
                                    │
                                    └─→ [選択完了]
```

## レスポンシブデザイン

- **モバイル**: フォームを縦積み、提案カードを1列表示
- **タブレット**: 提案カードを2列表示
- **デスクトップ**: 提案カードを3列表示

## アクセシビリティ

- フォームのラベルと入力の適切な関連付け
- エラーメッセージの明確な表示
- キーボードナビゲーション対応
- スクリーンリーダー対応

## 注意事項

- 進捗表示はユーザーに明確なフィードバックを提供
- エラー発生時は分かりやすいメッセージを表示
- ローディング状態の適切な表示
- 提案がない場合の空状態表示

