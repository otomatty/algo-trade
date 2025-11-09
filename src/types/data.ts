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

export interface DataCollectionSchedule {
  schedule_id: string;
  name: string;
  source: 'yahoo' | 'alphavantage';
  symbol: string;
  start_date: string | null;
  end_date: string | null;
  cron_expression: string;
  enabled: boolean;
  api_key: string | null;
  data_set_name: string | null;
  created_at: string;
  updated_at: string;
}

export interface DataCollectionJob {
  job_id: string;
  schedule_id: string | null;
  source: 'yahoo' | 'alphavantage';
  symbol: string;
  start_date: string;
  end_date: string;
  name: string | null;
  api_key: string | null;
  status: 'pending' | 'running' | 'completed' | 'failed';
  progress: number;
  message: string | null;
  error: string | null;
  data_set_id: number | null;
  created_at: string;
  completed_at: string | null;
}

export interface ConfigureDataCollectionRequest {
  action: 'create' | 'update' | 'delete';
  schedule_id?: string;
  name?: string;
  source?: 'yahoo' | 'alphavantage';
  symbol?: string;
  cron_expression?: string;
  start_date?: string;
  end_date?: string;
  api_key?: string;
  data_set_name?: string;
  enabled?: boolean;
}

export interface ConfigureDataCollectionResponse {
  schedule_id: string;
}


