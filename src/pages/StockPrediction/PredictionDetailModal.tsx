/**
 * Prediction Detail Modal Component
 * 
 * DEPENDENCY MAP:
 * 
 * Parents (Files that import this file):
 *   └─ src/pages/StockPrediction/PredictionList.tsx
 * 
 * Dependencies (External files that this file imports):
 *   ├─ @mantine/core
 *   ├─ src/types/stock-prediction
 *   └─ ./AssociationChain
 * 
 * Related Documentation:
 *   └─ Plan: docs/03_plans/stock-prediction/README.md
 */
import { Modal, Stack, Text, Badge, ScrollArea, Group, Divider } from '@mantine/core';
import { StockPrediction } from '../../types/stock-prediction';
import { AssociationChain } from './AssociationChain';

interface PredictionDetailModalProps {
  prediction: StockPrediction | null;
  opened: boolean;
  onClose: () => void;
}

export function PredictionDetailModal({ prediction, opened, onClose }: PredictionDetailModalProps) {
  if (!prediction) {
    return null;
  }

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
    <Modal
      opened={opened}
      onClose={onClose}
      title={`${prediction.symbol} - Stock Prediction`}
      size="xl"
    >
      <ScrollArea h={600}>
        <Stack gap="md">
          <Group justify="space-between">
            <Text size="sm" c="dimmed">
              Prediction ID: {prediction.prediction_id}
            </Text>
            <Group gap="xs">
              <Badge color={confidenceColor} variant="light" size="lg">
                Confidence: {(prediction.confidence_score * 100).toFixed(0)}%
              </Badge>
              <Badge color={directionColor} variant="light">
                {directionIcon} {prediction.predicted_direction.toUpperCase()}
              </Badge>
              <Badge color={actionColor} variant="light">
                {prediction.suggested_action.toUpperCase()}
              </Badge>
            </Group>
          </Group>

          {prediction.name && (
            <div>
              <Text fw={500} size="sm" mb="xs">
                Company Name
              </Text>
              <Text size="sm">{prediction.name}</Text>
            </div>
          )}

          {prediction.predicted_change_percent !== undefined && (
            <div>
              <Text fw={500} size="sm" mb="xs">
                Predicted Change
              </Text>
              <Text size="sm" c={prediction.predicted_change_percent >= 0 ? 'green' : 'red'}>
                {prediction.predicted_change_percent > 0 ? '+' : ''}
                {prediction.predicted_change_percent.toFixed(2)}%
              </Text>
            </div>
          )}

          {prediction.time_horizon && (
            <div>
              <Text fw={500} size="sm" mb="xs">
                Time Horizon
              </Text>
              <Badge variant="light">{prediction.time_horizon}</Badge>
            </div>
          )}

          <Divider />

          <div>
            <Text fw={500} size="sm" mb="xs">
              Reasoning
            </Text>
            <Text size="sm" style={{ whiteSpace: 'pre-wrap' }}>
              {prediction.reasoning || prediction.rationale || 'No reasoning provided'}
            </Text>
          </div>

          {prediction.risk_factors && prediction.risk_factors.length > 0 && (
            <div>
              <Text fw={500} size="sm" mb="xs">
                Risk Factors
              </Text>
              <Stack gap="xs">
                {prediction.risk_factors.map((risk, index) => (
                  <Badge key={index} color="red" variant="light">
                    {risk}
                  </Badge>
                ))}
              </Stack>
            </div>
          )}

          <Divider />

          {prediction.association_chain && prediction.association_chain.length > 0 && (
            <AssociationChain chain={prediction.association_chain} />
          )}

          {prediction.created_at && (
            <Text size="xs" c="dimmed">
              Created at: {new Date(prediction.created_at).toLocaleString()}
            </Text>
          )}
        </Stack>
      </ScrollArea>
    </Modal>
  );
}

