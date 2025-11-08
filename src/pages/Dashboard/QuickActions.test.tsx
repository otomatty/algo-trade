/**
 * Tests for QuickActions component
 * 
 * Related Documentation:
 *   ├─ Spec: src/pages/Dashboard/Dashboard.spec.md
 *   └─ Plan: docs/03_plans/dashboard/README.md
 */
import { describe, it, expect, beforeEach, beforeAll, mock } from 'bun:test';
import { render, within, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { QuickActions } from './QuickActions';
import { MantineProvider } from '@mantine/core';
import { ModalsProvider } from '@mantine/modals';
import { setupDOM, setupDOMSync } from '../../test-utils/dom-setup';

// Setup DOM synchronously before module initialization
setupDOMSync();

// Mock Zustand store
const mockDeleteAlgorithm = mock(async (_algorithmId: number) => {
  // Mock handler
});

mock.module('../../stores/dashboard', () => ({
  useDashboardStore: () => ({
    deleteAlgorithm: mockDeleteAlgorithm,
  }),
}));

describe('QuickActions', () => {
  beforeAll(async () => {
    await setupDOM();
  });

  beforeEach(() => {
    mockDeleteAlgorithm.mockClear();
  });

  it('should render quick actions', () => {
    const mockNavigate = mock((page: string) => {
      // Mock handler
    });

    const { container } = render(
      <MantineProvider>
        <ModalsProvider>
          <QuickActions onNavigate={mockNavigate} />
        </ModalsProvider>
      </MantineProvider>
    );

    expect(within(container).getByText('アルゴリズム提案')).toBeDefined();
  });

  it('should call onNavigate when proposal button is clicked', async () => {
    const mockNavigate = mock((page: string) => {
      // Mock handler
    });

    const { container } = render(
      <MantineProvider>
        <ModalsProvider>
          <QuickActions onNavigate={mockNavigate} />
        </ModalsProvider>
      </MantineProvider>
    );

    const proposalButton = within(container).getByText('アルゴリズム提案');
    await userEvent.click(proposalButton);

    await waitFor(() => {
      expect(mockNavigate).toHaveBeenCalledWith('algorithm-proposal');
    });
  });
});

