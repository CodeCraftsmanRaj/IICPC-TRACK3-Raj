import { motion } from 'framer-motion';
import { Settings as SettingsIcon, Bell, Shield, Database, Globe, Moon } from 'lucide-react';
import { Layout } from '@/components/layout/Layout';
import { cn } from '@/lib/utils';

const settingsGroups = [
  {
    title: 'Notifications',
    icon: Bell,
    settings: [
      { label: 'Critical alerts', description: 'Get notified for critical risk events', enabled: true },
      { label: 'High risk alerts', description: 'Get notified for high risk events', enabled: true },
      { label: 'Daily summary', description: 'Receive daily summary reports', enabled: false },
    ],
  },
  {
    title: 'Detection Settings',
    icon: Shield,
    settings: [
      { label: 'VM Detection', description: 'Enable virtual machine detection', enabled: true },
      { label: 'Remote Access Detection', description: 'Detect RDP, AnyDesk, TeamViewer', enabled: true },
      { label: 'Behavior Analysis', description: 'AI-powered behavior analysis', enabled: true },
      { label: 'Multi-monitor Detection', description: 'Detect multiple monitor setups', enabled: false },
    ],
  },
  {
    title: 'Data & Privacy',
    icon: Database,
    settings: [
      { label: 'Telemetry logging', description: 'Log all telemetry data', enabled: true },
      { label: 'Auto-archive', description: 'Archive old sessions after 30 days', enabled: true },
    ],
  },
];

export default function Settings() {
  return (
    <Layout>
      <div className="space-y-6">
        {/* Header */}
        <div>
          <h1 className="flex items-center gap-2 text-2xl font-bold text-foreground">
            <SettingsIcon className="h-6 w-6 text-primary" />
            Settings
          </h1>
          <p className="text-sm text-muted-foreground">
            Configure dashboard preferences and detection settings
          </p>
        </div>

        {/* Settings Groups */}
        {settingsGroups.map((group, groupIndex) => (
          <motion.div
            key={group.title}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: groupIndex * 0.1 }}
            className="rounded-xl border border-border bg-card"
          >
            <div className="flex items-center gap-3 border-b border-border p-4">
              <group.icon className="h-5 w-5 text-primary" />
              <h2 className="font-semibold text-foreground">{group.title}</h2>
            </div>
            <div className="divide-y divide-border">
              {group.settings.map((setting) => (
                <div 
                  key={setting.label}
                  className="flex items-center justify-between p-4"
                >
                  <div>
                    <p className="font-medium text-foreground">{setting.label}</p>
                    <p className="text-sm text-muted-foreground">{setting.description}</p>
                  </div>
                  <button
                    className={cn(
                      'relative h-6 w-11 rounded-full transition-colors',
                      setting.enabled ? 'bg-primary' : 'bg-muted'
                    )}
                  >
                    <span
                      className={cn(
                        'absolute top-1 h-4 w-4 rounded-full bg-white transition-transform',
                        setting.enabled ? 'left-6' : 'left-1'
                      )}
                    />
                  </button>
                </div>
              ))}
            </div>
          </motion.div>
        ))}

        {/* API Configuration */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3, delay: 0.4 }}
          className="rounded-xl border border-border bg-card"
        >
          <div className="flex items-center gap-3 border-b border-border p-4">
            <Globe className="h-5 w-5 text-primary" />
            <h2 className="font-semibold text-foreground">API Configuration</h2>
          </div>
          <div className="p-4 space-y-4">
            <div>
              <label className="text-sm font-medium text-foreground">Backend URL</label>
              <input
                type="text"
                defaultValue="http://localhost:8000"
                className="mt-1 h-10 w-full rounded-lg border border-border bg-background px-3 text-sm text-foreground focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary"
              />
            </div>
            <div>
              <label className="text-sm font-medium text-foreground">Polling Interval (ms)</label>
              <input
                type="number"
                defaultValue="3000"
                className="mt-1 h-10 w-full rounded-lg border border-border bg-background px-3 text-sm text-foreground focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary"
              />
            </div>
          </div>
        </motion.div>

        {/* Theme Toggle */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3, delay: 0.5 }}
          className="rounded-xl border border-border bg-card p-4"
        >
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <Moon className="h-5 w-5 text-primary" />
              <div>
                <p className="font-medium text-foreground">Dark Mode</p>
                <p className="text-sm text-muted-foreground">Dashboard is optimized for dark mode</p>
              </div>
            </div>
            <span className="rounded-lg bg-primary/10 px-3 py-1 text-xs font-medium text-primary">
              Always On
            </span>
          </div>
        </motion.div>
      </div>
    </Layout>
  );
}
