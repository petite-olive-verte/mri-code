import type { HttpClient } from '@/shared/api/http-client';
import { type HealthReport, toHealthReport } from '../model/health-status';

/**
 * The feature's outbound adapter: it knows the endpoint and hands the raw payload to
 * the model for parsing. It stays a plain function taking the port as an argument —
 * no module-level client, no singleton — so tests inject a fake and nothing global
 * needs resetting between them.
 */
export async function fetchHealth(http: HttpClient, signal?: AbortSignal): Promise<HealthReport> {
  const payload = await http.get<unknown>('/health', signal ? { signal } : undefined);
  return toHealthReport(payload);
}
