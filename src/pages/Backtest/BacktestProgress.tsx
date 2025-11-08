/**
 * Backtest Progress Component
 * 
 * DEPENDENCY MAP:
 * 
 * Parents (Files that import this file):
 *   └─ src/pages/Backtest/BacktestSettings.tsx
 * 
 * Dependencies (External files that this file imports):
 *   ├─ @tauri-apps/api/core
 *   ├─ @mantine/core
 *   └─ src/types/backtest
 * 
 * Related Documentation:
 *   └─ Plan: docs/03_plans/backtest/README.md
 */
import { useState, useEffect, useRef } from 'react';
import { invoke } from '@tauri-apps/api/core';
import {
  Paper,
  Text,
  Progress,
  Stack,
  Alert,
} from '@mantine/core';
import { BacktestJob } from '../../types/backtest';

type BacktestJobStatus = 'pending' | 'running' | 'completed' | 'failed';

interface BacktestProgressProps {
  jobId: string;
  onCompleted?: () => void;
  onError?: (error: string) => void;
}

export function BacktestProgress({ jobId, onCompleted, onError }: BacktestProgressProps) {
  const [status, setStatus] = useState<BacktestJobStatus>('pending');
  const [progress, setProgress] = useState(0);
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const intervalRef = useRef<number | null>(null);

  useEffect(() => {
    const pollStatus = async () => {
      try {
        const response = await invoke<{
          status: BacktestJobStatus;
          progress: number;
          message: string;
          error?: string;
        }>('get_backtest_status', { job_id: jobId });

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
        const errorMessage = err instanceof Error ? err.message : 'Failed to get backtest status';
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

    // Set up polling interval (1 second)
    intervalRef.current = window.setInterval(pollStatus, 1000);

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
        <Text fw={500}>Backtest Progress</Text>

        {error && (
          <Alert color="red">
            {error}
          </Alert>
        )}

        <Progress value={progress * 100} color={getStatusColor()} size="lg" />

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

