/**
 * Tests for SelectAlgorithmDialog component - Phase 6
 * 
 * Related Documentation:
 *   ├─ Spec: src/pages/AlgorithmProposal/AlgorithmProposal.spec.md
 *   └─ Plan: docs/03_plans/algorithm-proposal/IMPLEMENTATION_GUIDE.md
 */
import { describe, it, expect, beforeEach, beforeAll, mock } from 'bun:test';
import { render, within, waitFor } from '@testing-library/react';
import { SelectAlgorithmDialog } from './SelectAlgorithmDialog';
import { MantineProvider } from '@mantine/core';
import { setupDOM, setupDOMSync } from '../../test-utils/dom-setup';
import { AlgorithmProposal } from '../../types/algorithm';

// Setup DOM synchronously before module initialization
setupDOMSync();

// Mock Tauri API
const mockInvoke = mock((_cmd: string, ..._args: any[]) => Promise.resolve({ algorithm_id: 1, name: 'Test Algorithm' }));

mock.module('@tauri-apps/api/core', () => ({
  invoke: mockInvoke,
}));

// Mock notifications
const mockNotificationsShow = mock(() => {});

mock.module('@mantine/notifications', () => ({
  notifications: {
    show: mockNotificationsShow,
  },
}));

describe('SelectAlgorithmDialog - Phase 6', () => {
  // Ensure DOM is set up before all tests
  beforeAll(async () => {
    await setupDOM();
  });

  beforeEach(() => {
    // Reset mocks
    mockInvoke.mockClear();
    mockNotificationsShow.mockClear();
  });

  const mockProposal: AlgorithmProposal = {
    proposal_id: 'prop-123',
    name: 'Test Algorithm Proposal',
    description: 'This is a test algorithm proposal description.',
    rationale: 'This algorithm is based on RSI and MACD indicators.',
    expected_performance: {
      expected_return: 0.15,
      risk_level: 'medium',
    },
    definition: {
      triggers: [
        {
          type: 'rsi',
          condition: {
            operator: 'lt',
            value: 30,
            period: 14,
          },
        },
      ],
      actions: [
        {
          type: 'buy',
          parameters: {
            percentage: 10,
          },
        },
      ],
    },
    confidence_score: 0.75,
    created_at: '2023-01-01T00:00:00',
  };

  it('should render dialog when opened with proposal', () => {
    const onClose = mock(() => {});

    const { baseElement } = render(
      <MantineProvider>
        <SelectAlgorithmDialog proposal={mockProposal} opened={true} onClose={onClose} />
      </MantineProvider>
    );

    expect(within(baseElement).getByText('Select Algorithm')).toBeDefined();
    expect(within(baseElement).getByText('Test Algorithm Proposal')).toBeDefined();
    expect(within(baseElement).getByText('This is a test algorithm proposal description.')).toBeDefined();
  });

  it('should not render dialog when proposal is null', () => {
    const onClose = mock(() => {});

    const { baseElement } = render(
      <MantineProvider>
        <SelectAlgorithmDialog proposal={null} opened={true} onClose={onClose} />
      </MantineProvider>
    );

    const dialogTitle = within(baseElement).queryByText('Select Algorithm');
    expect(dialogTitle).toBeNull();
  });

  it('should display confidence score badge', () => {
    const onClose = mock(() => {});

    const { baseElement } = render(
      <MantineProvider>
        <SelectAlgorithmDialog proposal={mockProposal} opened={true} onClose={onClose} />
      </MantineProvider>
    );

    expect(within(baseElement).getByText('Confidence: 75%')).toBeDefined();
  });

  it('should display custom name input field', () => {
    const onClose = mock(() => {});

    const { baseElement } = render(
      <MantineProvider>
        <SelectAlgorithmDialog proposal={mockProposal} opened={true} onClose={onClose} />
      </MantineProvider>
    );

    expect(within(baseElement).getByLabelText(/Custom Name/i)).toBeDefined();
    expect(within(baseElement).getByPlaceholderText(/Enter a custom name/i)).toBeDefined();
  });

  it('should call select_algorithm command when Select Algorithm button is clicked', async () => {
    const onClose = mock(() => {});
    const { userEvent } = await import('@testing-library/user-event');

    const { baseElement } = render(
      <MantineProvider>
        <SelectAlgorithmDialog proposal={mockProposal} opened={true} onClose={onClose} />
      </MantineProvider>
    );

    const buttons = within(baseElement).getAllByRole('button');
    const selectButton = buttons.find(btn => btn.textContent?.includes('Select Algorithm') && !(btn as HTMLButtonElement).disabled);
    expect(selectButton).toBeDefined();
    if (selectButton) {
      await userEvent.click(selectButton);
    }

    await waitFor(() => {
      expect(mockInvoke).toHaveBeenCalledWith('select_algorithm', {
        proposal_id: 'prop-123',
        custom_name: undefined,
      });
    });
  });

  it('should call select_algorithm with custom name when provided', async () => {
    const onClose = mock(() => {});
    const { userEvent } = await import('@testing-library/user-event');

    const { baseElement } = render(
      <MantineProvider>
        <SelectAlgorithmDialog proposal={mockProposal} opened={true} onClose={onClose} />
      </MantineProvider>
    );

    const customNameInput = within(baseElement).getByLabelText(/Custom Name/i);
    await userEvent.type(customNameInput, 'My Custom Algorithm');

    const buttons = within(baseElement).getAllByRole('button');
    const selectButton = buttons.find(btn => btn.textContent?.includes('Select Algorithm') && !(btn as HTMLButtonElement).disabled);
    expect(selectButton).toBeDefined();
    if (selectButton) {
      await userEvent.click(selectButton);
    }

    await waitFor(() => {
      expect(mockInvoke).toHaveBeenCalledWith('select_algorithm', {
        proposal_id: 'prop-123',
        custom_name: 'My Custom Algorithm',
      });
    });
  });

  it('should show success notification on successful selection', async () => {
    const onClose = mock(() => {});
    const { userEvent } = await import('@testing-library/user-event');

    const { baseElement } = render(
      <MantineProvider>
        <SelectAlgorithmDialog proposal={mockProposal} opened={true} onClose={onClose} />
      </MantineProvider>
    );

    const buttons = within(baseElement).getAllByRole('button');
    const selectButton = buttons.find(btn => btn.textContent?.includes('Select Algorithm') && !(btn as HTMLButtonElement).disabled);
    expect(selectButton).toBeDefined();
    if (selectButton) {
      await userEvent.click(selectButton);
    }

    await waitFor(() => {
      expect(mockNotificationsShow).toHaveBeenCalledWith(
        expect.objectContaining({
          title: 'Algorithm Selected',
          color: 'green',
        })
      );
    });
  });

  it('should show error notification on failed selection', async () => {
    const onClose = mock(() => {});
    mockInvoke.mockRejectedValueOnce(new Error('Failed to select algorithm'));
    const { userEvent } = await import('@testing-library/user-event');

    const { baseElement } = render(
      <MantineProvider>
        <SelectAlgorithmDialog proposal={mockProposal} opened={true} onClose={onClose} />
      </MantineProvider>
    );

    const buttons = within(baseElement).getAllByRole('button');
    const selectButton = buttons.find(btn => btn.textContent?.includes('Select Algorithm') && !(btn as HTMLButtonElement).disabled);
    expect(selectButton).toBeDefined();
    if (selectButton) {
      await userEvent.click(selectButton);
    }

    await waitFor(() => {
      expect(mockNotificationsShow).toHaveBeenCalledWith(
        expect.objectContaining({
          title: 'Selection Failed',
          color: 'red',
        })
      );
    });
  });

  it('should call onClose when Cancel button is clicked', async () => {
    const onClose = mock(() => {});
    const { userEvent } = await import('@testing-library/user-event');

    const { baseElement } = render(
      <MantineProvider>
        <SelectAlgorithmDialog proposal={mockProposal} opened={true} onClose={onClose} />
      </MantineProvider>
    );

    const cancelButton = within(baseElement).getByText('Cancel');
    await userEvent.click(cancelButton);

    expect(onClose).toHaveBeenCalled();
  });

  it('should reset custom name when dialog is closed', async () => {
    const onClose = mock(() => {});
    const { userEvent } = await import('@testing-library/user-event');

    const { baseElement, rerender } = render(
      <MantineProvider>
        <SelectAlgorithmDialog proposal={mockProposal} opened={true} onClose={onClose} />
      </MantineProvider>
    );

    const customNameInput = within(baseElement).getByLabelText(/Custom Name/i) as HTMLInputElement;
    await userEvent.type(customNameInput, 'Test Name');

    expect(customNameInput.value).toBe('Test Name');

    // Close and reopen dialog
    await userEvent.click(within(baseElement).getByText('Cancel'));

    rerender(
      <MantineProvider>
        <SelectAlgorithmDialog proposal={mockProposal} opened={true} onClose={onClose} />
      </MantineProvider>
    );

    const newCustomNameInput = within(baseElement).getByLabelText(/Custom Name/i) as HTMLInputElement;
    expect(newCustomNameInput.value).toBe('');
  });

  it('should call onSuccess callback when selection succeeds', async () => {
    const onClose = mock(() => {});
    const onSuccess = mock(() => {});
    const { userEvent } = await import('@testing-library/user-event');

    const { baseElement } = render(
      <MantineProvider>
        <SelectAlgorithmDialog proposal={mockProposal} opened={true} onClose={onClose} onSuccess={onSuccess} />
      </MantineProvider>
    );

    const buttons = within(baseElement).getAllByRole('button');
    const selectButton = buttons.find(btn => btn.textContent?.includes('Select Algorithm') && !(btn as HTMLButtonElement).disabled);
    expect(selectButton).toBeDefined();
    if (selectButton) {
      await userEvent.click(selectButton);
    }

    await waitFor(() => {
      expect(onSuccess).toHaveBeenCalled();
    });
  });
});

