import { Eye, EyeOff } from 'lucide-react'
import type { ReactElement } from 'react'
import { useEffect, useState } from 'react'
import type { LLMModel, Provider, UserAIConfig } from '../api/aiConfiguration'
import {
  getModelsByProvider,
  getProvidersByType,
  getUserConfig,
  saveUserConfig,
} from '../api/aiConfiguration'
import { Dropdown } from '../components/Dropdown'

type PageState = 'loading' | 'empty' | 'configuring' | 'configured'

const MODEL_TYPE_OPTIONS = [
  { value: 'cloud', label: 'Cloud' },
  { value: 'local', label: 'Local' },
]

function maskApiKey(key: string): string {
  if (!key) return ''
  if (key.length <= 4) return key
  return '*'.repeat(Math.min(key.length - 4, 24)) + key.slice(-4)
}

export function ConfigureAIPage(): ReactElement {
  const [pageState, setPageState] = useState<PageState>('loading')
  const [existingConfig, setExistingConfig] = useState<UserAIConfig | null>(null)
  const [loadError, setLoadError] = useState<string | null>(null)

  const [selectedType, setSelectedType] = useState<'local' | 'cloud' | ''>('')
  const [providers, setProviders] = useState<Provider[]>([])
  const [selectedProvider, setSelectedProvider] = useState<string>('')
  const [models, setModels] = useState<LLMModel[]>([])
  const [selectedModelId, setSelectedModelId] = useState<string>('')
  const [loadingProviders, setLoadingProviders] = useState(false)
  const [loadingModels, setLoadingModels] = useState(false)
  const [apiKey, setApiKey] = useState('')
  const [showApiKey, setShowApiKey] = useState(false)
  const [maxTokens, setMaxTokens] = useState('')
  const [saving, setSaving] = useState(false)
  const [formError, setFormError] = useState<string | null>(null)

  useEffect(() => {
    void (async (): Promise<void> => {
      try {
        const config = await getUserConfig()
        if (config === null) {
          setPageState('empty')
        } else {
          setExistingConfig(config)
          setPageState('configured')
        }
      } catch {
        setLoadError('Failed to load configuration.')
        setPageState('empty')
      }
    })()
  }, [])

  function handleTypeChange(type: string): void {
    setSelectedType(type as 'local' | 'cloud')
    setProviders([])
    setSelectedProvider('')
    setModels([])
    setSelectedModelId('')
    if (!type) return
    setLoadingProviders(true)
    void (async (): Promise<void> => {
      try {
        const data = await getProvidersByType(type as 'local' | 'cloud')
        setProviders(data)
      } catch {
        setFormError('Failed to load providers.')
      } finally {
        setLoadingProviders(false)
      }
    })()
  }

  function handleProviderChange(providerName: string): void {
    setSelectedProvider(providerName)
    setModels([])
    setSelectedModelId('')
    if (!providerName) return
    setLoadingModels(true)
    void (async (): Promise<void> => {
      try {
        const data = await getModelsByProvider(providerName)
        setModels(data)
      } catch {
        setFormError('Failed to load models.')
      } finally {
        setLoadingModels(false)
      }
    })()
  }

  function handleSave(): void {
    setFormError(null)
    if (!selectedModelId) {
      setFormError('Please select a model.')
      return
    }
    const tokens = parseInt(maxTokens, 10)
    if (!maxTokens || isNaN(tokens) || tokens < 1 || tokens > 32768) {
      setFormError('Max tokens must be between 1 and 32768.')
      return
    }
    if (selectedType === 'cloud' && !apiKey.trim()) {
      setFormError('API key is required for cloud models.')
      return
    }
    setSaving(true)
    void (async (): Promise<void> => {
      try {
        const config = await saveUserConfig({
          llm_model_id: parseInt(selectedModelId, 10),
          api_key: selectedType === 'local' ? '' : apiKey,
          max_tokens: tokens,
        })
        setExistingConfig(config)
        setPageState('configured')
      } catch {
        setFormError('Failed to save configuration.')
      } finally {
        setSaving(false)
      }
    })()
  }

  const providerOptions = providers.map((p) => ({
    value: p.provider_name,
    label: p.provider_name,
  }))

  const modelOptions = models.map((m) => ({
    value: String(m.id),
    label: m.model_name,
  }))

  if (pageState === 'loading') {
    return (
      <div className="p-8">
        <h1 className="text-2xl font-semibold text-white mb-1">Configure AI</h1>
        <p className="text-gray-600 text-sm mt-4">Loading configuration...</p>
      </div>
    )
  }

  if (pageState === 'configured' && existingConfig !== null) {
    return (
      <div className="p-8">
        <div className="flex items-start justify-between mb-8">
          <div>
            <h1 className="text-2xl font-semibold text-white mb-1">Configure AI</h1>
            <p className="text-gray-500 text-sm">Current AI configuration for Marvis.</p>
          </div>
          <button
            type="button"
            onClick={() => { setPageState('configuring') }}
            className="px-5 py-2 bg-gray-800 hover:bg-gray-700 text-white text-sm font-semibold rounded-lg transition-colors cursor-pointer"
          >
            Edit
          </button>
        </div>

        <div className="grid grid-cols-2 gap-x-12 gap-y-6">
          <div className="space-y-2">
            <p className="text-xs font-medium tracking-wide uppercase text-gray-500">Model Type</p>
            <div className="border-t border-gray-800" />
            <span
              className={`inline-block text-xs font-semibold px-2.5 py-1 rounded-full ${
                existingConfig.model_type === 'cloud'
                  ? 'bg-cyan-500/10 text-cyan-400'
                  : 'bg-purple-500/10 text-purple-400'
              }`}
            >
              {existingConfig.model_type}
            </span>
          </div>

          <div className="space-y-2">
            <p className="text-xs font-medium tracking-wide uppercase text-gray-500">Provider</p>
            <div className="border-t border-gray-800" />
            <p className="text-sm text-white">{existingConfig.provider_name}</p>
          </div>

          <div className="space-y-2">
            <p className="text-xs font-medium tracking-wide uppercase text-gray-500">Model</p>
            <div className="border-t border-gray-800" />
            <p className="text-sm text-white">{existingConfig.model_name}</p>
          </div>

          <div className="space-y-2">
            <p className="text-xs font-medium tracking-wide uppercase text-gray-500">Max Tokens</p>
            <div className="border-t border-gray-800" />
            <p className="text-sm text-white">{existingConfig.max_tokens.toLocaleString()}</p>
          </div>

          {existingConfig.api_key && (
            <div className="space-y-2 col-span-2">
              <p className="text-xs font-medium tracking-wide uppercase text-gray-500">API Key</p>
              <div className="border-t border-gray-800" />
              <p className="text-sm text-white font-mono">{maskApiKey(existingConfig.api_key)}</p>
            </div>
          )}
        </div>
      </div>
    )
  }

  if (pageState === 'empty') {
    return (
      <div className="p-8">
        <h1 className="text-2xl font-semibold text-white mb-1">Configure AI</h1>
        <p className="text-gray-500 text-sm mb-8">Select a provider and model for Marvis to use.</p>

        {loadError !== null && <p className="text-red-400 text-sm mb-6">{loadError}</p>}

        <div className="flex flex-col items-center justify-center w-full py-16 border border-dashed border-gray-800 rounded-2xl gap-4">
          <p className="text-gray-500 text-sm">No AI configuration set.</p>
          <button
            type="button"
            onClick={() => {
              setPageState('configuring')
            }}
            className="px-6 py-2.5 bg-cyan-500 hover:bg-cyan-400 text-gray-950 font-semibold rounded-lg transition-colors cursor-pointer"
          >
            Configure
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="p-8">
      <h1 className="text-2xl font-semibold text-white mb-1">Configure AI</h1>
      <p className="text-gray-500 text-sm mb-8">Select a provider and model for Marvis to use.</p>

      {formError !== null && <p className="text-red-400 text-sm mb-6">{formError}</p>}

      <div className="flex flex-col gap-6">
        <div className="flex gap-8">
          <div className="flex-1 space-y-5">
            <div className="space-y-3">
              <label className="text-xs font-medium tracking-wide uppercase text-gray-500">
                Model Type
              </label>
              <Dropdown
                value={selectedType}
                onChange={handleTypeChange}
                placeholder="Select a type"
                options={MODEL_TYPE_OPTIONS}
              />
            </div>

            <div className="space-y-3">
              <label
                className={`text-xs font-medium tracking-wide uppercase ${selectedType ? 'text-gray-500' : 'text-gray-700'}`}
              >
                Provider
              </label>
              <Dropdown
                value={selectedProvider}
                onChange={handleProviderChange}
                disabled={!selectedType || loadingProviders}
                placeholder={
                  !selectedType
                    ? 'Select a type first'
                    : loadingProviders
                      ? 'Loading providers...'
                      : 'Select a provider'
                }
                options={providerOptions}
              />
            </div>

            <div className="space-y-3">
              <label
                className={`text-xs font-medium tracking-wide uppercase ${selectedProvider ? 'text-gray-500' : 'text-gray-700'}`}
              >
                Model
              </label>
              <Dropdown
                value={selectedModelId}
                onChange={setSelectedModelId}
                disabled={!selectedProvider || loadingModels}
                placeholder={
                  !selectedProvider
                    ? 'Select a provider first'
                    : loadingModels
                      ? 'Loading models...'
                      : 'Select a model'
                }
                options={modelOptions}
              />
            </div>
          </div>

          <div className="w-px bg-gray-800 self-stretch" />

          <div className="flex-1 space-y-5">
            <div className="space-y-3">
              <label className="text-xs font-medium tracking-wide uppercase text-gray-500">
                API Key
              </label>
              <div className="relative">
                <input
                  type={showApiKey ? 'text' : 'password'}
                  value={apiKey}
                  onChange={(e) => {
                    setApiKey(e.target.value)
                  }}
                  placeholder={
                    selectedType === 'local'
                      ? 'Not required for local models'
                      : 'Paste your API key here'
                  }
                  disabled={selectedType === 'local'}
                  className="w-full bg-gray-900 border border-gray-700 hover:border-gray-600 focus:border-cyan-500 text-white rounded-xl px-4 py-3.5 pr-11 outline-none transition-colors placeholder:text-gray-600 disabled:opacity-40 disabled:cursor-not-allowed"
                />
                <button
                  type="button"
                  onClick={() => {
                    setShowApiKey((prev) => !prev)
                  }}
                  disabled={selectedType === 'local'}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-300 transition-colors cursor-pointer disabled:opacity-40 disabled:cursor-not-allowed"
                >
                  {showApiKey ? <EyeOff size={16} /> : <Eye size={16} />}
                </button>
              </div>
            </div>

            <div className="space-y-3">
              <label className="text-xs font-medium tracking-wide uppercase text-gray-500">
                Max Tokens
              </label>
              <input
                type="number"
                value={maxTokens}
                onChange={(e) => {
                  setMaxTokens(e.target.value)
                }}
                placeholder="e.g. 1024"
                min={1}
                max={32768}
                className="w-full bg-gray-900 border border-gray-700 hover:border-gray-600 focus:border-cyan-500 text-white rounded-xl px-4 py-3.5 outline-none transition-colors placeholder:text-gray-600 [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
              />
            </div>
          </div>
        </div>

        <div className="flex justify-end gap-3">
          {existingConfig !== null && (
            <button
              type="button"
              onClick={() => {
                setPageState('configured')
              }}
              className="px-6 py-2.5 bg-gray-800 hover:bg-gray-700 text-white font-semibold rounded-lg transition-colors cursor-pointer"
            >
              Cancel
            </button>
          )}
          <button
            type="button"
            onClick={handleSave}
            disabled={saving}
            className="px-6 py-2.5 bg-cyan-500 hover:bg-cyan-400 disabled:opacity-50 disabled:cursor-not-allowed text-gray-950 font-semibold rounded-lg transition-colors cursor-pointer"
          >
            {saving ? 'Saving...' : 'Save Configuration'}
          </button>
        </div>
      </div>
    </div>
  )
}
