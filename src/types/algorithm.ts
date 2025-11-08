/**
 * Algorithm Proposal Types
 * 
 * Related Documentation:
 * - Plan: docs/03_plans/algorithm-proposal/README.md
 * - Data Model: docs/03_plans/algorithm-proposal/data-model.md
 */

export interface AlgorithmProposal {
  proposal_id: string;
  name: string;
  description: string;
  rationale: string;
  expected_performance?: ExpectedPerformance;
  definition: AlgorithmDefinition;
  confidence_score?: number;
  created_at: string;
}

export interface ExpectedPerformance {
  expected_return?: number;
  risk_level?: 'low' | 'medium' | 'high';
}

export interface AlgorithmDefinition {
  triggers: TriggerDefinition[];
  actions: ActionDefinition[];
}

export interface TriggerDefinition {
  type: 'rsi' | 'macd' | 'price' | 'volume' | 'moving_average' | string;
  condition: TriggerCondition;
  logical_operator?: 'AND' | 'OR';
}

export interface TriggerCondition {
  operator: 'gt' | 'lt' | 'gte' | 'lte' | 'eq' | 'between' | 'cross_above' | 'cross_below';
  value: number | [number, number];
  period?: number;
  indicator?: string;
}

export interface ActionDefinition {
  type: 'buy' | 'sell' | 'hold';
  parameters: ActionParameters;
  execution_type?: 'market' | 'limit' | 'stop';
}

export interface ActionParameters {
  quantity?: number;
  percentage?: number;
  stop_loss?: number;
  take_profit?: number;
  limit_price?: number;
}

export interface UserPreferences {
  risk_tolerance?: 'low' | 'medium' | 'high';
  trading_frequency?: 'low' | 'medium' | 'high';
  preferred_indicators?: string[];
}

export interface ProposalGenerationJob {
  job_id: string;
  data_set_id: number;
  analysis_id: number | null;
  num_proposals: number;
  user_preferences: UserPreferences | null;
  status: 'pending' | 'analyzing' | 'generating' | 'completed' | 'failed';
  progress: number;
  message: string | null;
  error: string | null;
  created_at: string;
  completed_at: string | null;
}

export interface Algorithm {
  id: number;
  name: string;
  description: string | null;
  definition: AlgorithmDefinition;
  proposal_id: string | null;
  created_at: string;
  updated_at: string;
}

