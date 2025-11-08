/**
 * Analysis Job Form Component
 * 
 * DEPENDENCY MAP:
 * 
 * Parents (Files that import this file):
 *   └─ src/pages/DataAnalysis/DataAnalysis.tsx
 * 
 * Dependencies (External files that this file imports):
 *   ├─ @tauri-apps/api/core
 *   ├─ @mantine/core
 *   └─ src/types/data
 * 
 * Related Documentation:
 *   ├─ Spec: src/pages/DataAnalysis/DataAnalysis.spec.md
 *   ├─ Tests: src/pages/DataAnalysis/AnalysisJobForm.test.tsx
 *   └─ Plan: docs/03_plans/data-analysis/README.md
 */
import { useState, useEffect } from 'react';
import { invoke } from '@tauri-apps/api/core';
import {
  Select,
  Button,
  Stack,
  Text,
  Alert,
  Paper,
} from '@mantine/core';
import { DataSet } from '../../types/data';

interface AnalysisJobFormProps {
  onJobStarted?: (jobId: string) => void;
}

export function AnalysisJobForm({ onJobStarted }: AnalysisJobFormProps) {
  const [dataSets, setDataSets] = useState<DataSet[]>([]);
  const [selectedDataSetId, setSelectedDataSetId] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadDataSets();
  }, []);

  const loadDataSets = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await invoke<{ data_list: DataSet[] }>('get_data_list');
      setDataSets(response.data_list);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load data sets');
    } finally {
      setLoading(false);
    }
  };

  const handleRunAnalysis = async () => {
    if (!selectedDataSetId) {
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await invoke<{ job_id: string }>('run_data_analysis', {
        data_set_id: selectedDataSetId,
      });

      if (onJobStarted) {
        onJobStarted(response.job_id);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to run analysis');
    } finally {
      setLoading(false);
    }
  };

  const selectOptions = dataSets.map((ds) => ({
    value: ds.id.toString(),
    label: `${ds.name}${ds.symbol ? ` (${ds.symbol})` : ''}`,
  }));

  return (
    <Paper p="md" withBorder>
      <Stack gap="md">
        <Text fw={500}>Run Data Analysis</Text>

        {error && (
          <Alert color="red">
            {error}
          </Alert>
        )}

        <Select
          label="Select Data Set"
          placeholder={dataSets.length === 0 ? 'No data sets available' : 'Choose a data set'}
          data={selectOptions}
          value={selectedDataSetId?.toString() || null}
          onChange={(value) => setSelectedDataSetId(value ? parseInt(value, 10) : null)}
          disabled={loading || dataSets.length === 0}
          searchable
        />

        {dataSets.length === 0 && !loading && (
          <Text c="dimmed" size="sm">
            No data sets available. Please import data first.
          </Text>
        )}

        <Button
          onClick={handleRunAnalysis}
          loading={loading}
          disabled={!selectedDataSetId || dataSets.length === 0}
        >
          Run Analysis
        </Button>
      </Stack>
    </Paper>
  );
}

