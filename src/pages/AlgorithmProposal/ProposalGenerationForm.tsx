/**
 * Proposal Generation Form Component
 * 
 * DEPENDENCY MAP:
 * 
 * Parents (Files that import this file):
 *   └─ src/pages/AlgorithmProposal/AlgorithmProposal.tsx
 * 
 * Dependencies (External files that this file imports):
 *   ├─ @tauri-apps/api/core
 *   ├─ @mantine/core
 *   ├─ src/types/data
 *   └─ src/types/algorithm
 * 
 * Related Documentation:
 *   ├─ Spec: src/pages/AlgorithmProposal/AlgorithmProposal.spec.md
 *   ├─ Tests: src/pages/AlgorithmProposal/AlgorithmProposal.test.tsx
 *   └─ Plan: docs/03_plans/algorithm-proposal/README.md
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
  NumberInput,
  MultiSelect,
} from '@mantine/core';
import { DataSet } from '../../types/data';
import { UserPreferences } from '../../types/algorithm';

interface ProposalGenerationFormProps {
  onJobStarted?: (jobId: string) => void;
}

export function ProposalGenerationForm({ onJobStarted }: ProposalGenerationFormProps) {
  const [dataSets, setDataSets] = useState<DataSet[]>([]);
  const [selectedDataSetId, setSelectedDataSetId] = useState<number | null>(null);
  const [riskTolerance, setRiskTolerance] = useState<'low' | 'medium' | 'high' | null>(null);
  const [tradingFrequency, setTradingFrequency] = useState<'low' | 'medium' | 'high' | null>(null);
  const [preferredIndicators, setPreferredIndicators] = useState<string[]>([]);
  const [numProposals, setNumProposals] = useState<number>(5);
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

  const handleGenerateProposals = async () => {
    if (!selectedDataSetId) {
      setError('Please select a data set');
      return;
    }

    // Phase 1: Button is disabled, this function will be implemented in Phase 3
    // TODO: Implement in Phase 3
    console.log('Generate proposals - to be implemented in Phase 3');
  };

  const selectOptions = dataSets.map((ds) => ({
    value: ds.id.toString(),
    label: `${ds.name}${ds.symbol ? ` (${ds.symbol})` : ''}`,
  }));

  const riskToleranceOptions = [
    { value: 'low', label: 'Low' },
    { value: 'medium', label: 'Medium' },
    { value: 'high', label: 'High' },
  ];

  const tradingFrequencyOptions = [
    { value: 'low', label: 'Low' },
    { value: 'medium', label: 'Medium' },
    { value: 'high', label: 'High' },
  ];

  const indicatorOptions = [
    { value: 'RSI', label: 'RSI (Relative Strength Index)' },
    { value: 'MACD', label: 'MACD (Moving Average Convergence Divergence)' },
    { value: 'Bollinger Bands', label: 'Bollinger Bands' },
    { value: 'Moving Average', label: 'Moving Average' },
    { value: 'Volume', label: 'Volume' },
  ];

  return (
    <Paper p="md" withBorder>
      <Stack gap="md">
        <Text fw={500}>Generate Algorithm Proposals</Text>

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

        <Select
          label="Risk Tolerance"
          placeholder="Select risk tolerance (optional)"
          data={riskToleranceOptions}
          value={riskTolerance || null}
          onChange={(value) => setRiskTolerance(value as 'low' | 'medium' | 'high' | null)}
          clearable
        />

        <Select
          label="Trading Frequency"
          placeholder="Select trading frequency (optional)"
          data={tradingFrequencyOptions}
          value={tradingFrequency || null}
          onChange={(value) => setTradingFrequency(value as 'low' | 'medium' | 'high' | null)}
          clearable
        />

        <MultiSelect
          label="Preferred Indicators"
          placeholder="Select preferred indicators (optional)"
          data={indicatorOptions}
          value={preferredIndicators}
          onChange={setPreferredIndicators}
          clearable
          searchable
        />

        <NumberInput
          label="Number of Proposals"
          placeholder="Number of proposals to generate"
          value={numProposals}
          onChange={(value) => setNumProposals(typeof value === 'number' ? value : 5)}
          min={1}
          max={10}
          required
        />

        <Button
          onClick={handleGenerateProposals}
          loading={loading}
          disabled={!selectedDataSetId || dataSets.length === 0}
        >
          Generate Proposals
        </Button>
      </Stack>
    </Paper>
  );
}

