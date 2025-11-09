/**
 * Prediction Card Component
 * 
 * DEPENDENCY MAP:
 * 
 * Parents (Files that import this file):
 *   └─ src/pages/StockPrediction/PredictionList.tsx
 * 
 * Dependencies (External files that this file imports):
 *   ├─ @mantine/core
 *   └─ src/types/stock-prediction
 * 
 * Related Documentation:
 *   └─ Plan: docs/03_plans/stock-prediction/README.md
 */
import {
  Card,
  Text,
  Badge,
  Button,
  Stack,
  Group,
} from '@mantine/core';
import { StockPrediction } from '../../types/stock-prediction';

interface PredictionCardProps {
  prediction: StockPrediction;
  onViewDetails: (prediction: StockPrediction) => void;
}

export function PredictionCard({ prediction, onViewDetails }: PredictionCardProps) {
  const confidenceColor = prediction.confidence_score >= 0.8
    ? 'green'
    : prediction.confidence_score >= 0.6
    ? 'yellow'
    : 'red';

  const directionColor = prediction.predicted_direction === 'up'
    ? 'green'
    : prediction.predicted_direction === 'down'
    ? 'red'
    : 'gray';

  const directionIcon = prediction.predicted_direction === 'up'
    ? '↑'
    : prediction.predicted_direction === 'down'
    ? '↓'
    : '→';

  const actionColor = prediction.suggested_action === 'buy'
    ? 'green'
    : prediction.suggested_action === 'sell'
    ? 'red'
    : prediction.suggested_action === 'hold'
    ? 'yellow'
    : 'gray';

  return (
    <Card shadow="sm" padding="lg" radius="md" withBorder>
      <Stack gap="sm">
        <Group justify="space-between" align="flex-start">
          <div>
            <Text fw={500} size="lg">
              {prediction.symbol}
            </Text>
            {prediction.name && (
              <Text size="sm" c="dimmed">
                {prediction.name}
              </Text>
            )}
          </div>
          <Badge color={confidenceColor} variant="light">
            {(prediction.confidence_score * 100).toFixed(0)}%
          </Badge>
        </Group>

        <Group gap="xs">
          <Badge color={directionColor} variant="light">
            {directionIcon} {prediction.predicted_direction.toUpperCase()}
          </Badge>
          <Badge color={actionColor} variant="light">
            {prediction.suggested_action.toUpperCase()}
          </Badge>
        </Group>

        <Text size="sm" c="dimmed" lineClamp={2}>
          {prediction.reasoning || prediction.rationale || 'No reasoning provided'}
        </Text>

        {prediction.predicted_change_percent !== undefined && (
          <Text size="sm" fw={500}>
            Predicted Change: {prediction.predicted_change_percent > 0 ? '+' : ''}
            {prediction.predicted_change_percent.toFixed(2)}%
          </Text>
        )}

        <Button
          variant="light"
          size="xs"
          fullWidth
          onClick={() => onViewDetails(prediction)}
        >
          View Details
        </Button>
      </Stack>
    </Card>
  );
}

