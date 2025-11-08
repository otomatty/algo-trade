/**
 * Tests for ProgressIndicator component - Phase 4
 * 
 * Related Documentation:
 *   ├─ Spec: src/pages/AlgorithmProposal/AlgorithmProposal.spec.md
 *   └─ Plan: docs/03_plans/algorithm-proposal/README.md
 */
import { describe, it, expect, beforeEach, beforeAll, mock } from 'bun:test';
import { render, waitFor, within } from '@testing-library/react';
import { ProgressIndicator } from './ProgressIndicator';
import { MantineProvider } from '@mantine/core';
import { setupDOM, setupDOMSync } from '../../test-utils/dom-setup';

// Setup DOM synchronously before module initialization
setupDOMSync();

// Mock Tauri API
const mockInvoke = mock((_cmd: string, ..._args: any[]) => Promise.resolve({}));

mock.module('@tauri-apps/api/core', () => ({
  invoke: mockInvoke,
}));

describe('ProgressIndicator - Phase 4', () => {
  // Ensure DOM is set up before all tests
  beforeAll(async () => {
    await setupDOM();
  });

  beforeEach(() => {
    mockInvoke.mockClear();
  });

  it('should poll job status and display progress', async () => {
    const jobId = 'test-job-123';
    let callCount = 0;

    mockInvoke.mockImplementation((cmd: string, args?: any) => {
      if (cmd === 'get_proposal_generation_status' && args?.job_id === jobId) {
        callCount++;
        if (callCount === 1) {
          return Promise.resolve({
            status: 'generating',
            progress: 0.5,
            message: 'Generating proposals...',
          });
        } else if (callCount === 2) {
          return Promise.resolve({
            status: 'completed',
            progress: 1.0,
            message: 'Generated 5 proposals',
          });
        }
        return Promise.resolve({
          status: 'completed',
          progress: 1.0,
          message: 'Generated 5 proposals',
        });
      }
      return Promise.resolve({});
    });

    const onCompleted = mock(() => {});

    const { container } = render(
      <MantineProvider>
        <ProgressIndicator jobId={jobId} onCompleted={onCompleted} />
      </MantineProvider>
    );

    // Wait for initial poll
    await waitFor(() => {
      expect(mockInvoke).toHaveBeenCalledWith('get_proposal_generation_status', { job_id: jobId });
    });

    // Wait for status to be displayed
    await waitFor(() => {
      expect(within(container).queryByText(/generating/i)).toBeDefined();
    }, { timeout: 2000 });
  });

  it('should display error when job fails', async () => {
    const jobId = 'test-job-456';

    mockInvoke.mockImplementation((cmd: string, args?: any) => {
      if (cmd === 'get_proposal_generation_status') {
        return Promise.resolve({
          status: 'failed',
          progress: 0.0,
          message: 'Generation failed',
          error: 'LLM API error',
        });
      }
      return Promise.resolve({});
    });

    const onError = mock(() => {});

    const { container } = render(
      <MantineProvider>
        <ProgressIndicator jobId={jobId} onError={onError} />
      </MantineProvider>
    );

    // Wait for error to be displayed
    await waitFor(() => {
      expect(within(container).queryByText(/LLM API error/i)).toBeDefined();
    }, { timeout: 2000 });
  });

  it('should call onCompleted when job completes', async () => {
    const jobId = 'test-job-789';

    mockInvoke.mockImplementation((cmd: string, args?: any) => {
      if (cmd === 'get_proposal_generation_status') {
        return Promise.resolve({
          status: 'completed',
          progress: 1.0,
          message: 'Generated 5 proposals',
        });
      }
      return Promise.resolve({});
    });

    const onCompleted = mock(() => {});

    render(
      <MantineProvider>
        <ProgressIndicator jobId={jobId} onCompleted={onCompleted} />
      </MantineProvider>
    );

    // Wait for onCompleted to be called
    await waitFor(() => {
      expect(onCompleted).toHaveBeenCalled();
    }, { timeout: 2000 });
  });
});

