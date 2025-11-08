/**
 * Dashboard Types
 * 
 * Related Documentation:
 * - Plan: docs/03_plans/dashboard/README.md
 * - Data Model: docs/03_plans/dashboard/data-model.md
 * - API Spec: docs/03_plans/dashboard/api-spec.md
 */

import { Algorithm } from './algorithm';
import { PerformanceMetrics } from './backtest';

/**
 * Backtest Result Summary
 * Summary of backtest results for dashboard display
 */
export interface BacktestResultSummary {
  job_id: string;
  algorithm_id: number;
  algorithm_name: string;
  start_date: string;      // YYYY-MM-DD format
  end_date: string;         // YYYY-MM-DD format
  completed_at: string;    // ISO 8601 format
  performance: PerformanceMetrics;
}

/**
 * Get Selected Algorithms Response
 */
export interface GetSelectedAlgorithmsResponse {
  algorithms: Algorithm[];
}

/**
 * Get Backtest Results Summary Request
 */
export interface GetBacktestResultsSummaryRequest {
  algorithm_ids?: number[];
  limit?: number;
}

/**
 * Get Backtest Results Summary Response
 */
export interface GetBacktestResultsSummaryResponse {
  results: BacktestResultSummary[];
}

/**
 * Delete Algorithm Request
 */
export interface DeleteAlgorithmRequest {
  algo_id: number;
}

/**
 * Delete Algorithm Response
 */
export interface DeleteAlgorithmResponse {
  success: boolean;
  message?: string;
}

/**
 * Dashboard State (for Zustand store)
 */
export interface DashboardState {
  algorithms: Algorithm[];
  backtestResults: BacktestResultSummary[];
  loading: boolean;
  error: string | null;
  selectedAlgorithmId: number | null;
}

/**
 * Dashboard Actions (for Zustand store)
 */
export interface DashboardActions {
  fetchAlgorithms: () => Promise<void>;
  fetchBacktestResults: (algorithmIds?: number[]) => Promise<void>;
  deleteAlgorithm: (algorithmId: number) => Promise<void>;
  setSelectedAlgorithmId: (id: number | null) => void;
  clearError: () => void;
}

