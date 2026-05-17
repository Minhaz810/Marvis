import type { CSSProperties, ReactElement } from 'react'
import { Navigate, useNavigate } from 'react-router-dom'
import { getAccessToken } from '../api/auth'
import { MarvisOrb } from '../components/MarvisOrb'

const gridStyle: CSSProperties = {
  backgroundImage:
    'linear-gradient(rgba(6,182,212,1) 1px, transparent 1px), linear-gradient(90deg, rgba(6,182,212,1) 1px, transparent 1px)',
  backgroundSize: '60px 60px',
}

export function HomePage(): ReactElement {
  const navigate = useNavigate()

  if (getAccessToken()) {
    return <Navigate to="/dashboard" replace />
  }

  return (
    <div className="min-h-screen bg-gray-950 flex flex-col items-center justify-center gap-14 overflow-hidden relative">
      <div className="fixed inset-0 opacity-[0.025]" style={gridStyle} />

      <MarvisOrb />

      <div
        className="text-center space-y-3 relative z-10"
        style={{ animation: 'fadeInUp 1s ease-out 0.3s both' }}
      >
        <h1 className="text-5xl font-bold text-white tracking-tight">
          Hello, I am{' '}
          <span
            className="text-cyan-400"
            style={{ textShadow: '0 0 24px rgba(6,182,212,0.7)' }}
          >
            Marvis
          </span>
          !
        </h1>
        <p className="text-xl text-gray-400">Your Personal AI Assistant</p>
        <p
          className="text-xs tracking-[0.4em] uppercase text-cyan-500 pt-2"
          style={{ animation: 'breathe 2.5s ease-in-out infinite' }}
        >
          Always At Your Service!
        </p>

        <div className="flex gap-4 justify-center pt-6">
          <button
            onClick={() => { void navigate('/login') }}
            className="px-8 py-3 rounded-lg border border-cyan-500 text-cyan-400 font-semibold hover:bg-cyan-500/10 transition-colors"
          >
            Login
          </button>
          <button
            onClick={() => { void navigate('/register') }}
            className="px-8 py-3 rounded-lg bg-cyan-500 hover:bg-cyan-400 text-gray-950 font-semibold transition-colors"
          >
            Register
          </button>
        </div>
      </div>
    </div>
  )
}
