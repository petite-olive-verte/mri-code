- **Node ≥ 22.12** (the floor Vite 8 requires); **pnpm** via corepack, pinned in `packageManager`.
- **React 19** + **Vite 8** — SPA, no meta-framework unless the spec calls for SSR.
- **TypeScript 7**, `strict` plus `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`,
  `verbatimModuleSyntax` and `erasableSyntaxOnly` — no `any`, no non-null assertions (`!`).
- **Biome** for lint *and* format (one tool, one config) — `pnpm lint`; type checking via
  `pnpm typecheck` (`tsc --noEmit`).
- **Vitest** + **Testing Library** for tests (`pnpm test`); query by accessible role, never by test id.
- Logic lives in pure TypeScript (`model/`), free of React; hooks orchestrate; components render.
- **Layout**: organise **by feature**, not by technical role, under `src/features/<feature>/`. Each
  feature exposes a public API via `index.ts`.
- **Naming**: `PascalCase` for components and their files, `camelCase` for hooks (`useX`) and
  variables; one unit `foo.ts` ↔ one test file `foo.test.ts` **next to it**, not in a mirror tree.
