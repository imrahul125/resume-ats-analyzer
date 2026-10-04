/** Small, centralized frontend client for the ResumeLens API. */

const configuredBaseUrl = import.meta.env.VITE_API_BASE_URL?.trim()
const defaultBaseUrl = import.meta.env.PROD
  ? 'https://resumelens-api-mbxb.onrender.com'
  : 'http://127.0.0.1:8000'

export const API_BASE_URL = (
  configuredBaseUrl || defaultBaseUrl
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
import type { AnalysisResult } from '../types/analysis'


interface AnalyzeRequest {
  file: File
  jobDescription: string
  jobTitle?: string
  company?: string
}

export async function analyzeResume(input: AnalyzeRequest): Promise<AnalysisResult> {
  const body = new FormData()
  body.append('resume_file', input.file)
  body.append('job_description', input.jobDescription)
  if (input.jobTitle?.trim()) body.append('job_title', input.jobTitle.trim())
  if (input.company?.trim()) body.append('company', input.company.trim())

  const response = await fetch(`${API_BASE_URL}/api/v1/analyze`, {
    method: 'POST',
    headers: { Accept: 'application/json' },
    body,
  })
  if (!response.ok) {
    let message = `Analysis failed (HTTP ${response.status}). Please try again.`
    try {
      const payload: unknown = await response.json()
      if (typeof payload === 'object' && payload !== null && 'detail' in payload && typeof payload.detail === 'string') {
        message = payload.detail
      }
    } catch {
      // Keep the safe status-based message when the server returned no JSON.
    }
    throw new Error(message)
  }
  return (await response.json()) as AnalysisResult
}
