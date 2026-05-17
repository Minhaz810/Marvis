import type { CSSProperties, ReactElement, SyntheticEvent } from 'react'
import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { register } from '../api/auth'

const gridStyle: CSSProperties = {
  backgroundImage:
    'linear-gradient(rgba(6,182,212,1) 1px, transparent 1px), linear-gradient(90deg, rgba(6,182,212,1) 1px, transparent 1px)',
  backgroundSize: '60px 60px',
}

export function RegisterPage(): ReactElement {
  const navigate = useNavigate()
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  function handleSubmit(e: SyntheticEvent): void {
    e.preventDefault()
    void (async (): Promise<void> => {
      setError(null)
      setLoading(true)
      try {
        await register(username, password, confirmPassword)
        void navigate('/login')
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Registration failed')
      } finally {
        setLoading(false)
      }
    })()
  }

  return (
    <div className="min-h-screen bg-gray-950 flex items-center justify-center overflow-hidden relative">
      <div className="fixed inset-0 opacity-[0.025]" style={gridStyle} />

      <div
        className="relative z-10 w-full max-w-md mx-4 bg-gray-900/80 backdrop-blur border border-cyan-500/30 rounded-2xl p-8"
        style={{ boxShadow: '0 0 40px rgba(6,182,212,0.08)' }}
      >
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-white">
            Join{' '}
            <span
              className="text-cyan-400"
              style={{ textShadow: '0 0 16px rgba(6,182,212,0.7)' }}
            >
              Marvis
            </span>
          </h1>
          <p className="text-gray-400 mt-2 text-sm">Create your account</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-5">
          <div className="space-y-1">
            <label className="text-sm text-gray-400">Username</label>
            <input
              type="text"
              value={username}
              onChange={(e) => { setUsername(e.target.value) }}
              required
              autoComplete="username"
              className="w-full bg-gray-950 border border-gray-700 focus:border-cyan-500 text-white rounded-lg px-4 py-3 outline-none transition-colors"
            />
          </div>

          <div className="space-y-1">
            <label className="text-sm text-gray-400">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => { setPassword(e.target.value) }}
              required
              autoComplete="new-password"
              className="w-full bg-gray-950 border border-gray-700 focus:border-cyan-500 text-white rounded-lg px-4 py-3 outline-none transition-colors"
            />
          </div>

          <div className="space-y-1">
            <label className="text-sm text-gray-400">Confirm Password</label>
            <input
              type="password"
              value={confirmPassword}
              onChange={(e) => { setConfirmPassword(e.target.value) }}
              required
              autoComplete="new-password"
              className="w-full bg-gray-950 border border-gray-700 focus:border-cyan-500 text-white rounded-lg px-4 py-3 outline-none transition-colors"
            />
          </div>

          {error !== null && (
            <p className="text-red-400 text-sm text-center">{error}</p>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-cyan-500 hover:bg-cyan-400 disabled:opacity-50 disabled:cursor-not-allowed text-gray-950 font-semibold py-3 rounded-lg transition-colors"
          >
            {loading ? 'Creating account...' : 'Create Account'}
          </button>
        </form>

        <p className="text-center text-gray-500 text-sm mt-6">
          Already have an account?{' '}
          <button
            onClick={() => { void navigate('/login') }}
            className="text-cyan-400 hover:text-cyan-300 transition-colors"
          >
            Sign in
          </button>
        </p>

        <button
          onClick={() => { void navigate('/') }}
          className="mt-4 w-full text-center text-gray-600 hover:text-gray-400 text-sm transition-colors"
        >
          ← Back to home
        </button>
      </div>
    </div>
  )
}
