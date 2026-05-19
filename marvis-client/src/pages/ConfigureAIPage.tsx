import type { ReactElement } from 'react'
import { useState } from 'react'
import type { LLMModel, Provider } from '../api/aiConfiguration'
import { getModelsByProvider, getProvidersByType } from '../api/aiConfiguration'
import { Dropdown } from '../components/Dropdown'

const MODEL_TYPE_OPTIONS = [
  { value: 'cloud', label: 'Cloud' },
  { value: 'local', label: 'Local' },
]

export function ConfigureAIPage(): ReactElement {
  const [selectedType, setSelectedType] = useState<'local' | 'cloud' | ''>('')
  const [providers, setProviders] = useState<Provider[]>([])
  const [selectedProvider, setSelectedProvider] = useState<string>('')
  const [models, setModels] = useState<LLMModel[]>([])
  const [selectedModel, setSelectedModel] = useState<string>('')
  const [loadingProviders, setLoadingProviders] = useState(false)
  const [loadingModels, setLoadingModels] = useState(false)
  const [error, setError] = useState<string | null>(null)

  function handleTypeChange(type: string): void {
    setSelectedType(type as 'local' | 'cloud')
    setProviders([])
    setSelectedProvider('')
    setModels([])
    setSelectedModel('')
    if (!type) return
    setLoadingProviders(true)
    void (async (): Promise<void> => {
      try {
        const data = await getProvidersByType(type as 'local' | 'cloud')
        setProviders(data)
      } catch {
        setError('Failed to load providers.')
      } finally {
        setLoadingProviders(false)
      }
    })()
  }

  function handleProviderChange(providerName: string): void {
    setSelectedProvider(providerName)
    setModels([])
    setSelectedModel('')
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
    label: p.provider_name,
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
          <label className="text-xs font-medium tracking-wide uppercase text-gray-500">Model Type</label>
          <Dropdown
            value={selectedType}
            onChange={handleTypeChange}
            placeholder="Select a type"
            options={MODEL_TYPE_OPTIONS}
          />
        </div>

        <div className="space-y-3">
          <label className={`text-xs font-medium tracking-wide uppercase ${selectedType ? 'text-gray-500' : 'text-gray-700'}`}>
            Provider
          </label>
          <Dropdown
            value={selectedProvider}
            onChange={handleProviderChange}
            disabled={!selectedType || loadingProviders}
            placeholder={
              !selectedType ? 'Select a type first'
              : loadingProviders ? 'Loading providers...'
              : 'Select a provider'
            }
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
