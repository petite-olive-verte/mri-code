import { useEffect, useState } from 'react';
import type { HttpClient } from '@/shared/api/http-client';
import { fetchHealth } from '../api/health-client';
import type { HealthReport } from '../model/health-status';

/**
 * A discriminated union, not `{ data, isLoading, error }`.
 *
 * The three-booleans shape makes impossible states representable — loading *and*
 * failed, ready *without* data — and every component then re-derives the real state
 * with a ladder of `if`s. Here the compiler forces the caller to handle exactly one
 * of three cases, and `report` only exists where it is actually available.
 */
export type HealthState =
  | { readonly kind: 'loading' }
  | { readonly kind: 'ready'; readonly report: HealthReport }
  | { readonly kind: 'failed'; readonly message: string };

/**
 * The hook is the seam — this template's "application layer".
 *
 * It orchestrates (call the adapter, track the lifecycle) and holds no business
 * rules: those stay in `model/`. Components below it stay pure views, so the only
 * place React and I/O meet is here.
 *
 * The `http` port comes in as an argument rather than being imported. That is what
 * makes the test below inject a fake without touching the network or `vi.mock`.
 *
 * Scope note: this hand-rolled fetch-in-an-effect is the honest minimum. The moment
 * you have real server state — caching, refetching, invalidation, pagination — adopt
 * TanStack Query and delete this. Re-implementing a cache by hand is the classic way
 * a React codebase rots.
 */
export function useHealth(http: HttpClient): HealthState {
  const [state, setState] = useState<HealthState>({ kind: 'loading' });

  useEffect(() => {
    // An effect that starts async work must be able to cancel it. Without this,
    // a fast unmount (or a changed `http`) leaves a late response racing to set state
    // on a dead component — and under StrictMode's double-invoke in dev, every effect
    // is exercised for exactly this bug.
    const controller = new AbortController();
    setState({ kind: 'loading' });

    fetchHealth(http, controller.signal)
      .then((report) => {
        if (!controller.signal.aborted) {
          setState({ kind: 'ready', report });
        }
      })
      .catch((error: unknown) => {
        if (controller.signal.aborted) {
          return;
        }
        setState({
          kind: 'failed',
          message: error instanceof Error ? error.message : 'Unknown error',
        });
      });

    return () => controller.abort();
  }, [http]);

  return state;
}
