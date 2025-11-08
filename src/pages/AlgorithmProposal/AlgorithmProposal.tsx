/**
 * Algorithm Proposal Page
 * 
 * DEPENDENCY MAP:
 * 
 * Parents (Files that import this file):
 *   └─ src/App.tsx (via routing, to be implemented)
 * 
 * Dependencies (External files that this file imports):
 *   ├─ @tauri-apps/api/core
 *   ├─ @mantine/core
 *   ├─ ./ProposalGenerationForm
 *   ├─ ./ProposalList
 *   └─ ./ProgressIndicator
 * 
 * Related Documentation:
 *   ├─ Spec: src/pages/AlgorithmProposal/AlgorithmProposal.spec.md
 *   ├─ Tests: src/pages/AlgorithmProposal/AlgorithmProposal.test.tsx
 *   └─ Plan: docs/03_plans/algorithm-proposal/README.md
 */
import { useState } from 'react';
import {
  Container,
  Title,
  Stack,
} from '@mantine/core';
import { ProposalGenerationForm } from './ProposalGenerationForm';
import { ProposalList } from './ProposalList';
import { ProgressIndicator } from './ProgressIndicator';

export function AlgorithmProposal() {
  const [jobId, setJobId] = useState<string | null>(null);
  const [showResults, setShowResults] = useState(false);

  const handleJobStarted = (newJobId: string) => {
    setJobId(newJobId);
    setShowResults(false);
  };

  const handleJobCompleted = () => {
    setShowResults(true);
  };

  return (
    <Container size="xl" py="md">
      <Stack gap="md">
        <Title order={2}>Algorithm Proposal</Title>

        <ProposalGenerationForm onJobStarted={handleJobStarted} />

        {jobId && (
          <ProgressIndicator jobId={jobId} onCompleted={handleJobCompleted} />
        )}

        <ProposalList proposals={[]} />
      </Stack>
    </Container>
  );
}

