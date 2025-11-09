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

