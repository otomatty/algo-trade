/**
 * Data Collection & Management Types
 * 
 * Related Documentation:
 * - Plan: docs/03_plans/data-collection/README.md
 * - Plan: docs/03_plans/data-management/README.md
 */

export interface DataSet {
  id: number;
  name: string;
  symbol: string | null;
  start_date: string | null;
  end_date: string | null;
  record_count: number;
  imported_at: string;
  source: 'csv' | 'api' | 'manual';
  created_at: string;
}

export interface OHLCVData {
  id: number;
  data_set_id: number;
  date: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
}

