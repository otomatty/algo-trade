/**
 * Trade History Component
 * 
 * DEPENDENCY MAP:
 * 
 * Parents (Files that import this file):
 *   └─ src/pages/Backtest/BacktestResults.tsx
 * 
 * Dependencies (External files that this file imports):
 *   ├─ @mantine/core
 *   └─ src/types/backtest
 * 
 * Related Documentation:
 *   └─ Plan: docs/03_plans/backtest/README.md
 */
import { Paper, Table, Text, Stack } from '@mantine/core';
import { Trade } from '../../types/backtest';
import { useState } from 'react';
import { TradeDetailModal } from './TradeDetailModal';

interface TradeHistoryProps {
  trades: Trade[];
}

export function TradeHistory({ trades }: TradeHistoryProps) {
  const [selectedTrade, setSelectedTrade] = useState<Trade | null>(null);
  const [modalOpened, setModalOpened] = useState(false);

  if (trades.length === 0) {
    return (
      <Paper p="md" withBorder>
        <Text c="dimmed">No trades executed during this backtest period.</Text>
      </Paper>
    );
  }

  const handleTradeClick = (trade: Trade) => {
    setSelectedTrade(trade);
    setModalOpened(true);
  };

  return (
    <Paper p="md" withBorder>
      <Stack gap="md">
        <Text fw={500}>Trade History</Text>
        <Table striped highlightOnHover>
          <Table.Thead>
            <Table.Tr>
              <Table.Th>Entry Date</Table.Th>
              <Table.Th>Exit Date</Table.Th>
              <Table.Th>Entry Price</Table.Th>
              <Table.Th>Exit Price</Table.Th>
              <Table.Th>Quantity</Table.Th>
              <Table.Th>Profit</Table.Th>
              <Table.Th>Profit Rate</Table.Th>
            </Table.Tr>
          </Table.Thead>
          <Table.Tbody>
            {trades.map((trade, index) => (
              <Table.Tr 
                key={index}
                style={{ cursor: 'pointer' }}
                onClick={() => handleTradeClick(trade)}
              >
                <Table.Td>{trade.entry_date}</Table.Td>
                <Table.Td>{trade.exit_date}</Table.Td>
                <Table.Td>${trade.entry_price.toFixed(2)}</Table.Td>
                <Table.Td>${trade.exit_price.toFixed(2)}</Table.Td>
                <Table.Td>{trade.quantity}</Table.Td>
                <Table.Td c={trade.profit >= 0 ? 'green' : 'red'}>
                  ${trade.profit.toFixed(2)}
                </Table.Td>
                <Table.Td c={trade.profit_rate >= 0 ? 'green' : 'red'}>
                  {trade.profit_rate >= 0 ? '+' : ''}{trade.profit_rate.toFixed(2)}%
                </Table.Td>
              </Table.Tr>
            ))}
          </Table.Tbody>
        </Table>

        <TradeDetailModal
          trade={selectedTrade}
          opened={modalOpened}
          onClose={() => setModalOpened(false)}
        />
      </Stack>
    </Paper>
  );
}

