/**
 * Algorithm Card Component
 * 
 * DEPENDENCY MAP:
 * 
 * Parents (Files that import this file):
 *   └─ src/pages/Dashboard/AlgorithmList.tsx
 * 
 * Dependencies (External files that this file imports):
 *   ├─ @mantine/core
 *   ├─ src/types/algorithm
 *   └─ src/types/dashboard
 * 
 * Related Documentation:
 *   ├─ Spec: src/pages/Dashboard/Dashboard.spec.md
 *   └─ Plan: docs/03_plans/dashboard/README.md
 */
import {
  Card,
  Text,
  Badge,
  Button,
  Stack,
  Group,
} from '@mantine/core';
import { Algorithm } from '../../types/algorithm';
import { BacktestResultSummary } from '../../types/dashboard';

interface AlgorithmCardProps {
  algorithm: Algorithm;
  backtestResult?: BacktestResultSummary;
  onSelect?: (algorithm: Algorithm) => void;
  onDelete?: (algorithmId: number) => void;
}

export function AlgorithmCard({ algorithm, backtestResult, onSelect, onDelete }: AlgorithmCardProps) {
  const returnColor = backtestResult?.performance.total_return
    ? backtestResult.performance.total_return > 0
      ? 'green'
      : 'red'
    : 'gray';

  return (
    <Card shadow="sm" padding="lg" radius="md" withBorder>
      <Stack gap="sm">
        <Group justify="space-between" align="flex-start">
          <div>
            <Text fw={500} size="lg">
              {algorithm.name}
            </Text>
            {algorithm.description && (
              <Text size="sm" c="dimmed" lineClamp={2}>
                {algorithm.description}
              </Text>
            )}
          </div>
          {backtestResult && (
            <Badge color={returnColor} variant="light">
              {backtestResult.performance.total_return.toFixed(2)}%
            </Badge>
          )}
        </Group>

        {backtestResult && (
          <Group gap="xs">
            <Text size="xs" c="dimmed">
              Sharpe: {backtestResult.performance.sharpe_ratio.toFixed(2)}
            </Text>
            <Text size="xs" c="dimmed">
              Win Rate: {backtestResult.performance.win_rate.toFixed(1)}%
            </Text>
          </Group>
        )}

        <Group justify="flex-end" gap="xs">
          {onSelect && (
            <Button
              variant="light"
              size="xs"
              onClick={() => onSelect(algorithm)}
            >
              詳細
            </Button>
          )}
          {onDelete && (
            <Button
              variant="light"
              color="red"
              size="xs"
              onClick={() => onDelete(algorithm.id)}
            >
              削除
            </Button>
          )}
        </Group>
      </Stack>
    </Card>
  );
}

