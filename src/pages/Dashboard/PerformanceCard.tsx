/**
 * Performance Card Component
 * 
 * DEPENDENCY MAP:
 * 
 * Parents (Files that import this file):
 *   └─ src/pages/Dashboard/ResultSummary.tsx
 * 
 * Dependencies (External files that this file imports):
 *   ├─ @mantine/core
 *   └─ src/types/backtest
 * 
 * Related Documentation:
 *   ├─ Spec: src/pages/Dashboard/Dashboard.spec.md
 *   └─ Plan: docs/03_plans/dashboard/README.md
 */
import { Card, Text, Stack } from '@mantine/core';
import { PerformanceMetrics } from '../../types/backtest';

interface PerformanceCardProps {
  label: string;
  value: string;
  color?: string;
}

export function PerformanceCard({ label, value, color = 'gray' }: PerformanceCardProps) {
  return (
    <Card p="md" withBorder>
      <Stack gap="xs">
        <Text size="sm" c="dimmed">
          {label}
        </Text>
        <Text size="xl" fw={500} c={color}>
          {value}
        </Text>
      </Stack>
    </Card>
  );
}

