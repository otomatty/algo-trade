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

export interface DataPreview {
  data_set_id: number;
  data: OHLCVData[];
  statistics: {
    count: number;
    date_range: {
      start: string;
      end: string;
    };
    open: { mean: number; min: number; max: number; std: number };
    high: { mean: number; min: number; max: number; std: number };
    low: { mean: number; min: number; max: number; std: number };
    close: { mean: number; min: number; max: number; std: number };
    volume: { mean: number; min: number; max: number; std: number };
  };
}

