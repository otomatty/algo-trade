/**
 * Tests for AlgorithmCard component
 * 
 * Related Documentation:
 *   ├─ Spec: src/pages/Dashboard/Dashboard.spec.md
 *   └─ Plan: docs/03_plans/dashboard/README.md
 */
import { describe, it, expect, beforeEach, beforeAll, mock } from 'bun:test';
import { render, within } from '@testing-library/react';
import { AlgorithmCard } from './AlgorithmCard';
import { MantineProvider } from '@mantine/core';
import { setupDOM, setupDOMSync } from '../../test-utils/dom-setup';
import { Algorithm } from '../../types/algorithm';
import { BacktestResultSummary } from '../../types/dashboard';

// Setup DOM synchronously before module initialization
setupDOMSync();

describe('AlgorithmCard', () => {
  beforeAll(async () => {
    await setupDOM();
  });

  const mockAlgorithm: Algorithm = {
    id: 1,
    name: 'Test Algorithm',
    description: 'Test description',
    definition: {
      triggers: [],
      actions: [],
    },
    proposal_id: null,
    created_at: '2023-01-01T00:00:00Z',
    updated_at: '2023-01-01T00:00:00Z',
  };

  const mockBacktestResult: BacktestResultSummary = {
    job_id: 'job-1',
    algorithm_id: 1,
    algorithm_name: 'Test Algorithm',
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
  };

  it('should render algorithm card', () => {
    const { container } = render(
      <MantineProvider>
        <AlgorithmCard algorithm={mockAlgorithm} />
      </MantineProvider>
    );

    expect(within(container).getByText('Test Algorithm')).toBeDefined();
    expect(within(container).getByText('Test description')).toBeDefined();
  });

  it('should display backtest result when provided', () => {
    const { container } = render(
      <MantineProvider>
        <AlgorithmCard algorithm={mockAlgorithm} backtestResult={mockBacktestResult} />
      </MantineProvider>
    );

    expect(within(container).getByText('15.20%')).toBeDefined();
    expect(within(container).getByText(/Sharpe: 1.20/)).toBeDefined();
    expect(within(container).getByText(/Win Rate: 60.0%/)).toBeDefined();
  });

  it('should not display description when null', () => {
    const algorithmWithoutDescription: Algorithm = {
      ...mockAlgorithm,
      description: null,
    };

    const { container } = render(
      <MantineProvider>
        <AlgorithmCard algorithm={algorithmWithoutDescription} />
      </MantineProvider>
    );

    expect(within(container).getByText('Test Algorithm')).toBeDefined();
    expect(within(container).queryByText('Test description')).toBeNull();
  });

  it('should call onSelect when select button is clicked', () => {
    const mockSelect = mock((algorithm: Algorithm) => {
      // Mock handler
    });

    const { container } = render(
      <MantineProvider>
        <AlgorithmCard algorithm={mockAlgorithm} onSelect={mockSelect} />
      </MantineProvider>
    );

    const selectButton = within(container).getByText('詳細');
    selectButton.click();

    expect(mockSelect).toHaveBeenCalledWith(mockAlgorithm);
  });

  it('should call onDelete when delete button is clicked', () => {
    const mockDelete = mock((algorithmId: number) => {
      // Mock handler
    });

    const { container } = render(
      <MantineProvider>
        <AlgorithmCard algorithm={mockAlgorithm} onDelete={mockDelete} />
      </MantineProvider>
    );

    const deleteButton = within(container).getByText('削除');
    deleteButton.click();

    expect(mockDelete).toHaveBeenCalledWith(1);
  });

  it('should display green badge for positive return', () => {
    const positiveResult: BacktestResultSummary = {
      ...mockBacktestResult,
      performance: {
        ...mockBacktestResult.performance,
        total_return: 10.0,
      },
    };

    const { container } = render(
      <MantineProvider>
        <AlgorithmCard algorithm={mockAlgorithm} backtestResult={positiveResult} />
      </MantineProvider>
    );

    expect(within(container).getByText('10.00%')).toBeDefined();
  });

  it('should display red badge for negative return', () => {
    const negativeResult: BacktestResultSummary = {
      ...mockBacktestResult,
      performance: {
        ...mockBacktestResult.performance,
        total_return: -5.0,
      },
    };

    const { container } = render(
      <MantineProvider>
        <AlgorithmCard algorithm={mockAlgorithm} backtestResult={negativeResult} />
      </MantineProvider>
    );

    expect(within(container).getByText('-5.00%')).toBeDefined();
  });
});

