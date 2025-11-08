/**
 * Progress Indicator Component
 * 
 * DEPENDENCY MAP:
 * 
 * Parents (Files that import this file):
 *   └─ src/pages/AlgorithmProposal/AlgorithmProposal.tsx
 * 
 * Dependencies (External files that this file imports):
 *   ├─ @mantine/core
 * 
 * Related Documentation:
 *   ├─ Spec: src/pages/AlgorithmProposal/AlgorithmProposal.spec.md
 *   └─ Plan: docs/03_plans/algorithm-proposal/README.md
 */
import { Paper, Text, Progress, Stack } from '@mantine/core';

interface ProgressIndicatorProps {
  jobId: string;
  onCompleted?: () => void;
}

export function ProgressIndicator({ jobId, onCompleted }: ProgressIndicatorProps) {
  // Phase 4で実装予定: ジョブ状態のポーリングと進捗表示
  // 現時点では基本構造のみ
  
  return (
    <Paper p="md" withBorder>
      <Stack gap="sm">
        <Text fw={500}>Generating Proposals</Text>
        <Text c="dimmed" size="sm">
          Job ID: {jobId}
        </Text>
        <Progress value={0} animated />
        <Text c="dimmed" size="xs">
          Progress tracking will be implemented in Phase 4
        </Text>
      </Stack>
    </Paper>
  );
}

