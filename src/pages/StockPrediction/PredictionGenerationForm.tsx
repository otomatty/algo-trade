/**
 * Prediction Generation Form Component
 * 
 * DEPENDENCY MAP:
 * 
 * Parents (Files that import this file):
 *   └─ src/pages/StockPrediction/StockPrediction.tsx
 * 
 * Dependencies (External files that this file imports):
 *   ├─ @tauri-apps/api/core
 *   ├─ @mantine/core
 *   └─ src/types/stock-prediction
 * 
 * Related Documentation:
 *   └─ Plan: docs/03_plans/stock-prediction/README.md
 */
import { useState } from 'react';
import { invoke } from '@tauri-apps/api/core';
import {
  Select,
  Button,
  Stack,
  Text,
  Alert,
  Paper,
  NumberInput,
  Textarea,
  TextInput,
} from '@mantine/core';
import {
  GenerateStockPredictionsRequest,
  GenerateStockPredictionsResponse,
} from '../../types/stock-prediction';

interface PredictionGenerationFormProps {
  onJobStarted?: (jobId: string) => void;
}

export function PredictionGenerationForm({ onJobStarted }: PredictionGenerationFormProps) {
  const [newsJobId, setNewsJobId] = useState<string | null>(null);
  const [numPredictions, setNumPredictions] = useState<number>(5);
  const [riskTolerance, setRiskTolerance] = useState<'low' | 'medium' | 'high' | null>(null);
  const [investmentHorizon, setInvestmentHorizon] = useState<'short' | 'medium' | 'long' | null>(null);
  const [investmentStyle, setInvestmentStyle] = useState<'conservative' | 'balanced' | 'aggressive' | null>(null);
  const [marketTrends, setMarketTrends] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleGeneratePredictions = async () => {
    setLoading(true);
    setError(null);

    try {
      // Build user preferences object
      const userPreferences: GenerateStockPredictionsRequest['user_preferences'] = {};
      if (riskTolerance) {
        userPreferences.risk_tolerance = riskTolerance;
      }
      if (investmentHorizon) {
        userPreferences.investment_horizon = investmentHorizon;
      }
      if (investmentStyle) {
        userPreferences.investment_style = investmentStyle;
      }

      // Build request
      const request: GenerateStockPredictionsRequest = {
        news_job_id: newsJobId || undefined,
        num_predictions: numPredictions,
        user_preferences: Object.keys(userPreferences).length > 0 ? userPreferences : undefined,
        market_trends: marketTrends.trim() || undefined,
      };

      // Call generate_stock_predictions
      const response = await invoke<GenerateStockPredictionsResponse>('generate_stock_predictions', {
        news_job_id: request.news_job_id,
        num_predictions: request.num_predictions,
        user_preferences: request.user_preferences,
        market_trends: request.market_trends,
      });

      if (onJobStarted) {
        onJobStarted(response.job_id);
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to generate predictions';
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const riskToleranceOptions = [
    { value: 'low', label: 'Low' },
    { value: 'medium', label: 'Medium' },
    { value: 'high', label: 'High' },
  ];

  const investmentHorizonOptions = [
    { value: 'short', label: 'Short Term' },
    { value: 'medium', label: 'Medium Term' },
    { value: 'long', label: 'Long Term' },
  ];

  const investmentStyleOptions = [
    { value: 'conservative', label: 'Conservative' },
    { value: 'balanced', label: 'Balanced' },
    { value: 'aggressive', label: 'Aggressive' },
  ];

  return (
    <Paper p="md" withBorder>
      <Stack gap="md">
        <Text fw={500} size="lg">Generate Stock Predictions</Text>

        {error && (
          <Alert color="red">
            {error}
          </Alert>
        )}

        <TextInput
          label="News Job ID (Optional)"
          placeholder="Leave empty to use latest news"
          value={newsJobId || ''}
          onChange={(e) => setNewsJobId(e.currentTarget.value || null)}
          description="If provided, predictions will be based on news from this job. Otherwise, latest news will be used."
        />

        <NumberInput
          label="Number of Predictions"
          placeholder="Number of predictions to generate"
          value={numPredictions}
          onChange={(value) => setNumPredictions(typeof value === 'number' ? value : 5)}
          min={1}
          max={10}
          required
        />

        <Select
          label="Risk Tolerance"
          placeholder="Select risk tolerance (optional)"
          data={riskToleranceOptions}
          value={riskTolerance || null}
          onChange={(value) => setRiskTolerance(value as 'low' | 'medium' | 'high' | null)}
          clearable
        />

        <Select
          label="Investment Horizon"
          placeholder="Select investment horizon (optional)"
          data={investmentHorizonOptions}
          value={investmentHorizon || null}
          onChange={(value) => setInvestmentHorizon(value as 'short' | 'medium' | 'long' | null)}
          clearable
        />

        <Select
          label="Investment Style"
          placeholder="Select investment style (optional)"
          data={investmentStyleOptions}
          value={investmentStyle || null}
          onChange={(value) => setInvestmentStyle(value as 'conservative' | 'balanced' | 'aggressive' | null)}
          clearable
        />

        <Textarea
          label="Market Trends (Optional)"
          placeholder="Enter any additional market trends or context..."
          value={marketTrends}
          onChange={(e) => setMarketTrends(e.currentTarget.value)}
          rows={3}
          description="Additional context about current market trends that may influence predictions"
        />

        <Button
          onClick={handleGeneratePredictions}
          loading={loading}
        >
          Generate Predictions
        </Button>
      </Stack>
    </Paper>
  );
}

