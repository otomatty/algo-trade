/**
 * Statistics Component
 */
import { Statistics as StatisticsType } from '../../types/analysis';
import { Card, Text, Stack, Group } from '@mantine/core';

interface StatisticsProps {
  statistics: StatisticsType;
}

export function Statistics({ statistics }: StatisticsProps) {
  return (
    <Card withBorder p="md">
      <Stack gap="md">
        <Text fw={500}>Statistics</Text>
        
        <Stack gap="xs">
          <Text size="sm" fw={500}>Price Range:</Text>
          <Group>
            <Text size="sm">Min: {statistics.price_range.min.toFixed(2)}</Text>
            <Text size="sm">Max: {statistics.price_range.max.toFixed(2)}</Text>
            <Text size="sm">Current: {statistics.price_range.current.toFixed(2)}</Text>
          </Group>
        </Stack>
        
        <Group>
          <Text size="sm">Average Volume:</Text>
          <Text fw={500}>{statistics.volume_average.toLocaleString()}</Text>
        </Group>
        
        <Group>
          <Text size="sm">Price Change:</Text>
          <Text fw={500} c={statistics.price_change_percent >= 0 ? 'green' : 'red'}>
            {statistics.price_change_percent >= 0 ? '+' : ''}{statistics.price_change_percent.toFixed(2)}%
          </Text>
        </Group>
      </Stack>
    </Card>
  );
}

