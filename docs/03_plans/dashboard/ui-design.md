# ダッシュボード機能 UI/UX設計書

## 概要

ダッシュボード機能のUI/UX設計詳細です。

## 関連ドキュメント

- **実装計画**: `docs/03_plans/dashboard/README.md`
- **データモデル**: `docs/03_plans/dashboard/data-model.md`

## 画面レイアウト設計

### 全体レイアウト

```
┌─────────────────────────────────────────────────────────┐
│ Header (アプリ名、ユーザー情報)                            │
├──────────┬──────────────────────────────────────────────┤
│          │                                              │
│ Sidebar  │         Main Content Area                    │
│          │                                              │
│ - ダッシュ│  ┌──────────────────────────────────────┐  │
│   ボード │  │ Algorithm List                        │  │
│ - アルゴリ│  │ ┌──────────┐ ┌──────────┐          │  │
│   ズム提案│  │ │ Algo 1   │ │ Algo 2   │          │  │
│ - バックテ│  │ │ +15.2%   │ │ +8.5%    │          │  │
│   スト   │  │ │ Sharpe:  │ │ Sharpe:  │          │  │
│ - データ管│  │ │   1.2    │ │   0.8    │          │  │
│   理     │  │ └──────────┘ └──────────┘          │  │
│ - データ解│  │                                      │  │
│   析     │  │ ┌──────────────────────────────────┐ │  │
│ - 銘柄予測│  │ │ Performance Summary              │ │  │
│          │  │ │ [Chart Area]                     │ │  │
│          │  │ └──────────────────────────────────┘ │  │
│          │                                              │
└──────────┴──────────────────────────────────────────────┘
```

## コンポーネント構造

```
Dashboard/
├── Dashboard.tsx              # メインコンポーネント
│   ├── Header.tsx             # ヘッダー
│   ├── Sidebar.tsx            # サイドバーナビゲーション
│   └── MainContent.tsx        # メインコンテンツエリア
│       ├── AlgorithmList.tsx  # アルゴリズム一覧
│       │   └── AlgorithmCard.tsx  # アルゴリズムカード
│       └── ResultSummary.tsx  # 検証結果サマリー
│           └── PerformanceChart.tsx  # パフォーマンスチャート
└── QuickActions.tsx           # クイックアクション
```

## コンポーネント詳細設計

### Dashboard.tsx

**役割**: ダッシュボードのメインコンテナ

**Props**: なし

**State管理**: Zustand storeを使用

**レイアウト**:
- Mantineの`AppShell`コンポーネントを使用
- レスポンシブ対応（モバイル時はサイドバーをドロワーに）

```typescript
import { AppShell } from '@mantine/core';
import { useDashboardStore } from '@/stores/dashboard';

export function Dashboard() {
  const { algorithms, backtestResults, loading, fetchAlgorithms } = useDashboardStore();

  useEffect(() => {
    fetchAlgorithms();
  }, []);

  return (
    <AppShell
      navbar={<Sidebar />}
      header={<Header />}
    >
      <MainContent
        algorithms={algorithms}
        backtestResults={backtestResults}
        loading={loading}
      />
    </AppShell>
  );
}
```

### AlgorithmList.tsx

**役割**: アルゴリズム一覧の表示

**Props**:
```typescript
interface AlgorithmListProps {
  algorithms: Algorithm[];
  onSelect?: (algorithm: Algorithm) => void;
  onDelete?: (algorithmId: number) => void;
}
```

**レイアウト**:
- Mantineの`Grid`コンポーネントを使用
- カード形式で表示
- レスポンシブ: デスクトップ3列、タブレット2列、モバイル1列

```typescript
import { Grid } from '@mantine/core';
import { AlgorithmCard } from './AlgorithmCard';

export function AlgorithmList({ algorithms, onSelect, onDelete }: AlgorithmListProps) {
  return (
    <Grid>
      {algorithms.map((algorithm) => (
        <Grid.Col key={algorithm.id} span={{ base: 12, sm: 6, md: 4 }}>
          <AlgorithmCard
            algorithm={algorithm}
            onSelect={onSelect}
            onDelete={onDelete}
          />
        </Grid.Col>
      ))}
    </Grid>
  );
}
```

### AlgorithmCard.tsx

**役割**: 個別のアルゴリズムカード表示

**Props**:
```typescript
interface AlgorithmCardProps {
  algorithm: Algorithm;
  backtestResult?: BacktestResultSummary;
  onSelect?: (algorithm: Algorithm) => void;
  onDelete?: (algorithmId: number) => void;
}
```

**表示内容**:
- アルゴリズム名
- 説明（省略可能）
- 最新のパフォーマンス指標（総リターン、シャープレシオ）
- アクションボタン（詳細、削除）

```typescript
import { Card, Text, Badge, Group, Button } from '@mantine/core';

export function AlgorithmCard({ algorithm, backtestResult, onSelect, onDelete }: AlgorithmCardProps) {
  return (
    <Card shadow="sm" padding="lg" radius="md" withBorder>
      <Group justify="space-between" mb="xs">
        <Text fw={500}>{algorithm.name}</Text>
        {backtestResult && (
          <Badge color={backtestResult.performance.total_return > 0 ? 'green' : 'red'}>
            {backtestResult.performance.total_return.toFixed(2)}%
          </Badge>
        )}
      </Group>

      {algorithm.description && (
        <Text size="sm" c="dimmed" mb="md">
          {algorithm.description}
        </Text>
      )}

      {backtestResult && (
        <Group gap="xs" mb="md">
          <Text size="xs">Sharpe: {backtestResult.performance.sharpe_ratio.toFixed(2)}</Text>
          <Text size="xs">Win Rate: {backtestResult.performance.win_rate.toFixed(1)}%</Text>
        </Group>
      )}

      <Group justify="flex-end">
        <Button variant="light" size="xs" onClick={() => onSelect?.(algorithm)}>
          詳細
        </Button>
        <Button variant="light" color="red" size="xs" onClick={() => onDelete?.(algorithm.id)}>
          削除
        </Button>
      </Group>
    </Card>
  );
}
```

### ResultSummary.tsx

**役割**: 検証結果のサマリー表示

**Props**:
```typescript
interface ResultSummaryProps {
  results: BacktestResultSummary[];
  selectedAlgorithmId?: number;
}
```

**表示内容**:
- パフォーマンス指標の一覧表示
- チャート表示（オプション）

## 状態管理設計

### Zustand Store

```typescript
import { create } from 'zustand';
import { invoke } from '@tauri-apps/api/core';
import type { Algorithm, BacktestResultSummary } from '@/types';

interface DashboardState {
  algorithms: Algorithm[];
  backtestResults: BacktestResultSummary[];
  loading: boolean;
  error: string | null;
  selectedAlgorithmId: number | null;
}

interface DashboardActions {
  fetchAlgorithms: () => Promise<void>;
  fetchBacktestResults: (algorithmIds?: number[]) => Promise<void>;
  deleteAlgorithm: (algorithmId: number) => Promise<void>;
  setSelectedAlgorithmId: (id: number | null) => void;
  clearError: () => void;
}

export const useDashboardStore = create<DashboardState & DashboardActions>((set, get) => ({
  algorithms: [],
  backtestResults: [],
  loading: false,
  error: null,
  selectedAlgorithmId: null,

  fetchAlgorithms: async () => {
    set({ loading: true, error: null });
    try {
      const response = await invoke<{ algorithms: Algorithm[] }>('get_selected_algorithms');
      set({ algorithms: response.algorithms, loading: false });
    } catch (error) {
      set({ error: String(error), loading: false });
    }
  },

  fetchBacktestResults: async (algorithmIds) => {
    set({ loading: true, error: null });
    try {
      const response = await invoke<{ results: BacktestResultSummary[] }>(
        'get_backtest_results',
        { algorithm_ids: algorithmIds }
      );
      set({ backtestResults: response.results, loading: false });
    } catch (error) {
      set({ error: String(error), loading: false });
    }
  },

  deleteAlgorithm: async (algorithmId: number) => {
    try {
      await invoke('delete_algorithm', { algo_id: algorithmId });
      await get().fetchAlgorithms();
    } catch (error) {
      set({ error: String(error) });
    }
  },

  setSelectedAlgorithmId: (id) => set({ selectedAlgorithmId: id }),
  clearError: () => set({ error: null }),
}));
```

## ユーザーフロー図

```
[アプリ起動]
    │
    ▼
[ダッシュボード表示]
    │
    ├─→ [アルゴリズム一覧表示]
    │       │
    │       ├─→ [アルゴリズム詳細表示]
    │       │
    │       └─→ [アルゴリズム削除]
    │               │
    │               └─→ [確認ダイアログ]
    │                       │
    │                       └─→ [削除実行]
    │
    └─→ [検証結果サマリー表示]
            │
            └─→ [詳細チャート表示]
```

## レスポンシブデザイン

### ブレークポイント

- **モバイル**: < 768px
- **タブレット**: 768px - 1024px
- **デスクトップ**: > 1024px

### レイアウト変更

- **モバイル**: サイドバーをドロワーに変更、アルゴリズムカードを1列表示
- **タブレット**: アルゴリズムカードを2列表示
- **デスクトップ**: アルゴリズムカードを3列表示

## アクセシビリティ

- ARIA属性の適切な使用
- キーボードナビゲーション対応
- スクリーンリーダー対応
- コントラスト比の確保（WCAG 2.1 AA準拠）

## 注意事項

- Mantineのテーマ設定を統一
- ローディング状態の適切な表示（Skeleton loader等）
- エラー状態の分かりやすい表示
- 空状態の適切な表示（アルゴリズムがない場合等）

