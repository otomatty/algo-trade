/**
 * Algorithm List Component
 * 
 * DEPENDENCY MAP:
 * 
 * Parents (Files that import this file):
 *   └─ src/pages/Dashboard/Dashboard.tsx
 * 
 * Dependencies (External files that this file imports):
 *   ├─ @mantine/core
 *   ├─ src/types/algorithm
 *   ├─ src/types/dashboard
 *   └─ ./AlgorithmCard
 * 
 * Related Documentation:
 *   ├─ Spec: src/pages/Dashboard/Dashboard.spec.md
 *   └─ Plan: docs/03_plans/dashboard/README.md
 */
import { Paper, Text, Stack, Grid, Skeleton } from '@mantine/core';
import { Algorithm } from '../../types/algorithm';
import { BacktestResultSummary } from '../../types/dashboard';
import { AlgorithmCard } from './AlgorithmCard';

interface AlgorithmListProps {
  algorithms: Algorithm[];
  backtestResults?: BacktestResultSummary[];
  loading?: boolean;
  onSelect?: (algorithm: Algorithm) => void;
  onDelete?: (algorithmId: number) => void;
}

export function AlgorithmList({
  algorithms,
  backtestResults = [],
  loading = false,
  onSelect,
  onDelete,
}: AlgorithmListProps) {
  const getBacktestResult = (algorithmId: number): BacktestResultSummary | undefined => {
    return backtestResults.find((result) => result.algorithm_id === algorithmId);
  };

  if (loading) {
    return (
      <Paper p="md" withBorder>
        <Stack gap="md">
          <Text fw={500} size="lg">
            Algorithms
          </Text>
          <Grid>
            {[1, 2, 3].map((i) => (
              <Grid.Col key={i} span={{ base: 12, sm: 6, md: 4 }}>
                <Skeleton height={200} radius="md" />
              </Grid.Col>
            ))}
          </Grid>
        </Stack>
      </Paper>
    );
  }

  if (algorithms.length === 0) {
    return (
      <Paper p="md" withBorder>
        <Stack gap="sm" align="center">
          <Text c="dimmed" size="sm">
            アルゴリズムが選択されていません。まずアルゴリズム提案を生成してください。
          </Text>
          <Text c="dimmed" size="xs">
            No algorithms selected. Please generate algorithm proposals first.
          </Text>
        </Stack>
      </Paper>
    );
  }

  return (
    <Paper p="md" withBorder>
      <Stack gap="md">
        <Text fw={500} size="lg">
          Algorithms
        </Text>
        <Grid>
          {algorithms.map((algorithm) => (
            <Grid.Col key={algorithm.id} span={{ base: 12, sm: 6, md: 4 }}>
              <AlgorithmCard
                algorithm={algorithm}
                backtestResult={getBacktestResult(algorithm.id)}
                onSelect={onSelect}
                onDelete={onDelete}
              />
            </Grid.Col>
          ))}
        </Grid>
      </Stack>
    </Paper>
  );
}

