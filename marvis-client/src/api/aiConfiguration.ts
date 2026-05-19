import { fetchWithAuth } from './client'

const BASE_URL = (import.meta.env.VITE_API_URL as string | undefined) ?? 'http://localhost:8000'

export interface Provider {
  id: number
  provider_name: string
  model_type: 'local' | 'cloud'
  created_at: string
  updated_at: string
}

export interface LLMModel {
  id: number
  provider_id: number
  model_name: string
  is_active: boolean
  created_at: string
  updated_at: string
}

export async function getProviders(): Promise<Provider[]> {
  const res = await fetchWithAuth(`${BASE_URL}/api/v1/ai-configuration/providers`)
  if (!res.ok) throw new Error('Failed to fetch providers')
  return res.json() as Promise<Provider[]>
}

export async function getProvidersByType(modelType: 'local' | 'cloud'): Promise<Provider[]> {
  const res = await fetchWithAuth(
    `${BASE_URL}/api/v1/ai-configuration/providers/by-type?model_type=${modelType}`,
  )
  if (!res.ok) throw new Error('Failed to fetch providers')
  return res.json() as Promise<Provider[]>
}

export async function getModelsByProvider(providerName: string): Promise<LLMModel[]> {
  const res = await fetchWithAuth(
    `${BASE_URL}/api/v1/ai-configuration/providers/${encodeURIComponent(providerName)}/models`,
  )
  if (!res.ok) throw new Error('Failed to fetch models')
  return res.json() as Promise<LLMModel[]>
}
