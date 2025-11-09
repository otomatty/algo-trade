/**
 * Tests for ActionProposal component - Phase 7
 * 
 * Related Documentation:
 *   └─ Plan: docs/03_plans/stock-prediction/README.md
 */
import { describe, it, expect, beforeEach, beforeAll, mock } from 'bun:test';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { ActionProposal } from './ActionProposal';
import { MantineProvider } from '@mantine/core';
import { setupDOM, setupDOMSync } from '../../test-utils/dom-setup';
import { notifications } from '@mantine/notifications';

// Setup DOM synchronously before module initialization
setupDOMSync();

// Mock Tauri invoke
const mockInvoke = mock(() => Promise.resolve({
  action_id: 1,
  prediction_id: 'test-prediction-123',
  action: 'buy'
}));

// Mock notifications
mock.module('@mantine/notifications', () => ({
  notifications: {
    show: mock(() => {}),
  },
}));

describe('ActionProposal - Phase 7', () => {
  beforeAll(async () => {
    await setupDOM();
  });

  beforeEach(() => {
    mockInvoke.mockClear();
  });

  it('should render action selection UI', () => {
    render(
      <MantineProvider>
        <ActionProposal predictionId="test-prediction-123" />
      </MantineProvider>
    );

    expect(screen.getByText('Select Your Action')).toBeInTheDocument();
    expect(screen.getByLabelText('Buy')).toBeInTheDocument();
    expect(screen.getByLabelText('Sell')).toBeInTheDocument();
    expect(screen.getByLabelText('Hold')).toBeInTheDocument();
    expect(screen.getByLabelText('Watch')).toBeInTheDocument();
    expect(screen.getByLabelText('Ignore')).toBeInTheDocument();
  });

  it('should show suggested action when provided', () => {
    render(
      <MantineProvider>
        <ActionProposal predictionId="test-prediction-123" suggestedAction="buy" />
      </MantineProvider>
    );

    expect(screen.getByText(/Suggested: Buy/i)).toBeInTheDocument();
  });

  it('should allow selecting different actions', async () => {
    const user = userEvent.setup();
    render(
      <MantineProvider>
        <ActionProposal predictionId="test-prediction-123" />
      </MantineProvider>
    );

    const sellRadio = screen.getByLabelText('Sell');
    await user.click(sellRadio);

    expect(sellRadio).toBeChecked();
  });

  it('should allow entering notes', async () => {
    const user = userEvent.setup();
    render(
      <MantineProvider>
        <ActionProposal predictionId="test-prediction-123" />
      </MantineProvider>
    );

    const notesTextarea = screen.getByPlaceholderText(/Add any notes/i);
    await user.type(notesTextarea, 'Test notes');

    expect(notesTextarea).toHaveValue('Test notes');
  });

  it('should save action when save button is clicked', async () => {
    const user = userEvent.setup();
    const mockOnActionSaved = mock(() => {});

    // Mock Tauri invoke
    const { invoke } = await import('@tauri-apps/api/core');
    mock.module('@tauri-apps/api/core', () => ({
      invoke: mockInvoke,
    }));

    render(
      <MantineProvider>
        <ActionProposal 
          predictionId="test-prediction-123" 
          onActionSaved={mockOnActionSaved}
        />
      </MantineProvider>
    );

    const saveButton = screen.getByText('Save Action');
    await user.click(saveButton);

    await waitFor(() => {
      expect(mockInvoke).toHaveBeenCalledWith('save_prediction_action', {
        prediction_id: 'test-prediction-123',
        action: 'watch', // Default action
        notes: undefined,
      });
    });
  });

  it('should save action with notes when provided', async () => {
    const user = userEvent.setup();

    render(
      <MantineProvider>
        <ActionProposal predictionId="test-prediction-123" />
      </MantineProvider>
    );

    const notesTextarea = screen.getByPlaceholderText(/Add any notes/i);
    await user.type(notesTextarea, 'My test notes');

    const buyRadio = screen.getByLabelText('Buy');
    await user.click(buyRadio);

    const saveButton = screen.getByText('Save Action');
    await user.click(saveButton);

    await waitFor(() => {
      expect(mockInvoke).toHaveBeenCalledWith('save_prediction_action', {
        prediction_id: 'test-prediction-123',
        action: 'buy',
        notes: 'My test notes',
      });
    });
  });

  it('should handle save errors gracefully', async () => {
    const user = userEvent.setup();
    const errorInvoke = mock(() => Promise.reject(new Error('Save failed')));

    mock.module('@tauri-apps/api/core', () => ({
      invoke: errorInvoke,
    }));

    render(
      <MantineProvider>
        <ActionProposal predictionId="test-prediction-123" />
      </MantineProvider>
    );

    const saveButton = screen.getByText('Save Action');
    await user.click(saveButton);

    await waitFor(() => {
      expect(errorInvoke).toHaveBeenCalled();
    });
  });

  it('should reset notes after successful save', async () => {
    const user = userEvent.setup();
    const mockOnActionSaved = mock(() => {});

    render(
      <MantineProvider>
        <ActionProposal 
          predictionId="test-prediction-123" 
          onActionSaved={mockOnActionSaved}
        />
      </MantineProvider>
    );

    const notesTextarea = screen.getByPlaceholderText(/Add any notes/i);
    await user.type(notesTextarea, 'Test notes');

    const saveButton = screen.getByText('Save Action');
    await user.click(saveButton);

    await waitFor(() => {
      expect(notesTextarea).toHaveValue('');
    });
  });
});

