# __PROJECT_NAME__

__PROJECT_DESCRIPTION__

## Development

```bash
corepack enable             # once per machine: provides the pinned pnpm
pnpm install                # install dependencies
pnpm dev                    # run the app (http://localhost:5173)

pnpm test                   # run the tests (Vitest)
pnpm typecheck              # type-check (tsc --noEmit)
pnpm lint                   # lint + format check (Biome)
pnpm format                 # apply lint fixes + formatting
pnpm check                  # lint + typecheck + tests (CI gate)
```

## Layout

Code is organised **by feature**, not by technical role. A feature owns its model, its
hooks and its components, and exposes them through a single `index.ts`.

```
src/
  app/          # composition root: wiring, providers, routing
  features/
    health/     # one folder per feature — the unit of ownership
      model/      # pure TypeScript: rules, types, parsing. No React.
      api/        # outbound adapters — talk to the port, parse via model/
      hooks/      # the seam: orchestration + lifecycle. React lives here.
      components/ # views. Props in, JSX out.
      index.ts    # public API — the only entry point other code may import
  shared/
    api/        # the HttpClient port + its fetch adapter
    ui/         # design-system primitives, used by any feature
    lib/        # framework-agnostic helpers
  test/         # test setup
```

## The four rules

1. **Logic is pure.** Anything in `model/` imports neither React nor I/O. It is tested
   without a DOM and without mocks — that is where the bulk of your tests belong.
2. **Hooks are the seam.** They orchestrate; they hold no business rules. Dependencies
   (the `HttpClient` port) arrive as arguments, so tests inject a fake.
3. **Components are views.** They receive state as props and render it. A component that
   fetches its own data cannot be tested without mocks — push the fetch up into a hook.
4. **Features talk through `index.ts`.** No cross-feature deep imports, ever. Shared code
   moves to `shared/`; features never import each other.

Follow those four and the layout stays honest as it grows. The day a genuinely rich
client-side domain appears (offline sync, an editor, a scheduling engine), `model/` is
already the domain layer — promoting it to a full hexagonal core is mechanical.

## What is deliberately absent

No router, no state manager, no data-fetching library. They are real dependencies with
real trade-offs and the right choice depends on the app:

- **Server state** (anything that lives in a database): reach for **TanStack Query**
  before hand-rolling a cache. `useHealth` is the honest minimum, not a pattern to copy
  across twenty endpoints.
- **Client state**: `useState` and Context cover more than people expect. Add Zustand or
  Redux Toolkit when you can name the problem they solve for you.
- **Routing**: React Router or TanStack Router — pick when the app has a second screen.
