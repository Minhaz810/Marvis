import type { CSSProperties, ReactElement } from 'react'

const PING_DELAYS: readonly number[] = [0, 1, 2]

const CARDINAL_ANGLES: readonly number[] = [0, 90, 180, 270]

const SOUND_BARS: readonly { delay: number; duration: number }[] = [
  { delay: 0.00, duration: 0.70 },
  { delay: 0.15, duration: 0.90 },
  { delay: 0.30, duration: 0.60 },
  { delay: 0.10, duration: 1.10 },
  { delay: 0.25, duration: 0.80 },
  { delay: 0.40, duration: 0.65 },
  { delay: 0.05, duration: 0.95 },
  { delay: 0.20, duration: 0.75 },
  { delay: 0.35, duration: 0.85 },
  { delay: 0.12, duration: 0.70 },
  { delay: 0.28, duration: 1.00 },
]

function SoundBars(): ReactElement {
  return (
    <div className="flex items-end gap-[3px]" style={{ height: '32px' }}>
      {SOUND_BARS.map(({ delay, duration }, i) => (
        <div
          key={i}
          className="bg-cyan-400 rounded-full"
          style={{
            width: '3px',
            height: '4px',
            animation: `soundBar ${duration}s ease-in-out infinite alternate`,
            animationDelay: `${delay}s`,
          }}
        />
      ))}
    </div>
  )
}

export function MarvisOrb(): ReactElement {
  const coreGlowStyle: CSSProperties = {
    background:
      'radial-gradient(circle, rgba(6,182,212,0.5) 0%, rgba(6,182,212,0.15) 60%, transparent 100%)',
    boxShadow:
      '0 0 30px rgba(6,182,212,0.6), 0 0 60px rgba(6,182,212,0.3), 0 0 100px rgba(6,182,212,0.1)',
    animation: 'breathe 3s ease-in-out infinite',
  }

  const coreBorderStyle: CSSProperties = {
    boxShadow: '0 0 20px rgba(6,182,212,0.5) inset, 0 0 20px rgba(6,182,212,0.4)',
  }

  const letterStyle: CSSProperties = {
    textShadow: '0 0 16px rgba(6,182,212,1), 0 0 32px rgba(6,182,212,0.6)',
  }

  return (
    <div className="flex flex-col items-center gap-5">
      <div className="relative flex items-center justify-center w-72 h-72">

        {/* Sonar ping rings */}
        {PING_DELAYS.map((delay) => (
          <div
            key={delay}
            className="absolute rounded-full border border-cyan-400/30"
            style={{
              width: '112px',
              height: '112px',
              animation: 'sonarPing 3s ease-out infinite',
              animationDelay: `${delay}s`,
            }}
          />
        ))}

        {/* Outer rotating dashed ring */}
        <div
          className="absolute w-64 h-64 rounded-full border border-dashed border-cyan-500/30"
          style={{ animation: 'spinCW 20s linear infinite' }}
        />

        {/* Mid counter-rotating dashed ring */}
        <div
          className="absolute w-52 h-52 rounded-full border border-dashed border-cyan-400/40"
          style={{ animation: 'spinCCW 12s linear infinite' }}
        />

        {/* Inner slow ring */}
        <div
          className="absolute w-40 h-40 rounded-full border border-cyan-300/20"
          style={{ animation: 'spinCW 8s linear infinite' }}
        />

        {/* Cardinal dots on outer ring */}
        {CARDINAL_ANGLES.map((deg) => (
          <div
            key={deg}
            className="absolute w-2 h-2 rounded-full bg-cyan-400"
            style={{
              top: '50%',
              left: '50%',
              boxShadow: '0 0 6px rgba(6,182,212,0.9)',
              transform: `translate(-50%, -50%) rotate(${deg}deg) translateY(-128px)`,
            }}
          />
        ))}

        {/* Core glow fill */}
        <div className="absolute w-28 h-28 rounded-full" style={coreGlowStyle} />

        {/* Core border */}
        <div
          className="absolute w-28 h-28 rounded-full border-2 border-cyan-400"
          style={coreBorderStyle}
        />

        {/* Center M */}
        <span
          className="relative text-cyan-300 text-3xl font-bold z-10 select-none"
          style={letterStyle}
        >
          M
        </span>
      </div>

      {/* Audio visualiser */}
      <SoundBars />
    </div>
  )
}
