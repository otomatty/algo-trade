/**
 * Dashboard Header Component
 * 
 * DEPENDENCY MAP:
 * 
 * Parents (Files that import this file):
 *   └─ src/App.tsx (via common layout)
 * 
 * Dependencies (External files that this file imports):
 *   ├─ @mantine/core
 *   └─ @mantine/hooks
 * 
 * Related Documentation:
 *   ├─ Spec: src/pages/Dashboard/Dashboard.spec.md
 *   └─ Plan: docs/03_plans/dashboard/README.md
 */
import { Group, Title, Burger } from '@mantine/core';

interface HeaderProps {
  opened?: boolean;
  toggle?: () => void;
}

export function Header({ opened, toggle }: HeaderProps) {
  return (
    <Group h="100%" px="md" justify="space-between">
      <Group>
        {toggle && (
          <Burger
            opened={opened}
            onClick={toggle}
            hiddenFrom="sm"
            size="sm"
          />
        )}
        <Title order={3}>Algorithm Trading Platform</Title>
      </Group>
    </Group>
  );
}

