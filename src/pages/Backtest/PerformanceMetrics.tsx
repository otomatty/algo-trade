/**
 * Performance Metrics Component
 * 
 * DEPENDENCY MAP:
 * 
 * Parents (Files that import this file):
 *   └─ src/pages/Backtest/BacktestResults.tsx
 * 
 * Dependencies (External files that this file imports):
 *   ├─ @mantine/core
 *   └─ src/types/backtest
 * 
 * Related Documentation:
 *   └─ Plan: docs/03_plans/backtest/README.md
 */
import { Grid, Card, Text, Stack } from '@mantine/core';
import { PerformanceMetrics as PerformanceMetricsType } from '../../types/backtest';

interface PerformanceMetricsProps {
  performance: PerformanceMetricsType;
}

export function PerformanceMetrics({ performance }: PerformanceMetricsProps) {
  const metrics = [
    {
      label: 'Total Return',
      value: `${performance.total_return >= 0 ? '+' : ''}${performance.total_return.toFixed(2)}%`,
      color: performance.total_return >= 0 ? 'green' : 'red',
    },
    {
      label: 'Sharpe Ratio',
      value: performance.sharpe_ratio.toFixed(2),
      color: 'blue',
    },
    {
      label: 'Max Drawdown',
      value: `${performance.max_drawdown.toFixed(2)}%`,
      color: 'red',
    },
    {
      label: 'Win Rate',
      value: `${performance.win_rate.toFixed(2)}%`,
      color: 'blue',
    },
    {
      label: 'Total Trades',
      value: performance.total_trades.toString(),
      color: 'gray',
    },
    {
      label: 'Average Profit',
      value: `$${performance.average_profit.toFixed(2)}`,
      color: 'green',
    },
    {
      label: 'Average Loss',
      value: `$${performance.average_loss.toFixed(2)}`,
      color: 'red',
    },
  ];

  return (
    <Grid>
      {metrics.map((metric) => (
        <Grid.Col key={metric.label} span={{ base: 12, sm: 6, md: 4 }}>
          <Card p="md" withBorder>
            <Stack gap="xs">
              <Text size="sm" c="dimmed">
                {metric.label}
              </Text>
              <Text size="xl" fw={500} c={metric.color}>
                {metric.value}
              </Text>
            </Stack>
          </Card>
        </Grid.Col>
      ))}
    </Grid>
  );
}

