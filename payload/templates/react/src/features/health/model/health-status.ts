/**
 * The feature's model layer: pure TypeScript, no React import, no I/O.
 *
 * This is the rule that carries most of the architecture's value. Logic that lives
 * here is tested without a DOM, without mocks and without a renderer — in
 * milliseconds. Everything else in the feature (hooks, components, api) is an
 * adapter around this core. If you ever need to move this app to another renderer,
 * or share it with React Native, this is the part that survives untouched.
 */

/**
 * A closed set of states. The idiomatic PHP/Java answer is an `enum`; in modern
 * TypeScript it is a const tuple plus a derived union type.
 *
 * TS `enum` is deliberately avoided: it emits runtime code, so it is banned by
 * `erasableSyntaxOnly` in tsconfig.json, and its nominal typing surprises people.
 * The const-tuple form is erasable, gives an exhaustive union for free, and — unlike
 * an enum — leaves the values iterable at runtime (see `isHealthStatus`).
 */
export const HEALTH_STATUSES = ['ok', 'degraded', 'down'] as const;

export type HealthStatus = (typeof HEALTH_STATUSES)[number];

export type HealthReport = {
  readonly status: HealthStatus;
  readonly label: string;
};

/** Behaviour lives next to the data it describes, exactly as it would on an enum. */
export function labelFor(status: HealthStatus): string {
  switch (status) {
    case 'ok':
      return 'All systems operational';
    case 'degraded':
      return 'Running with degraded performance';
    case 'down':
      return 'Service unavailable';
  }
}

/**
 * Type guard — the boundary between "data we received" and "data we trust".
 */
export function isHealthStatus(value: unknown): value is HealthStatus {
  return typeof value === 'string' && HEALTH_STATUSES.some((status) => status === value);
}

/**
 * Parse, don't validate: the payload crosses the boundary as `unknown` and comes out
 * as a `HealthReport` — or not at all. Every downstream consumer is then statically
 * guaranteed a valid status, so no component ever needs a defensive check.
 *
 * A schema library (zod, valibot) is the natural upgrade once payloads grow; the
 * boundary stays exactly here.
 */
export function toHealthReport(payload: unknown): HealthReport {
  if (typeof payload !== 'object' || payload === null || !('status' in payload)) {
    throw new Error('Malformed health payload: expected an object with a `status` field.');
  }

  const { status } = payload as { status: unknown };
  if (!isHealthStatus(status)) {
    throw new Error(`Malformed health payload: unknown status ${JSON.stringify(status)}.`);
  }

  return { status, label: labelFor(status) };
}
