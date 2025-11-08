/**
 * Tests for AnalysisJobForm component
 * 
 * Related Documentation:
 *   ├─ Spec: src/pages/DataAnalysis/DataAnalysis.spec.md
 *   └─ Plan: docs/03_plans/data-analysis/README.md
 */
import { describe, it, expect, beforeEach, beforeAll, mock } from 'bun:test';
import { render, waitFor, within, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { AnalysisJobForm } from './AnalysisJobForm';
import { MantineProvider } from '@mantine/core';
import { setupDOM, setupDOMSync } from '../../test-utils/dom-setup';

// Setup DOM synchronously before module initialization
setupDOMSync();

// Mock Tauri API
const mockInvoke = mock((_cmd: string, ..._args: any[]) => Promise.resolve({}));

mock.module('@tauri-apps/api/core', () => ({
  invoke: mockInvoke,
}));

describe('AnalysisJobForm', () => {
  // Ensure DOM is set up before all tests
  beforeAll(async () => {
    await setupDOM();
  });

  beforeEach(() => {
    mockInvoke.mockClear();
  });

  it('should render analysis job form', () => {
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
        <AnalysisJobForm />
      </MantineProvider>
    );

    expect(within(container).getByText('Run Analysis')).toBeDefined();
  });

  it('should disable run button when no data set is selected', async () => {
    mockInvoke.mockResolvedValue({ data_list: [] });

    const { container } = render(
      <MantineProvider>
        <AnalysisJobForm />
      </MantineProvider>
    );

    await waitFor(() => {
      expect(mockInvoke).toHaveBeenCalledWith('get_data_list');
    });

    const runButton = within(container).getByText('Run Analysis');
    // Mantine Button uses data-disabled attribute or disabled property
    expect(runButton.hasAttribute('disabled') || runButton.hasAttribute('data-disabled')).toBe(true);
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
        <AnalysisJobForm />
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
      expect(runButton.hasAttribute('data-disabled')).toBe(false);
    }, { timeout: 2000 });

    // Check that run button is enabled
    await waitFor(() => {
    const runButton = within(container).getByText('Run Analysis');
    expect(runButton.hasAttribute('disabled')).toBe(false);
      expect(runButton.hasAttribute('data-disabled')).toBe(false);
    });
  });

  it('should call run_data_analysis with selected data set id', async () => {
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
    const onJobStarted = mock(() => {});
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
        <AnalysisJobForm onJobStarted={onJobStarted} />
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
      expect(runButton.hasAttribute('data-disabled')).toBe(false);
    }, { timeout: 2000 });

    // Click run button
    const runButton = within(container).getByText('Run Analysis');
    await userEvent.click(runButton);

    await waitFor(() => {
      expect(mockInvoke).toHaveBeenCalledWith('run_data_analysis', {
        data_set_id: 1,
      });
      expect(onJobStarted).toHaveBeenCalledWith('test-job-123');
    });
  });

  it('should show loading state while running analysis', async () => {
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
        return new Promise((resolve) => {
          setTimeout(() => resolve({ job_id: 'test-job-123' }), 100);
        });
      }
      return Promise.resolve({});
    });

    const { container } = render(
      <MantineProvider>
        <AnalysisJobForm />
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
      expect(runButton.hasAttribute('data-disabled')).toBe(false);
    }, { timeout: 2000 });

    // Click run button
    const runButton = within(container).getByText('Run Analysis');
    await userEvent.click(runButton);

    // Check loading state
    expect(runButton.hasAttribute('disabled')).toBe(true);
  });

  it('should display error message when analysis fails', async () => {
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
        <AnalysisJobForm />
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
      expect(runButton.hasAttribute('data-disabled')).toBe(false);
    }, { timeout: 2000 });

    // Click run button
    const runButton = within(container).getByText('Run Analysis');
    await userEvent.click(runButton);

    await waitFor(() => {
      expect(within(container).getByText(/Analysis failed/)).toBeDefined();
    });
  });
});
