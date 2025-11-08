/**
 * Data Set Selector Component
 * 
 * DEPENDENCY MAP:
 * 
 * Parents (Files that import this file):
 *   └─ src/pages/Backtest/BacktestSettings.tsx
 * 
 * Dependencies (External files that this file imports):
 *   ├─ @mantine/core
 *   └─ src/types/data
 * 
 * Related Documentation:
 *   └─ Plan: docs/03_plans/backtest/README.md
 */
import { Select, Text, Stack } from '@mantine/core';
import { DataSet } from '../../types/data';

interface DataSetSelectorProps {
  dataSets: DataSet[];
  selectedDataSetId: number | null;
  onSelectionChange: (id: number | null) => void;
}

export function DataSetSelector({
  dataSets,
  selectedDataSetId,
  onSelectionChange,
}: DataSetSelectorProps) {
  const selectOptions = dataSets.map((ds) => ({
    value: ds.id.toString(),
    label: `${ds.name}${ds.symbol ? ` (${ds.symbol})` : ''}`,
  }));

  const handleChange = (value: string | null) => {
    onSelectionChange(value ? parseInt(value, 10) : null);
  };

  return (
    <Stack gap="xs">
      <Select
        label="Select Data Set"
        placeholder={
          dataSets.length === 0 ? 'No data sets available' : 'Choose a data set'
        }
        data={selectOptions}
        value={selectedDataSetId?.toString() || null}
        onChange={handleChange}
        disabled={dataSets.length === 0}
        searchable
        required
      />
      {dataSets.length === 0 && (
        <Text c="dimmed" size="sm">
          No data sets available. Please import data first.
        </Text>
      )}
    </Stack>
  );
}

