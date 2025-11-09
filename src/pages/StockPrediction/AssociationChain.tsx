/**
 * Association Chain Component
 * 
 * DEPENDENCY MAP:
 * 
 * Parents (Files that import this file):
 *   └─ src/pages/StockPrediction/PredictionDetailModal.tsx
 * 
 * Dependencies (External files that this file imports):
 *   ├─ @mantine/core
 *   └─ src/types/stock-prediction
 * 
 * Related Documentation:
 *   └─ Plan: docs/03_plans/stock-prediction/README.md
 */
import { Stack, Text, Paper, Group, Badge } from '@mantine/core';
import { AssociationStep } from '../../types/stock-prediction';

interface AssociationChainProps {
  chain: AssociationStep[];
}

export function AssociationChain({ chain }: AssociationChainProps) {
  if (!chain || chain.length === 0) {
    return (
      <Paper p="md" withBorder>
        <Text c="dimmed" size="sm">
          No association chain available
        </Text>
      </Paper>
    );
  }

  // Sort by step number
  const sortedChain = [...chain].sort((a, b) => a.step - b.step);

  return (
    <Paper p="md" withBorder>
      <Stack gap="md">
        <Text fw={500} size="sm">
          Association Chain
        </Text>
        <Stack gap="xs">
          {sortedChain.map((step, index) => (
            <Group key={step.step} gap="md" align="flex-start">
              <Badge variant="light" color="blue" size="lg">
                Step {step.step}
              </Badge>
              <Stack gap={4} style={{ flex: 1 }}>
                <Text size="sm" fw={500}>
                  {step.concept}
                </Text>
                <Text size="xs" c="dimmed">
                  {step.connection}
                </Text>
              </Stack>
              {index < sortedChain.length - 1 && (
                <Text size="sm" c="dimmed" style={{ marginLeft: 'auto' }}>
                  →
                </Text>
              )}
            </Group>
          ))}
        </Stack>
      </Stack>
    </Paper>
  );
}

