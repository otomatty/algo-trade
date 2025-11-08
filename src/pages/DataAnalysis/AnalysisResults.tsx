/**
 * Analysis Results Component
 * 
 * DEPENDENCY MAP:
 * 
 * Parents (Files that import this file):
 *   └─ src/pages/DataAnalysis/DataAnalysis.tsx
 * 
 * Dependencies (External files that this file imports):
 *   ├─ @tauri-apps/api/core
 *   ├─ @mantine/core
 *   ├─ src/types/analysis
 *   └─ Sub-components
 * 
 * Related Documentation:
 *   ├─ Spec: src/pages/DataAnalysis/AnalysisResults.spec.md
 *   └─ Plan: docs/03_plans/data-analysis/README.md
 */
import { useState, useEffect } from 'react';
import { invoke } from '@tauri-apps/api/core';
import { Stack, Alert, Text, Button } from '@mantine/core';
import { AnalysisResult } from '../../types/analysis';
import { TrendAnalysis } from './TrendAnalysis';
import { TechnicalIndicators } from './TechnicalIndicators';
import { Statistics } from './Statistics';
import { DataAnalysisCharts } from './DataAnalysisCharts';

interface AnalysisResultsProps {
  jobId: string;
  onNavigateToProposal?: (jobId: string) => void;
}

export function AnalysisResults({ jobId, onNavigateToProposal }: AnalysisResultsProps) {
  const [results, setResults] = useState<AnalysisResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadResults();
  }, [jobId]);

  const loadResults = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await invoke<{
        job_id: string;
        data_set_id: number;
        analysis_summary: AnalysisResult['analysis_summary'];
        technical_indicators: AnalysisResult['technical_indicators'];
        statistics: AnalysisResult['statistics'];
      }>('get_analysis_results', { job_id: jobId });

      setResults({
        id: 0,
        job_id: response.job_id,
        data_set_id: response.data_set_id,
        analysis_summary: response.analysis_summary,
        technical_indicators: response.technical_indicators,
        statistics: response.statistics,
        created_at: new Date().toISOString(),
      });
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load analysis results');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <Text>Loading results...</Text>;
  }

  if (error) {
    return <Alert color="red">{error}</Alert>;
  }

  if (!results) {
    return null;
  }

  return (
    <Stack gap="md">
      <TrendAnalysis summary={results.analysis_summary} />
      <TechnicalIndicators indicators={results.technical_indicators} />
      <Statistics statistics={results.statistics} />
      <DataAnalysisCharts result={results} />
      
      {onNavigateToProposal && (
        <Button
          onClick={() => onNavigateToProposal(jobId)}
          size="lg"
          fullWidth
        >
          Generate Algorithm Proposals
        </Button>
      )}
    </Stack>
  );
}
