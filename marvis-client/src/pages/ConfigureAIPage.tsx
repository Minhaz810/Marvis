import type { ReactElement } from 'react'
import { useEffect, useState } from 'react'
import type { LLMModel, Provider } from '../api/aiConfiguration'
import { getModelsByProvider, getProviders } from '../api/aiConfiguration'
import { Dropdown } from '../components/Dropdown'

export function ConfigureAIPage(): ReactElement {
  const [providers, setProviders] = useState<Provider[]>([])
  const [models, setModels] = useState<LLMModel[]>([])
  const [selectedProvider, setSelectedProvider] = useState<string>('')
  const [selectedModel, setSelectedModel] = useState<string>('')
  const [loadingProviders, setLoadingProviders] = useState(true)
  const [loadingModels, setLoadingModels] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    void (async (): Promise<void> => {
      try {
        const data = await getProviders()
        setProviders(data)
      } catch {
        setError('Failed to load providers.')
      } finally {
        setLoadingProviders(false)
      }
    })()
  }, [])

  function handleProviderChange(providerName: string): void {
    setSelectedProvider(providerName)
    setSelectedModel('')
    setModels([])
    if (!providerName) return
    setLoadingModels(true)
    void (async (): Promise<void> => {
      try {
        const data = await getModelsByProvider(providerName)
        setModels(data)
      } catch {
        setError('Failed to load models.')
      } finally {
        setLoadingModels(false)
      }
    })()
  }

  const providerOptions = providers.map((p) => ({
    value: p.provider_name,
    label: `${p.provider_name} (${p.model_type})`,
  }))

  const modelOptions = models.map((m) => ({
    value: m.model_name,
    label: m.model_name,
  }))

  return (
    <div className="p-8 max-w-lg">
      <h1 className="text-2xl font-semibold text-white mb-1">Configure AI</h1>
      <p className="text-gray-500 text-sm mb-8">Select a provider and model for Marvis to use.</p>

      {error !== null && (
        <p className="text-red-400 text-sm mb-6">{error}</p>
      )}

      <div className="space-y-5">
        <div className="space-y-3">
          <label className="text-xs font-medium tracking-wide uppercase text-gray-500">Provider</label>
          <Dropdown
            value={selectedProvider}
            onChange={handleProviderChange}
            disabled={loadingProviders}
            placeholder={loadingProviders ? 'Loading providers...' : 'Select a provider'}
            options={providerOptions}
          />
        </div>

        <div className="space-y-3">
          <label className={`text-xs font-medium tracking-wide uppercase ${selectedProvider ? 'text-gray-500' : 'text-gray-700'}`}>
            Model
          </label>
          <Dropdown
            value={selectedModel}
            onChange={setSelectedModel}
            disabled={!selectedProvider || loadingModels}
            placeholder={
              !selectedProvider ? 'Select a provider first'
              : loadingModels ? 'Loading models...'
              : 'Select a model'
            }
            options={modelOptions}
          />
        </div>
      </div>
    </div>
  )
}
