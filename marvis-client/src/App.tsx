import type { CSSProperties, ReactElement } from 'react'
import { MarvisOrb } from './components/MarvisOrb'

const gridStyle: CSSProperties = {
  backgroundImage:
    'linear-gradient(rgba(6,182,212,1) 1px, transparent 1px), linear-gradient(90deg, rgba(6,182,212,1) 1px, transparent 1px)',
  backgroundSize: '60px 60px',
}

function App(): ReactElement {
  return (
    <div className="min-h-screen bg-gray-950 flex flex-col items-center justify-center gap-14 overflow-hidden relative">

      {/* Subtle cyan grid */}
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
      </div>
    </div>
  )
}

export default App
