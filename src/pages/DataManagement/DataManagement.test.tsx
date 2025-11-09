/**
 * Tests for DataManagement component
 * 
 * Related Documentation:
 *   └─ Plan: docs/03_plans/data-management/README.md
 */
import { describe, it, expect, beforeEach, vi } from 'bun:test';
import { render, screen, waitFor } from '@testing-library/react';
import { DataManagement } from './DataManagement';
import { MantineProvider } from '@mantine/core';

// Mock Tauri API
vi.mock('@tauri-apps/api/core', () => ({
  invoke: vi.fn(),
}));

vi.mock('@tauri-apps/plugin-dialog', () => ({
  open: vi.fn(),
}));

describe('DataManagement', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render data management page', () => {
    const { invoke } = require('@tauri-apps/api/core');
    invoke.mockResolvedValue({ data_list: [] });

    render(
      <MantineProvider>
        <DataManagement />
      </MantineProvider>
    );

    expect(screen.getByText('Data Management')).toBeDefined();
    expect(screen.getByText('Data Sets')).toBeDefined();
  });

  it('should load and display data sets', async () => {
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

    render(
      <MantineProvider>
        <DataManagement />
      </MantineProvider>
    );

    await waitFor(() => {
      expect(screen.getByText('Test Dataset')).toBeDefined();
      expect(screen.getByText('AAPL')).toBeDefined();
    });
  });

  it('should display error message on load failure', async () => {
    const { invoke } = require('@tauri-apps/api/core');
    invoke.mockRejectedValue(new Error('Failed to load data sets'));

    render(
      <MantineProvider>
        <DataManagement />
      </MantineProvider>
    );

    await waitFor(() => {
      expect(screen.getByText(/Failed to load data sets/)).toBeDefined();
    });
  });

  it('should show empty state when no data sets', async () => {
    const { invoke } = require('@tauri-apps/api/core');
    invoke.mockResolvedValue({ data_list: [] });

    render(
      <MantineProvider>
        <DataManagement />
      </MantineProvider>
    );

    await waitFor(() => {
      expect(
        screen.getByText(/No data sets found. Import a CSV file to get started./)
      ).toBeDefined();
    });
  });
});

