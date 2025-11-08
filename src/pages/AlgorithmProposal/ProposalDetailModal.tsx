/**
 * Proposal Detail Modal Component
 * 
 * DEPENDENCY MAP:
 * 
 * Parents (Files that import this file):
 *   └─ src/pages/AlgorithmProposal/ProposalList.tsx
 * 
 * Dependencies (External files that this file imports):
 *   ├─ @mantine/core
 *   ├─ react-markdown (external)
 *   ├─ src/types/algorithm
 * 
 * Related Documentation:
 *   ├─ Spec: src/pages/AlgorithmProposal/AlgorithmProposal.spec.md
 *   └─ Plan: docs/03_plans/algorithm-proposal/README.md
 */
import { Modal, Stack, Text, Badge, Code, ScrollArea, Group } from '@mantine/core';
import ReactMarkdown from 'react-markdown';
import { AlgorithmProposal } from '../../types/algorithm';

interface ProposalDetailModalProps {
  proposal: AlgorithmProposal | null;
  opened: boolean;
  onClose: () => void;
}

export function ProposalDetailModal({ proposal, opened, onClose }: ProposalDetailModalProps) {
  if (!proposal) {
    return null;
  }

  const confidenceColor = proposal.confidence_score
    ? proposal.confidence_score >= 0.8
      ? 'green'
      : proposal.confidence_score >= 0.6
      ? 'yellow'
      : 'red'
    : 'gray';

  return (
    <Modal
      opened={opened}
      onClose={onClose}
      title={proposal.name}
      size="xl"
    >
      <ScrollArea h={600}>
        <Stack gap="md">
          <Group justify="space-between">
            <Text size="sm" c="dimmed">
              Proposal ID: {proposal.proposal_id}
            </Text>
            {proposal.confidence_score !== undefined && (
              <Badge color={confidenceColor} variant="light" size="lg">
                Confidence: {(proposal.confidence_score * 100).toFixed(0)}%
              </Badge>
            )}
          </Group>

          <div>
            <Text fw={500} size="sm" mb="xs">
              Description
            </Text>
            <ReactMarkdown>{proposal.description}</ReactMarkdown>
          </div>

          <div>
            <Text fw={500} size="sm" mb="xs">
              Rationale
            </Text>
            <ReactMarkdown>{proposal.rationale}</ReactMarkdown>
          </div>

          {proposal.expected_performance && (
            <div>
              <Text fw={500} size="sm" mb="xs">
                Expected Performance
              </Text>
              <Stack gap="xs">
                {proposal.expected_performance.expected_return !== undefined && (
                  <Text size="sm">
                    Expected Return: {proposal.expected_performance.expected_return.toFixed(2)}%
                  </Text>
                )}
                {proposal.expected_performance.risk_level && (
                  <Group gap="xs">
                    <Text size="sm">Risk Level:</Text>
                    <Badge size="sm">{proposal.expected_performance.risk_level}</Badge>
                  </Group>
                )}
              </Stack>
            </div>
          )}

          <div>
            <Text fw={500} size="sm" mb="xs">
              Algorithm Definition
            </Text>
            <Code block>
              {JSON.stringify(proposal.definition, null, 2)}
            </Code>
          </div>
        </Stack>
      </ScrollArea>
    </Modal>
  );
}

