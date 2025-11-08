/**
 * Tests for ProposalDetailModal component - Phase 5
 * 
 * Related Documentation:
 *   ├─ Spec: src/pages/AlgorithmProposal/AlgorithmProposal.spec.md
 *   └─ Plan: docs/03_plans/algorithm-proposal/README.md
 */
import { describe, it, expect, beforeEach, beforeAll, mock } from 'bun:test';
import { render, within } from '@testing-library/react';
import { ProposalDetailModal } from './ProposalDetailModal';
import { MantineProvider } from '@mantine/core';
import { setupDOM, setupDOMSync } from '../../test-utils/dom-setup';
import { AlgorithmProposal } from '../../types/algorithm';

// Setup DOM synchronously before module initialization
setupDOMSync();

// Mock react-markdown
mock.module('react-markdown', () => ({
  default: ({ children }: { children: string }) => <div>{children}</div>,
}));

describe('ProposalDetailModal - Phase 5', () => {
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

  it('should render modal when opened with proposal', () => {
    const onClose = mock(() => {});

    const { baseElement } = render(
      <MantineProvider>
        <ProposalDetailModal proposal={mockProposal} opened={true} onClose={onClose} />
      </MantineProvider>
    );

    expect(within(baseElement).getByText('Test Algorithm Proposal')).toBeDefined();
    expect(within(baseElement).getByText(/Proposal ID: prop-123/)).toBeDefined();
    expect(within(baseElement).getByText('This is a test algorithm proposal description.')).toBeDefined();
    expect(within(baseElement).getByText('This algorithm is based on RSI and MACD indicators.')).toBeDefined();
  });

  it('should not render modal when proposal is null', () => {
    const onClose = mock(() => {});

    const { baseElement } = render(
      <MantineProvider>
        <ProposalDetailModal proposal={null} opened={true} onClose={onClose} />
      </MantineProvider>
    );

    const modalTitle = within(baseElement).queryByText('Test Algorithm Proposal');
    expect(modalTitle).toBeNull();
  });

  it('should display confidence score badge with correct percentage', () => {
    const onClose = mock(() => {});

    const { baseElement } = render(
      <MantineProvider>
        <ProposalDetailModal proposal={mockProposal} opened={true} onClose={onClose} />
      </MantineProvider>
    );

    expect(within(baseElement).getByText('Confidence: 75%')).toBeDefined();
  });

  it('should display expected performance when available', () => {
    const onClose = mock(() => {});

    const { baseElement } = render(
      <MantineProvider>
        <ProposalDetailModal proposal={mockProposal} opened={true} onClose={onClose} />
      </MantineProvider>
    );

    expect(within(baseElement).getByText('Expected Performance')).toBeDefined();
    expect(within(baseElement).getByText(/Expected Return: 0\.15%/)).toBeDefined();
    expect(within(baseElement).getByText('medium')).toBeDefined();
  });

  it('should display algorithm definition as JSON', () => {
    const onClose = mock(() => {});

    const { baseElement } = render(
      <MantineProvider>
        <ProposalDetailModal proposal={mockProposal} opened={true} onClose={onClose} />
      </MantineProvider>
    );

    expect(within(baseElement).getByText('Algorithm Definition')).toBeDefined();
    const codeBlock = within(baseElement).getByText(/triggers/);
    expect(codeBlock).toBeDefined();
  });

  it('should not display expected performance section when not available', () => {
    const proposalWithoutPerformance: AlgorithmProposal = {
      ...mockProposal,
      expected_performance: undefined,
    };
    const onClose = mock(() => {});

    const { baseElement } = render(
      <MantineProvider>
        <ProposalDetailModal proposal={proposalWithoutPerformance} opened={true} onClose={onClose} />
      </MantineProvider>
    );

    const expectedPerformanceSection = within(baseElement).queryByText('Expected Performance');
    expect(expectedPerformanceSection).toBeNull();
  });

  it('should display confidence badge with correct color for high confidence', () => {
    const highConfidenceProposal: AlgorithmProposal = {
      ...mockProposal,
      confidence_score: 0.85,
    };
    const onClose = mock(() => {});

    const { baseElement } = render(
      <MantineProvider>
        <ProposalDetailModal proposal={highConfidenceProposal} opened={true} onClose={onClose} />
      </MantineProvider>
    );

    expect(within(baseElement).getByText('Confidence: 85%')).toBeDefined();
  });

  it('should display confidence badge with correct color for medium confidence', () => {
    const mediumConfidenceProposal: AlgorithmProposal = {
      ...mockProposal,
      confidence_score: 0.65,
    };
    const onClose = mock(() => {});

    const { baseElement } = render(
      <MantineProvider>
        <ProposalDetailModal proposal={mediumConfidenceProposal} opened={true} onClose={onClose} />
      </MantineProvider>
    );

    expect(within(baseElement).getByText('Confidence: 65%')).toBeDefined();
  });

  it('should display confidence badge with correct color for low confidence', () => {
    const lowConfidenceProposal: AlgorithmProposal = {
      ...mockProposal,
      confidence_score: 0.45,
    };
    const onClose = mock(() => {});

    const { baseElement } = render(
      <MantineProvider>
        <ProposalDetailModal proposal={lowConfidenceProposal} opened={true} onClose={onClose} />
      </MantineProvider>
    );

    expect(within(baseElement).getByText('Confidence: 45%')).toBeDefined();
  });

  it('should not display confidence badge when confidence_score is undefined', () => {
    const noConfidenceProposal: AlgorithmProposal = {
      ...mockProposal,
      confidence_score: undefined,
    };
    const onClose = mock(() => {});

    const { baseElement } = render(
      <MantineProvider>
        <ProposalDetailModal proposal={noConfidenceProposal} opened={true} onClose={onClose} />
      </MantineProvider>
    );

    const confidenceBadge = within(baseElement).queryByText(/Confidence:/);
    expect(confidenceBadge).toBeNull();
  });
});

