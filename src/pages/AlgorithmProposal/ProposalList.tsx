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
 *   ├─ src/types/algorithm
 *   ├─ ./ProposalCard
 *   ├─ ./ProposalDetailModal
 *   └─ ./SelectAlgorithmDialog
 * 
 * Related Documentation:
 *   ├─ Spec: src/pages/AlgorithmProposal/AlgorithmProposal.spec.md
 *   └─ Plan: docs/03_plans/algorithm-proposal/README.md
 */
import { useState } from 'react';
import { Paper, Text, Stack, Grid } from '@mantine/core';
import { AlgorithmProposal as AlgorithmProposalType } from '../../types/algorithm';
import { ProposalCard } from './ProposalCard';
import { ProposalDetailModal } from './ProposalDetailModal';
import { SelectAlgorithmDialog } from './SelectAlgorithmDialog';

interface ProposalListProps {
  proposals: AlgorithmProposalType[];
}

export function ProposalList({ proposals }: ProposalListProps) {
  const [selectedProposal, setSelectedProposal] = useState<AlgorithmProposalType | null>(null);
  const [modalOpened, setModalOpened] = useState(false);
  const [selectProposal, setSelectProposal] = useState<AlgorithmProposalType | null>(null);
  const [selectDialogOpened, setSelectDialogOpened] = useState(false);

  const handleViewDetails = (proposal: AlgorithmProposalType) => {
    setSelectedProposal(proposal);
    setModalOpened(true);
  };

  const handleCloseModal = () => {
    setModalOpened(false);
    setSelectedProposal(null);
  };

  const handleSelect = (proposal: AlgorithmProposalType) => {
    setSelectProposal(proposal);
    setSelectDialogOpened(true);
  };

  const handleCloseSelectDialog = () => {
    setSelectDialogOpened(false);
    setSelectProposal(null);
  };

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

  return (
    <>
      <Paper p="md" withBorder>
        <Stack gap="md">
          <Text fw={500} size="lg">
            Algorithm Proposals
          </Text>
          <Grid>
            {proposals.map((proposal) => (
              <Grid.Col key={proposal.proposal_id} span={{ base: 12, sm: 6, md: 4 }}>
                <ProposalCard
                  proposal={proposal}
                  onViewDetails={handleViewDetails}
                  onSelect={handleSelect}
                />
              </Grid.Col>
            ))}
          </Grid>
        </Stack>
      </Paper>
      <ProposalDetailModal
        proposal={selectedProposal}
        opened={modalOpened}
        onClose={handleCloseModal}
      />
      <SelectAlgorithmDialog
        proposal={selectProposal}
        opened={selectDialogOpened}
        onClose={handleCloseSelectDialog}
      />
    </>
  );
}

