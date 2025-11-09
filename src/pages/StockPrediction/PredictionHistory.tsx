/**
 * Prediction History Component
 * 
 * DEPENDENCY MAP:
 * 
 * Parents (Files that import this file):
 *   └─ src/pages/StockPrediction/StockPrediction.tsx
 * 
 * Dependencies (External files that this file imports):
 *   ├─ @tauri-apps/api/core
 *   ├─ @mantine/core
 *   ├─ @mantine/dates
 *   ├─ src/types/stock-prediction
 *   └─ ./AccuracyStats
 * 
 * Related Documentation:
 *   └─ Plan: docs/03_plans/stock-prediction/README.md
 */
import { useState, useEffect } from 'react';
import { invoke } from '@tauri-apps/api/core';
import {
  Paper,
  Table,
  Text,
  Stack,
  Group,
  Button,
  TextInput,
  Badge,
  Loader,
  Center,
} from '@mantine/core';
import { DatePickerInput } from '@mantine/dates';
import { GetPredictionHistoryResponse, PredictionHistory as PredictionHistoryType } from '../../types/stock-prediction';
import { AccuracyStats } from './AccuracyStats';

interface PredictionHistoryProps {
  onUpdateAccuracy?: (predictionId: string) => void;
}

export function PredictionHistory({ onUpdateAccuracy }: PredictionHistoryProps) {
  const [predictions, setPredictions] = useState<PredictionHistoryType[]>([]);
  const [accuracyStats, setAccuracyStats] = useState<{ total_predictions: number; correct_predictions: number; accuracy_rate: number } | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  // Filter state
  const [limit, setLimit] = useState<number>(50);
  const [startDate, setStartDate] = useState<Date | null>(null);
  const [endDate, setEndDate] = useState<Date | null>(null);
  const [symbolFilter, setSymbolFilter] = useState<string>('');

  const loadHistory = async () => {
    setLoading(true);
    setError(null);
    try {
      const request = {
        limit: limit || undefined,
        start_date: startDate ? startDate.toISOString().split('T')[0] : undefined,
        end_date: endDate ? endDate.toISOString().split('T')[0] : undefined,
        symbol: symbolFilter.trim() || undefined,
      };

      const response = await invoke<GetPredictionHistoryResponse>('get_prediction_history', request);
      setPredictions(response.predictions || []);
      setAccuracyStats(response.accuracy_stats || null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load prediction history');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadHistory();
  }, []);

  const handleFilter = () => {
    loadHistory();
  };

  const handleClearFilters = () => {
    setLimit(50);
    setStartDate(null);
    setEndDate(null);
    setSymbolFilter('');
    loadHistory();
  };

  const getDirectionColor = (direction: string) => {
    switch (direction) {
      case 'up':
        return 'green';
      case 'down':
        return 'red';
      case 'sideways':
        return 'gray';
      default:
        return 'gray';
    }
  };

  const getDirectionIcon = (direction: string) => {
    switch (direction) {
      case 'up':
        return '↑';
      case 'down':
        return '↓';
      case 'sideways':
        return '→';
      default:
        return '?';
    }
  };

  const getActionColor = (action?: string) => {
    switch (action) {
      case 'buy':
        return 'green';
      case 'sell':
        return 'red';
      case 'hold':
        return 'yellow';
      case 'watch':
        return 'blue';
      case 'ignore':
        return 'gray';
      default:
        return 'gray';
    }
  };

  return (
    <Stack gap="md">
      <Paper p="md" withBorder>
        <Stack gap="md">
          <Group justify="space-between">
            <Text fw={500} size="lg">Prediction History</Text>
            <Button onClick={loadHistory} loading={loading} size="xs">
              Refresh
            </Button>
          </Group>

          {/* Filters */}
          <Group gap="md" align="flex-end">
            <TextInput
              label="Symbol"
              placeholder="Filter by symbol"
              value={symbolFilter}
              onChange={(e) => setSymbolFilter(e.target.value)}
              style={{ flex: 1 }}
            />
            <DatePickerInput
              label="Start Date"
              placeholder="Select start date"
              value={startDate}
              onChange={setStartDate}
              clearable
            />
            <DatePickerInput
              label="End Date"
              placeholder="Select end date"
              value={endDate}
              onChange={setEndDate}
              clearable
            />
            <TextInput
              label="Limit"
              type="number"
              value={limit}
              onChange={(e) => setLimit(parseInt(e.target.value) || 50)}
              style={{ width: 100 }}
            />
            <Group gap="xs">
              <Button onClick={handleFilter} size="xs">
                Filter
              </Button>
              <Button onClick={handleClearFilters} variant="outline" size="xs">
                Clear
              </Button>
            </Group>
          </Group>

          {error && (
            <Text c="red" size="sm">
              {error}
            </Text>
          )}

          {/* Accuracy Stats */}
          {accuracyStats && (
            <AccuracyStats stats={accuracyStats} />
          )}
        </Stack>
      </Paper>

      {/* Predictions Table */}
      <Paper p="md" withBorder>
        {loading ? (
          <Center py="xl">
            <Loader />
          </Center>
        ) : predictions.length === 0 ? (
          <Text c="dimmed" ta="center" py="xl">
            No prediction history found.
          </Text>
        ) : (
          <Table striped highlightOnHover>
            <Table.Thead>
              <Table.Tr>
                <Table.Th>Symbol</Table.Th>
                <Table.Th>Predicted</Table.Th>
                <Table.Th>Actual</Table.Th>
                <Table.Th>Accuracy</Table.Th>
                <Table.Th>User Action</Table.Th>
                <Table.Th>Predicted At</Table.Th>
                <Table.Th>Change %</Table.Th>
              </Table.Tr>
            </Table.Thead>
            <Table.Tbody>
              {predictions.map((prediction) => (
                <Table.Tr key={prediction.prediction_id}>
                  <Table.Td>
                    <Text fw={500}>{prediction.symbol}</Text>
                  </Table.Td>
                  <Table.Td>
                    <Badge color={getDirectionColor(prediction.predicted_direction)} variant="light">
                      {getDirectionIcon(prediction.predicted_direction)} {prediction.predicted_direction.toUpperCase()}
                    </Badge>
                  </Table.Td>
                  <Table.Td>
                    {prediction.actual_direction ? (
                      <Badge color={getDirectionColor(prediction.actual_direction)} variant="light">
                        {getDirectionIcon(prediction.actual_direction)} {prediction.actual_direction.toUpperCase()}
                      </Badge>
                    ) : (
                      <Text c="dimmed" size="sm">-</Text>
                    )}
                  </Table.Td>
                  <Table.Td>
                    {prediction.accuracy !== undefined ? (
                      <Badge color={prediction.accuracy ? 'green' : 'red'} variant="light">
                        {prediction.accuracy ? '✓ Correct' : '✗ Incorrect'}
                      </Badge>
                    ) : (
                      <Text c="dimmed" size="sm">Pending</Text>
                    )}
                  </Table.Td>
                  <Table.Td>
                    {prediction.user_action ? (
                      <Badge color={getActionColor(prediction.user_action)} variant="light">
                        {prediction.user_action.toUpperCase()}
                      </Badge>
                    ) : (
                      <Text c="dimmed" size="sm">-</Text>
                    )}
                  </Table.Td>
                  <Table.Td>
                    <Text size="sm">
                      {new Date(prediction.predicted_at).toLocaleDateString()}
                    </Text>
                  </Table.Td>
                  <Table.Td>
                    {prediction.actual_change_percent !== undefined ? (
                      <Text
                        size="sm"
                        c={prediction.actual_change_percent >= 0 ? 'green' : 'red'}
                      >
                        {prediction.actual_change_percent >= 0 ? '+' : ''}
                        {prediction.actual_change_percent.toFixed(2)}%
                      </Text>
                    ) : (
                      <Text c="dimmed" size="sm">-</Text>
                    )}
                  </Table.Td>
                </Table.Tr>
              ))}
            </Table.Tbody>
          </Table>
        )}
      </Paper>
    </Stack>
  );
}

