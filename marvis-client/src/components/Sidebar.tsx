import {
  CalendarDays,
  History,
  LogOut,
  Menu,
  MessagesSquare,
  Settings2,
  ShieldCheck,
} from 'lucide-react'
import type { ReactElement } from 'react'

interface NavItem {
  label: string
  icon: ReactElement
}

const NAV_ITEMS: NavItem[] = [
  { label: 'Configure AI', icon: <Settings2 size={20} /> },
  { label: 'Communication Channel', icon: <MessagesSquare size={20} /> },
  { label: 'Access Management', icon: <ShieldCheck size={20} /> },
  { label: 'Scheduler', icon: <CalendarDays size={20} /> },
  { label: 'Chat History', icon: <History size={20} /> },
]

interface SidebarProps {
  collapsed: boolean
  onToggle: () => void
  activeItem: string
  onNavClick: (label: string) => void
}

export function Sidebar({ collapsed, onToggle, activeItem, onNavClick }: SidebarProps): ReactElement {
  return (
    <aside
      className="relative flex flex-col h-screen bg-gray-900 border-r border-gray-800 transition-all duration-300 shrink-0"
      style={{ width: collapsed ? '64px' : '240px' }}
    >
      {/* Logo area with hamburger toggle */}
      <div className="flex items-center gap-3 px-4 py-5 border-b border-gray-800 overflow-hidden">
        <button
          onClick={onToggle}
          className="shrink-0 text-gray-400 hover:text-cyan-400 transition-colors cursor-pointer"
        >
          <Menu size={20} />
        </button>
        {!collapsed && (
          <span className="text-white font-semibold tracking-wide whitespace-nowrap">
            Marvis
          </span>
        )}
      </div>

      {/* Nav items */}
      <nav className="flex-1 py-4 overflow-hidden">
        {NAV_ITEMS.map(({ label, icon }) => {
          const isActive = activeItem === label
          return (
            <button
              key={label}
              onClick={() => { onNavClick(label) }}
              className={`w-full flex items-center gap-3 px-4 py-3 transition-colors group cursor-pointer border-l-2 ${
                isActive
                  ? 'border-cyan-400 bg-cyan-500/10 text-cyan-400'
                  : 'border-transparent text-gray-400 hover:text-white hover:bg-gray-800'
              }`}
              title={collapsed ? label : undefined}
            >
              <span className={`shrink-0 transition-colors ${isActive ? 'text-cyan-400' : 'group-hover:text-cyan-400'}`}>
                {icon}
              </span>
              {!collapsed && (
                <span className="text-sm whitespace-nowrap">{label}</span>
              )}
            </button>
          )
        })}
      </nav>

      {/* Bottom section */}
      <div className="border-t border-gray-800 p-4 space-y-4">
        {/* Usage bar */}
        <div className="overflow-hidden">
          {!collapsed ? (
            <div className="space-y-2">
              <div className="flex justify-between items-center">
                <span className="text-xs text-gray-400">Usage</span>
                <span className="text-xs text-cyan-400">42%</span>
              </div>
              <div className="h-1.5 bg-gray-800 rounded-full overflow-hidden">
                <div
                  className="h-full bg-cyan-500 rounded-full"
                  style={{ width: '42%' }}
                />
              </div>
              <p className="text-xs text-gray-600">2,100 / 5,000 messages</p>
            </div>
          ) : (
            <div className="flex justify-center">
              <div className="w-8 h-1.5 bg-gray-800 rounded-full overflow-hidden">
                <div className="h-full bg-cyan-500 rounded-full" style={{ width: '42%' }} />
              </div>
            </div>
          )}
        </div>

        {/* Logout button */}
        <button
          className="w-full flex items-center gap-3 px-2 py-2 text-gray-400 hover:text-red-400 hover:bg-red-400/10 rounded-lg transition-colors group"
          title={collapsed ? 'Logout' : undefined}
        >
          <span className="shrink-0">
            <LogOut size={18} />
          </span>
          {!collapsed && (
            <span className="text-sm whitespace-nowrap">Logout</span>
          )}
        </button>
      </div>
    </aside>
  )
}
