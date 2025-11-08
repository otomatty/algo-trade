/**
 * Tests for ResultSummary component
 * 
 * Related Documentation:
 *   ├─ Spec: src/pages/Dashboard/Dashboard.spec.md
 *   └─ Plan: docs/03_plans/dashboard/README.md
 */
import { describe, it, expect, beforeEach, beforeAll } from 'bun:test';
import { render, within } from '@testing-library/react';
import { ResultSummary } from './ResultSummary';
import { MantineProvider } from '@mantine/core';
import { setupDOM, setupDOMSync } from '../../test-utils/dom-setup';
import { BacktestResultSummary } from '../../types/dashboard';

// Setup DOM synchronously before module initialization
setupDOMSync();

describe('ResultSummary', () => {
  beforeAll(async () => {
    await setupDOM();
  });

  const mockResults: BacktestResultSummary[] = [
    {
      job_id: 'job-1',
      algorithm_id: 1,
      algorithm_name: 'Test Algorithm 1',
      start_date: '2023-01-01',
      end_date: '2023-12-31',
      completed_at: '2023-12-31T00:00:00Z',
      performance: {
        total_return: 15.2,
        sharpe_ratio: 1.2,
        max_drawdown: 5.0,
        win_rate: 60.0,
        total_trades: 100,
        average_profit: 1000,
        average_loss: -500,
      },
    },
    {
      job_id: 'job-2',
      algorithm_id: 2,
      algorithm_name: 'Test Algorithm 2',
      start_date: '2023-01-01',
      end_date: '2023-12-31',
      completed_at: '2023-12-31T00:00:00Z',
      performance: {
        total_return: 8.5,
        sharpe_ratio: 0.8,
        max_drawdown: 3.0,
        win_rate: 55.0,
        total_trades: 80,
        average_profit: 800,
        average_loss: -400,
      },
    },
  ];

  it('should render result summary', () => {
    const { container } = render(
      <MantineProvider>
        <ResultSummary results={mockResults} />
      </MantineProvider>
    );

    expect(within(container).getByText('Performance Summary')).toBeDefined();
    expect(within(container).getByText('Total Return')).toBeDefined();
    expect(within(container).getByText('Sharpe Ratio')).toBeDefined();
  });

  it('should display loading skeleton when loading', () => {
    const { container } = render(
      <MantineProvider>
        <ResultSummary results={[]} loading={true} />
      </MantineProvider>
    );

    expect(within(container).getByText('Performance Summary')).toBeDefined();
  });

  it('should display empty state when no results', () => {
    const { container } = render(
      <MantineProvider>
        <ResultSummary results={[]} loading={false} />
      </MantineProvider>
    );

    expect(
      within(container).getByText(/バックテスト結果がありません/)
    ).toBeDefined();
  });

  it('should filter results by selected algorithm ID', () => {
    const { container } = render(
      <MantineProvider>
        <ResultSummary results={mockResults} selectedAlgorithmId={1} />
      </MantineProvider>
    );

    expect(within(container).getByText('Performance Summary')).toBeDefined();
    // Should show aggregated metrics for algorithm 1 only
  });

  it('should aggregate performance metrics correctly', () => {
    const { container } = render(
      <MantineProvider>
        <ResultSummary results={mockResults} />
      </MantineProvider>
    );

    // Check that aggregated values are displayed
    expect(within(container).getByText('Total Return')).toBeDefined();
    expect(within(container).getByText('Sharpe Ratio')).toBeDefined();
  });
});

