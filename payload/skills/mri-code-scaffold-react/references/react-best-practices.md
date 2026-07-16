# React + TypeScript (latest stable) — best practices (enforced conventions)

> The rules the implementation must follow on a React project. Most are **enforced** by Biome and
> TypeScript's strict flags; the rest are review criteria. Keep the logic free of the framework —
> the constitution's "dependencies point inward" applies here too, with `model/` as the inward core.

## TypeScript

- **No `any`** (Biome `noExplicitAny`) and **no `!` non-null assertions** (`noNonNullAssertion`).
  Narrow with a guard or throw explicitly — an assertion is a promise nothing verifies.
- **No `enum`**, no namespaces, no constructor parameter properties: they emit runtime code and are
  banned by `erasableSyntaxOnly`. Model a closed set as a const tuple + derived union.
- **`import type`** for type-only imports (`verbatimModuleSyntax` enforces it).
- Type the **boundary**, not the interior: parse `unknown` into a trusted type once, at the edge
  (`toHealthReport`). Downstream code then needs no defensive checks. Reach for zod/valibot when
  payloads grow — the boundary stays in the same place.
- Prefer **`type`** over `interface` for data shapes (no accidental declaration merging).
- Derive types rather than restating them: `(typeof HEALTH_STATUSES)[number]`, `ReturnType<…>`.

```ts
// A closed set: erasable, iterable at runtime, exhaustive at compile time.
export const ORDER_STATUSES = ['pending', 'paid', 'cancelled'] as const;
export type OrderStatus = (typeof ORDER_STATUSES)[number];

export function isTerminal(status: OrderStatus): boolean {
  switch (status) {
    case 'paid':
    case 'cancelled':
      return true;
    case 'pending':
      return false;
  }
  // No `default`: adding a status breaks compilation here, which is the point.
}
```

## State

- **Make impossible states unrepresentable.** Model async state as a discriminated union, never as
  `{ data, isLoading, error }` — that shape allows "loading and failed at once" and forces every
  consumer to re-derive the truth.
- **Derive, don't duplicate.** If a value is computable from props/state, compute it during render.
  A `useState` + `useEffect` pair that mirrors a prop is a bug waiting to desynchronise.
- **`useState` first.** Context for wiring that crosses the tree; a store (Zustand, Redux Toolkit)
  only when you can name the problem it solves. Most "we need global state" is server state.
- **Server state is not client state.** Anything owned by a database belongs in **TanStack Query**,
  not in `useState` + `useEffect`. Hand-rolling a cache is how a React codebase rots.

```ts
type Result<T> =
  | { readonly kind: 'loading' }
  | { readonly kind: 'ready'; readonly value: T }
  | { readonly kind: 'failed'; readonly message: string };
```

## Effects

- **Most code is not an effect.** No effect for: deriving values, transforming data for render, or
  handling a user event (that is the event handler's job). An effect synchronises with something
  *outside* React.
- **Every effect that starts async work cleans up** — `AbortController` or a cancelled flag.
  Otherwise a late response races to set state on a dead component.
- **Dependencies are not negotiable** (Biome `useExhaustiveDependencies`). If the lint fights you,
  the design is wrong — move the value out, or into a ref, or use the updater form of `setState`.
- **Stable identities.** Objects/functions passed as dependencies must be created outside render
  (module scope, `useMemo`, `useCallback`). A new object per render + a `[dep]` effect = infinite loop.
- **Keep `StrictMode`.** Its double-invoke in dev exists to surface exactly the two bugs above.

## Components

- **Components are views**: props in, JSX out. A component that fetches its own data cannot be tested
  without mocks — push the I/O up into a hook.
- **Hooks are the seam**: they orchestrate and hold lifecycle, never business rules.
- **Inject dependencies as arguments** (the `HttpClient` port), don't import them deep inside a
  feature — a module-level import is a dependency you cannot substitute in a test.
- **`key` is identity**, not a loop counter. Never `key={index}` on a reorderable list.
- Colocate: a component lives next to its test, its hook and its model, inside its feature.
- **React Compiler** (`babel-plugin-react-compiler`) is stable — adopt it *instead of* scattering
  `useMemo`/`useCallback` for performance. Do not hand-memoize preemptively.

## Boundaries

- **One folder per feature**, owning `model/` · `api/` · `hooks/` · `components/` · `index.ts`.
- **`index.ts` is the only public surface.** Cross-feature deep imports (`@/features/x/model/y`) are
  a review failure: the day they are allowed, "feature" stops meaning anything.
- **Features never import each other.** Shared code moves to `shared/`.
- **`model/` imports neither React nor I/O.** This is the rule that carries the architecture.
- Wiring lives in `app/` — the composition root, and the only place that names concrete
  implementations.

## Tests & tooling

- **Vitest** + **Testing Library**. The bulk of tests should be pure `model/` tests: no DOM, no mocks,
  milliseconds.
- **Query by accessible role** (`getByRole('status')`), never by test id or class. The test then fails
  when the UI stops being usable, not when styling changes.
- **Prefer fakes to mocks.** A three-line fake `HttpClient` beats `vi.mock` hoisting and shared global
  state. Use **MSW** when you need HTTP-level fidelity.
- `userEvent` over `fireEvent` — it models what a user actually does.
- **`pnpm check`** (lint + typecheck + tests) is the gate; it must be green before review.

## Accessibility & performance

- Semantic elements before ARIA: a `<button>` beats `<div role="button" tabIndex={0}>`.
- Live regions (`role="status"`, `role="alert"`) for async state changes — otherwise the update is
  invisible to a screen reader.
- Every interactive element reachable and operable by keyboard; visible focus.
- Only variables prefixed `VITE_` reach the client, and everything that reaches it is public. Secrets
  live on a server.
- Measure before optimising: `vite build` reports bundle size; lazy-load routes with `React.lazy`
  when a chunk actually hurts.
