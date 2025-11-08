/**
 * Trend Analysis Component
 * 
 * DEPENDENCY MAP:
 * 
 * Parents (Files that import this file):
 *   └─ src/pages/DataAnalysis/AnalysisResults.tsx
 * 
 * Dependencies (External files that this file imports):
 *   ├─ @mantine/core
 *   └─ src/types/analysis
 */
import { AnalysisSummary } from '../../types/analysis';
import { Card, Text, Badge, Stack, Group } from '@mantine/core';

interface TrendAnalysisProps {
  summary: AnalysisSummary;
}

export function TrendAnalysis({ summary }: TrendAnalysisProps) {
  const getTrendColor = () => {
    switch (summary.trend_direction) {
      case 'upward':
        return 'green';
      case 'downward':
        return 'red';
      default:
        return 'gray';
    }
  };

  const getVolatilityColor = () => {
    switch (summary.volatility_level) {
      case 'high':
        return 'red';
      case 'medium':
        return 'yellow';
      default:
        return 'green';
    }
  };

  return (
    <Card withBorder p="md">
      <Stack gap="md">
        <Text fw={500}>Trend Analysis</Text>
        <Group>
          <Text size="sm">Trend:</Text>
          <Badge color={getTrendColor()}>{summary.trend_direction}</Badge>
        </Group>
        <Group>
          <Text size="sm">Volatility:</Text>
          <Badge color={getVolatilityColor()}>{summary.volatility_level}</Badge>
        </Group>
        {summary.dominant_patterns.length > 0 && (
          <Stack gap="xs">
            <Text size="sm" fw={500}>Dominant Patterns:</Text>
            {summary.dominant_patterns.map((pattern, idx) => (
              <Badge key={idx} variant="light">{pattern}</Badge>
            ))}
          </Stack>
        )}
      </Stack>
    </Card>
  );
}

