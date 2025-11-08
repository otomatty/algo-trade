/**
 * Entry/Exit Chart Component
 * 
 * DEPENDENCY MAP:
 * 
 * Parents (Files that import this file):
 *   └─ src/pages/Backtest/BacktestResults.tsx
 * 
 * Dependencies (External files that this file imports):
 *   ├─ @mantine/core
 *   ├─ recharts
 *   └─ src/types/backtest
 * 
 * Related Documentation:
 *   └─ Plan: docs/03_plans/backtest/README.md
 */
import { Card, Text } from '@mantine/core';
import { 
  LineChart, 
  Line, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  Legend, 
  ResponsiveContainer,
  ReferenceLine
} from 'recharts';
import { Trade, EquityPoint } from '../../types/backtest';

interface EntryExitChartProps {
  trades: Trade[];
  equityCurve: EquityPoint[];
}

export function EntryExitChart({ trades, equityCurve }: EntryExitChartProps) {
  if (trades.length === 0) {
    return (
      <Card withBorder p="md">
        <Text c="dimmed">No trades to display.</Text>
      </Card>
    );
  }

  // Create chart data combining equity curve with entry/exit points
  const chartData = equityCurve.map((point) => {
    return {
      date: point.date,
      equity: point.equity,
    };
  });

  // Create entry/exit markers
  const entryMarkers = trades.map(trade => ({
    date: trade.entry_date,
    price: trade.entry_price,
    type: 'entry',
  }));

  const exitMarkers = trades.map(trade => ({
    date: trade.exit_date,
    price: trade.exit_price,
    type: 'exit',
  }));

  return (
    <Card withBorder p="md">
      <Text fw={500} mb="md">Entry/Exit Points on Equity Curve</Text>
      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis 
            dataKey="date" 
            tick={{ fontSize: 12 }}
            angle={-45}
            textAnchor="end"
            height={80}
          />
          <YAxis 
            tick={{ fontSize: 12 }}
            tickFormatter={(value) => `$${value.toLocaleString()}`}
          />
          <Tooltip 
            formatter={(value: number) => `$${value.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`}
            labelFormatter={(label) => `Date: ${label}`}
          />
          <Legend />
          <Line 
            type="monotone" 
            dataKey="equity" 
            stroke="#8884d8" 
            strokeWidth={2}
            dot={false}
            name="Equity"
          />
          {/* Entry points as vertical lines */}
          {entryMarkers.map((marker, index) => {
            const dataPoint = chartData.find(d => d.date === marker.date);
            if (!dataPoint) return null;
            return (
              <ReferenceLine
                key={`entry-${index}`}
                x={marker.date}
                stroke="#00ff00"
                strokeWidth={2}
                strokeDasharray="5 5"
                label={{ value: 'Entry', position: 'top', fill: '#00ff00' }}
              />
            );
          })}
          {/* Exit points as vertical lines */}
          {exitMarkers.map((marker, index) => {
            const dataPoint = chartData.find(d => d.date === marker.date);
            if (!dataPoint) return null;
            return (
              <ReferenceLine
                key={`exit-${index}`}
                x={marker.date}
                stroke="#ff0000"
                strokeWidth={2}
                strokeDasharray="5 5"
                label={{ value: 'Exit', position: 'top', fill: '#ff0000' }}
              />
            );
          })}
        </LineChart>
      </ResponsiveContainer>
    </Card>
  );
}

