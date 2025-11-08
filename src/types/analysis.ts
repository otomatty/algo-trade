/**
 * Data Analysis Types
 * 
 * Related Documentation:
 * - Plan: docs/03_plans/data-analysis/README.md
 */

export interface AnalysisJob {
  job_id: string;
  data_set_id: number;
  status: 'pending' | 'running' | 'completed' | 'failed';
  progress: number;
  message: string | null;
  error: string | null;
  created_at: string;
  completed_at: string | null;
}

export interface AnalysisResult {
  id: number;
  job_id: string;
  data_set_id: number;
  analysis_summary: AnalysisSummary;
  technical_indicators: TechnicalIndicators;
  statistics: Statistics;
  created_at: string;
}

export interface AnalysisSummary {
  trend_direction: 'upward' | 'downward' | 'sideways';
  volatility_level: 'low' | 'medium' | 'high';
  dominant_patterns: string[];
}

export interface TechnicalIndicators {
  rsi?: RSIResult;
  macd?: MACDResult;
  sma?: SMAResult[];
  ema?: EMAResult[];
  bollinger_bands?: BollingerBandsResult;
}

export interface RSIResult {
  value: number;
  period: number;
  signal: 'overbought' | 'oversold' | 'neutral';
}

export interface MACDResult {
  macd: number;
  signal: number;
  histogram: number;
  signal_type: 'bullish' | 'bearish' | 'neutral';
}

export interface SMAResult {
  period: number;
  value: number;
}

export interface EMAResult {
  period: number;
  value: number;
}

export interface BollingerBandsResult {
  upper: number;
  middle: number;
  lower: number;
  period: number;
}

export interface Statistics {
  price_range: {
    min: number;
    max: number;
    current: number;
  };
  volume_average: number;
  price_change_percent: number;
}

