/**
 * Proposal List Component
 * 
 * DEPENDENCY MAP:
 * 
 * Parents (Files that import this file):
 *   └─ src/pages/AlgorithmProposal/AlgorithmProposal.tsx
 * 
 * Dependencies (External files that this file imports):
 *   ├─ @mantine/core
 *   └─ src/types/algorithm
 * 
 * Related Documentation:
 *   ├─ Spec: src/pages/AlgorithmProposal/AlgorithmProposal.spec.md
 *   └─ Plan: docs/03_plans/algorithm-proposal/README.md
 */
import { Paper, Text, Stack } from '@mantine/core';
import { AlgorithmProposal as AlgorithmProposalType } from '../../types/algorithm';

interface ProposalListProps {
  proposals: AlgorithmProposalType[];
}

export function ProposalList({ proposals }: ProposalListProps) {
  if (proposals.length === 0) {
    return (
      <Paper p="md" withBorder>
        <Stack gap="sm" align="center">
          <Text c="dimmed" size="sm">
            提案が生成されると、ここに表示されます
          </Text>
          <Text c="dimmed" size="xs">
            Proposals will be displayed here once generated
          </Text>
        </Stack>
      </Paper>
    );
  }

  // Phase 5で実装予定: 提案カードの表示
  return (
    <Paper p="md" withBorder>
      <Stack gap="md">
        <Text fw={500}>Algorithm Proposals</Text>
        {/* Phase 5で実装予定 */}
      </Stack>
    </Paper>
  );
}

