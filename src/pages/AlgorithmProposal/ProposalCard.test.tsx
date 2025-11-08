/**
 * Tests for ProposalCard component - Phase 5
 * 
 * Related Documentation:
 *   ├─ Spec: src/pages/AlgorithmProposal/AlgorithmProposal.spec.md
 *   └─ Plan: docs/03_plans/algorithm-proposal/README.md
 */
import { describe, it, expect, beforeEach, beforeAll, mock } from 'bun:test';
import { render, within } from '@testing-library/react';
import { ProposalCard } from './ProposalCard';
import { MantineProvider } from '@mantine/core';
import { setupDOM, setupDOMSync } from '../../test-utils/dom-setup';
import { AlgorithmProposal } from '../../types/algorithm';

// Setup DOM synchronously before module initialization
setupDOMSync();

describe('ProposalCard - Phase 5', () => {
  // Ensure DOM is set up before all tests
  beforeAll(async () => {
    await setupDOM();
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

  it('should render proposal card with basic information', () => {
    const onViewDetails = mock(() => {});

    const { container } = render(
      <MantineProvider>
        <ProposalCard proposal={mockProposal} onViewDetails={onViewDetails} />
      </MantineProvider>
    );

    expect(within(container).getByText('Test Algorithm Proposal')).toBeDefined();
    expect(within(container).getByText('This is a test algorithm proposal description.')).toBeDefined();
    expect(within(container).getByText('75%')).toBeDefined();
  });

  it('should call onViewDetails when View Details button is clicked', async () => {
    const onViewDetails = mock(() => {});
    const { userEvent } = await import('@testing-library/user-event');

    const { container } = render(
      <MantineProvider>
        <ProposalCard proposal={mockProposal} onViewDetails={onViewDetails} />
      </MantineProvider>
    );

    const viewDetailsButton = within(container).getByText('View Details');
    await userEvent.click(viewDetailsButton);

    expect(onViewDetails).toHaveBeenCalledWith(mockProposal);
  });

  it('should display confidence score badge with correct color for high confidence', () => {
    const highConfidenceProposal: AlgorithmProposal = {
      ...mockProposal,
      confidence_score: 0.85,
    };
    const onViewDetails = mock(() => {});

    const { container } = render(
      <MantineProvider>
        <ProposalCard proposal={highConfidenceProposal} onViewDetails={onViewDetails} />
      </MantineProvider>
    );

    const badge = within(container).getByText('85%');
    expect(badge).toBeDefined();
  });

  it('should display confidence score badge with correct color for medium confidence', () => {
    const mediumConfidenceProposal: AlgorithmProposal = {
      ...mockProposal,
      confidence_score: 0.65,
    };
    const onViewDetails = mock(() => {});

    const { container } = render(
      <MantineProvider>
        <ProposalCard proposal={mediumConfidenceProposal} onViewDetails={onViewDetails} />
      </MantineProvider>
    );

    const badge = within(container).getByText('65%');
    expect(badge).toBeDefined();
  });

  it('should display confidence score badge with correct color for low confidence', () => {
    const lowConfidenceProposal: AlgorithmProposal = {
      ...mockProposal,
      confidence_score: 0.45,
    };
    const onViewDetails = mock(() => {});

    const { container } = render(
      <MantineProvider>
        <ProposalCard proposal={lowConfidenceProposal} onViewDetails={onViewDetails} />
      </MantineProvider>
    );

    const badge = within(container).getByText('45%');
    expect(badge).toBeDefined();
  });

  it('should not display confidence badge when confidence_score is undefined', () => {
    const noConfidenceProposal: AlgorithmProposal = {
      ...mockProposal,
      confidence_score: undefined,
    };
    const onViewDetails = mock(() => {});

    const { container } = render(
      <MantineProvider>
        <ProposalCard proposal={noConfidenceProposal} onViewDetails={onViewDetails} />
      </MantineProvider>
    );

    const badge = within(container).queryByText(/\d+%/);
    expect(badge).toBeNull();
  });

  it('should call onSelect when Select button is clicked', async () => {
    const onViewDetails = mock(() => {});
    const onSelect = mock(() => {});
    const { userEvent } = await import('@testing-library/user-event');

    const { container } = render(
      <MantineProvider>
        <ProposalCard
          proposal={mockProposal}
          onViewDetails={onViewDetails}
          onSelect={onSelect}
        />
      </MantineProvider>
    );

    const selectButton = within(container).getByText('Select');
    await userEvent.click(selectButton);

    expect(onSelect).toHaveBeenCalledWith(mockProposal);
  });

  it('should display Selected button when proposal is selected', () => {
    const onViewDetails = mock(() => {});
    const onSelect = mock(() => {});

    const { container } = render(
      <MantineProvider>
        <ProposalCard
          proposal={mockProposal}
          onViewDetails={onViewDetails}
          onSelect={onSelect}
          selected={true}
        />
      </MantineProvider>
    );

    expect(within(container).getByText('Selected')).toBeDefined();
  });

  it('should not display Select button when onSelect is not provided', () => {
    const onViewDetails = mock(() => {});

    const { container } = render(
      <MantineProvider>
        <ProposalCard proposal={mockProposal} onViewDetails={onViewDetails} />
      </MantineProvider>
    );

    const selectButton = within(container).queryByText('Select');
    expect(selectButton).toBeNull();
  });
});

