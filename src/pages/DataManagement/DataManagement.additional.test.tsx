/**
 * Additional tests for DataManagement component
 * 
 * Related Documentation:
 *   └─ Plan: docs/03_plans/data-management/README.md
 */
import { describe, it, expect, beforeEach, vi } from 'bun:test';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { DataManagement } from './DataManagement';
import { MantineProvider } from '@mantine/core';

// Mock Tauri API
vi.mock('@tauri-apps/api/core', () => ({
  invoke: vi.fn(),
}));

vi.mock('@tauri-apps/plugin-dialog', () => ({
  open: vi.fn(),
}));

describe('DataManagement - Additional Tests', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should handle delete data set', async () => {
    const { invoke } = require('@tauri-apps/api/core');
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
    
    // Mock get_data_list
    invoke.mockImplementation((cmd) => {
      if (cmd === 'get_data_list') {
        return Promise.resolve({ data_list: mockDataSets });
      }
      if (cmd === 'delete_data_set') {
        return Promise.resolve({ message: 'Data set deleted successfully' });
      }
      return Promise.resolve({});
    });

    // Mock window.confirm
    const originalConfirm = window.confirm;
    window.confirm = vi.fn(() => true);

    render(
      <MantineProvider>
        <DataManagement />
      </MantineProvider>
    );

    await waitFor(() => {
      expect(screen.getByText('Test Dataset')).toBeDefined();
    });

    const deleteButton = screen.getByText('Delete');
    await userEvent.click(deleteButton);

    await waitFor(() => {
      expect(invoke).toHaveBeenCalledWith('delete_data_set', { data_set_id: 1 });
      expect(invoke).toHaveBeenCalledWith('get_data_list');
    });

    window.confirm = originalConfirm;
  });

  it('should handle delete cancellation', async () => {
    const { invoke } = require('@tauri-apps/api/core');
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
    
    invoke.mockResolvedValue({ data_list: mockDataSets });

    // Mock window.confirm to return false
    const originalConfirm = window.confirm;
    window.confirm = vi.fn(() => false);

    render(
      <MantineProvider>
        <DataManagement />
      </MantineProvider>
    );

    await waitFor(() => {
      expect(screen.getByText('Test Dataset')).toBeDefined();
    });

    const deleteButton = screen.getByText('Delete');
    await userEvent.click(deleteButton);

    // Should not call delete_data_set
    await waitFor(() => {
      expect(invoke).not.toHaveBeenCalledWith('delete_data_set', expect.any(Object));
    });

    window.confirm = originalConfirm;
  });

  it('should handle refresh button', async () => {
    const { invoke } = require('@tauri-apps/api/core');
    invoke.mockResolvedValue({ data_list: [] });

    render(
      <MantineProvider>
        <DataManagement />
      </MantineProvider>
    );

    await waitFor(() => {
      expect(invoke).toHaveBeenCalledWith('get_data_list');
    });

    const refreshButton = screen.getByText('Refresh');
    await userEvent.click(refreshButton);

    await waitFor(() => {
      expect(invoke).toHaveBeenCalledTimes(2); // Initial load + refresh
    });
  });

  it('should handle delete error', async () => {
    const { invoke } = require('@tauri-apps/api/core');
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
    
    invoke.mockImplementation((cmd) => {
      if (cmd === 'get_data_list') {
        return Promise.resolve({ data_list: mockDataSets });
      }
      if (cmd === 'delete_data_set') {
        return Promise.reject(new Error('Delete failed'));
      }
      return Promise.resolve({});
    });

    const originalConfirm = window.confirm;
    window.confirm = vi.fn(() => true);

    render(
      <MantineProvider>
        <DataManagement />
      </MantineProvider>
    );

    await waitFor(() => {
      expect(screen.getByText('Test Dataset')).toBeDefined();
    });

    const deleteButton = screen.getByText('Delete');
    await userEvent.click(deleteButton);

    await waitFor(() => {
      expect(screen.getByText(/Delete failed/)).toBeDefined();
    });

    window.confirm = originalConfirm;
  });
});

