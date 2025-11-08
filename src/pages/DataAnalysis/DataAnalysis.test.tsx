/**
 * Tests for DataAnalysis component
 * 
 * Related Documentation:
 *   ├─ Spec: src/pages/DataAnalysis/DataAnalysis.spec.md
 *   └─ Plan: docs/03_plans/data-analysis/README.md
 */
import { describe, it, expect, beforeEach, beforeAll, mock } from 'bun:test';
import { render, waitFor, within, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { DataAnalysis } from './DataAnalysis';
import { MantineProvider } from '@mantine/core';
import { setupDOM, setupDOMSync } from '../../test-utils/dom-setup';

// Setup DOM synchronously before module initialization
setupDOMSync();

// Mock Tauri API
const mockInvoke = mock((_cmd: string, ..._args: any[]) => Promise.resolve({}));

mock.module('@tauri-apps/api/core', () => ({
  invoke: mockInvoke,
}));

describe('DataAnalysis', () => {
  // Ensure DOM is set up before all tests
  beforeAll(async () => {
    await setupDOM();
  });

  beforeEach(() => {
    mockInvoke.mockClear();
  });

  it('should render data analysis page', () => {
    mockInvoke.mockResolvedValue({ data_list: [] });

    const { container } = render(
      <MantineProvider>
        <DataAnalysis />
      </MantineProvider>
    );

    expect(within(container).getByText('Data Analysis')).toBeDefined();
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
        <DataAnalysis />
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
        <DataAnalysis />
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
        <DataAnalysis />
      </MantineProvider>
    );

    await waitFor(() => {
      expect(
        within(container).getByText(/No data sets available. Please import data first./)
      ).toBeDefined();
    });
  });

  it('should enable run button when data set is selected', async () => {
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
        <DataAnalysis />
      </MantineProvider>
    );

    await waitFor(() => {
      expect(mockInvoke).toHaveBeenCalledWith('get_data_list');
    });

    // Wait for Select component to be rendered - find by label text
    await waitFor(() => {
      const label = within(container).queryByText('Select Data Set');
      expect(label).toBeDefined();
    });

    // Find the Select component by label and set value directly
    const selectInput = within(container).getByLabelText('Select Data Set');
    
    // Set the value directly using fireEvent.change
    // Mantine Select expects the value to be the string representation of the ID
    fireEvent.change(selectInput, { target: { value: '1' } });
    
    // Wait for the value to be set
    await waitFor(() => {
      expect(selectInput).toHaveProperty('value', '1');
    });

    // Check that run button is enabled
    const runButton = within(container).getByText('Run Analysis');
    expect(runButton.hasAttribute('disabled')).toBe(false);
  });

  it('should call run_data_analysis when run button is clicked', async () => {
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
    mockInvoke.mockImplementation((cmd: string) => {
      if (cmd === 'get_data_list') {
        return Promise.resolve({ data_list: mockDataSets });
      }
      if (cmd === 'run_data_analysis') {
        return Promise.resolve({ job_id: 'test-job-123' });
      }
      return Promise.resolve({});
    });

    const { container } = render(
      <MantineProvider>
        <DataAnalysis />
      </MantineProvider>
    );

    await waitFor(() => {
      expect(mockInvoke).toHaveBeenCalledWith('get_data_list');
    });

    // Wait for Select component to be rendered
    await waitFor(() => {
      const selectInput = within(container).queryByLabelText('Select Data Set');
      expect(selectInput).toBeDefined();
    });

    // Mantine Select's onChange handler needs to be called directly
    // Since fireEvent doesn't trigger Mantine's internal onChange, we need to manually trigger it
    // Find the Select component and trigger onChange by simulating user interaction
    const selectInput = within(container).getByLabelText('Select Data Set') as HTMLInputElement;
    
    // Type the value to trigger Mantine Select's search/filter, then press Enter
    await userEvent.click(selectInput);
    await userEvent.type(selectInput, 'Test Dataset');
    await userEvent.keyboard('{Enter}');
    
    // Wait for the value to be set and button to be enabled
    await waitFor(() => {
      const runButton = within(container).getByText('Run Analysis');
      expect(runButton.hasAttribute('disabled')).toBe(false);
    }, { timeout: 2000 });

    // Click run button
    const runButton = within(container).getByText('Run Analysis');
    await userEvent.click(runButton);

    await waitFor(() => {
      expect(mockInvoke).toHaveBeenCalledWith('run_data_analysis', {
        data_set_id: 1,
      });
    });
  });

  it('should display error when run_data_analysis fails', async () => {
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
    mockInvoke.mockImplementation((cmd: string) => {
      if (cmd === 'get_data_list') {
        return Promise.resolve({ data_list: mockDataSets });
      }
      if (cmd === 'run_data_analysis') {
        return Promise.reject(new Error('Analysis failed'));
      }
      return Promise.resolve({});
    });

    const { container } = render(
      <MantineProvider>
        <DataAnalysis />
      </MantineProvider>
    );

    await waitFor(() => {
      expect(mockInvoke).toHaveBeenCalledWith('get_data_list');
    });

    // Wait for Select component to be rendered
    await waitFor(() => {
      const selectInput = within(container).queryByLabelText('Select Data Set');
      expect(selectInput).toBeDefined();
    });

    // Mantine Select's onChange handler needs to be called directly
    // Since fireEvent doesn't trigger Mantine's internal onChange, we need to manually trigger it
    // Find the Select component and trigger onChange by simulating user interaction
    const selectInput = within(container).getByLabelText('Select Data Set') as HTMLInputElement;
    
    // Type the value to trigger Mantine Select's search/filter, then press Enter
    await userEvent.click(selectInput);
    await userEvent.type(selectInput, 'Test Dataset');
    await userEvent.keyboard('{Enter}');
    
    // Wait for the value to be set and button to be enabled
    await waitFor(() => {
      const runButton = within(container).getByText('Run Analysis');
      expect(runButton.hasAttribute('disabled')).toBe(false);
    }, { timeout: 2000 });

    // Click run button
    const runButton = within(container).getByText('Run Analysis');
    await userEvent.click(runButton);

    await waitFor(() => {
      expect(within(container).getByText(/Analysis failed/)).toBeDefined();
    });
  });

  it('should show results when job is completed', async () => {
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
    mockInvoke.mockImplementation((cmd: string) => {
      if (cmd === 'get_data_list') {
        return Promise.resolve({ data_list: mockDataSets });
      }
      if (cmd === 'run_data_analysis') {
        return Promise.resolve({ job_id: 'test-job-123' });
      }
      if (cmd === 'get_analysis_status') {
        return Promise.resolve({
          status: 'completed',
          progress: 100,
          message: 'Completed',
        });
      }
      if (cmd === 'get_analysis_results') {
        return Promise.resolve({
          job_id: 'test-job-123',
          data_set_id: 1,
          analysis_summary: {
            trend_direction: 'upward',
            volatility_level: 'medium',
            dominant_patterns: [],
          },
          technical_indicators: {},
          statistics: {
            price_range: { min: 100, max: 110, current: 105 },
            volume_average: 1000000,
            price_change_percent: 5.0,
          },
        });
      }
      return Promise.resolve({});
    });

    const { container } = render(
      <MantineProvider>
        <DataAnalysis />
      </MantineProvider>
    );

    await waitFor(() => {
      expect(mockInvoke).toHaveBeenCalledWith('get_data_list');
    });

    // Wait for Select component to be rendered
    await waitFor(() => {
      const selectInput = within(container).queryByLabelText('Select Data Set');
      expect(selectInput).toBeDefined();
    });

    // Select and run analysis
    const selectInput = within(container).getByLabelText('Select Data Set');
    await userEvent.click(selectInput);
    const option = within(container).getByText('Test Dataset');
    await userEvent.click(option);

    const runButton = within(container).getByText('Run Analysis');
    await userEvent.click(runButton);

    // Wait for completion and results display
    await waitFor(() => {
      expect(within(container).getByText(/Trend Analysis/)).toBeDefined();
    }, { timeout: 5000 });
  });
});
