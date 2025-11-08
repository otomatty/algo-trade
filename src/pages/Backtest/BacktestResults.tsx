/**
 * Backtest Results Component
 * 
 * DEPENDENCY MAP:
 * 
 * Parents (Files that import this file):
 *   └─ src/pages/Backtest/BacktestSettings.tsx (or future BacktestResults page)
 * 
 * Dependencies (External files that this file imports):
 *   ├─ @tauri-apps/api/core
 *   ├─ @mantine/core
 *   ├─ src/types/backtest
 *   └─ Sub-components
 * 
 * Related Documentation:
 *   └─ Plan: docs/03_plans/backtest/README.md
 */
import { useState, useEffect } from 'react';
import { invoke } from '@tauri-apps/api/core';
import { Stack, Alert, Text, Container, Title, Group } from '@mantine/core';
import { BacktestResult } from '../../types/backtest';
import { PerformanceMetrics } from './PerformanceMetrics';
import { TradeHistory } from './TradeHistory';
import { EquityChart } from './EquityChart';
import { EntryExitChart } from './EntryExitChart';
import { ExportButton } from './ExportButton';

interface BacktestResultsProps {
  jobId: string;
}

export function BacktestResults({ jobId }: BacktestResultsProps) {
  const [results, setResults] = useState<BacktestResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadResults();
  }, [jobId]);

  const loadResults = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await invoke<BacktestResult>('get_backtest_results', {
        job_id: jobId,
      });

      setResults(response);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load backtest results');
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
    <Container size="xl" py="md">
      <Stack gap="md">
        <Group justify="space-between">
          <Title order={2}>Backtest Results</Title>
          {results && <ExportButton result={results} />}
        </Group>

        <PerformanceMetrics performance={results.performance} />

        <EquityChart equityCurve={results.equity_curve} />

        <EntryExitChart trades={results.trades} equityCurve={results.equity_curve} />

        <TradeHistory trades={results.trades} />
      </Stack>
    </Container>
  );
}

