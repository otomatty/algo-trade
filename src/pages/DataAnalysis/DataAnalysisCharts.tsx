/**
 * Data Analysis Charts Component
 * 
 * DEPENDENCY MAP:
 * 
 * Parents (Files that import this file):
 *   └─ src/pages/DataAnalysis/AnalysisResults.tsx
 * 
 * Dependencies (External files that this file imports):
 *   ├─ @mantine/core
 *   ├─ recharts
 *   └─ src/types/analysis
 * 
 * Related Documentation:
 *   ├─ Spec: src/pages/DataAnalysis/DataAnalysisCharts.spec.md
 *   └─ Plan: docs/03_plans/data-analysis/README.md
 */
import { AnalysisResult } from '../../types/analysis';
import { Card, Text, Stack } from '@mantine/core';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

interface DataAnalysisChartsProps {
  result: AnalysisResult;
}

export function DataAnalysisCharts({ result }: DataAnalysisChartsProps) {
  // RSIチャート用のデータ（簡易版）
  const rsiData = result.technical_indicators.rsi ? [
    { name: 'RSI', value: result.technical_indicators.rsi.value },
  ] : [];

  // MACDチャート用のデータ
  const macdData = result.technical_indicators.macd ? [
    {
      name: 'MACD',
      macd: result.technical_indicators.macd.macd,
      signal: result.technical_indicators.macd.signal,
      histogram: result.technical_indicators.macd.histogram,
    },
  ] : [];

  return (
    <Stack gap="md">
      {result.technical_indicators.rsi && (
        <Card withBorder p="md">
          <Text fw={500} mb="md">RSI Indicator</Text>
          <ResponsiveContainer width="100%" height={200}>
            <LineChart data={rsiData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis domain={[0, 100]} />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="value" stroke="#8884d8" strokeWidth={2} />
              <Line type="monotone" dataKey={70} stroke="#ff0000" strokeDasharray="5 5" />
              <Line type="monotone" dataKey={30} stroke="#00ff00" strokeDasharray="5 5" />
            </LineChart>
          </ResponsiveContainer>
        </Card>
      )}

      {result.technical_indicators.macd && (
        <Card withBorder p="md">
          <Text fw={500} mb="md">MACD Indicator</Text>
          <ResponsiveContainer width="100%" height={200}>
            <LineChart data={macdData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="macd" stroke="#8884d8" strokeWidth={2} />
              <Line type="monotone" dataKey="signal" stroke="#82ca9d" strokeWidth={2} />
              <Line type="monotone" dataKey="histogram" stroke="#ffc658" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </Card>
      )}

      {/* 統計情報の可視化 */}
      <Card withBorder p="md">
        <Text fw={500} mb="md">Price Range</Text>
        <ResponsiveContainer width="100%" height={200}>
          <LineChart data={[
            { name: 'Min', value: result.statistics.price_range.min },
            { name: 'Current', value: result.statistics.price_range.current },
            { name: 'Max', value: result.statistics.price_range.max },
          ]}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="value" stroke="#8884d8" strokeWidth={2} />
          </LineChart>
        </ResponsiveContainer>
      </Card>
    </Stack>
  );
}

