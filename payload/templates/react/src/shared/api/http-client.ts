/**
 * The one place this template inverts a dependency on purpose.
 *
 * `HttpClient` is a port: features depend on this type, never on `fetch` directly.
 * That single indirection is what lets a hook be tested with a three-line fake
 * instead of a network stub (see `use-health.test.ts`).
 *
 * Resist the urge to generalise this into a repository-per-entity layer. In a
 * frontend the server owns the domain; mirroring its whole API behind hand-written
 * ports buys ceremony, not safety. One seam at the network edge is enough.
 */
export type HttpClient = {
  get<T>(path: string, options?: { signal: AbortSignal }): Promise<T>;
};

export class HttpError extends Error {
  // Written out longhand rather than as constructor parameter properties
  // (`constructor(readonly status: number)`): that shorthand emits runtime code and is
  // banned by `erasableSyntaxOnly` in tsconfig.json.
  readonly status: number;
  readonly path: string;

  constructor(status: number, path: string) {
    super(`GET ${path} failed with HTTP ${status}`);
    this.name = 'HttpError';
    this.status = status;
    this.path = path;
  }
}

/**
 * The production adapter. Note it returns `T` unchecked: `fetch` cannot know the
 * shape of what it parsed. Narrowing `unknown` to a trusted type is the model
 * layer's job (`toHealthReport`), not the transport's — which is why callers here
 * ask for `get<unknown>`.
 */
export function createHttpClient(baseUrl: string): HttpClient {
  return {
    async get<T>(path: string, options?: { signal: AbortSignal }): Promise<T> {
      const response = await fetch(`${baseUrl}${path}`, {
        headers: { Accept: 'application/json' },
        ...(options?.signal ? { signal: options.signal } : {}),
      });

      if (!response.ok) {
        throw new HttpError(response.status, path);
      }

      return (await response.json()) as T;
    },
  };
}
