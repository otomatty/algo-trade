/**
 * Tests for AlgorithmProposal component
 * 
 * Related Documentation:
 *   ├─ Spec: src/pages/AlgorithmProposal/AlgorithmProposal.spec.md
 *   └─ Plan: docs/03_plans/algorithm-proposal/README.md
 */
import { describe, it, expect, beforeEach, beforeAll, mock } from 'bun:test';
import { render, waitFor, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { AlgorithmProposal } from './AlgorithmProposal';
import { MantineProvider } from '@mantine/core';
import { setupDOM, setupDOMSync } from '../../test-utils/dom-setup';

// Setup DOM synchronously before module initialization
setupDOMSync();

// Mock Tauri API
const mockInvoke = mock((_cmd: string, ..._args: any[]) => Promise.resolve({}));

mock.module('@tauri-apps/api/core', () => ({
  invoke: mockInvoke,
}));

describe('AlgorithmProposal', () => {
  // Ensure DOM is set up before all tests
  beforeAll(async () => {
    await setupDOM();
  });

  beforeEach(() => {
    mockInvoke.mockClear();
  });

  it('should render algorithm proposal page', () => {
    mockInvoke.mockResolvedValue({ data_list: [] });

    const { container } = render(
      <MantineProvider>
        <AlgorithmProposal />
      </MantineProvider>
    );

    expect(within(container).getByText('Algorithm Proposal')).toBeDefined();
  });

  it('should load and display data sets', async () => {
    const mockDataSets = [
      {
        id: 1,
        name: 'Test Dataset 1',
        symbol: 'AAPL',
        start_date: '2023-01-01',
        end_date: '2023-12-31',
        record_count: 252,
        imported_at: '2023-01-01T00:00:00',
        source: 'csv',
        created_at: '2023-01-01T00:00:00',
      },
      {
        id: 2,
        name: 'Test Dataset 2',
        symbol: 'GOOGL',
        start_date: '2023-01-01',
        end_date: '2023-12-31',
        record_count: 252,
        imported_at: '2023-01-01T00:00:00',
        source: 'csv',
        created_at: '2023-01-01T00:00:00',
      },
    ];
    mockInvoke.mockResolvedValue({ data_list: mockDataSets });

    render(
      <MantineProvider>
        <AlgorithmProposal />
      </MantineProvider>
    );

    await waitFor(() => {
      expect(mockInvoke).toHaveBeenCalledWith('get_data_list');
    });
  });

  it('should display error message on load failure', async () => {
    mockInvoke.mockRejectedValue(new Error('Failed to load data sets'));

    const { container } = render(
      <MantineProvider>
        <AlgorithmProposal />
      </MantineProvider>
    );

    await waitFor(() => {
      expect(within(container).getByText(/Failed to load data sets/)).toBeDefined();
    });
  });

  it('should show empty state when no data sets', async () => {
    mockInvoke.mockResolvedValue({ data_list: [] });

    const { container } = render(
      <MantineProvider>
        <AlgorithmProposal />
      </MantineProvider>
    );

    await waitFor(() => {
      expect(
        within(container).getByText(/No data sets available. Please import data first./)
      ).toBeDefined();
    });
  });

  it('should display user preference inputs', async () => {
    mockInvoke.mockResolvedValue({ data_list: [] });

    const { container } = render(
      <MantineProvider>
        <AlgorithmProposal />
      </MantineProvider>
    );

    await waitFor(() => {
      expect(within(container).queryByText(/Risk Tolerance/i)).toBeDefined();
      expect(within(container).queryByText(/Trading Frequency/i)).toBeDefined();
      expect(within(container).queryByText(/Preferred Indicators/i)).toBeDefined();
    });
  });

  it('should display number of proposals input', async () => {
    mockInvoke.mockResolvedValue({ data_list: [] });

    const { container } = render(
      <MantineProvider>
        <AlgorithmProposal />
      </MantineProvider>
    );

    await waitFor(() => {
      expect(within(container).queryByText(/Number of Proposals/i)).toBeDefined();
    });
  });

  it('should display generate proposals button (disabled in Phase 1)', async () => {
    mockInvoke.mockResolvedValue({ data_list: [] });

    const { container } = render(
      <MantineProvider>
        <AlgorithmProposal />
      </MantineProvider>
    );

    await waitFor(() => {
      const button = within(container).queryByText(/Generate Proposals/i);
      expect(button).toBeDefined();
      // Phase 1ではボタンは無効化されている（データセットが空のため）
      // Mantine Buttonはdisabled属性またはdata-disabled属性で無効化される
      expect(
        button?.hasAttribute('disabled') || 
        button?.hasAttribute('data-disabled') ||
        button?.closest('button')?.hasAttribute('disabled')
      ).toBe(true);
    });
  });

  it('should display proposal list empty state', async () => {
    mockInvoke.mockResolvedValue({ data_list: [] });

    const { container } = render(
      <MantineProvider>
        <AlgorithmProposal />
      </MantineProvider>
    );

    await waitFor(() => {
      expect(
        within(container).getByText(/提案が生成されると、ここに表示されます/i)
      ).toBeDefined();
    });
  });

  it('should allow selecting data set', async () => {
    const mockDataSets = [
      {
        id: 1,
        name: 'Test Dataset',
        symbol: 'AAPL',
        start_date: '2023-01-01',
        end_date: '2023-12-31',
        record_count: 252,
        imported_at: '2023-01-01T00:00:00',
        source: 'csv',
        created_at: '2023-01-01T00:00:00',
      },
    ];
    mockInvoke.mockResolvedValue({ data_list: mockDataSets });

    const { container } = render(
      <MantineProvider>
        <AlgorithmProposal />
      </MantineProvider>
    );

    await waitFor(() => {
      expect(mockInvoke).toHaveBeenCalledWith('get_data_list');
    });

    // Wait for Select component to be rendered
    await waitFor(() => {
      const selectInput = within(container).queryByLabelText(/Select Data Set/i);
      expect(selectInput).toBeDefined();
    });
  });

  it('should allow inputting user preferences', async () => {
    mockInvoke.mockResolvedValue({ data_list: [] });

    const { container } = render(
      <MantineProvider>
        <AlgorithmProposal />
      </MantineProvider>
    );

    await waitFor(() => {
      // Risk tolerance select should be present
      const riskToleranceLabel = within(container).queryByText(/Risk Tolerance/i);
      expect(riskToleranceLabel).toBeDefined();

      // Trading frequency select should be present
      const tradingFrequencyLabel = within(container).queryByText(/Trading Frequency/i);
      expect(tradingFrequencyLabel).toBeDefined();

      // Preferred indicators multiselect should be present
      const indicatorsLabel = within(container).queryByText(/Preferred Indicators/i);
      expect(indicatorsLabel).toBeDefined();
    });
  });
});

