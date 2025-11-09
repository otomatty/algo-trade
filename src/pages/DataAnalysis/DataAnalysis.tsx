/**
 * Data Analysis Page
 * 
 * DEPENDENCY MAP:
 * 
 * Parents (Files that import this file):
 *   └─ src/App.tsx (via routing)
 * 
 * Dependencies (External files that this file imports):
 *   ├─ @tauri-apps/api/core
 *   ├─ @mantine/core
 *   └─ ./AnalysisJobForm
 * 
 * Related Documentation:
 *   ├─ Spec: src/pages/DataAnalysis/DataAnalysis.spec.md
 *   ├─ Tests: src/pages/DataAnalysis/DataAnalysis.test.tsx
 *   └─ Plan: docs/03_plans/data-analysis/README.md
 */
import { useState } from 'react';
import {
  Container,
  Title,
  Stack,
} from '@mantine/core';
import { AnalysisJobForm } from './AnalysisJobForm';
import { AnalysisProgress } from './AnalysisProgress';
import { AnalysisResults } from './AnalysisResults';

interface DataAnalysisProps {
  currentPage?: string;
  onNavigate?: (page: string) => void;
}

export function DataAnalysis({ currentPage, onNavigate }: DataAnalysisProps) {
  const [jobId, setJobId] = useState<string | null>(null);
  const [showResults, setShowResults] = useState(false);

  const handleJobStarted = (newJobId: string) => {
    setJobId(newJobId);
    setShowResults(false);
  };

  const handleJobCompleted = () => {
    setShowResults(true);
  };

  const handleNavigateToProposal = (analysisJobId: string) => {
    // Navigate to algorithm proposal page
    if (onNavigate) {
      onNavigate('algorithm-proposal');
    }
    console.log('Navigate to algorithm proposal with job ID:', analysisJobId);
  };

  return (
    <Container size="xl" py="md">
      <Stack gap="md">
        <Title order={2}>Data Analysis</Title>

        <AnalysisJobForm onJobStarted={handleJobStarted} />

        {jobId && (
          <AnalysisProgress jobId={jobId} onCompleted={handleJobCompleted} />
        )}

        {showResults && jobId && (
          <AnalysisResults jobId={jobId} onNavigateToProposal={handleNavigateToProposal} />
        )}
      </Stack>
    </Container>
  );
}

