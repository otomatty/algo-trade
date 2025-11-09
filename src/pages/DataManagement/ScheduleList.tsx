/**
 * Schedule List Component
 * 
 * DEPENDENCY MAP:
 * 
 * Parents (Files that import this file):
 *   └─ src/pages/DataManagement/DataManagement.tsx
 * 
 * Dependencies (External files that this file imports):
 *   ├─ @tauri-apps/api/core
 *   ├─ @mantine/core
 *   ├─ @mantine/modals
 *   └─ src/types/data
 * 
 * Related Documentation:
 *   └─ Plan: docs/03_plans/data-management/README.md
 */
import { useState, useEffect } from 'react';
import { invoke } from '@tauri-apps/api/core';
import {
  Table,
  Button,
  Group,
  Text,
  Badge,
  Stack,
  Title,
  Switch,
} from '@mantine/core';
import { modals } from '@mantine/modals';
import { DataCollectionSchedule } from '../../types/data';

interface ScheduleListProps {
  onEdit?: (schedule: DataCollectionSchedule) => void;
  onRefresh?: () => void;
}

export function ScheduleList({ onEdit, onRefresh }: ScheduleListProps) {
  const [schedules, setSchedules] = useState<DataCollectionSchedule[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadSchedules = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await invoke<{ schedules: DataCollectionSchedule[] }>(
        'get_data_collection_schedules'
      );
      setSchedules(response.schedules);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load schedules');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadSchedules();
  }, []);

  useEffect(() => {
    if (onRefresh) {
      // Reload when refresh is triggered
      loadSchedules();
    }
  }, [onRefresh]);

  const handleToggleEnabled = async (schedule: DataCollectionSchedule) => {
    try {
      await invoke('configure_data_collection', {
        action: 'update',
        schedule_id: schedule.schedule_id,
        enabled: !schedule.enabled,
      });
      await loadSchedules();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update schedule');
    }
  };

  const handleDelete = (schedule: DataCollectionSchedule) => {
    modals.openConfirmModal({
      title: 'Delete Schedule',
      children: (
        <Text size="sm">
          Are you sure you want to delete the schedule &quot;{schedule.name}&quot;?
        </Text>
      ),
      labels: { confirm: 'Delete', cancel: 'Cancel' },
      confirmProps: { color: 'red' },
      onConfirm: async () => {
        try {
          await invoke('configure_data_collection', {
            action: 'delete',
            schedule_id: schedule.schedule_id,
          });
          await loadSchedules();
        } catch (err) {
          setError(err instanceof Error ? err.message : 'Failed to delete schedule');
        }
      },
    });
  };

  return (
    <Stack gap="md">
      <Group justify="space-between">
        <Title order={3}>Data Collection Schedules</Title>
        <Button onClick={loadSchedules} loading={loading}>
          Refresh
        </Button>
      </Group>

      {error && (
        <Text c="red" size="sm">
          {error}
        </Text>
      )}

      <Table>
        <Table.Thead>
          <Table.Tr>
            <Table.Th>Name</Table.Th>
            <Table.Th>Source</Table.Th>
            <Table.Th>Symbol</Table.Th>
            <Table.Th>Cron Expression</Table.Th>
            <Table.Th>Status</Table.Th>
            <Table.Th>Actions</Table.Th>
          </Table.Tr>
        </Table.Thead>
        <Table.Tbody>
          {schedules.map((schedule) => (
            <Table.Tr key={schedule.schedule_id}>
              <Table.Td>{schedule.name}</Table.Td>
              <Table.Td>
                <Badge>{schedule.source}</Badge>
              </Table.Td>
              <Table.Td>{schedule.symbol}</Table.Td>
              <Table.Td>
                <Text size="xs" ff="monospace">
                  {schedule.cron_expression}
                </Text>
              </Table.Td>
              <Table.Td>
                <Switch
                  checked={schedule.enabled}
                  onChange={() => handleToggleEnabled(schedule)}
                  size="sm"
                />
              </Table.Td>
              <Table.Td>
                <Group gap="xs">
                  <Button
                    size="xs"
                    variant="light"
                    onClick={() => onEdit && onEdit(schedule)}
                  >
                    Edit
                  </Button>
                  <Button
                    size="xs"
                    color="red"
                    variant="light"
                    onClick={() => handleDelete(schedule)}
                  >
                    Delete
                  </Button>
                </Group>
              </Table.Td>
            </Table.Tr>
          ))}
        </Table.Tbody>
      </Table>

      {schedules.length === 0 && !loading && (
        <Text c="dimmed" ta="center" py="xl">
          No schedules found. Create a schedule to get started.
        </Text>
      )}
    </Stack>
  );
}

