/**
 * Data Management Page
 * 
 * DEPENDENCY MAP:
 * 
 * Parents (Files that import this file):
 *   └─ src/App.tsx (via routing)
 * 
 * Dependencies (External files that this file imports):
 *   ├─ @tauri-apps/api/core
 *   ├─ @mantine/core
 *   ├─ @mantine/dropzone
 *   ├─ src/types/data
 *   ├─ ./DataImportForm
 *   └─ ./DataPreviewModal
 * 
 * Related Documentation:
 *   ├─ Plan: docs/03_plans/data-management/README.md
 *   ├─ API Spec: docs/03_plans/data-management/api-spec.md
 *   └─ UI Design: docs/03_plans/data-management/ui-design.md
 */
import { useState, useEffect } from 'react';
import { invoke } from '@tauri-apps/api/core';
import { 
  Container, 
  Title, 
  Table, 
  Button, 
  Group, 
  Text,
  Paper,
  Stack
} from '@mantine/core';
import { DataSet } from '../../types/data';
import { DataImportForm } from './DataImportForm';
import { DataPreviewModal } from './DataPreviewModal';

interface DataManagementProps {
  currentPage?: string;
  onNavigate?: (page: string) => void;
}

export function DataManagement({ currentPage, onNavigate }: DataManagementProps) {
  const [dataSets, setDataSets] = useState<DataSet[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [previewDataSet, setPreviewDataSet] = useState<DataSet | null>(null);
  const [previewOpened, setPreviewOpened] = useState(false);

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

  useEffect(() => {
    loadDataSets();
  }, []);

  const handleDelete = async (id: number) => {
    if (!confirm('Are you sure you want to delete this data set?')) {
      return;
    }

    try {
      await invoke('delete_data_set', { data_set_id: id });
      await loadDataSets();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete data set');
    }
  };

  const handlePreview = (dataSet: DataSet) => {
    setPreviewDataSet(dataSet);
    setPreviewOpened(true);
  };

  const handleImportSuccess = () => {
    loadDataSets();
  };

  return (
    <Container size="xl" py="md">
      <Stack gap="md">
        <Title order={2}>Data Management</Title>

        <Paper p="md" withBorder>
          <DataImportForm onSuccess={handleImportSuccess} />
        </Paper>

        <Paper p="md" withBorder>
          <Group justify="space-between" mb="md">
            <Title order={3}>Data Sets</Title>
            <Button onClick={loadDataSets} loading={loading}>
              Refresh
            </Button>
          </Group>

          {error && (
            <Text c="red" mb="md">
              {error}
            </Text>
          )}

          <Table>
            <Table.Thead>
              <Table.Tr>
                <Table.Th>ID</Table.Th>
                <Table.Th>Name</Table.Th>
                <Table.Th>Symbol</Table.Th>
                <Table.Th>Start Date</Table.Th>
                <Table.Th>End Date</Table.Th>
                <Table.Th>Records</Table.Th>
                <Table.Th>Source</Table.Th>
                <Table.Th>Actions</Table.Th>
              </Table.Tr>
            </Table.Thead>
            <Table.Tbody>
              {dataSets.map((dataSet) => (
                <Table.Tr key={dataSet.id}>
                  <Table.Td>{dataSet.id}</Table.Td>
                  <Table.Td>{dataSet.name}</Table.Td>
                  <Table.Td>{dataSet.symbol || '-'}</Table.Td>
                  <Table.Td>{dataSet.start_date || '-'}</Table.Td>
                  <Table.Td>{dataSet.end_date || '-'}</Table.Td>
                  <Table.Td>{dataSet.record_count}</Table.Td>
                  <Table.Td>{dataSet.source}</Table.Td>
                  <Table.Td>
                    <Group gap="xs">
                      <Button
                        size="xs"
                        variant="light"
                        onClick={() => handlePreview(dataSet)}
                      >
                        Preview
                      </Button>
                      <Button
                        size="xs"
                        color="red"
                        onClick={() => handleDelete(dataSet.id)}
                      >
                        Delete
                      </Button>
                    </Group>
                  </Table.Td>
                </Table.Tr>
              ))}
            </Table.Tbody>
          </Table>

          {dataSets.length === 0 && !loading && (
            <Text c="dimmed" ta="center" py="xl">
              No data sets found. Import a CSV file to get started.
            </Text>
          )}
        </Paper>
      </Stack>

      <DataPreviewModal
        dataSet={previewDataSet}
        opened={previewOpened}
        onClose={() => {
          setPreviewOpened(false);
          setPreviewDataSet(null);
        }}
      />
    </Container>
  );
}


