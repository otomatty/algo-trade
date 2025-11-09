/**
 * Data Preview Modal Component
 * 
 * DEPENDENCY MAP:
 * 
 * Parents (Files that import this file):
 *   └─ src/pages/DataManagement/DataManagement.tsx
 * 
 * Dependencies (External files that this file imports):
 *   ├─ @mantine/core
 *   ├─ src/types/data
 *   └─ @tauri-apps/api/core
 * 
 * Related Documentation:
 *   ├─ Plan: docs/03_plans/data-management/README.md
 *   └─ Spec: docs/03_plans/data-management/api-spec.md
 */
import { useState, useEffect } from 'react';
import { invoke } from '@tauri-apps/api/core';
import {
  Modal,
  Stack,
  Text,
  ScrollArea,
  Paper,
  Grid,
  Table,
  Loader,
  Alert,
  Group,
  Divider,
} from '@mantine/core';
import { DataSet, DataPreview } from '../../types/data';

interface DataPreviewModalProps {
  dataSet: DataSet | null;
  opened: boolean;
  onClose: () => void;
}

export function DataPreviewModal({ dataSet, opened, onClose }: DataPreviewModalProps) {
  const [preview, setPreview] = useState<DataPreview | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (opened && dataSet) {
      loadPreview();
    } else {
      setPreview(null);
      setError(null);
    }
  }, [opened, dataSet]);

  const loadPreview = async () => {
    if (!dataSet) return;

    setLoading(true);
    setError(null);

    try {
      const response = await invoke<DataPreview>('get_data_preview', {
        data_set_id: dataSet.id,
        limit: 100,
      });
      setPreview(response);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load data preview');
    } finally {
      setLoading(false);
    }
  };

  if (!dataSet) {
    return null;
  }

  return (
    <Modal
      opened={opened}
      onClose={onClose}
      title={`${dataSet.name} - Data Preview`}
      size="xl"
    >
      {loading && (
        <Group justify="center" py="xl">
          <Loader />
          <Text>Loading preview...</Text>
        </Group>
      )}

      {error && (
        <Alert color="red" mb="md">
          {error}
        </Alert>
      )}

      {preview && !loading && (
        <ScrollArea h={600}>
          <Stack gap="md">
            {/* Statistics Section */}
            <Paper p="md" withBorder>
              <Text fw={500} size="lg" mb="md">
                Statistics
              </Text>
              <Grid>
                <Grid.Col span={12}>
                  <Group gap="md">
                    <Text size="sm">
                      <strong>Count:</strong> {preview.statistics.count} records
                    </Text>
                    <Text size="sm">
                      <strong>Date Range:</strong>{' '}
                      {new Date(preview.statistics.date_range.start).toLocaleDateString()} -{' '}
                      {new Date(preview.statistics.date_range.end).toLocaleDateString()}
                    </Text>
                  </Group>
                </Grid.Col>
              </Grid>
              <Divider my="md" />
              <Grid>
                {(['open', 'high', 'low', 'close', 'volume'] as const).map((field) => {
                  const stats = preview.statistics[field];
                  return (
                    <Grid.Col key={field} span={{ base: 12, sm: 6, md: 4 }}>
                      <Paper p="sm" withBorder>
                        <Text fw={500} size="sm" mb="xs" tt="capitalize">
                          {field}
                        </Text>
                        <Stack gap="xs">
                          <Text size="xs">
                            Mean: <strong>{stats.mean.toFixed(2)}</strong>
                          </Text>
                          <Text size="xs">
                            Min: <strong>{stats.min.toFixed(2)}</strong>
                          </Text>
                          <Text size="xs">
                            Max: <strong>{stats.max.toFixed(2)}</strong>
                          </Text>
                          <Text size="xs">
                            Std: <strong>{stats.std.toFixed(2)}</strong>
                          </Text>
                        </Stack>
                      </Paper>
                    </Grid.Col>
                  );
                })}
              </Grid>
            </Paper>

            {/* Data Table Section */}
            <Paper p="md" withBorder>
              <Text fw={500} size="lg" mb="md">
                Data ({preview.data.length} records shown)
              </Text>
              <ScrollArea h={400}>
                <Table striped highlightOnHover>
                  <Table.Thead>
                    <Table.Tr>
                      <Table.Th>Date</Table.Th>
                      <Table.Th>Open</Table.Th>
                      <Table.Th>High</Table.Th>
                      <Table.Th>Low</Table.Th>
                      <Table.Th>Close</Table.Th>
                      <Table.Th>Volume</Table.Th>
                    </Table.Tr>
                  </Table.Thead>
                  <Table.Tbody>
                    {preview.data.map((row) => (
                      <Table.Tr key={row.id}>
                        <Table.Td>{new Date(row.date).toLocaleDateString()}</Table.Td>
                        <Table.Td>{row.open.toFixed(2)}</Table.Td>
                        <Table.Td>{row.high.toFixed(2)}</Table.Td>
                        <Table.Td>{row.low.toFixed(2)}</Table.Td>
                        <Table.Td>{row.close.toFixed(2)}</Table.Td>
                        <Table.Td>{row.volume.toLocaleString()}</Table.Td>
                      </Table.Tr>
                    ))}
                  </Table.Tbody>
                </Table>
              </ScrollArea>
            </Paper>
          </Stack>
        </ScrollArea>
      )}
    </Modal>
  );
}

