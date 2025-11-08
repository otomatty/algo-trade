/**
 * Tests for AlgorithmList component
 * 
 * Related Documentation:
 *   ├─ Spec: src/pages/Dashboard/Dashboard.spec.md
 *   └─ Plan: docs/03_plans/dashboard/README.md
 */
import { describe, it, expect, beforeEach, beforeAll, mock } from 'bun:test';
import { render, within } from '@testing-library/react';
import { AlgorithmList } from './AlgorithmList';
import { MantineProvider } from '@mantine/core';
import { setupDOM, setupDOMSync } from '../../test-utils/dom-setup';
import { Algorithm } from '../../types/algorithm';
import { BacktestResultSummary } from '../../types/dashboard';

// Setup DOM synchronously before module initialization
setupDOMSync();

describe('AlgorithmList', () => {
  beforeAll(async () => {
    await setupDOM();
  });

  const mockAlgorithms: Algorithm[] = [
    {
      id: 1,
      name: 'Test Algorithm 1',
      description: 'Test description 1',
      definition: {
        triggers: [],
        actions: [],
      },
      proposal_id: null,
      created_at: '2023-01-01T00:00:00Z',
      updated_at: '2023-01-01T00:00:00Z',
    },
    {
      id: 2,
      name: 'Test Algorithm 2',
      description: null,
      definition: {
        triggers: [],
        actions: [],
      },
      proposal_id: null,
      created_at: '2023-01-01T00:00:00Z',
      updated_at: '2023-01-01T00:00:00Z',
    },
  ];

  const mockBacktestResults: BacktestResultSummary[] = [
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
  ];

  it('should render algorithm list', () => {
    const { container } = render(
      <MantineProvider>
        <AlgorithmList algorithms={mockAlgorithms} />
      </MantineProvider>
    );

    expect(within(container).getByText('Algorithms')).toBeDefined();
    expect(within(container).getByText('Test Algorithm 1')).toBeDefined();
    expect(within(container).getByText('Test Algorithm 2')).toBeDefined();
  });

  it('should display loading skeleton when loading', () => {
    const { container } = render(
      <MantineProvider>
        <AlgorithmList algorithms={[]} loading={true} />
      </MantineProvider>
    );

    expect(within(container).getByText('Algorithms')).toBeDefined();
  });

  it('should display empty state when no algorithms', () => {
    const { container } = render(
      <MantineProvider>
        <AlgorithmList algorithms={[]} loading={false} />
      </MantineProvider>
    );

    expect(
      within(container).getByText(/アルゴリズムが選択されていません/)
    ).toBeDefined();
  });

  it('should display backtest results when provided', () => {
    const { container } = render(
      <MantineProvider>
        <AlgorithmList
          algorithms={mockAlgorithms}
          backtestResults={mockBacktestResults}
        />
      </MantineProvider>
    );

    expect(within(container).getByText('15.20%')).toBeDefined();
    expect(within(container).getByText(/Sharpe: 1.20/)).toBeDefined();
    expect(within(container).getByText(/Win Rate: 60.0%/)).toBeDefined();
  });

  it('should call onSelect when select button is clicked', () => {
    const mockSelect = mock((algorithm: Algorithm) => {
      // Mock handler
    });

    const { container } = render(
      <MantineProvider>
        <AlgorithmList algorithms={mockAlgorithms} onSelect={mockSelect} />
      </MantineProvider>
    );

    const selectButtons = within(container).getAllByText('詳細');
    selectButtons[0].click();

    expect(mockSelect).toHaveBeenCalledWith(mockAlgorithms[0]);
  });

  it('should call onDelete when delete button is clicked', () => {
    const mockDelete = mock((algorithmId: number) => {
      // Mock handler
    });

    const { container } = render(
      <MantineProvider>
        <AlgorithmList algorithms={mockAlgorithms} onDelete={mockDelete} />
      </MantineProvider>
    );

    const deleteButtons = within(container).getAllByText('削除');
    deleteButtons[0].click();

    expect(mockDelete).toHaveBeenCalledWith(1);
  });
});

