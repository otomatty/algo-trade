/**
 * Data Import Form Component
 * 
 * DEPENDENCY MAP:
 * 
 * Parents (Files that import this file):
 *   └─ src/pages/DataManagement/DataManagement.tsx
 * 
 * Dependencies (External files that this file imports):
 *   ├─ @tauri-apps/api/core
 *   ├─ @tauri-apps/plugin-dialog
 *   ├─ @mantine/core
 *   └─ @mantine/dropzone
 * 
 * Related Documentation:
 *   └─ Plan: docs/03_plans/data-management/README.md
 */
import { useState } from 'react';
import { invoke } from '@tauri-apps/api/core';
import { open } from '@tauri-apps/plugin-dialog';
import { 
  Button, 
  TextInput, 
  Group, 
  Stack,
  Text,
  Alert
} from '@mantine/core';
// Note: @tabler/icons-react not installed, using text labels instead
// TODO: Install @tabler/icons-react or use Mantine icons

interface DataImportFormProps {
  onSuccess?: () => void;
}

export function DataImportForm({ onSuccess }: DataImportFormProps) {
  const [filePath, setFilePath] = useState<string>('');
  const [name, setName] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  const handleSelectFile = async () => {
    try {
      const selected = await open({
        multiple: false,
        filters: [{
          name: 'CSV Files',
          extensions: ['csv']
        }]
      });

      if (selected && typeof selected === 'string') {
        setFilePath(selected);
        setError(null);
        setSuccess(false);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to select file');
    }
  };

  const handleImport = async () => {
    if (!filePath) {
      setError('Please select a CSV file');
      return;
    }

    setLoading(true);
    setError(null);
    setSuccess(false);

    try {
      const result = await invoke<{ data_set_id: number; name: string; record_count: number }>(
        'import_ohlcv_data',
        {
          file_path: filePath,
          name: name || undefined
        }
      );

      setSuccess(true);
      setFilePath('');
      setName('');
      
      if (onSuccess) {
        onSuccess();
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to import data');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Stack gap="md">
      <Text fw={500}>Import OHLCV Data from CSV</Text>

      {error && (
        <Alert color="red">
          {error}
        </Alert>
      )}

      {success && (
        <Alert color="green">
          Data imported successfully!
        </Alert>
      )}

      <Group>
        <Button
          onClick={handleSelectFile}
          disabled={loading}
        >
          Select CSV File
        </Button>
        {filePath && (
          <Text c="dimmed" size="sm">
            {filePath.split('/').pop()}
          </Text>
        )}
      </Group>

      <TextInput
        label="Dataset Name (optional)"
        placeholder="Leave empty for auto-generated name"
        value={name}
        onChange={(e) => setName(e.currentTarget.value)}
        disabled={loading}
      />

      <Button
        onClick={handleImport}
        loading={loading}
        disabled={!filePath}
      >
        Import
      </Button>
    </Stack>
  );
}

