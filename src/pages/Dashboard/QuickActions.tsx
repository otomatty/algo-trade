/**
 * Quick Actions Component
 * 
 * DEPENDENCY MAP:
 * 
 * Parents (Files that import this file):
 *   └─ src/pages/Dashboard/Dashboard.tsx
 * 
 * Dependencies (External files that this file imports):
 *   ├─ @mantine/core
 *   ├─ @mantine/modals
 *   └─ src/stores/dashboard
 * 
 * Related Documentation:
 *   ├─ Spec: src/pages/Dashboard/Dashboard.spec.md
 *   └─ Plan: docs/03_plans/dashboard/README.md
 */
import { Button, Group } from '@mantine/core';
import { modals } from '@mantine/modals';
import { useDashboardStore } from '../../stores/dashboard';

interface QuickActionsProps {
  onNavigate?: (page: string) => void;
}

export function QuickActions({ onNavigate }: QuickActionsProps) {
  const { deleteAlgorithm } = useDashboardStore();

  const handleDelete = (algorithmId: number, algorithmName: string) => {
    modals.openConfirmModal({
      title: 'アルゴリズムの削除',
      children: (
        <div>
          <p>アルゴリズム「{algorithmName}」を削除してもよろしいですか？</p>
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

  const handleNavigateToProposal = () => {
    if (onNavigate) {
      onNavigate('algorithm-proposal');
    }
  };

  return (
    <Group gap="md">
      <Button onClick={handleNavigateToProposal} variant="light">
        アルゴリズム提案
      </Button>
    </Group>
  );
}

