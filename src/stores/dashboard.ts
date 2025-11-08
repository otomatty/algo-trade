/**
 * Dashboard Zustand Store
 * 
 * DEPENDENCY MAP:
 * 
 * Parents (Files that import this file):
 *   ├─ src/pages/Dashboard/Dashboard.tsx
 *   ├─ src/pages/Dashboard/AlgorithmList.tsx
 *   └─ src/pages/Dashboard/QuickActions.tsx
 * 
 * Dependencies (External files that this file imports):
 *   ├─ zustand
 *   ├─ @tauri-apps/api/core
 *   ├─ src/types/dashboard
 *   └─ src/types/algorithm
 * 
 * Related Documentation:
 *   ├─ Spec: src/pages/Dashboard/Dashboard.spec.md
 *   └─ Plan: docs/03_plans/dashboard/README.md
 */
import { create } from 'zustand';
import { invoke } from '@tauri-apps/api/core';
import type {
  DashboardState,
  DashboardActions,
  GetSelectedAlgorithmsResponse,
  GetBacktestResultsSummaryResponse,
  DeleteAlgorithmResponse,
  Algorithm,
} from '../../types/dashboard';

export const useDashboardStore = create<DashboardState & DashboardActions>((set, get) => ({
  algorithms: [],
  backtestResults: [],
  loading: false,
  error: null,
  selectedAlgorithmId: null,

  fetchAlgorithms: async () => {
    set({ loading: true, error: null });
    try {
      const response = await invoke<GetSelectedAlgorithmsResponse>('get_selected_algorithms');
      set({ algorithms: response.algorithms || [], loading: false });
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Failed to fetch algorithms',
        loading: false,
      });
    }
  },

  fetchBacktestResults: async (algorithmIds?: number[]) => {
    set({ loading: true, error: null });
    try {
      const response = await invoke<GetBacktestResultsSummaryResponse>(
        'get_backtest_results_summary',
        { algorithm_ids: algorithmIds, limit: 10 }
      );
      set({ backtestResults: response.results || [], loading: false });
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Failed to fetch backtest results',
        loading: false,
      });
    }
  },

  deleteAlgorithm: async (algorithmId: number) => {
    try {
      await invoke<DeleteAlgorithmResponse>('delete_algorithm', { algo_id: algorithmId });
      // Refresh algorithms list
      await get().fetchAlgorithms();
      // Refresh backtest results
      const algorithms = get().algorithms;
      if (algorithms.length > 0) {
        const algorithmIds = algorithms.map((a) => a.id);
        await get().fetchBacktestResults(algorithmIds);
      }
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Failed to delete algorithm',
      });
      throw error;
    }
  },

  setSelectedAlgorithmId: (id) => set({ selectedAlgorithmId: id }),

  clearError: () => set({ error: null }),
}));

