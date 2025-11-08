/**
 * Proposal Card Component
 * 
 * DEPENDENCY MAP:
 * 
 * Parents (Files that import this file):
 *   └─ src/pages/AlgorithmProposal/ProposalList.tsx
 * 
 * Dependencies (External files that this file imports):
 *   ├─ @mantine/core
 *   ├─ src/types/algorithm
 * 
 * Related Documentation:
 *   ├─ Spec: src/pages/AlgorithmProposal/AlgorithmProposal.spec.md
 *   └─ Plan: docs/03_plans/algorithm-proposal/README.md
 */
import {
  Card,
  Text,
  Badge,
  Button,
  Stack,
  Group,
} from '@mantine/core';
import { AlgorithmProposal } from '../../types/algorithm';

interface ProposalCardProps {
  proposal: AlgorithmProposal;
  onViewDetails: (proposal: AlgorithmProposal) => void;
  onSelect?: (proposal: AlgorithmProposal) => void;
  selected?: boolean;
}

export function ProposalCard({ proposal, onViewDetails, onSelect, selected }: ProposalCardProps) {
  const confidenceColor = proposal.confidence_score
    ? proposal.confidence_score >= 0.8
      ? 'green'
      : proposal.confidence_score >= 0.6
      ? 'yellow'
      : 'red'
    : 'gray';

  return (
    <Card shadow="sm" padding="lg" radius="md" withBorder>
      <Stack gap="sm">
        <Group justify="space-between" align="flex-start">
          <div>
            <Text fw={500} size="lg">
              {proposal.name}
            </Text>
            <Text size="sm" c="dimmed" lineClamp={2}>
              {proposal.description}
            </Text>
          </div>
          {proposal.confidence_score !== undefined && (
            <Badge color={confidenceColor} variant="light">
              {(proposal.confidence_score * 100).toFixed(0)}%
            </Badge>
          )}
        </Group>

        <Group gap="xs">
          <Button
            variant="light"
            size="xs"
            onClick={() => onViewDetails(proposal)}
          >
            View Details
          </Button>
          {onSelect && (
            <Button
              variant={selected ? 'filled' : 'outline'}
              size="xs"
              onClick={() => onSelect(proposal)}
            >
              {selected ? 'Selected' : 'Select'}
            </Button>
          )}
        </Group>
      </Stack>
    </Card>
  );
}

