import { clearTokens, getAccessToken, refreshAccessToken } from './auth'

const BASE_URL = (import.meta.env.VITE_API_URL as string | undefined) ?? 'http://localhost:8000'

function buildHeaders(token: string | null, extra?: HeadersInit): Record<string, string> {
  const base: Record<string, string> = {
    'Content-Type': 'application/json',
    Authorization: `Bearer ${token ?? ''}`,
  }
  if (!extra) return base
  const entries = extra instanceof Headers
    ? [...extra.entries()]
    : Array.isArray(extra)
      ? extra
      : Object.entries(extra)
  for (const [k, v] of entries) {
    base[k] = v
  }
  return base
}

export { BASE_URL }

export async function fetchWithAuth(url: string, options: RequestInit = {}): Promise<Response> {
  const res = await fetch(url, {
    ...options,
    headers: buildHeaders(getAccessToken(), options.headers),
  })

  if (res.status !== 401) return res

  const refreshed = await refreshAccessToken()
  if (!refreshed) {
    clearTokens()
    window.location.href = '/login'
    return res
  }

  return fetch(url, {
    ...options,
    headers: buildHeaders(getAccessToken(), options.headers),
  })
}
