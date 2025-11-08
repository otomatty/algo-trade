/**
 * Algorithm Selector Component
 * 
 * DEPENDENCY MAP:
 * 
 * Parents (Files that import this file):
 *   └─ src/pages/Backtest/BacktestSettings.tsx
 * 
 * Dependencies (External files that this file imports):
 *   ├─ @mantine/core
 *   └─ src/types/algorithm
 * 
 * Related Documentation:
 *   └─ Plan: docs/03_plans/backtest/README.md
 */
import { MultiSelect, Text, Stack } from '@mantine/core';
import { Algorithm } from '../../types/algorithm';

interface AlgorithmSelectorProps {
  algorithms: Algorithm[];
  selectedAlgorithmIds: number[];
  onSelectionChange: (ids: number[]) => void;
  loading?: boolean;
}

export function AlgorithmSelector({
  algorithms,
  selectedAlgorithmIds,
  onSelectionChange,
  loading = false,
}: AlgorithmSelectorProps) {
  const selectOptions = algorithms.map((algo) => ({
    value: algo.id.toString(),
    label: algo.name,
  }));

  const handleChange = (values: string[]) => {
    const ids = values.map((v) => parseInt(v, 10));
    onSelectionChange(ids);
  };

  return (
    <Stack gap="xs">
      <MultiSelect
        label="Select Algorithms"
        placeholder={
          algorithms.length === 0
            ? 'No algorithms available'
            : 'Choose algorithms to backtest'
        }
        data={selectOptions}
        value={selectedAlgorithmIds.map((id) => id.toString())}
        onChange={handleChange}
        disabled={loading || algorithms.length === 0}
        searchable
        required
      />
      {algorithms.length === 0 && !loading && (
        <Text c="dimmed" size="sm">
          No algorithms available. Please select algorithms from the Algorithm Proposal page first.
        </Text>
      )}
    </Stack>
  );
}

