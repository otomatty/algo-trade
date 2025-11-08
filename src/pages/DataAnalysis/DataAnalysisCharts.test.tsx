/**
 * Tests for DataAnalysisCharts component
 * 
 * Related Documentation:
 *   ├─ Spec: src/pages/DataAnalysis/DataAnalysisCharts.spec.md
 *   └─ Plan: docs/03_plans/data-analysis/README.md
 */
import { describe, it, expect, beforeAll } from 'bun:test';
import { render } from '@testing-library/react';
import { DataAnalysisCharts } from './DataAnalysisCharts';
import { MantineProvider } from '@mantine/core';
import { setupDOM, setupDOMSync } from '../../test-utils/dom-setup';

// Setup DOM synchronously before module initialization
setupDOMSync();

describe('DataAnalysisCharts', () => {
  // Ensure DOM is set up before all tests
  beforeAll(async () => {
    await setupDOM();
  });
  
  const mockResult = {
    id: 1,
    job_id: 'test-job-123',
    data_set_id: 1,
    analysis_summary: {
      trend_direction: 'upward' as const,
      volatility_level: 'medium' as const,
      dominant_patterns: ['higher_highs'],
    },
    technical_indicators: {
      rsi: {
        value: 65.5,
        period: 14,
        signal: 'neutral' as const,
      },
      macd: {
        macd: 1.2,
        signal: 0.8,
        histogram: 0.4,
        signal_type: 'bullish' as const,
      },
    },
    statistics: {
      price_range: {
        min: 99.0,
        max: 110.0,
        current: 103.0,
      },
      volume_average: 1000000,
      price_change_percent: 3.0,
    },
    created_at: '2023-01-01T00:00:00',
  };

  it('should render charts component', () => {
    const { container } = render(
      <MantineProvider>
        <DataAnalysisCharts result={mockResult} />
      </MantineProvider>
    );

    // Check if component rendered by looking for text content
    expect(container.textContent).toContain('RSI Indicator');
    expect(container.textContent).toContain('MACD Indicator');
    expect(container.textContent).toContain('Price Range');
  });
});

