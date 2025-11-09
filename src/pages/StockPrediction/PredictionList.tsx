/**
 * Prediction List Component
 * 
 * DEPENDENCY MAP:
 * 
 * Parents (Files that import this file):
 *   └─ src/pages/StockPrediction/StockPrediction.tsx
 * 
 * Dependencies (External files that this file imports):
 *   ├─ @mantine/core
 *   ├─ src/types/stock-prediction
 *   ├─ ./PredictionCard
 *   └─ ./PredictionDetailModal
 * 
 * Related Documentation:
 *   └─ Plan: docs/03_plans/stock-prediction/README.md
 */
import { useState } from 'react';
import { Paper, Text, Stack, Grid } from '@mantine/core';
import { StockPrediction } from '../../types/stock-prediction';
import { PredictionCard } from './PredictionCard';
import { PredictionDetailModal } from './PredictionDetailModal';

interface PredictionListProps {
  predictions: StockPrediction[];
}

export function PredictionList({ predictions }: PredictionListProps) {
  const [selectedPrediction, setSelectedPrediction] = useState<StockPrediction | null>(null);
  const [modalOpened, setModalOpened] = useState(false);

  const handleViewDetails = (prediction: StockPrediction) => {
    setSelectedPrediction(prediction);
    setModalOpened(true);
  };

  const handleCloseModal = () => {
    setModalOpened(false);
    setSelectedPrediction(null);
  };

  if (predictions.length === 0) {
    return (
      <Paper p="md" withBorder>
        <Stack gap="sm" align="center">
          <Text c="dimmed" size="sm">
            予測が生成されると、ここに表示されます
          </Text>
          <Text c="dimmed" size="xs">
            Predictions will be displayed here once generated
          </Text>
        </Stack>
      </Paper>
    );
  }

  return (
    <>
      <Paper p="md" withBorder>
        <Stack gap="md">
          <Text fw={500} size="lg">
            Stock Predictions
          </Text>
          <Grid>
            {predictions.map((prediction) => (
              <Grid.Col key={prediction.prediction_id} span={{ base: 12, sm: 6, md: 4 }}>
                <PredictionCard
                  prediction={prediction}
                  onViewDetails={handleViewDetails}
                />
              </Grid.Col>
            ))}
          </Grid>
        </Stack>
      </Paper>
      <PredictionDetailModal
        prediction={selectedPrediction}
        opened={modalOpened}
        onClose={handleCloseModal}
      />
    </>
  );
}

