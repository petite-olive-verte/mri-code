import type { HealthState } from '../hooks/use-health';

type HealthPanelProps = {
  readonly state: HealthState;
};

/**
 * A view, and nothing else: no fetching, no `useEffect`, no knowledge of where its
 * state came from. It takes the union and renders one branch per case.
 *
 * Because the state arrives as a prop, its test needs no mock, no provider and no
 * fake timers — it passes the three states in directly. Components that fetch their
 * own data cannot be tested that way, which is the whole reason the fetch lives in a
 * hook one level up.
 *
 * Note the absence of a `default:` branch. `HealthState` is a closed union, so if a
 * fourth case is ever added, this switch stops compiling — the type-checker points at
 * every place that must handle it. A `default` would silently swallow that.
 */
export function HealthPanel({ state }: HealthPanelProps) {
  switch (state.kind) {
    case 'loading':
      // `role="status"` / `role="alert"` are not decoration: they make the state
      // audible to screen readers and let tests query by role, the way a user
      // perceives the UI rather than by CSS class.
      return <p role="status">Checking service health…</p>;

    case 'failed':
      return <p role="alert">Health check failed: {state.message}</p>;

    case 'ready':
      return (
        <p role="status" data-status={state.report.status}>
          {state.report.label}
        </p>
      );
  }
}
