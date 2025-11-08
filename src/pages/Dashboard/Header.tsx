/**
 * Dashboard Header Component
 * 
 * DEPENDENCY MAP:
 * 
 * Parents (Files that import this file):
 *   └─ src/pages/Dashboard/Dashboard.tsx
 * 
 * Dependencies (External files that this file imports):
 *   ├─ @mantine/core
 * 
 * Related Documentation:
 *   ├─ Spec: src/pages/Dashboard/Dashboard.spec.md
 *   └─ Plan: docs/03_plans/dashboard/README.md
 */
import { Group, Title } from '@mantine/core';

export function Header() {
  return (
    <Group h="100%" px="md" justify="space-between">
      <Title order={3}>Algorithm Trading Platform</Title>
    </Group>
  );
}

