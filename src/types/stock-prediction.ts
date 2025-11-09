/**
 * Stock Prediction Types
 * 
 * Related Documentation:
 * - Plan: docs/03_plans/stock-prediction/README.md
 * - Data Model: docs/03_plans/stock-prediction/data-model.md
 */

export interface StockPrediction {
  prediction_id: string;
  symbol: string;
  predicted_direction: 'up' | 'down' | 'sideways';
  confidence_score: number;
  reasoning: string;
  association_chain: AssociationStep[];
  suggested_action: 'buy' | 'sell' | 'hold' | 'watch';
  // Additional fields from backend
  name?: string;
  predicted_change_percent?: number;
  rationale?: string;
  recommended_action?: 'buy' | 'sell' | 'hold' | 'watch';
  risk_factors?: string[];
  time_horizon?: '短期' | '中期' | '長期';
  created_at?: string;
}

export interface AssociationStep {
  step: number;
  concept: string;
  connection: string;
}

export interface StockPredictionJobStatus {
  status: 'pending' | 'analyzing' | 'generating' | 'completed' | 'failed';
  progress: number;
  message: string;
  error?: string;
}

export interface GenerateStockPredictionsRequest {
  news_job_id?: string;
  num_predictions?: number;
  user_preferences?: {
    risk_tolerance?: 'low' | 'medium' | 'high';
    investment_horizon?: 'short' | 'medium' | 'long';
    investment_style?: 'conservative' | 'balanced' | 'aggressive';
  };
  market_trends?: string;
}

export interface GenerateStockPredictionsResponse {
  job_id: string;
}

export interface GetStockPredictionsResponse {
  job_id: string;
  predictions: StockPrediction[];
}

// Phase 7: Action Proposal Types
export interface SavePredictionActionRequest {
  prediction_id: string;
  action: 'buy' | 'sell' | 'hold' | 'watch' | 'ignore';
  notes?: string;
}

export interface SavePredictionActionResponse {
  action_id: number;
  prediction_id: string;
  action: 'buy' | 'sell' | 'hold' | 'watch' | 'ignore';
}

// Phase 8: Prediction History & Accuracy Tracking Types
export interface GetPredictionHistoryRequest {
  limit?: number;
  start_date?: string;
  end_date?: string;
  symbol?: string;
}

export interface PredictionHistory {
  prediction_id: string;
  symbol: string;
  predicted_direction: 'up' | 'down' | 'sideways';
  predicted_at: string;
  actual_direction?: 'up' | 'down' | 'sideways';
  actual_change_percent?: number;
  accuracy?: boolean;
  user_action?: 'buy' | 'sell' | 'hold' | 'watch' | 'ignore';
  reasoning: string;
}

export interface AccuracyStats {
  total_predictions: number;
  correct_predictions: number;
  accuracy_rate: number;
}

export interface GetPredictionHistoryResponse {
  predictions: PredictionHistory[];
  accuracy_stats?: AccuracyStats;
}

export interface UpdatePredictionAccuracyRequest {
  prediction_id: string;
  actual_price: number;
  actual_direction: 'up' | 'down' | 'sideways';
}

export interface UpdatePredictionAccuracyResponse {
  success: boolean;
  accuracy_updated: boolean;
}


