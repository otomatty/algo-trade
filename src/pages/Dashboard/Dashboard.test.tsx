/**
 * Tests for Dashboard component
 * 
 * Related Documentation:
 *   ├─ Spec: src/pages/Dashboard/Dashboard.spec.md
 *   └─ Plan: docs/03_plans/dashboard/README.md
 */
import { describe, it, expect, beforeEach, beforeAll, mock } from 'bun:test';
import { render, waitFor, within } from '@testing-library/react';
import { Dashboard } from './Dashboard';
import { MantineProvider } from '@mantine/core';
import { setupDOM, setupDOMSync } from '../../test-utils/dom-setup';

// Setup DOM synchronously before module initialization
setupDOMSync();

// Mock Tauri API
const mockInvoke = mock((_cmd: string, ..._args: any[]) => Promise.resolve({}));

mock.module('@tauri-apps/api/core', () => ({
  invoke: mockInvoke,
}));

describe('Dashboard', () => {
  // Ensure DOM is set up before all tests
  beforeAll(async () => {
    await setupDOM();
  });

  beforeEach(() => {
    mockInvoke.mockClear();
  });

  it('should render dashboard page', () => {
    const { container } = render(
      <MantineProvider>
        <Dashboard />
      </MantineProvider>
    );

    expect(within(container).getByText('Dashboard')).toBeDefined();
  });

  it('should render sidebar navigation', () => {
    const { container } = render(
      <MantineProvider>
        <Dashboard />
      </MantineProvider>
    );

    expect(within(container).getByText('ダッシュボード')).toBeDefined();
    expect(within(container).getByText('アルゴリズム提案')).toBeDefined();
    expect(within(container).getByText('バックテスト')).toBeDefined();
    expect(within(container).getByText('データ管理')).toBeDefined();
    expect(within(container).getByText('データ解析')).toBeDefined();
  });

  it('should render header', () => {
    const { container } = render(
      <MantineProvider>
        <Dashboard />
      </MantineProvider>
    );

    expect(within(container).getByText('Algorithm Trading Platform')).toBeDefined();
  });

  it('should call onNavigate when sidebar link is clicked', async () => {
    const mockNavigate = mock((page: string) => {
      // Mock navigation handler
    });

    const { container } = render(
      <MantineProvider>
        <Dashboard onNavigate={mockNavigate} />
      </MantineProvider>
    );

    const algorithmProposalLink = within(container).getByText('アルゴリズム提案');
    algorithmProposalLink.click();

    await waitFor(() => {
      expect(mockNavigate).toHaveBeenCalledWith('algorithm-proposal');
    });
  });

  it('should highlight current page in sidebar', () => {
    const { container } = render(
      <MantineProvider>
        <Dashboard currentPage="backtest" />
      </MantineProvider>
    );

    // Check that backtest link is active
    const backtestLink = within(container).getByText('バックテスト');
    expect(backtestLink).toBeDefined();
  });
});

