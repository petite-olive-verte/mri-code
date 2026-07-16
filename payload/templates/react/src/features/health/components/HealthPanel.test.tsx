import { render, screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import { HealthPanel } from './HealthPanel';

/**
 * Zero mocks. The component takes its state as a prop, so each case is one line of
 * setup. Queries go through accessible roles rather than test ids: the test then
 * fails when the UI stops being usable, not when a class name changes.
 */
describe('HealthPanel', () => {
  it('announces that the check is in flight', () => {
    render(<HealthPanel state={{ kind: 'loading' }} />);

    expect(screen.getByRole('status')).toHaveTextContent(/checking/i);
  });

  it('renders the report label when ready', () => {
    render(
      <HealthPanel
        state={{ kind: 'ready', report: { status: 'ok', label: 'All systems operational' } }}
      />,
    );

    expect(screen.getByRole('status')).toHaveTextContent('All systems operational');
  });

  it('surfaces a failure as an alert', () => {
    render(<HealthPanel state={{ kind: 'failed', message: 'network down' }} />);

    expect(screen.getByRole('alert')).toHaveTextContent('network down');
  });
});
