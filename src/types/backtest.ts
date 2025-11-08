/**
 * Backtest Types
 * 
 * Related Documentation:
 * - Plan: docs/03_plans/backtest/README.md
 * - Data Model: docs/03_plans/backtest/data-model.md
 */

export interface BacktestJob {
  job_id: string;
  algorithm_id: number;
  start_date: string;
  end_date: string;
  data_set_id: number | null;
  status: 'pending' | 'running' | 'completed' | 'failed';
  progress: number;
  message: string | null;
  error: string | null;
  created_at: string;
  completed_at: string | null;
}

export interface BacktestResult {
  id: number;
  job_id: string;
  algorithm_id: number;
  start_date: string;
  end_date: string;
  performance: PerformanceMetrics;
  trades: Trade[];
  equity_curve: EquityPoint[];
  created_at: string;
}

export interface PerformanceMetrics {
  total_return: number;
  sharpe_ratio: number;
  max_drawdown: number;
  win_rate: number;
  total_trades: number;
  average_profit: number;
  average_loss: number;
}

export interface Trade {
  id: number;
  job_id: string;
  entry_date: string;
  exit_date: string;
  entry_price: number;
  exit_price: number;
  quantity: number;
  profit: number;
  profit_rate: number;
}

export interface EquityPoint {
  id: number;
  job_id: string;
  date: string;
  equity: number;
}

