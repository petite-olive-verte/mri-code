import { HealthPanel, useHealth } from '@/features/health';
import { createHttpClient } from '@/shared/api/http-client';

/**
 * The composition root: the single place that picks concrete implementations and wires
 * them to features. Everything below takes its dependencies as arguments, which is what
 * keeps them testable.
 *
 * The client is built once at module scope on purpose. Creating it inside the component
 * would hand `useHealth` a new object identity on every render, and its `[http]` effect
 * would refetch forever — the most common self-inflicted infinite loop in React.
 *
 * When wiring outgrows one line, move it into a Context provider rather than importing
 * the client from deep inside features: a module-level import is a dependency you cannot
 * substitute in a test.
 */
const http = createHttpClient(import.meta.env.VITE_API_BASE_URL ?? '');

export function App() {
  const state = useHealth(http);

  return (
    <main>
      <h1>__PROJECT_NAME__</h1>
      <HealthPanel state={state} />
    </main>
  );
}
