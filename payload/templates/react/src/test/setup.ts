import '@testing-library/jest-dom/vitest';
import { cleanup } from '@testing-library/react';
import { afterEach } from 'vitest';

// Vitest isolates modules per test file, not the DOM between tests in the same file.
// Without this, a second `render` mounts alongside the first and `getByRole` throws on
// duplicate matches — a confusing failure that looks like a component bug.
afterEach(() => {
  cleanup();
});
