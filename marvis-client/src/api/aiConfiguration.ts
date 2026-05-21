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

export interface UserAIConfig {
  id: number
  llm_model_id: number
  user_id: number | null
  api_key: string
  max_tokens: number
  is_active: boolean
  model_name: string
  provider_name: string
  model_type: 'local' | 'cloud'
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

export async function getUserConfig(): Promise<UserAIConfig | null> {
  const res = await fetchWithAuth(`${BASE_URL}/api/v1/ai-configuration/config`)
  if (res.status === 404) return null
  if (!res.ok) throw new Error('Failed to fetch config')
  return res.json() as Promise<UserAIConfig>
}

export async function saveUserConfig(payload: {
  llm_model_id: number
  api_key: string
  max_tokens: number
}): Promise<UserAIConfig> {
  const res = await fetchWithAuth(`${BASE_URL}/api/v1/ai-configuration/config`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
  if (!res.ok) throw new Error('Failed to save config')
  return res.json() as Promise<UserAIConfig>
}

export async function updateUserConfig(payload: {
  llm_model_id: number
  api_key: string
  max_tokens: number
}): Promise<UserAIConfig> {
  const res = await fetchWithAuth(`${BASE_URL}/api/v1/ai-configuration/config`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
  if (!res.ok) throw new Error('Failed to update config')
  return res.json() as Promise<UserAIConfig>
}
