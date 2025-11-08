/**
 * Technical Indicators Component
 */
import { TechnicalIndicators as TechnicalIndicatorsType } from '../../types/analysis';
import { Card, Text, Stack, Group, Badge } from '@mantine/core';

interface TechnicalIndicatorsProps {
  indicators: TechnicalIndicatorsType;
}

export function TechnicalIndicators({ indicators }: TechnicalIndicatorsProps) {
  return (
    <Card withBorder p="md">
      <Stack gap="md">
        <Text fw={500}>Technical Indicators</Text>
        
        {indicators.rsi && (
          <Group>
            <Text size="sm">RSI ({indicators.rsi.period}):</Text>
            <Text fw={500}>{indicators.rsi.value.toFixed(2)}</Text>
            <Badge color={indicators.rsi.signal === 'overbought' ? 'red' : indicators.rsi.signal === 'oversold' ? 'green' : 'gray'}>
              {indicators.rsi.signal}
            </Badge>
          </Group>
        )}
        
        {indicators.macd && (
          <Stack gap="xs">
            <Text size="sm" fw={500}>MACD:</Text>
            <Group>
              <Text size="sm">MACD: {indicators.macd.macd.toFixed(4)}</Text>
              <Text size="sm">Signal: {indicators.macd.signal.toFixed(4)}</Text>
              <Text size="sm">Histogram: {indicators.macd.histogram.toFixed(4)}</Text>
              <Badge color={indicators.macd.signal_type === 'bullish' ? 'green' : indicators.macd.signal_type === 'bearish' ? 'red' : 'gray'}>
                {indicators.macd.signal_type}
              </Badge>
            </Group>
          </Stack>
        )}
      </Stack>
    </Card>
  );
}

