/**
 * Tests for ProposalList component - Phase 5
 * 
 * Related Documentation:
 *   ├─ Spec: src/pages/AlgorithmProposal/AlgorithmProposal.spec.md
 *   └─ Plan: docs/03_plans/algorithm-proposal/README.md
 */
import { describe, it, expect, beforeEach, beforeAll, mock } from 'bun:test';
import { render, within } from '@testing-library/react';
import { ProposalList } from './ProposalList';
import { MantineProvider } from '@mantine/core';
import { setupDOM, setupDOMSync } from '../../test-utils/dom-setup';
import { AlgorithmProposal } from '../../types/algorithm';

// Setup DOM synchronously before module initialization
setupDOMSync();

describe('ProposalList - Phase 5', () => {
  // Ensure DOM is set up before all tests
  beforeAll(async () => {
    await setupDOM();
  });

  const mockProposals: AlgorithmProposal[] = [
    {
      proposal_id: 'prop-123',
      name: 'Test Algorithm Proposal 1',
      description: 'This is a test algorithm proposal description 1.',
      rationale: 'This algorithm is based on RSI indicators.',
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
    },
    {
      proposal_id: 'prop-456',
      name: 'Test Algorithm Proposal 2',
      description: 'This is a test algorithm proposal description 2.',
      rationale: 'This algorithm is based on MACD indicators.',
      expected_performance: {
        expected_return: 0.20,
        risk_level: 'high',
      },
      definition: {
        triggers: [
          {
            type: 'macd',
            condition: {
              operator: 'cross_above',
              value: 0,
            },
          },
        ],
        actions: [
          {
            type: 'buy',
            parameters: {
              percentage: 15,
            },
          },
        ],
      },
      confidence_score: 0.85,
      created_at: '2023-01-02T00:00:00',
    },
  ];

  it('should display empty state when no proposals are provided', () => {
    const { container } = render(
      <MantineProvider>
        <ProposalList proposals={[]} />
      </MantineProvider>
    );

    expect(within(container).getByText('提案が生成されると、ここに表示されます')).toBeDefined();
    expect(within(container).getByText('Proposals will be displayed here once generated')).toBeDefined();
  });

  it('should render proposal cards when proposals are provided', () => {
    const onViewDetails = mock(() => {});

    const { container } = render(
      <MantineProvider>
        <ProposalList proposals={mockProposals} />
      </MantineProvider>
    );

    expect(within(container).getByText('Test Algorithm Proposal 1')).toBeDefined();
    expect(within(container).getByText('Test Algorithm Proposal 2')).toBeDefined();
  });

  it('should display all proposal information for each proposal', () => {
    const onViewDetails = mock(() => {});

    const { container } = render(
      <MantineProvider>
        <ProposalList proposals={mockProposals} />
      </MantineProvider>
    );

    expect(within(container).getByText('This is a test algorithm proposal description 1.')).toBeDefined();
    expect(within(container).getByText('This is a test algorithm proposal description 2.')).toBeDefined();
  });

  it('should display confidence scores for proposals', () => {
    const onViewDetails = mock(() => {});

    const { container } = render(
      <MantineProvider>
        <ProposalList proposals={mockProposals} />
      </MantineProvider>
    );

    expect(within(container).getByText('75%')).toBeDefined();
    expect(within(container).getByText('85%')).toBeDefined();
  });
});

