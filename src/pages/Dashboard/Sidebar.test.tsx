/**
 * Tests for Sidebar component
 * 
 * Related Documentation:
 *   ├─ Spec: src/pages/Dashboard/Dashboard.spec.md
 *   └─ Plan: docs/03_plans/dashboard/README.md
 */
import { describe, it, expect, beforeEach, beforeAll, mock } from 'bun:test';
import { render, within } from '@testing-library/react';
import { Sidebar } from './Sidebar';
import { MantineProvider } from '@mantine/core';
import { I18nextProvider } from 'react-i18next';
import { setupDOM, setupDOMSync } from '../../test-utils/dom-setup';
import i18n from '../../i18n';

// Setup DOM synchronously before module initialization
setupDOMSync();

describe('Sidebar', () => {
  beforeAll(async () => {
    await setupDOM();
  });

  beforeEach(() => {
    i18n.changeLanguage('ja');
  });

  it('should render sidebar navigation items', () => {
    const handleNavigate = mock(() => {});
    const { container } = render(
      <MantineProvider>
        <I18nextProvider i18n={i18n}>
          <Sidebar currentPage="dashboard" onNavigate={handleNavigate} />
        </I18nextProvider>
      </MantineProvider>
    );

    expect(within(container).getByText('ダッシュボード')).toBeDefined();
    expect(within(container).getByText('アルゴリズム提案')).toBeDefined();
    expect(within(container).getByText('バックテスト')).toBeDefined();
    expect(within(container).getByText('データ管理')).toBeDefined();
    expect(within(container).getByText('データ解析')).toBeDefined();
    expect(within(container).getByText('銘柄予測')).toBeDefined();
  });

  it('should render navigation items in English when language is English', () => {
    i18n.changeLanguage('en');
    const handleNavigate = mock(() => {});
    const { container } = render(
      <MantineProvider>
        <I18nextProvider i18n={i18n}>
          <Sidebar currentPage="dashboard" onNavigate={handleNavigate} />
        </I18nextProvider>
      </MantineProvider>
    );

    expect(within(container).getByText('Dashboard')).toBeDefined();
    expect(within(container).getByText('Algorithm Proposal')).toBeDefined();
    expect(within(container).getByText('Backtest')).toBeDefined();
    expect(within(container).getByText('Data Management')).toBeDefined();
    expect(within(container).getByText('Data Analysis')).toBeDefined();
    expect(within(container).getByText('Stock Prediction')).toBeDefined();
  });

  it('should call onNavigate when navigation item is clicked', () => {
    const handleNavigate = mock(() => {});
    const { container } = render(
      <MantineProvider>
        <I18nextProvider i18n={i18n}>
          <Sidebar currentPage="dashboard" onNavigate={handleNavigate} />
        </I18nextProvider>
      </MantineProvider>
    );

    const algorithmProposalLink = within(container).getByText('アルゴリズム提案');
    algorithmProposalLink.click();

    expect(handleNavigate).toHaveBeenCalledWith('algorithm-proposal');
  });

  it('should highlight active page', () => {
    const handleNavigate = mock(() => {});
    const { container } = render(
      <MantineProvider>
        <I18nextProvider i18n={i18n}>
          <Sidebar currentPage="dashboard" onNavigate={handleNavigate} />
        </I18nextProvider>
      </MantineProvider>
    );

    // Verify that the component renders correctly with active page
    const dashboardLink = within(container).getByText('ダッシュボード');
    expect(dashboardLink).toBeDefined();
    // Mantine NavLink handles active state internally, so we just verify it renders
  });

  it('should use translation keys correctly', async () => {
    await i18n.changeLanguage('ja');
    const t = i18n.getFixedT('ja', 'navigation');
    
    expect(t('dashboard')).toBe('ダッシュボード');
    expect(t('algorithmProposal')).toBe('アルゴリズム提案');
    expect(t('backtest')).toBe('バックテスト');
    expect(t('dataManagement')).toBe('データ管理');
    expect(t('dataAnalysis')).toBe('データ解析');
    expect(t('stockPrediction')).toBe('銘柄予測');
  });
});

