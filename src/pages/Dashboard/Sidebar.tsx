/**
 * Dashboard Sidebar Component
 * 
 * DEPENDENCY MAP:
 * 
 * Parents (Files that import this file):
 *   └─ src/pages/Dashboard/Dashboard.tsx
 * 
 * Dependencies (External files that this file imports):
 *   ├─ @mantine/core
 *   ├─ @mantine/hooks (for navigation state)
 *   └─ react-i18next
 * 
 * Related Documentation:
 *   ├─ Spec: src/pages/Dashboard/Dashboard.spec.md
 *   └─ Plan: docs/03_plans/dashboard/README.md
 */
import { NavLink } from '@mantine/core';
import { useTranslation } from 'react-i18next';

interface SidebarProps {
  currentPage?: string;
  onNavigate?: (page: string) => void;
}

export function Sidebar({ currentPage, onNavigate }: SidebarProps) {
  const { t } = useTranslation('navigation');
  
  const navItems = [
    { label: t('dashboard'), page: 'dashboard' },
    { label: t('algorithmProposal'), page: 'algorithm-proposal' },
    { label: t('backtest'), page: 'backtest' },
    { label: t('dataManagement'), page: 'data-management' },
    { label: t('dataAnalysis'), page: 'data-analysis' },
    { label: t('stockPrediction'), page: 'stock-prediction' },
  ];

  const handleClick = (page: string) => {
    if (onNavigate) {
      onNavigate(page);
    }
  };

  return (
    <nav style={{ padding: '1rem' }}>
      {navItems.map((item) => {
        const isActive = currentPage === item.page;
        
        return (
          <NavLink
            key={item.page}
            label={item.label}
            active={isActive}
            onClick={() => handleClick(item.page)}
            style={{ marginBottom: '0.5rem' }}
          />
        );
      })}
    </nav>
  );
}

