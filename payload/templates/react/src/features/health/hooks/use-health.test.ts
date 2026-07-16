import { renderHook, waitFor } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import type { HttpClient } from '@/shared/api/http-client';
import { useHealth } from './use-health';

/**
 * The payoff of taking `HttpClient` as an argument: the fakes below are one line each,
 * the tests touch no network, and there is no `vi.mock` hoisting to reason about.
 *
 * Compare with a hook that calls `fetch` directly — you would be stubbing a global, and
 * every test in the file would share that mutable state.
 */

// `get` is generic (`get<T>(): Promise<T>`), so any concrete fake has to assert its way
// out of that promise. `as never` is the narrowest way to say "trust me" here, and it is
// confined to test doubles — production code never casts like this.
function httpReturning(payload: unknown): HttpClient {
  return { get: async () => payload as never };
}

function httpFailingWith(error: Error): HttpClient {
  return { get: () => Promise.reject(error) };
}

function httpNeverResolving(): HttpClient {
  return { get: () => new Promise(() => {}) };
}

/**
 * Note where the fake is built: on the line *before* `renderHook`, never inside its
 * callback. `useHealth` keys its effect on `[http]`, so a client constructed inside the
 * callback would be a new object on every render — the effect would re-run, set state,
 * trigger a render, build another client, and loop until the heap dies.
 *
 * This is the same rule App.tsx follows by creating the client at module scope, and it
 * is the most common self-inflicted infinite loop in React. Passing dependencies by
 * argument makes the constraint explicit: the caller owns the identity.
 */
describe('useHealth', () => {
  it('starts in the loading state', () => {
    const http = httpNeverResolving();

    const { result } = renderHook(() => useHealth(http));

    expect(result.current).toEqual({ kind: 'loading' });
  });

  it('exposes the parsed report once the call resolves', async () => {
    const http = httpReturning({ status: 'ok' });

    const { result } = renderHook(() => useHealth(http));

    await waitFor(() => {
      expect(result.current).toEqual({
        kind: 'ready',
        report: { status: 'ok', label: 'All systems operational' },
      });
    });
  });

  it('reports a rejected call as failed rather than throwing', async () => {
    const http = httpFailingWith(new Error('network down'));

    const { result } = renderHook(() => useHealth(http));

    await waitFor(() => {
      expect(result.current).toEqual({ kind: 'failed', message: 'network down' });
    });
  });

  it('treats a malformed payload as a failure, not as data', async () => {
    // The model's parser rejects the unknown status, so the UI never sees a bad value.
    const http = httpReturning({ status: 'exploded' });

    const { result } = renderHook(() => useHealth(http));

    await waitFor(() => {
      expect(result.current).toMatchObject({ kind: 'failed' });
    });
  });
});
