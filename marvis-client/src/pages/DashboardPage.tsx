import type { ReactElement } from 'react'
import { useState } from 'react'
import { Sidebar } from '../components/Sidebar'

export function DashboardPage(): ReactElement {
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false)

  return (
    <div className="flex h-screen bg-gray-950 overflow-hidden">
      <Sidebar
        collapsed={sidebarCollapsed}
        onToggle={() => { setSidebarCollapsed((prev) => !prev) }}
      />
      <main className="flex-1 overflow-auto" />
    </div>
  )
}
