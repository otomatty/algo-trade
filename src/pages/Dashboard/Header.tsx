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
 *   ├─ @mantine/hooks
 *   └─ react-i18next
 * 
 * Related Documentation:
 *   ├─ Spec: src/pages/Dashboard/Dashboard.spec.md
 *   └─ Plan: docs/03_plans/dashboard/README.md
 */
import { Group, Title, Burger, Select } from '@mantine/core';
import { useTranslation } from 'react-i18next';

interface HeaderProps {
  opened?: boolean;
  toggle?: () => void;
}

export function Header({ opened, toggle }: HeaderProps) {
  const { t, i18n } = useTranslation('navigation');

  const handleLanguageChange = (value: string | null) => {
    if (value) {
      i18n.changeLanguage(value);
    }
  };

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
        <Title order={3}>{t('appTitle')}</Title>
      </Group>
      <Select
        value={i18n.language}
        onChange={handleLanguageChange}
        data={[
          { value: 'ja', label: '日本語' },
          { value: 'en', label: 'English' },
        ]}
        w={120}
      />
    </Group>
  );
}

