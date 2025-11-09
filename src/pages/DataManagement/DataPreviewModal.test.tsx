/**
 * Tests for DataPreviewModal component
 * 
 * Related Documentation:
 *   ├─ Plan: docs/03_plans/data-management/README.md
 *   └─ API Spec: docs/03_plans/data-management/api-spec.md
 */
import { describe, it, expect, beforeEach, beforeAll, mock } from 'bun:test';
import { render, within, waitFor } from '@testing-library/react';
import { DataPreviewModal } from './DataPreviewModal';
import { MantineProvider } from '@mantine/core';
import { setupDOM, setupDOMSync } from '../../test-utils/dom-setup';
import { DataSet, DataPreview } from '../../types/data';
import * as tauriApi from '@tauri-apps/api/core';

// Setup DOM synchronously before module initialization
setupDOMSync();

// Mock Tauri API
mock.module('@tauri-apps/api/core', () => ({
  invoke: mock(() => Promise.resolve({})),
}));

describe('DataPreviewModal', () => {
  // Ensure DOM is set up before all tests
  beforeAll(async () => {
    await setupDOM();
  });

  const mockDataSet: DataSet = {
    id: 1,
    name: 'Test Dataset',
    symbol: 'AAPL',
    start_date: '2023-01-01',
    end_date: '2023-01-05',
    record_count: 5,
    imported_at: '2023-01-01T00:00:00',
    source: 'csv',
    created_at: '2023-01-01T00:00:00',
  };

  const mockPreview: DataPreview = {
    data_set_id: 1,
    data: [
      {
        id: 1,
        data_set_id: 1,
        date: '2023-01-01',
        open: 100.0,
        high: 105.0,
        low: 99.0,
        close: 103.0,
        volume: 1000000,
      },
      {
        id: 2,
        data_set_id: 1,
        date: '2023-01-02',
        open: 103.0,
        high: 108.0,
        low: 102.0,
        close: 106.0,
        volume: 1200000,
      },
    ],
    statistics: {
      count: 2,
      date_range: {
        start: '2023-01-01',
        end: '2023-01-02',
      },
      open: { mean: 101.5, min: 100.0, max: 103.0, std: 1.5 },
      high: { mean: 106.5, min: 105.0, max: 108.0, std: 1.5 },
      low: { mean: 100.5, min: 99.0, max: 102.0, std: 1.5 },
      close: { mean: 104.5, min: 103.0, max: 106.0, std: 1.5 },
      volume: { mean: 1100000, min: 1000000, max: 1200000, std: 100000 },
    },
  };

  beforeEach(() => {
    mock.restore();
  });

  it('should not render modal when dataSet is null', () => {
    const onClose = mock(() => {});

    const { baseElement } = render(
      <MantineProvider>
        <DataPreviewModal dataSet={null} opened={true} onClose={onClose} />
      </MantineProvider>
    );

    const modalTitle = within(baseElement).queryByText(/Test Dataset/);
    expect(modalTitle).toBeNull();
  });

  it('should render modal when opened with dataSet', () => {
    const onClose = mock(() => {});
    const invokeMock = mock(() => Promise.resolve(mockPreview));
    mock.module('@tauri-apps/api/core', () => ({
      invoke: invokeMock,
    }));

    const { baseElement } = render(
      <MantineProvider>
        <DataPreviewModal dataSet={mockDataSet} opened={true} onClose={onClose} />
      </MantineProvider>
    );

    expect(within(baseElement).getByText(/Test Dataset - Data Preview/)).toBeDefined();
  });

  it('should display loading state initially', async () => {
    const onClose = mock(() => {});
    const invokeMock = mock(() => new Promise(() => {})); // Never resolves
    mock.module('@tauri-apps/api/core', () => ({
      invoke: invokeMock,
    }));

    const { baseElement } = render(
      <MantineProvider>
        <DataPreviewModal dataSet={mockDataSet} opened={true} onClose={onClose} />
      </MantineProvider>
    );

    await waitFor(() => {
      expect(within(baseElement).getByText('Loading preview...')).toBeDefined();
    });
  });

  it('should display error message when API call fails', async () => {
    const onClose = mock(() => {});
    const invokeMock = mock(() => Promise.reject(new Error('API Error')));
    mock.module('@tauri-apps/api/core', () => ({
      invoke: invokeMock,
    }));

    const { baseElement } = render(
      <MantineProvider>
        <DataPreviewModal dataSet={mockDataSet} opened={true} onClose={onClose} />
      </MantineProvider>
    );

    await waitFor(() => {
      expect(within(baseElement).getByText(/Failed to load data preview/)).toBeDefined();
    });
  });

  it('should display statistics when preview data is loaded', async () => {
    const onClose = mock(() => {});
    const invokeMock = mock(() => Promise.resolve(mockPreview));
    mock.module('@tauri-apps/api/core', () => ({
      invoke: invokeMock,
    }));

    const { baseElement } = render(
      <MantineProvider>
        <DataPreviewModal dataSet={mockDataSet} opened={true} onClose={onClose} />
      </MantineProvider>
    );

    await waitFor(() => {
      expect(within(baseElement).getByText(/Statistics/)).toBeDefined();
      expect(within(baseElement).getByText(/Count: 2 records/)).toBeDefined();
      expect(within(baseElement).getByText(/Mean: 101.50/)).toBeDefined();
    });
  });

  it('should display data table when preview data is loaded', async () => {
    const onClose = mock(() => {});
    const invokeMock = mock(() => Promise.resolve(mockPreview));
    mock.module('@tauri-apps/api/core', () => ({
      invoke: invokeMock,
    }));

    const { baseElement } = render(
      <MantineProvider>
        <DataPreviewModal dataSet={mockDataSet} opened={true} onClose={onClose} />
      </MantineProvider>
    );

    await waitFor(() => {
      expect(within(baseElement).getByText(/Data \(2 records shown\)/)).toBeDefined();
      expect(within(baseElement).getByText('100.00')).toBeDefined();
      expect(within(baseElement).getByText('103.00')).toBeDefined();
    });
  });

  it('should call invoke with correct parameters', async () => {
    const onClose = mock(() => {});
    const invokeMock = mock(() => Promise.resolve(mockPreview));
    mock.module('@tauri-apps/api/core', () => ({
      invoke: invokeMock,
    }));

    render(
      <MantineProvider>
        <DataPreviewModal dataSet={mockDataSet} opened={true} onClose={onClose} />
      </MantineProvider>
    );

    await waitFor(() => {
      expect(invokeMock).toHaveBeenCalledWith('get_data_preview', {
        data_set_id: 1,
        limit: 100,
      });
    });
  });

  it('should reset preview data when modal is closed', async () => {
    const onClose = mock(() => {});
    const invokeMock = mock(() => Promise.resolve(mockPreview));
    mock.module('@tauri-apps/api/core', () => ({
      invoke: invokeMock,
    }));

    const { rerender } = render(
      <MantineProvider>
        <DataPreviewModal dataSet={mockDataSet} opened={true} onClose={onClose} />
      </MantineProvider>
    );

    await waitFor(() => {
      expect(invokeMock).toHaveBeenCalled();
    });

    // Close modal
    rerender(
      <MantineProvider>
        <DataPreviewModal dataSet={mockDataSet} opened={false} onClose={onClose} />
      </MantineProvider>
    );

    // Open again - should reload
    rerender(
      <MantineProvider>
        <DataPreviewModal dataSet={mockDataSet} opened={true} onClose={onClose} />
      </MantineProvider>
    );

    await waitFor(() => {
      expect(invokeMock).toHaveBeenCalledTimes(2);
    });
  });

  it('should display date range in statistics', async () => {
    const onClose = mock(() => {});
    const invokeMock = mock(() => Promise.resolve(mockPreview));
    mock.module('@tauri-apps/api/core', () => ({
      invoke: invokeMock,
    }));

    const { baseElement } = render(
      <MantineProvider>
        <DataPreviewModal dataSet={mockDataSet} opened={true} onClose={onClose} />
      </MantineProvider>
    );

    await waitFor(() => {
      const dateRangeText = within(baseElement).getByText(/Date Range:/);
      expect(dateRangeText).toBeDefined();
    });
  });

  it('should display all statistics fields (open, high, low, close, volume)', async () => {
    const onClose = mock(() => {});
    const invokeMock = mock(() => Promise.resolve(mockPreview));
    mock.module('@tauri-apps/api/core', () => ({
      invoke: invokeMock,
    }));

    const { baseElement } = render(
      <MantineProvider>
        <DataPreviewModal dataSet={mockDataSet} opened={true} onClose={onClose} />
      </MantineProvider>
    );

    await waitFor(() => {
      expect(within(baseElement).getByText(/Open/i)).toBeDefined();
      expect(within(baseElement).getByText(/High/i)).toBeDefined();
      expect(within(baseElement).getByText(/Low/i)).toBeDefined();
      expect(within(baseElement).getByText(/Close/i)).toBeDefined();
      expect(within(baseElement).getByText(/Volume/i)).toBeDefined();
    });
  });
});

