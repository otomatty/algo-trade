/**
 * Accuracy Stats Component
 * 
 * DEPENDENCY MAP:
 * 
 * Parents (Files that import this file):
 *   └─ src/pages/StockPrediction/PredictionHistory.tsx
 * 
 * Dependencies (External files that this file imports):
 *   ├─ @mantine/core
 *   └─ src/types/stock-prediction
 * 
 * Related Documentation:
 *   └─ Plan: docs/03_plans/stock-prediction/README.md
 */
import { Card, Text, Stack, Group, Progress } from '@mantine/core';
import { AccuracyStats as AccuracyStatsType } from '../../types/stock-prediction';

interface AccuracyStatsProps {
  stats: AccuracyStatsType;
}

export function AccuracyStats({ stats }: AccuracyStatsProps) {
  const accuracyPercentage = (stats.accuracy_rate * 100).toFixed(1);
  const accuracyColor = stats.accuracy_rate >= 0.7
    ? 'green'
    : stats.accuracy_rate >= 0.5
    ? 'yellow'
    : 'red';

  return (
    <Card p="md" withBorder>
      <Stack gap="md">
        <Text fw={500} size="lg">Accuracy Statistics</Text>
        
        <Group gap="md" grow>
          <Card p="sm" withBorder>
            <Stack gap="xs">
              <Text size="sm" c="dimmed">
                Total Predictions
              </Text>
              <Text size="xl" fw={500}>
                {stats.total_predictions}
              </Text>
            </Stack>
          </Card>

          <Card p="sm" withBorder>
            <Stack gap="xs">
              <Text size="sm" c="dimmed">
                Correct Predictions
              </Text>
              <Text size="xl" fw={500} c="green">
                {stats.correct_predictions}
              </Text>
            </Stack>
          </Card>

          <Card p="sm" withBorder>
            <Stack gap="xs">
              <Text size="sm" c="dimmed">
                Accuracy Rate
              </Text>
              <Text size="xl" fw={500} c={accuracyColor}>
                {accuracyPercentage}%
              </Text>
            </Stack>
          </Card>
        </Group>

        <div>
          <Group justify="space-between" mb="xs">
            <Text size="sm" c="dimmed">
              Accuracy Progress
            </Text>
            <Text size="sm" fw={500} c={accuracyColor}>
              {accuracyPercentage}%
            </Text>
          </Group>
          <Progress
            value={stats.accuracy_rate * 100}
            color={accuracyColor}
            size="lg"
            radius="xl"
          />
        </div>

        {stats.total_predictions > 0 && (
          <Text size="xs" c="dimmed">
            {stats.correct_predictions} out of {stats.total_predictions} predictions were correct.
          </Text>
        )}
      </Stack>
    </Card>
  );
}

