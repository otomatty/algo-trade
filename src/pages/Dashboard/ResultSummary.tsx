/**
 * Result Summary Component
 * 
 * DEPENDENCY MAP:
 * 
 * Parents (Files that import this file):
 *   └─ src/pages/Dashboard/Dashboard.tsx
 * 
 * Dependencies (External files that this file imports):
 *   ├─ @mantine/core
 *   ├─ src/types/dashboard
 *   └─ ./PerformanceCard
 * 
 * Related Documentation:
 *   ├─ Spec: src/pages/Dashboard/Dashboard.spec.md
 *   └─ Plan: docs/03_plans/dashboard/README.md
 */
import { Paper, Text, Stack, Grid, Skeleton } from '@mantine/core';
import { BacktestResultSummary } from '../../types/dashboard';
import { PerformanceCard } from './PerformanceCard';

interface ResultSummaryProps {
  results: BacktestResultSummary[];
  loading?: boolean;
  selectedAlgorithmId?: number;
}

export function ResultSummary({
  results,
  loading = false,
  selectedAlgorithmId,
}: ResultSummaryProps) {
  const filteredResults = selectedAlgorithmId
    ? results.filter((r) => r.algorithm_id === selectedAlgorithmId)
    : results;

  if (loading) {
    return (
      <Paper p="md" withBorder>
        <Stack gap="md">
          <Text fw={500} size="lg">
            Performance Summary
          </Text>
          <Grid>
            {[1, 2, 3, 4].map((i) => (
              <Grid.Col key={i} span={{ base: 12, sm: 6, md: 3 }}>
                <Skeleton height={100} radius="md" />
              </Grid.Col>
            ))}
          </Grid>
        </Stack>
      </Paper>
    );
  }

  if (filteredResults.length === 0) {
    return (
      <Paper p="md" withBorder>
        <Stack gap="sm" align="center">
          <Text fw={500} size="lg">
            Performance Summary
          </Text>
          <Text c="dimmed" size="sm">
            バックテスト結果がありません。まずバックテストを実行してください。
          </Text>
          <Text c="dimmed" size="xs">
            No backtest results available. Please run a backtest first.
          </Text>
        </Stack>
      </Paper>
    );
  }

  // Aggregate performance metrics across all results
  const aggregateMetrics = filteredResults.reduce(
    (acc, result) => {
      acc.total_return += result.performance.total_return;
      acc.sharpe_ratio += result.performance.sharpe_ratio;
      acc.max_drawdown = Math.max(acc.max_drawdown, result.performance.max_drawdown);
      acc.win_rate += result.performance.win_rate;
      acc.total_trades += result.performance.total_trades;
      acc.average_profit += result.performance.average_profit;
      acc.average_loss += result.performance.average_loss;
      return acc;
    },
    {
      total_return: 0,
      sharpe_ratio: 0,
      max_drawdown: 0,
      win_rate: 0,
      total_trades: 0,
      average_profit: 0,
      average_loss: 0,
    }
  );

  const count = filteredResults.length;
  const avgTotalReturn = aggregateMetrics.total_return / count;
  const avgSharpeRatio = aggregateMetrics.sharpe_ratio / count;
  const avgWinRate = aggregateMetrics.win_rate / count;
  const avgProfit = aggregateMetrics.average_profit / count;
  const avgLoss = aggregateMetrics.average_loss / count;

  return (
    <Paper p="md" withBorder>
      <Stack gap="md">
        <Text fw={500} size="lg">
          Performance Summary
        </Text>
        <Grid>
          <Grid.Col span={{ base: 12, sm: 6, md: 3 }}>
            <PerformanceCard
              label="Total Return"
              value={`${avgTotalReturn >= 0 ? '+' : ''}${avgTotalReturn.toFixed(2)}%`}
              color={avgTotalReturn >= 0 ? 'green' : 'red'}
            />
          </Grid.Col>
          <Grid.Col span={{ base: 12, sm: 6, md: 3 }}>
            <PerformanceCard
              label="Sharpe Ratio"
              value={avgSharpeRatio.toFixed(2)}
              color="blue"
            />
          </Grid.Col>
          <Grid.Col span={{ base: 12, sm: 6, md: 3 }}>
            <PerformanceCard
              label="Max Drawdown"
              value={`${aggregateMetrics.max_drawdown.toFixed(2)}%`}
              color="red"
            />
          </Grid.Col>
          <Grid.Col span={{ base: 12, sm: 6, md: 3 }}>
            <PerformanceCard
              label="Win Rate"
              value={`${avgWinRate.toFixed(2)}%`}
              color="blue"
            />
          </Grid.Col>
          <Grid.Col span={{ base: 12, sm: 6, md: 3 }}>
            <PerformanceCard
              label="Total Trades"
              value={aggregateMetrics.total_trades.toString()}
              color="gray"
            />
          </Grid.Col>
          <Grid.Col span={{ base: 12, sm: 6, md: 3 }}>
            <PerformanceCard
              label="Average Profit"
              value={`$${avgProfit.toFixed(2)}`}
              color="green"
            />
          </Grid.Col>
          <Grid.Col span={{ base: 12, sm: 6, md: 3 }}>
            <PerformanceCard
              label="Average Loss"
              value={`$${avgLoss.toFixed(2)}`}
              color="red"
            />
          </Grid.Col>
        </Grid>
      </Stack>
    </Paper>
  );
}

