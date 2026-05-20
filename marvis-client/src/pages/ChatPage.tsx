import { useEffect, useRef, useState } from 'react'
import type { ReactElement, KeyboardEvent } from 'react'
import { SendHorizonal } from 'lucide-react'
import { getUsernameFromToken } from '../api/auth'
import { MarvisOrb } from '../components/MarvisOrb'

interface Message {
  id: number
  role: 'user' | 'assistant'
  text: string
}

export function ChatPage(): ReactElement {
  const username = getUsernameFromToken()
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const bottomRef = useRef<HTMLDivElement>(null)
  const textareaRef = useRef<HTMLTextAreaElement>(null)
  const chatStarted = messages.length > 0

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  function handleSend(): void {
    const text = input.trim()
    if (!text) return
    setMessages((prev) => [...prev, { id: Date.now(), role: 'user', text }])
    setInput('')
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto'
    }
  }

  function handleKeyDown(e: KeyboardEvent<HTMLTextAreaElement>): void {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  function handleInput(): void {
    const el = textareaRef.current
    if (!el) return
    el.style.height = 'auto'
    el.style.height = `${el.scrollHeight}px`
  }

  return (
    <div className="flex flex-col h-full">
      {/* Main content area */}
      <div className="flex-1 overflow-y-auto">
        {!chatStarted ? (
          <div className="flex flex-col items-center justify-center h-full gap-6">
            <MarvisOrb />
            <div className="flex flex-col items-center gap-2">
              <h1 className="text-4xl font-semibold text-white tracking-wide">
                Hello, {username ?? 'there'}
              </h1>
              <p className="text-xl text-cyan-400 tracking-widest uppercase">
                Marvis at your Service
              </p>
            </div>
          </div>
        ) : (
          <div className="flex flex-col gap-4 px-6 py-6 max-w-3xl mx-auto w-full">
            {messages.map((msg) => (
              <div
                key={msg.id}
                className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-[70%] px-4 py-3 rounded-2xl text-sm leading-relaxed ${
                    msg.role === 'user'
                      ? 'bg-cyan-500/20 text-white rounded-br-sm'
                      : 'bg-gray-800 text-gray-200 rounded-bl-sm'
                  }`}
                >
                  {msg.text}
                </div>
              </div>
            ))}
            <div ref={bottomRef} />
          </div>
        )}
      </div>

      {/* Chat input */}
      <div className="shrink-0 px-6 py-4">
        <div className="max-w-3xl mx-auto w-full">
          <div className="flex items-end gap-3 bg-gray-800 border border-gray-700 rounded-2xl px-4 py-3 focus-within:border-cyan-500/60 transition-colors">
            <textarea
              ref={textareaRef}
              rows={1}
              value={input}
              onChange={(e) => { setInput(e.target.value) }}
              onKeyDown={handleKeyDown}
              onInput={handleInput}
              placeholder="Message Marvis..."
              className="flex-1 bg-transparent text-white text-sm placeholder-gray-500 resize-none outline-none max-h-40 leading-relaxed"
            />
            <button
              onClick={handleSend}
              disabled={!input.trim()}
              className="shrink-0 text-gray-500 hover:text-cyan-400 disabled:opacity-30 disabled:cursor-not-allowed transition-colors cursor-pointer mb-0.5"
            >
              <SendHorizonal size={18} />
            </button>
          </div>
          <p className="text-center text-xs text-gray-600 mt-2">
            Press Enter to send · Shift+Enter for new line
          </p>
        </div>
      </div>
    </div>
  )
}
