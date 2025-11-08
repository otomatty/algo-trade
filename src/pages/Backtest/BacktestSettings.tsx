/**
 * Backtest Settings Component
 * 
 * DEPENDENCY MAP:
 * 
 * Parents (Files that import this file):
 *   └─ src/App.tsx (or future routing component)
 * 
 * Dependencies (External files that this file imports):
 *   ├─ @tauri-apps/api/core
 *   ├─ @mantine/core
 *   ├─ @mantine/dates
 *   ├─ src/types/algorithm
 *   ├─ src/types/data
 *   └─ src/pages/Backtest/AlgorithmSelector.tsx
 * 
 * Related Documentation:
 *   ├─ Spec: src/pages/Backtest/BacktestSettings.spec.md
 *   ├─ Tests: src/pages/Backtest/BacktestSettings.test.tsx
 *   └─ Plan: docs/03_plans/backtest/README.md
 */
import { useState, useEffect } from 'react';
import { invoke } from '@tauri-apps/api/core';
import {
  Container,
  Title,
  Paper,
  Stack,
  Button,
  Alert,
} from '@mantine/core';
import { DatePickerInput } from '@mantine/dates';
import { Algorithm } from '../../types/algorithm';
import { DataSet } from '../../types/data';
import { AlgorithmSelector } from './AlgorithmSelector';
import { DataSetSelector } from './DataSetSelector';
import { BacktestProgress } from './BacktestProgress';
import { BacktestResults } from './BacktestResults';

interface BacktestSettingsProps {
  onJobStarted?: (jobId: string) => void;
}

export function BacktestSettings({ onJobStarted }: BacktestSettingsProps) {
  const [algorithms, setAlgorithms] = useState<Algorithm[]>([]);
  const [selectedAlgorithmIds, setSelectedAlgorithmIds] = useState<number[]>([]);
  const [dataSets, setDataSets] = useState<DataSet[]>([]);
  const [selectedDataSetId, setSelectedDataSetId] = useState<number | null>(null);
  const [startDate, setStartDate] = useState<Date | null>(null);
  const [endDate, setEndDate] = useState<Date | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [jobId, setJobId] = useState<string | null>(null);
  const [showResults, setShowResults] = useState(false);

  useEffect(() => {
    loadAlgorithms();
    loadDataSets();
  }, []);

  const loadAlgorithms = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await invoke<{ algorithms: Algorithm[] }>('get_selected_algorithms');
      setAlgorithms(response.algorithms);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load algorithms');
    } finally {
      setLoading(false);
    }
  };

  const loadDataSets = async () => {
    try {
      const response = await invoke<{ data_list: DataSet[] }>('get_data_list');
      setDataSets(response.data_list);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load data sets');
    }
  };

  const handleRunBacktest = async () => {
    // Validation
    if (selectedAlgorithmIds.length === 0) {
      setError('Please select at least one algorithm');
      return;
    }

    if (!selectedDataSetId) {
      setError('Please select a data set');
      return;
    }

    if (!startDate || !endDate) {
      setError('Please select both start and end dates');
      return;
    }

    if (startDate >= endDate) {
      setError('Start date must be before end date');
      return;
    }

    setLoading(true);
    setError(null);
    try {
      const response = await invoke<{ job_id: string }>('run_backtest', {
        algorithm_ids: selectedAlgorithmIds,
        start_date: startDate.toISOString().split('T')[0],
        end_date: endDate.toISOString().split('T')[0],
        data_set_id: selectedDataSetId,
      });

      if (onJobStarted) {
        onJobStarted(response.job_id);
      }
      
      setJobId(response.job_id);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to run backtest');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container size="xl" py="md">
      <Stack gap="md">
        <Title order={2}>Backtest Settings</Title>

        <Paper p="md" withBorder>
          <Stack gap="md">
            {error && (
              <Alert color="red">
                {error}
              </Alert>
            )}

            <AlgorithmSelector
              algorithms={algorithms}
              selectedAlgorithmIds={selectedAlgorithmIds}
              onSelectionChange={setSelectedAlgorithmIds}
              loading={loading}
            />

            <DataSetSelector
              dataSets={dataSets}
              selectedDataSetId={selectedDataSetId}
              onSelectionChange={setSelectedDataSetId}
            />

            <DatePickerInput
              label="Start Date"
              placeholder="Select start date"
              value={startDate}
              onChange={(value) => setStartDate(value as Date | null)}
              required
            />

            <DatePickerInput
              label="End Date"
              placeholder="Select end date"
              value={endDate}
              onChange={(value) => setEndDate(value as Date | null)}
              required
            />

            <Button
              onClick={handleRunBacktest}
              loading={loading}
              disabled={
                selectedAlgorithmIds.length === 0 ||
                !selectedDataSetId ||
                !startDate ||
                !endDate ||
                algorithms.length === 0 ||
                dataSets.length === 0 ||
                jobId !== null
              }
            >
              Run Backtest
            </Button>

            {jobId && (
              <BacktestProgress
                jobId={jobId}
                onCompleted={() => {
                  setShowResults(true);
                }}
                onError={(error) => {
                  setError(error);
                  setJobId(null);
                }}
              />
            )}

            {showResults && jobId && (
              <BacktestResults jobId={jobId} />
            )}
          </Stack>
        </Paper>
      </Stack>
    </Container>
  );
}

