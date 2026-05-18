import type { ReactElement } from 'react'
import { useState } from 'react'
import { Sidebar } from '../components/Sidebar'
import { ConfigureAIPage } from './ConfigureAIPage'

function renderContent(activeItem: string): ReactElement {
  if (activeItem === 'Configure AI') return <ConfigureAIPage />
  return <div />
}

export function DashboardPage(): ReactElement {
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false)
  const [activeItem, setActiveItem] = useState('Configure AI')

  return (
    <div className="flex h-screen bg-gray-950 overflow-hidden">
      <Sidebar
        collapsed={sidebarCollapsed}
        onToggle={() => { setSidebarCollapsed((prev) => !prev) }}
        activeItem={activeItem}
        onNavClick={setActiveItem}
      />
      <main className="flex-1 overflow-auto p-2">
        {renderContent(activeItem)}
      </main>
    </div>
  )
}
