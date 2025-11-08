/**
 * Tests for DataImportForm component
 * 
 * Related Documentation:
 *   └─ Plan: docs/03_plans/data-management/README.md
 */
import { describe, it, expect, beforeEach, beforeAll, mock } from 'bun:test';
import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { setupDOM, setupDOMSync } from '../../test-utils/dom-setup';
import { MantineProvider } from '@mantine/core';

// Setup DOM synchronously before module initialization
setupDOMSync();

// Mock Tauri API - MUST be before importing DataImportForm
const mockInvoke = mock(() => Promise.resolve({}));
const mockOpen = mock(() => Promise.resolve<string | null>(null));

mock.module('@tauri-apps/api/core', () => ({
  invoke: mockInvoke,
}));

mock.module('@tauri-apps/api/dialog', () => ({
  open: mockOpen,
}));

// Import after mocks are set up
import { DataImportForm } from './DataImportForm';

describe('DataImportForm', () => {
  // Ensure DOM is set up before all tests
  beforeAll(async () => {
    await setupDOM();
  });

  beforeEach(() => {
    mockInvoke.mockClear();
    mockOpen.mockClear();
  });

  it('should render import form', () => {
    render(
      <MantineProvider>
        <DataImportForm />
      </MantineProvider>
    );

    expect(screen.getByText('Import OHLCV Data from CSV')).toBeDefined();
    expect(screen.getByText('Select CSV File')).toBeDefined();
  });

  it('should handle file selection', async () => {
    mockOpen.mockResolvedValue('/path/to/file.csv');

    render(
      <MantineProvider>
        <DataImportForm />
      </MantineProvider>
    );

    const selectButton = screen.getByText('Select CSV File');
    await userEvent.click(selectButton);

    await waitFor(() => {
      expect(mockOpen).toHaveBeenCalled();
    });
  });

  it('should import CSV file successfully', async () => {
    mockOpen.mockResolvedValue('/path/to/file.csv');
    mockInvoke.mockResolvedValue({
      data_set_id: 1,
      name: 'Test Dataset',
      record_count: 100,
    });

    const onSuccess = mock(() => {});

    render(
      <MantineProvider>
        <DataImportForm onSuccess={onSuccess} />
      </MantineProvider>
    );

    // Select file
    const selectButton = screen.getByText('Select CSV File');
    await userEvent.click(selectButton);

    await waitFor(() => {
      expect(mockOpen).toHaveBeenCalled();
    });

    // Import
    const importButton = screen.getByText('Import');
    await userEvent.click(importButton);

    await waitFor(() => {
      expect(mockInvoke).toHaveBeenCalledWith('import_ohlcv_data', {
        file_path: '/path/to/file.csv',
        name: undefined,
      });
      expect(screen.getByText(/Data imported successfully!/)).toBeDefined();
      expect(onSuccess).toHaveBeenCalled();
    });
  });

  it('should show error on import failure', async () => {
    mockOpen.mockResolvedValue('/path/to/file.csv');
    mockInvoke.mockRejectedValue(new Error('Import failed'));

    render(
      <MantineProvider>
        <DataImportForm />
      </MantineProvider>
    );

    const selectButton = screen.getByText('Select CSV File');
    await userEvent.click(selectButton);

    const importButton = screen.getByText('Import');
    await userEvent.click(importButton);

    await waitFor(() => {
      expect(screen.getByText(/Import failed/)).toBeDefined();
    });
  });

  it('should require file selection before import', async () => {
    render(
      <MantineProvider>
        <DataImportForm />
      </MantineProvider>
    );

    const importButton = screen.getByText('Import');
    // Mantine Button uses data-disabled attribute or disabled property
    expect(importButton.hasAttribute('disabled') || importButton.hasAttribute('data-disabled')).toBe(true);

    // Try to click disabled button (should not trigger invoke)
    if (!importButton.hasAttribute('disabled') && !importButton.hasAttribute('data-disabled')) {
      await userEvent.click(importButton);
    }
    expect(mockInvoke).not.toHaveBeenCalled();
  });
});

