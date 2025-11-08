# Data Analysis Engine Specification

## Related Files

- Implementation:
  - `src-python/modules/data_analysis/analyzer.py` - Main analyzer
  - `src-python/modules/data_analysis/technical_indicators.py` - Technical indicators
  - `src-python/modules/data_analysis/trend_analyzer.py` - Trend analysis
  - `src-python/modules/data_analysis/statistics.py` - Statistics calculation
- Tests:
  - `src-python/tests/unit/test_analyzer.py`
  - `src-python/tests/unit/test_technical_indicators.py`
  - `src-python/tests/unit/test_trend_analyzer.py`
  - `src-python/tests/unit/test_statistics.py`

## Related Documentation

- Plan: `docs/03_plans/data-analysis/README.md`
- API Spec: `docs/03_plans/data-analysis/api-spec.md`
- Analysis Algorithms: `docs/03_plans/data-analysis/analysis-algorithms.md`

## Requirements

### RQ-001: RSI (Relative Strength Index) Calculation
- Calculate RSI with default period of 14 days
- Formula: RSI = 100 - (100 / (1 + RS))
- RS = Average Gain / Average Loss
- Return current RSI value, average, and signal (overbought/oversold/neutral)
- Overbought: RSI > 70
- Oversold: RSI < 30
- Neutral: 30 <= RSI <= 70

### RQ-002: MACD (Moving Average Convergence Divergence) Calculation
- Calculate MACD line: 12-day EMA - 26-day EMA
- Calculate Signal line: 9-day EMA of MACD line
- Calculate Histogram: MACD - Signal
- Return MACD, signal, histogram, and trend (bullish/bearish/neutral)
- Bullish: MACD > Signal
- Bearish: MACD < Signal
- Neutral: MACD == Signal

### RQ-003: Trend Analysis
- Analyze trend direction (upward/downward/sideways)
- Use moving average slope
- Use price high/low trends
- Return trend direction and confidence level

### RQ-004: Statistics Calculation
- Calculate price range (min, max, current)
- Calculate average volume
- Calculate price change percentage
- Handle edge cases (empty data, single data point)

### RQ-005: Analysis Result Structure
- Structure results according to AnalysisResult type
- Save to `analysis_results` table
- Link to `analysis_jobs` table via job_id

## Test Cases

### TC-001: RSI Calculation with Valid Data
**Given**: OHLCV data with at least 14 data points  
**When**: RSI is calculated  
**Then**: 
- RSI value is between 0 and 100
- Signal is correctly determined (overbought/oversold/neutral)
- Average RSI is calculated correctly

### TC-002: RSI Calculation with Insufficient Data
**Given**: OHLCV data with less than 14 data points  
**When**: RSI is calculated  
**Then**: 
- Returns None or appropriate error
- Handles gracefully without crashing

### TC-003: MACD Calculation with Valid Data
**Given**: OHLCV data with at least 26 data points  
**When**: MACD is calculated  
**Then**: 
- MACD line is calculated correctly
- Signal line is calculated correctly
- Histogram is calculated correctly
- Trend is correctly determined (bullish/bearish/neutral)

### TC-004: MACD Calculation with Insufficient Data
**Given**: OHLCV data with less than 26 data points  
**When**: MACD is calculated  
**Then**: 
- Returns None or appropriate error
- Handles gracefully without crashing

### TC-005: Trend Analysis - Upward Trend
**Given**: OHLCV data showing upward trend  
**When**: Trend is analyzed  
**Then**: 
- Trend direction is 'upward'
- Confidence level is reasonable

### TC-006: Trend Analysis - Downward Trend
**Given**: OHLCV data showing downward trend  
**When**: Trend is analyzed  
**Then**: 
- Trend direction is 'downward'
- Confidence level is reasonable

### TC-007: Trend Analysis - Sideways Trend
**Given**: OHLCV data showing sideways trend  
**When**: Trend is analyzed  
**Then**: 
- Trend direction is 'sideways'
- Confidence level is reasonable

### TC-008: Statistics Calculation
**Given**: OHLCV data  
**When**: Statistics are calculated  
**Then**: 
- Price range (min, max, current) is correct
- Average volume is calculated correctly
- Price change percentage is calculated correctly

### TC-009: Statistics Calculation with Empty Data
**Given**: Empty OHLCV data  
**When**: Statistics are calculated  
**Then**: 
- Returns appropriate error or None
- Handles gracefully without crashing

### TC-010: Full Analysis Pipeline
**Given**: Valid OHLCV data and job_id  
**When**: Full analysis is run  
**Then**: 
- All indicators are calculated
- Results are structured correctly
- Results are saved to database
- Job status is updated to 'completed'

## Technical Details

### Dependencies
- pandas: Data manipulation
- numpy: Numerical calculations
- sqlite3: Database operations

### Data Format
Input OHLCV data format:
```python
[
    {"date": "2023-01-01", "open": 100.0, "high": 105.0, "low": 99.0, "close": 103.0, "volume": 1000000},
    ...
]
```

### Output Format
```python
{
    "analysis_summary": {
        "trend_direction": "upward" | "downward" | "sideways",
        "volatility_level": "low" | "medium" | "high",
        "dominant_patterns": ["pattern1", "pattern2"]
    },
    "technical_indicators": {
        "rsi": {"value": 65.5, "period": 14, "signal": "neutral"},
        "macd": {"macd": 1.2, "signal": 0.8, "histogram": 0.4, "signal_type": "bullish"}
    },
    "statistics": {
        "price_range": {"min": 99.0, "max": 110.0, "current": 103.0},
        "volume_average": 1000000,
        "price_change_percent": 3.0
    }
}
```

