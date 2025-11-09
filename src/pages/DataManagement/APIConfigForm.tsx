/**
 * API Configuration Form Component
 * 
 * DEPENDENCY MAP:
 * 
 * Parents (Files that import this file):
 *   └─ src/pages/DataManagement/DataManagement.tsx
 * 
 * Dependencies (External files that this file imports):
 *   ├─ @tauri-apps/api/core
 *   ├─ @mantine/core
 *   ├─ @mantine/dates
 *   └─ src/types/data
 * 
 * Related Documentation:
 *   └─ Plan: docs/03_plans/data-management/README.md
 */
import { useState } from 'react';
import { invoke } from '@tauri-apps/api/core';
import {
  Button,
  Stack,
  Text,
  Alert,
  Paper,
  TextInput,
  Select,
  Switch,
  Group,
  Title,
} from '@mantine/core';
import { DatePickerInput } from '@mantine/dates';
import { DataCollectionSchedule, ConfigureDataCollectionRequest } from '../../types/data';

interface APIConfigFormProps {
  onSuccess?: () => void;
  editingSchedule?: DataCollectionSchedule | null;
  onCancel?: () => void;
}

export function APIConfigForm({ onSuccess, editingSchedule, onCancel }: APIConfigFormProps) {
  const [name, setName] = useState(editingSchedule?.name || '');
  const [source, setSource] = useState<'yahoo' | 'alphavantage'>(editingSchedule?.source || 'yahoo');
  const [symbol, setSymbol] = useState(editingSchedule?.symbol || '');
  const [apiKey, setApiKey] = useState(editingSchedule?.api_key || '');
  const [dataSetName, setDataSetName] = useState(editingSchedule?.data_set_name || '');
  const [cronExpression, setCronExpression] = useState(editingSchedule?.cron_expression || '0 9 * * 1-5');
  const [startDate, setStartDate] = useState<Date | null>(
    editingSchedule?.start_date ? new Date(editingSchedule.start_date) : null
  );
  const [endDate, setEndDate] = useState<Date | null>(
    editingSchedule?.end_date ? new Date(editingSchedule.end_date) : null
  );
  const [enabled, setEnabled] = useState(editingSchedule?.enabled ?? true);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  const handleSubmit = async () => {
    // Validation
    if (!name.trim()) {
      setError('Schedule name is required');
      return;
    }
    if (!symbol.trim()) {
      setError('Symbol is required');
      return;
    }
    if (!cronExpression.trim()) {
      setError('Cron expression is required');
      return;
    }
    if (source === 'alphavantage' && !apiKey.trim()) {
      setError('API key is required for Alpha Vantage');
      return;
    }

    setLoading(true);
    setError(null);
    setSuccess(false);

    try {
      const request: ConfigureDataCollectionRequest = {
        action: editingSchedule ? 'update' : 'create',
        name: name.trim(),
        source,
        symbol: symbol.trim().toUpperCase(),
        cron_expression: cronExpression.trim(),
        start_date: startDate ? startDate.toISOString().split('T')[0] : undefined,
        end_date: endDate ? endDate.toISOString().split('T')[0] : undefined,
        api_key: source === 'alphavantage' ? apiKey.trim() : undefined,
        data_set_name: dataSetName.trim() || undefined,
        enabled,
      };

      if (editingSchedule) {
        request.schedule_id = editingSchedule.schedule_id;
      }

      await invoke<{ schedule_id: string }>('configure_data_collection', request);

      setSuccess(true);
      if (onSuccess) {
        onSuccess();
      }

      // Reset form if creating new schedule
      if (!editingSchedule) {
        setName('');
        setSymbol('');
        setApiKey('');
        setDataSetName('');
        setCronExpression('0 9 * * 1-5');
        setStartDate(null);
        setEndDate(null);
        setEnabled(true);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to configure data collection');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Paper p="md" withBorder>
      <Stack gap="md">
        <Title order={4}>{editingSchedule ? 'Edit Schedule' : 'Create Data Collection Schedule'}</Title>

        {error && (
          <Alert color="red" onClose={() => setError(null)} withCloseButton>
            {error}
          </Alert>
        )}

        {success && (
          <Alert color="green" onClose={() => setSuccess(false)} withCloseButton>
            Schedule {editingSchedule ? 'updated' : 'created'} successfully!
          </Alert>
        )}

        <TextInput
          label="Schedule Name"
          placeholder="e.g., Daily AAPL Collection"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
        />

        <Select
          label="Data Source"
          data={[
            { value: 'yahoo', label: 'Yahoo Finance' },
            { value: 'alphavantage', label: 'Alpha Vantage' },
          ]}
          value={source}
          onChange={(value) => setSource(value as 'yahoo' | 'alphavantage')}
          required
        />

        <TextInput
          label="Symbol"
          placeholder="e.g., AAPL"
          value={symbol}
          onChange={(e) => setSymbol(e.target.value.toUpperCase())}
          required
        />

        {source === 'alphavantage' && (
          <TextInput
            label="API Key"
            type="password"
            placeholder="Alpha Vantage API key"
            value={apiKey}
            onChange={(e) => setApiKey(e.target.value)}
            required
          />
        )}

        <TextInput
          label="Dataset Name (Optional)"
          placeholder="Leave empty to auto-generate"
          value={dataSetName}
          onChange={(e) => setDataSetName(e.target.value)}
        />

        <TextInput
          label="Cron Expression"
          placeholder="e.g., 0 9 * * 1-5 (Weekdays at 9 AM)"
          value={cronExpression}
          onChange={(e) => setCronExpression(e.target.value)}
          description="Format: minute hour day month day-of-week"
          required
        />

        <DatePickerInput
          label="Start Date (Optional)"
          value={startDate}
          onChange={setStartDate}
          clearable
        />

        <DatePickerInput
          label="End Date (Optional)"
          value={endDate}
          onChange={setEndDate}
          clearable
        />

        <Switch
          label="Enabled"
          checked={enabled}
          onChange={(e) => setEnabled(e.currentTarget.checked)}
        />

        <Group justify="flex-end">
          {editingSchedule && onCancel && (
            <Button variant="subtle" onClick={onCancel}>
              Cancel
            </Button>
          )}
          <Button onClick={handleSubmit} loading={loading}>
            {editingSchedule ? 'Update' : 'Create'} Schedule
          </Button>
        </Group>
      </Stack>
    </Paper>
  );
}

