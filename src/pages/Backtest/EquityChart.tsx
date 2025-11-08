/**
 * Equity Chart Component
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
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { EquityPoint } from '../../types/backtest';

interface EquityChartProps {
  equityCurve: EquityPoint[];
}

export function EquityChart({ equityCurve }: EquityChartProps) {
  if (equityCurve.length === 0) {
    return (
      <Card withBorder p="md">
        <Text c="dimmed">No equity curve data available.</Text>
      </Card>
    );
  }

  // Format data for chart
  const chartData = equityCurve.map((point) => ({
    date: point.date,
    equity: point.equity,
  }));

  return (
    <Card withBorder p="md">
      <Text fw={500} mb="md">Equity Curve</Text>
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
        </LineChart>
      </ResponsiveContainer>
    </Card>
  );
}

