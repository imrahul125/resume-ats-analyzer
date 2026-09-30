/** Small, centralized frontend client for the ResumeLens API. */

const configuredBaseUrl = import.meta.env.VITE_API_BASE_URL?.trim()

export const API_BASE_URL = (
  configuredBaseUrl || 'http://127.0.0.1:8000'
).replace(/\/+$/, '')

interface DatabaseHealthResponse {
  status: 'ok'
}

export async function checkDatabaseHealth(): Promise<DatabaseHealthResponse> {
  const response = await fetch(`${API_BASE_URL}/health/database`, {
    headers: { Accept: 'application/json' },
  })

  if (!response.ok) {
    throw new Error(`Database health check returned HTTP ${response.status}`)
  }

  const result: unknown = await response.json()
  if (
    typeof result !== 'object' ||
    result === null ||
    !('status' in result) ||
    result.status !== 'ok'
  ) {
    throw new Error('Database health response had an unexpected shape')
  }

  return result as DatabaseHealthResponse
}
