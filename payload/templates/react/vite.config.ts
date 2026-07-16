import { fileURLToPath } from 'node:url';
import react from '@vitejs/plugin-react';
import type { Plugin } from 'vite';
import { defineConfig } from 'vitest/config';

/**
 * Dev-only stub for `GET /health`, so `pnpm dev` is green before any backend exists.
 * Without it Vite's SPA fallback answers `/health` with index.html, and the panel reports
 * a baffling JSON parse error on a fresh clone.
 *
 * `apply: 'serve'` keeps it out of `vite build` — production never ships a stub. Delete
 * this plugin and its entry in `plugins` as soon as VITE_API_BASE_URL points at a real
 * API. For anything beyond one endpoint, use MSW rather than growing this.
 */
function healthStub(): Plugin {
  return {
    name: 'health-stub',
    apply: 'serve',
    configureServer(server) {
      server.middlewares.use('/health', (_req, res) => {
        res.setHeader('Content-Type', 'application/json');
        res.end(JSON.stringify({ status: 'ok' }));
      });
    },
  };
}

// `vitest/config` re-exports Vite's `defineConfig` with the `test` key typed, so the
// dev server, the build and the test runner all read one config and one module graph.
// A component therefore resolves the same way in a test as it does in the browser.
export default defineConfig({
  plugins: [react(), healthStub()],
  resolve: {
    // Mirrors `compilerOptions.paths` in tsconfig.json — TypeScript resolves the alias
    // for the editor, Vite resolves it at runtime. Both must agree.
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  test: {
    environment: 'jsdom',
    setupFiles: ['./src/test/setup.ts'],
    // No `globals: true`. Importing `describe`/`it`/`expect` explicitly keeps test files
    // honest ESM and lets the type-checker see them without ambient declarations.
    globals: false,
    include: ['src/**/*.test.{ts,tsx}'],
    coverage: {
      provider: 'v8',
      include: ['src/**/*.{ts,tsx}'],
      // Entry points and generated artifacts have no logic worth covering; counting them
      // only dilutes the signal.
      exclude: ['src/main.tsx', 'src/test/**', 'src/**/*.test.{ts,tsx}', 'src/**/index.ts'],
    },
  },
});
