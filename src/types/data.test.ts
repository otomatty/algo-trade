/**
 * Tests for data type definitions
 */
import { describe, it, expect } from 'bun:test';
import type { DataSet, OHLCVData } from './data';

describe('Data Types', () => {
  describe('DataSet', () => {
    it('should have required fields', () => {
      const dataSet: DataSet = {
        id: 1,
        name: 'Test Dataset',
        symbol: 'AAPL',
        start_date: '2023-01-01',
        end_date: '2023-12-31',
        record_count: 252,
        imported_at: '2023-01-01T00:00:00',
        source: 'csv',
        created_at: '2023-01-01T00:00:00',
      };

      expect(dataSet.id).toBe(1);
      expect(dataSet.name).toBe('Test Dataset');
      expect(dataSet.source).toBe('csv');
    });

    it('should allow null symbol', () => {
      const dataSet: DataSet = {
        id: 1,
        name: 'Test Dataset',
        symbol: null,
        start_date: null,
        end_date: null,
        record_count: 0,
        imported_at: '2023-01-01T00:00:00',
        source: 'csv',
        created_at: '2023-01-01T00:00:00',
      };

      expect(dataSet.symbol).toBeNull();
    });
  });

  describe('OHLCVData', () => {
    it('should have all OHLCV fields', () => {
      const ohlcv: OHLCVData = {
        id: 1,
        data_set_id: 1,
        date: '2023-01-01',
        open: 100.0,
        high: 105.0,
        low: 99.0,
        close: 103.0,
        volume: 1000000,
      };

      expect(ohlcv.open).toBe(100.0);
      expect(ohlcv.high).toBe(105.0);
      expect(ohlcv.low).toBe(99.0);
      expect(ohlcv.close).toBe(103.0);
      expect(ohlcv.volume).toBe(1000000);
    });
  });
});

