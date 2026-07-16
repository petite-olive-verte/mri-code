/**
 * The feature's public API — the real modularity boundary in a React codebase.
 *
 * Everything outside `features/health/` imports from `@/features/health` and nothing
 * else. Reaching into `@/features/health/model/health-status` from another feature is
 * the thing to forbid in review: the day it is allowed, "feature" stops meaning
 * anything and you are back to a folder of files that all know each other.
 *
 * Keeping this surface deliberately small is what lets the feature's internals be
 * rewritten without a cross-repo refactor. If two features need to share code, it
 * moves to `shared/` — they never import each other.
 */
export { HealthPanel } from './components/HealthPanel';
export type { HealthState } from './hooks/use-health';
export { useHealth } from './hooks/use-health';
export type { HealthReport, HealthStatus } from './model/health-status';
