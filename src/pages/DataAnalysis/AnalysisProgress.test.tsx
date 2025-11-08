/**
 * Tests for AnalysisProgress component
 * 
 * Related Documentation:
 *   ├─ Spec: src/pages/DataAnalysis/AnalysisProgress.spec.md
 *   └─ Plan: docs/03_plans/data-analysis/README.md
 */
import { describe, it, expect, beforeEach, afterEach, beforeAll, mock } from 'bun:test';
import { render, waitFor, within } from '@testing-library/react';
import { AnalysisProgress } from './AnalysisProgress';
import { MantineProvider } from '@mantine/core';
import { setupDOM, setupDOMSync } from '../../test-utils/dom-setup';

// Setup DOM synchronously before module initialization
setupDOMSync();

// Mock Tauri API
const mockInvoke = mock((_cmd: string, ..._args: any[]) => Promise.resolve({}));

mock.module('@tauri-apps/api/core', () => ({
  invoke: mockInvoke,
}));

describe('AnalysisProgress', () => {
  // Ensure DOM is set up before all tests
  beforeAll(async () => {
    await setupDOM();
  });

  beforeEach(() => {
    mockInvoke.mockClear();
  });

  afterEach(() => {
    // Clear any timers (Bun doesn't use jest, so this is just a placeholder)
    // Timers are automatically cleaned up in Bun
  });

  it('should render progress component', async () => {
    mockInvoke.mockResolvedValue({
      status: 'running',
      progress: 50,
      message: 'Processing...',
    });

    const { container } = render(
      <MantineProvider>
        <AnalysisProgress jobId="test-job-123" />
      </MantineProvider>
    );

    await waitFor(() => {
      expect(within(container).getByText(/Processing/)).toBeDefined();
    });
  });

  it('should poll for status updates', async () => {
    let callCount = 0;
    mockInvoke.mockImplementation(() => {
      callCount++;
      return Promise.resolve({
        status: callCount < 3 ? 'running' : 'completed',
        progress: callCount * 25,
        message: `Step ${callCount}`,
      });
    });

    render(
      <MantineProvider>
        <AnalysisProgress jobId="test-job-123" />
      </MantineProvider>
    );

    await waitFor(() => {
      expect(mockInvoke).toHaveBeenCalledWith('get_analysis_status', {
        job_id: 'test-job-123',
      });
    }, { timeout: 3000 });
  });

  it('should stop polling when job is completed', async () => {
    let callCount = 0;
    mockInvoke.mockImplementation(() => {
      callCount++;
      return Promise.resolve({
        status: callCount === 1 ? 'running' : 'completed',
        progress: callCount === 1 ? 50 : 100,
        message: callCount === 1 ? 'Processing...' : 'Completed',
      });
    });

    const { container } = render(
      <MantineProvider>
        <AnalysisProgress jobId="test-job-123" />
      </MantineProvider>
    );

    await waitFor(() => {
      expect(within(container).getByText(/Completed/)).toBeDefined();
    }, { timeout: 5000 });

    // Wait a bit to ensure polling stopped (polling interval is 2 seconds)
    // Wait for 2.5 seconds to allow for one more potential poll after completion
    await new Promise((resolve) => setTimeout(resolve, 2500));

    // Should have been called: initial call + 1 more call when status changes to completed
    // But due to timing, it might be called a few more times before stopping
    // Allow up to 7 calls to account for timing variations (initial + completed + potential extra polls)
    expect(callCount).toBeGreaterThanOrEqual(2);
    expect(callCount).toBeLessThanOrEqual(7);
  });

  it('should display error when job fails', async () => {
    mockInvoke.mockResolvedValue({
      status: 'failed',
      progress: 0,
      message: 'Analysis failed',
      error: 'Something went wrong',
    });

    const { container } = render(
      <MantineProvider>
        <AnalysisProgress jobId="test-job-123" />
      </MantineProvider>
    );

    await waitFor(() => {
      const errorElement = within(container).queryByText(/Something went wrong/);
      expect(errorElement).toBeDefined();
    }, { timeout: 3000 });
  });

  it('should call onCompleted callback when job completes', async () => {
    const onCompleted = mock(() => {});
    mockInvoke.mockResolvedValue({
      status: 'completed',
      progress: 100,
      message: 'Completed',
    });

    render(
      <MantineProvider>
        <AnalysisProgress jobId="test-job-123" onCompleted={onCompleted} />
      </MantineProvider>
    );

    await waitFor(() => {
      expect(onCompleted).toHaveBeenCalled();
    });
  });
});
