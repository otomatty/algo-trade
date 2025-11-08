/**
 * Analysis Progress Component
 * 
 * DEPENDENCY MAP:
 * 
 * Parents (Files that import this file):
 *   └─ src/pages/DataAnalysis/DataAnalysis.tsx
 * 
 * Dependencies (External files that this file imports):
 *   ├─ @tauri-apps/api/core
 *   ├─ @mantine/core
 *   └─ src/types/analysis
 * 
 * Related Documentation:
 *   ├─ Spec: src/pages/DataAnalysis/AnalysisProgress.spec.md
 *   ├─ Tests: src/pages/DataAnalysis/AnalysisProgress.test.tsx
 *   └─ Plan: docs/03_plans/data-analysis/README.md
 */
import { useState, useEffect, useRef } from 'react';
import { invoke } from '@tauri-apps/api/core';
import {
  Progress,
  Text,
  Paper,
  Alert,
  Stack,
} from '@mantine/core';
import { AnalysisJob } from '../../types/analysis';

interface AnalysisProgressProps {
  jobId: string;
  onCompleted?: () => void;
  onError?: (error: string) => void;
}

export function AnalysisProgress({ jobId, onCompleted, onError }: AnalysisProgressProps) {
  const [status, setStatus] = useState<AnalysisJob['status']>('pending');
  const [progress, setProgress] = useState(0);
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const intervalRef = useRef<number | null>(null);

  useEffect(() => {
    const pollStatus = async () => {
      try {
        const response = await invoke<{
          status: AnalysisJob['status'];
          progress: number;
          message: string;
          error?: string;
        }>('get_analysis_status', { job_id: jobId });

        setStatus(response.status);
        setProgress(response.progress);
        setMessage(response.message);

        if (response.error) {
          setError(response.error);
        }

        // Stop polling if job is completed or failed
        if (response.status === 'completed') {
          if (intervalRef.current) {
            clearInterval(intervalRef.current);
            intervalRef.current = null;
          }
          if (onCompleted) {
            onCompleted();
          }
        } else if (response.status === 'failed') {
          if (intervalRef.current) {
            clearInterval(intervalRef.current);
            intervalRef.current = null;
          }
          if (onError && response.error) {
            onError(response.error);
          }
        }
      } catch (err) {
        const errorMessage = err instanceof Error ? err.message : 'Failed to get analysis status';
        setError(errorMessage);
        if (intervalRef.current) {
          clearInterval(intervalRef.current);
          intervalRef.current = null;
        }
        if (onError) {
          onError(errorMessage);
        }
      }
    };

    // Initial poll
    pollStatus();

    // Set up polling interval (2 seconds)
    intervalRef.current = window.setInterval(pollStatus, 2000);

    // Cleanup on unmount
    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, [jobId, onCompleted, onError]);

  const getStatusColor = () => {
    switch (status) {
      case 'completed':
        return 'green';
      case 'failed':
        return 'red';
      case 'running':
        return 'blue';
      default:
        return 'gray';
    }
  };

  return (
    <Paper p="md" withBorder>
      <Stack gap="md">
        <Text fw={500}>Analysis Progress</Text>

        {error && (
          <Alert color="red">
            {error}
          </Alert>
        )}

        <Progress value={progress} color={getStatusColor()} size="lg" />

        <Stack gap="xs">
          <Text size="sm" c="dimmed">
            Status: <Text span fw={500} c={getStatusColor()}>{status}</Text>
          </Text>
          {message && (
            <Text size="sm" c="dimmed">
              {message}
            </Text>
          )}
        </Stack>
      </Stack>
    </Paper>
  );
}

