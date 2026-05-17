import type { ReactElement } from 'react'
import { Navigate } from 'react-router-dom'
import { getAccessToken } from '../api/auth'

interface Props {
  children: ReactElement
}

export function ProtectedRoute({ children }: Props): ReactElement {
  if (!getAccessToken()) {
    return <Navigate to="/login" replace />
  }
  return children
}
