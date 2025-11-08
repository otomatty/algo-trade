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
}

export interface AssociationStep {
  step: number;
  concept: string;
  connection: string;
}

