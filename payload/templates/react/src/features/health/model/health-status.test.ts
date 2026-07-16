import { describe, expect, it } from 'vitest';
import { HEALTH_STATUSES, isHealthStatus, labelFor, toHealthReport } from './health-status';

/**
 * Model tests: no `render`, no jsdom, no mocks — just functions. This is what the
 * "keep the logic pure" rule buys you, and it is why the bulk of a feature's tests
 * should look like this file rather than like a component test.
 */
describe('labelFor', () => {
  it.each(HEALTH_STATUSES)('returns a non-empty label for %s', (status) => {
    expect(labelFor(status)).not.toBe('');
  });
});

describe('isHealthStatus', () => {
  it('accepts a known status', () => {
    expect(isHealthStatus('ok')).toBe(true);
  });

  it.each([['unknown'], [null], [42], [undefined]])('rejects %s', (value) => {
    expect(isHealthStatus(value)).toBe(false);
  });
});

describe('toHealthReport', () => {
  it('maps a valid payload to a report', () => {
    expect(toHealthReport({ status: 'degraded' })).toEqual({
      status: 'degraded',
      label: 'Running with degraded performance',
    });
  });

  it('rejects an unknown status rather than letting it reach the UI', () => {
    expect(() => toHealthReport({ status: 'exploded' })).toThrow(/unknown status/);
  });

  it('rejects a payload that is not an object', () => {
    expect(() => toHealthReport('ok')).toThrow(/expected an object/);
  });
});
