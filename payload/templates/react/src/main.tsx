import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { App } from './app/App';

const container = document.getElementById('root');

// Not `document.getElementById('root')!`. Non-null assertions are banned by biome.jsonc
// for a reason: they are a promise to the compiler that nothing verifies. An explicit
// throw fails loudly at the one place the assumption is actually made.
if (!container) {
  throw new Error('Missing #root element in index.html');
}

// StrictMode double-invokes effects and renders in development — deliberately. It is a
// bug detector, not overhead: it surfaces missing effect cleanups and render-phase side
// effects now, instead of as a race in production. Never remove it to silence a warning.
createRoot(container).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
