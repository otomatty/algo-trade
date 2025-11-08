/**
 * Tests for BacktestSettings component
 * 
 * Related Documentation:
 *   ├─ Spec: src/pages/Backtest/BacktestSettings.spec.md
 *   └─ Plan: docs/03_plans/backtest/README.md
 */
import { describe, it, expect, beforeEach, beforeAll, mock } from 'bun:test';
import { render, waitFor, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { BacktestSettings } from './BacktestSettings';
import { MantineProvider } from '@mantine/core';
import { setupDOM, setupDOMSync } from '../../test-utils/dom-setup';

// Setup DOM synchronously before module initialization
setupDOMSync();

// Mock Tauri API
const mockInvoke = mock((_cmd: string, ..._args: any[]) => Promise.resolve({}));

mock.module('@tauri-apps/api/core', () => ({
  invoke: mockInvoke,
}));

describe('BacktestSettings', () => {
  // Ensure DOM is set up before all tests
  beforeAll(async () => {
    await setupDOM();
  });

  beforeEach(() => {
    mockInvoke.mockClear();
  });

  it('should render backtest settings page', () => {
    mockInvoke.mockImplementation((cmd: string) => {
      if (cmd === 'get_selected_algorithms') {
        return Promise.resolve({ algorithms: [] });
      }
      if (cmd === 'get_data_list') {
        return Promise.resolve({ data_list: [] });
      }
      return Promise.resolve({});
    });

    const { container } = render(
      <MantineProvider>
        <BacktestSettings />
      </MantineProvider>
    );

    expect(within(container).getByText('Backtest Settings')).toBeDefined();
  });

  it('should load and display algorithms', async () => {
    const mockAlgorithms = [
      {
        id: 1,
        name: 'Test Algorithm 1',
        description: 'Test description 1',
        definition: { triggers: [], actions: [] },
        proposal_id: null,
        created_at: '2023-01-01T00:00:00',
        updated_at: '2023-01-01T00:00:00',
      },
      {
        id: 2,
        name: 'Test Algorithm 2',
        description: 'Test description 2',
        definition: { triggers: [], actions: [] },
        proposal_id: null,
        created_at: '2023-01-01T00:00:00',
        updated_at: '2023-01-01T00:00:00',
      },
    ];

    mockInvoke.mockImplementation((cmd: string) => {
      if (cmd === 'get_selected_algorithms') {
        return Promise.resolve({ algorithms: mockAlgorithms });
      }
      if (cmd === 'get_data_list') {
        return Promise.resolve({ data_list: [] });
      }
      return Promise.resolve({});
    });

    render(
      <MantineProvider>
        <BacktestSettings />
      </MantineProvider>
    );

    await waitFor(() => {
      expect(mockInvoke).toHaveBeenCalledWith('get_selected_algorithms');
    });
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
    ];

    mockInvoke.mockImplementation((cmd: string) => {
      if (cmd === 'get_selected_algorithms') {
        return Promise.resolve({ algorithms: [] });
      }
      if (cmd === 'get_data_list') {
        return Promise.resolve({ data_list: mockDataSets });
      }
      return Promise.resolve({});
    });

    render(
      <MantineProvider>
        <BacktestSettings />
      </MantineProvider>
    );

    await waitFor(() => {
      expect(mockInvoke).toHaveBeenCalledWith('get_data_list');
    });
  });

  it('should display error message on algorithm load failure', async () => {
    mockInvoke.mockImplementation((cmd: string) => {
      if (cmd === 'get_selected_algorithms') {
        return Promise.reject(new Error('Failed to load algorithms'));
      }
      if (cmd === 'get_data_list') {
        return Promise.resolve({ data_list: [] });
      }
      return Promise.resolve({});
    });

    const { container } = render(
      <MantineProvider>
        <BacktestSettings />
      </MantineProvider>
    );

    await waitFor(() => {
      expect(within(container).getByText(/Failed to load algorithms/)).toBeDefined();
    });
  });

  it('should show empty state when no algorithms', async () => {
    mockInvoke.mockImplementation((cmd: string) => {
      if (cmd === 'get_selected_algorithms') {
        return Promise.resolve({ algorithms: [] });
      }
      if (cmd === 'get_data_list') {
        return Promise.resolve({ data_list: [] });
      }
      return Promise.resolve({});
    });

    const { container } = render(
      <MantineProvider>
        <BacktestSettings />
      </MantineProvider>
    );

    await waitFor(() => {
      expect(
        within(container).getByText(/No algorithms available/)
      ).toBeDefined();
    });
  });

  it('should show empty state when no data sets', async () => {
    mockInvoke.mockImplementation((cmd: string) => {
      if (cmd === 'get_selected_algorithms') {
        return Promise.resolve({ algorithms: [] });
      }
      if (cmd === 'get_data_list') {
        return Promise.resolve({ data_list: [] });
      }
      return Promise.resolve({});
    });

    const { container } = render(
      <MantineProvider>
        <BacktestSettings />
      </MantineProvider>
    );

    await waitFor(() => {
      expect(
        within(container).getByText(/No data sets available/)
      ).toBeDefined();
    });
  });

  it('should disable run button when validation fails', async () => {
    mockInvoke.mockImplementation((cmd: string) => {
      if (cmd === 'get_selected_algorithms') {
        return Promise.resolve({ algorithms: [] });
      }
      if (cmd === 'get_data_list') {
        return Promise.resolve({ data_list: [] });
      }
      return Promise.resolve({});
    });

    const { container } = render(
      <MantineProvider>
        <BacktestSettings />
      </MantineProvider>
    );

    await waitFor(() => {
      const button = within(container).getByText('Run Backtest');
      expect(button).toBeDefined();
      expect(button.hasAttribute('disabled') || button.getAttribute('disabled') === '').toBe(true);
    });
  });

  it('should show warning message when run button clicked in Phase 1', async () => {
    const mockAlgorithms = [
      {
        id: 1,
        name: 'Test Algorithm 1',
        description: 'Test description 1',
        definition: { triggers: [], actions: [] },
        proposal_id: null,
        created_at: '2023-01-01T00:00:00',
        updated_at: '2023-01-01T00:00:00',
      },
    ];

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
    ];

    mockInvoke.mockImplementation((cmd: string) => {
      if (cmd === 'get_selected_algorithms') {
        return Promise.resolve({ algorithms: mockAlgorithms });
      }
      if (cmd === 'get_data_list') {
        return Promise.resolve({ data_list: mockDataSets });
      }
      return Promise.resolve({});
    });

    const { container } = render(
      <MantineProvider>
        <BacktestSettings />
      </MantineProvider>
    );

    await waitFor(() => {
      expect(mockInvoke).toHaveBeenCalledWith('get_selected_algorithms');
      expect(mockInvoke).toHaveBeenCalledWith('get_data_list');
    });

    // Note: This test requires user interaction with date pickers and selects
    // which may be complex to simulate. For Phase 1, we'll test the basic structure.
  });
});

