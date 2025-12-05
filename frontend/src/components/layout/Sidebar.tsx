import { NavLink, useLocation } from 'react-router-dom';
import { 
  LayoutDashboard, 
  Users, 
  AlertTriangle, 
  Activity, 
  Settings,
  Shield,
  Wifi
} from 'lucide-react';
import { cn } from '@/lib/utils';

const navItems = [
  { path: '/', icon: LayoutDashboard, label: 'Dashboard' },
  { path: '/sessions', icon: Users, label: 'Live Sessions' },
  { path: '/alerts', icon: AlertTriangle, label: 'Alerts' },
  { path: '/health', icon: Activity, label: 'System Health' },
  { path: '/settings', icon: Settings, label: 'Settings' },
];

export function Sidebar() {
  const location = useLocation();

  return (
    <aside className="fixed left-0 top-0 z-40 flex h-screen w-64 flex-col border-r border-border bg-sidebar-background">
      {/* Logo */}
      <div className="flex h-16 items-center gap-3 border-b border-border px-6">
        <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary">
          <Shield className="h-6 w-6 text-primary-foreground" />
        </div>
        <div>
          <h1 className="font-semibold text-foreground">ProctorGuard</h1>
          <p className="text-xs text-muted-foreground">Security Dashboard</p>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 space-y-1 p-4">
        {navItems.map((item) => {
          const isActive = location.pathname === item.path;
          return (
            <NavLink
              key={item.path}
              to={item.path}
              className={cn(
                'flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-all duration-200',
                isActive
                  ? 'bg-primary/10 text-primary glow-primary'
                  : 'text-muted-foreground hover:bg-sidebar-accent hover:text-foreground'
              )}
            >
              <item.icon className={cn('h-5 w-5', isActive && 'text-primary')} />
              {item.label}
            </NavLink>
          );
        })}
      </nav>

      {/* System Status */}
      <div className="border-t border-border p-4">
        <div className="rounded-lg bg-sidebar-accent p-3">
          <div className="flex items-center gap-2">
            <div className="relative">
              <Wifi className="h-4 w-4 text-success" />
              <span className="absolute -right-0.5 -top-0.5 h-2 w-2 animate-pulse rounded-full bg-success" />
            </div>
            <span className="text-xs font-medium text-foreground">System Status</span>
          </div>
          <p className="mt-1 text-xs text-success">Online • All systems operational</p>
        </div>
      </div>

      {/* Version */}
      <div className="border-t border-border px-6 py-3">
        <p className="text-xs text-muted-foreground">v1.0.0 • IICPC Track 3</p>
      </div>
    </aside>
  );
}
