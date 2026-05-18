import { ChevronDown } from 'lucide-react'
import type { ReactElement } from 'react'
import { useEffect, useRef, useState } from 'react'

interface Option {
  value: string
  label: string
}

interface DropdownProps {
  value: string
  onChange?: (val: string) => void
  disabled?: boolean
  placeholder: string
  options: Option[]
}

export function Dropdown({ value, onChange, disabled = false, placeholder, options }: DropdownProps): ReactElement {
  const [open, setOpen] = useState(false)
  const ref = useRef<HTMLDivElement>(null)

  const selected = options.find((o) => o.value === value)

  useEffect(() => {
    function handleClickOutside(e: MouseEvent): void {
      if (ref.current && !ref.current.contains(e.target as Node)) {
        setOpen(false)
      }
    }
    document.addEventListener('mousedown', handleClickOutside)
    return (): void => { document.removeEventListener('mousedown', handleClickOutside) }
  }, [])

  function handleSelect(val: string): void {
    onChange?.(val)
    setOpen(false)
  }

  return (
    <div ref={ref} className="relative">
      <button
        type="button"
        disabled={disabled}
        onClick={() => { setOpen((prev) => !prev) }}
        className="w-full flex items-center justify-between gap-3 bg-gray-900 border border-gray-700 hover:border-gray-600 focus:border-cyan-500 text-left rounded-xl px-4 py-3.5 outline-none transition-colors disabled:opacity-40 disabled:cursor-not-allowed cursor-pointer"
      >
        <span className={selected ? 'text-white' : disabled ? 'text-gray-600' : 'text-gray-400'}>
          {selected ? selected.label : placeholder}
        </span>
        <ChevronDown
          size={16}
          className={`shrink-0 text-gray-500 transition-transform duration-200 ${open ? 'rotate-180' : ''}`}
        />
      </button>

      {open && !disabled && (
        <ul className="absolute z-50 w-full mt-2 bg-gray-900 border border-gray-700 rounded-xl overflow-y-auto max-h-56 shadow-xl shadow-black/40">
          {options.length === 0 ? (
            <li className="px-4 py-3 text-gray-500 text-sm">No options available</li>
          ) : (
            options.map((opt) => (
              <li
                key={opt.value}
                onClick={() => { handleSelect(opt.value) }}
                className={`px-4 py-2.5 text-sm cursor-pointer transition-colors ${
                  opt.value === value
                    ? 'bg-cyan-500/10 text-cyan-400'
                    : 'text-gray-300 hover:bg-gray-800 hover:text-white'
                }`}
              >
                {opt.label}
              </li>
            ))
          )}
        </ul>
      )}
    </div>
  )
}
