/**
 * Algorithm Proposal Page
 * 
 * DEPENDENCY MAP:
 * 
 * Parents (Files that import this file):
 *   └─ src/App.tsx (via routing)
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
import { invoke } from '@tauri-apps/api/core';
import {
  Container,
  Title,
  Stack,
  Alert,
  Loader,
  Center,
} from '@mantine/core';
import { ProposalGenerationForm } from './ProposalGenerationForm';
import { ProposalList } from './ProposalList';
import { ProgressIndicator } from './ProgressIndicator';
import { AlgorithmProposal as AlgorithmProposalType } from '../../types/algorithm';

interface AlgorithmProposalProps {
  currentPage?: string;
  onNavigate?: (page: string) => void;
}

export function AlgorithmProposal({ currentPage: _currentPage, onNavigate: _onNavigate }: AlgorithmProposalProps) {
  const [jobId, setJobId] = useState<string | null>(null);
  const [showResults, setShowResults] = useState(false);
  const [proposals, setProposals] = useState<AlgorithmProposalType[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleJobStarted = (newJobId: string) => {
    setJobId(newJobId);
    setShowResults(false);
    setProposals([]);
    setError(null);
  };

  const handleJobCompleted = async () => {
    setShowResults(true);
    if (jobId) {
      await loadProposals(jobId);
    }
  };

  const loadProposals = async (proposalJobId: string) => {
    setLoading(true);
    setError(null);
    try {
      const response = await invoke<{ proposals: AlgorithmProposalType[] }>('get_algorithm_proposals', {
        job_id: proposalJobId,
      });
      setProposals(response.proposals || []);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load proposals');
      setProposals([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container size="xl" py="md">
      <Stack gap="md">
        <Title order={2}>Algorithm Proposal</Title>

        {error && (
          <Alert color="red" title="Error">
            {error}
          </Alert>
        )}

        <ProposalGenerationForm onJobStarted={handleJobStarted} />

        {loading && (
          <Center py="xl">
            <Loader />
          </Center>
        )}

        {jobId && !loading && (
          <ProgressIndicator jobId={jobId} onCompleted={handleJobCompleted} />
        )}

        {showResults && !loading && (
          <ProposalList proposals={proposals} />
        )}

        {!showResults && !jobId && !loading && (
          <ProposalList proposals={[]} />
        )}
      </Stack>
    </Container>
  );
}

