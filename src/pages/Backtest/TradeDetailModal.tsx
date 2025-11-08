/**
 * Trade Detail Modal Component
 * 
 * DEPENDENCY MAP:
 * 
 * Parents (Files that import this file):
 *   └─ src/pages/Backtest/TradeHistory.tsx
 * 
 * Dependencies (External files that this file imports):
 *   ├─ @mantine/core
 *   └─ src/types/backtest
 * 
 * Related Documentation:
 *   └─ Plan: docs/03_plans/backtest/README.md
 */
import { Modal, Stack, Text, Group, Divider } from '@mantine/core';
import { Trade } from '../../types/backtest';

interface TradeDetailModalProps {
  trade: Trade | null;
  opened: boolean;
  onClose: () => void;
}

export function TradeDetailModal({ trade, opened, onClose }: TradeDetailModalProps) {
  if (!trade) {
    return null;
  }

  const profitColor = trade.profit >= 0 ? 'green' : 'red';
  const profitRateColor = trade.profit_rate >= 0 ? 'green' : 'red';

  return (
    <Modal
      opened={opened}
      onClose={onClose}
      title="Trade Details"
      size="md"
    >
      <Stack gap="md">
        <Group justify="space-between">
          <Text size="sm" c="dimmed">Entry Date</Text>
          <Text fw={500}>{trade.entry_date}</Text>
        </Group>

        <Group justify="space-between">
          <Text size="sm" c="dimmed">Exit Date</Text>
          <Text fw={500}>{trade.exit_date}</Text>
        </Group>

        <Divider />

        <Group justify="space-between">
          <Text size="sm" c="dimmed">Entry Price</Text>
          <Text fw={500}>${trade.entry_price.toFixed(2)}</Text>
        </Group>

        <Group justify="space-between">
          <Text size="sm" c="dimmed">Exit Price</Text>
          <Text fw={500}>${trade.exit_price.toFixed(2)}</Text>
        </Group>

        <Group justify="space-between">
          <Text size="sm" c="dimmed">Quantity</Text>
          <Text fw={500}>{trade.quantity}</Text>
        </Group>

        <Divider />

        <Group justify="space-between">
          <Text size="sm" c="dimmed">Profit</Text>
          <Text fw={500} c={profitColor}>
            ${trade.profit.toFixed(2)}
          </Text>
        </Group>

        <Group justify="space-between">
          <Text size="sm" c="dimmed">Profit Rate</Text>
          <Text fw={500} c={profitRateColor}>
            {trade.profit_rate >= 0 ? '+' : ''}{trade.profit_rate.toFixed(2)}%
          </Text>
        </Group>
      </Stack>
    </Modal>
  );
}

