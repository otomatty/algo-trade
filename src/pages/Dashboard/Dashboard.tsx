/**
 * Dashboard Main Component
 * 
 * DEPENDENCY MAP:
 * 
 * Parents (Files that import this file):
 *   └─ src/App.tsx (via routing)
 * 
 * Dependencies (External files that this file imports):
 *   ├─ @mantine/core
 *   ├─ @mantine/hooks
 *   ├─ ./Sidebar
 *   ├─ ./Header
 *   └─ src/stores/dashboard (to be created in Phase 2)
 * 
 * Related Documentation:
 *   ├─ Spec: src/pages/Dashboard/Dashboard.spec.md
 *   ├─ Tests: src/pages/Dashboard/Dashboard.test.tsx
 *   └─ Plan: docs/03_plans/dashboard/README.md
 */
import { useEffect } from 'react';
import { AppShell, Container, Stack, Alert } from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';
import { Sidebar } from './Sidebar';
import { Header } from './Header';
import { AlgorithmList } from './AlgorithmList';
import { ResultSummary } from './ResultSummary';
import { QuickActions } from './QuickActions';
import { useDashboardStore } from '../../stores/dashboard';
import { Algorithm } from '../../types/algorithm';

interface DashboardProps {
  currentPage?: string;
  onNavigate?: (page: string) => void;
}

export function Dashboard({ currentPage = 'dashboard', onNavigate }: DashboardProps) {
  const [opened, { toggle }] = useDisclosure();
  const {
    algorithms,
    backtestResults,
    loading,
    error,
    fetchAlgorithms,
    fetchBacktestResults,
    deleteAlgorithm,
  } = useDashboardStore();

  useEffect(() => {
    fetchAlgorithms();
  }, [fetchAlgorithms]);

  useEffect(() => {
    if (algorithms.length > 0) {
      const algorithmIds = algorithms.map((a) => a.id);
      fetchBacktestResults(algorithmIds);
    }
  }, [algorithms, fetchBacktestResults]);

  const handleDelete = async (algorithmId: number) => {
    const algorithm = algorithms.find((a) => a.id === algorithmId);
    if (!algorithm) return;

    // Use Mantine modals for confirmation
    const { modals } = await import('@mantine/modals');
    modals.openConfirmModal({
      title: 'アルゴリズムの削除',
      children: (
        <div>
          <p>アルゴリズム「{algorithm.name}」を削除してもよろしいですか？</p>
          <p style={{ fontSize: '0.875rem', color: '#666' }}>
            この操作は取り消せません。関連するバックテスト結果も削除されます。
          </p>
        </div>
      ),
      labels: { confirm: '削除', cancel: 'キャンセル' },
      confirmProps: { color: 'red' },
      onConfirm: async () => {
        try {
          await deleteAlgorithm(algorithmId);
          modals.closeAll();
        } catch (error) {
          modals.openConfirmModal({
            title: 'エラー',
            children: (
              <p>
                {error instanceof Error ? error.message : 'アルゴリズムの削除に失敗しました。'}
              </p>
            ),
            labels: { confirm: 'OK', cancel: '' },
            cancelProps: { style: { display: 'none' } },
          });
        }
      },
    });
  };

  const handleSelect = (algorithm: Algorithm) => {
    // Navigate to algorithm details or backtest page
    if (onNavigate) {
      onNavigate('backtest');
    }
  };

  return (
    <AppShell
      navbar={{
        width: 250,
        breakpoint: 'sm',
        collapsed: { mobile: !opened },
      }}
      header={{ height: 60 }}
      padding="md"
    >
      <AppShell.Header>
        <Header />
      </AppShell.Header>

      <AppShell.Navbar p="md">
        <Sidebar currentPage={currentPage} onNavigate={onNavigate} />
      </AppShell.Navbar>

      <AppShell.Main>
        <Container size="xl" py="md">
          <Stack gap="md">
            {error && (
              <Alert color="red" title="Error">
                {error}
              </Alert>
            )}
            <QuickActions onNavigate={onNavigate} />
            <AlgorithmList
              algorithms={algorithms}
              backtestResults={backtestResults}
              loading={loading}
              onSelect={handleSelect}
              onDelete={handleDelete}
            />
            <ResultSummary results={backtestResults} loading={loading} />
          </Stack>
        </Container>
      </AppShell.Main>
    </AppShell>
  );
}

