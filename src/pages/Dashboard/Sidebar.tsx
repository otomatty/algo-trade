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
 *   └─ @mantine/hooks (for navigation state)
 * 
 * Related Documentation:
 *   ├─ Spec: src/pages/Dashboard/Dashboard.spec.md
 *   └─ Plan: docs/03_plans/dashboard/README.md
 */
import { NavLink } from '@mantine/core';

interface SidebarProps {
  currentPage?: string;
  onNavigate?: (page: string) => void;
}

export function Sidebar({ currentPage, onNavigate }: SidebarProps) {
  const navItems = [
    { label: 'ダッシュボード', page: 'dashboard' },
    { label: 'アルゴリズム提案', page: 'algorithm-proposal' },
    { label: 'バックテスト', page: 'backtest' },
    { label: 'データ管理', page: 'data-management' },
    { label: 'データ解析', page: 'data-analysis' },
    { label: '銘柄予測', page: 'stock-prediction' },
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

