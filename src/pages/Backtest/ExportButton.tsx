/**
 * Export Button Component
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
import { Button, Group } from '@mantine/core';
import { BacktestResult } from '../../types/backtest';

interface ExportButtonProps {
  result: BacktestResult;
}

export function ExportButton({ result }: ExportButtonProps) {
  const handleExportCSV = () => {
    // Create CSV content
    const headers = [
      'Entry Date',
      'Exit Date',
      'Entry Price',
      'Exit Price',
      'Quantity',
      'Profit',
      'Profit Rate (%)'
    ];

    const rows = result.trades.map(trade => [
      trade.entry_date,
      trade.exit_date,
      trade.entry_price.toFixed(2),
      trade.exit_price.toFixed(2),
      trade.quantity.toString(),
      trade.profit.toFixed(2),
      trade.profit_rate.toFixed(2)
    ]);

    const csvContent = [
      headers.join(','),
      ...rows.map(row => row.join(','))
    ].join('\n');

    // Create blob and download
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    
    link.setAttribute('href', url);
    link.setAttribute('download', `backtest_results_${result.job_id}.csv`);
    link.style.visibility = 'hidden';
    
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <Group>
      <Button onClick={handleExportCSV} variant="outline">
        Export to CSV
      </Button>
    </Group>
  );
}

