import type { ReactElement } from 'react'

interface Props {
  size?: number
}

export function MarvisLogo({ size = 32 }: Props): ReactElement {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 288 288"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      {/* Outer dashed ring */}
      <circle
        cx="144" cy="144" r="128"
        stroke="rgba(6,182,212,0.3)"
        strokeWidth="1"
        strokeDasharray="4 6"
      />

      {/* Mid dashed ring */}
      <circle
        cx="144" cy="144" r="104"
        stroke="rgba(6,182,212,0.4)"
        strokeWidth="1"
        strokeDasharray="4 6"
      />

      {/* Inner ring */}
      <circle
        cx="144" cy="144" r="80"
        stroke="rgba(6,182,212,0.2)"
        strokeWidth="1"
      />

      {/* Cardinal dots */}
      <circle cx="144" cy="16"  r="4" fill="#22d3ee" style={{ filter: 'drop-shadow(0 0 3px rgba(6,182,212,0.9))' }} />
      <circle cx="272" cy="144" r="4" fill="#22d3ee" style={{ filter: 'drop-shadow(0 0 3px rgba(6,182,212,0.9))' }} />
      <circle cx="144" cy="272" r="4" fill="#22d3ee" style={{ filter: 'drop-shadow(0 0 3px rgba(6,182,212,0.9))' }} />
      <circle cx="16"  cy="144" r="4" fill="#22d3ee" style={{ filter: 'drop-shadow(0 0 3px rgba(6,182,212,0.9))' }} />

      {/* Core glow */}
      <circle
        cx="144" cy="144" r="56"
        fill="url(#coreGlow)"
      />

      {/* Core border */}
      <circle
        cx="144" cy="144" r="56"
        stroke="#22d3ee"
        strokeWidth="2"
        style={{ filter: 'drop-shadow(0 0 8px rgba(6,182,212,0.5))' }}
      />

      {/* Center M */}
      <text
        x="144" y="144"
        textAnchor="middle"
        dominantBaseline="central"
        fill="#67e8f9"
        fontSize="48"
        fontWeight="700"
        fontFamily="system-ui, sans-serif"
        style={{ filter: 'drop-shadow(0 0 10px rgba(6,182,212,1))' }}
      >
        M
      </text>

      <defs>
        <radialGradient id="coreGlow" cx="50%" cy="50%" r="50%">
          <stop offset="0%"   stopColor="rgba(6,182,212,0.5)" />
          <stop offset="60%"  stopColor="rgba(6,182,212,0.15)" />
          <stop offset="100%" stopColor="transparent" />
        </radialGradient>
      </defs>
    </svg>
  )
}
