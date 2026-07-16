/// <reference types="vite/client" />

/**
 * Declare every env var the app reads. Vite's own `ImportMetaEnv` carries an index
 * signature, so without this file `import.meta.env.VITE_TYPO` type-checks happily and
 * fails at runtime. Listing them here turns a missing variable into a compile error and
 * doubles as the documented contract with `.env.example`.
 */
interface ImportMetaEnv {
  readonly VITE_API_BASE_URL?: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
