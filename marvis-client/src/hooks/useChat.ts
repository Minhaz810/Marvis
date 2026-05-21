import { useCallback, useEffect, useRef, useState } from 'react'
import { BASE_URL } from '../api/client'
import { getAccessToken } from '../api/auth'

export interface ChatMessage {
  id: number
  role: 'user' | 'assistant'
  text: string
}

interface UseChatReturn {
  messages: ChatMessage[]
  send: (content: string) => void
  isThinking: boolean
  isConnected: boolean
  connectionError: string | null
}

export function useChat(): UseChatReturn {
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [isThinking, setIsThinking] = useState(false)
  const [isConnected, setIsConnected] = useState(false)
  const [connectionError, setConnectionError] = useState<string | null>(
    () => (!getAccessToken() ? 'No auth token found.' : null),
  )
  const wsRef = useRef<WebSocket | null>(null)

  useEffect(() => {
    const token = getAccessToken()
    if (!token) {
      return
    }

    const wsUrl = `${BASE_URL.replace(/^http/, 'ws')}/api/v1/chatbot/ws?token=${token}`
    const ws = new WebSocket(wsUrl)
    wsRef.current = ws

    ws.onopen = (): void => {
      setIsConnected(true)
      setConnectionError(null)
    }

    ws.onmessage = (event: MessageEvent): void => {
      const data = JSON.parse(event.data as string) as
        | { role: string; content: string }
        | { error: string }

      setIsThinking(false)

      if ('error' in data) {
        setConnectionError(data.error)
        return
      }

      setMessages((prev) => [
        ...prev,
        { id: Date.now(), role: 'assistant', text: data.content },
      ])
    }

    ws.onerror = (): void => {
      setIsConnected(false)
      setConnectionError('Connection error. Please try again.')
    }

    ws.onclose = (): void => {
      setIsConnected(false)
    }

    return (): void => {
      ws.close()
    }
  }, [])

  const send = useCallback((content: string) => {
    if (!wsRef.current || wsRef.current.readyState !== WebSocket.OPEN) return

    setMessages((prev) => [
      ...prev,
      { id: Date.now(), role: 'user', text: content },
    ])
    setIsThinking(true)
    wsRef.current.send(JSON.stringify({ content }))
  }, [])

  return { messages, send, isThinking, isConnected, connectionError }
}
