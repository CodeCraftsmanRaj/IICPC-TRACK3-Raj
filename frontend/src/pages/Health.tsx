import { motion } from 'framer-motion';
import { Activity, Server, Database, Wifi, CheckCircle, AlertCircle, Clock } from 'lucide-react';
import { Layout } from '@/components/layout/Layout';
import { cn } from '@/lib/utils';

const systemComponents = [
  { name: 'API Server', status: 'operational', latency: '23ms', icon: Server },
  { name: 'Database', status: 'operational', latency: '12ms', icon: Database },
  { name: 'WebSocket', status: 'operational', latency: '45ms', icon: Wifi },
  { name: 'VM Detection Service', status: 'operational', latency: '89ms', icon: Activity },
  { name: 'Remote Access Monitor', status: 'operational', latency: '56ms', icon: Activity },
  { name: 'Behavior Analysis', status: 'degraded', latency: '234ms', icon: Activity },
];

const recentIncidents = [
  { time: '2 hours ago', message: 'Behavior Analysis service restored', type: 'resolved' },
  { time: '3 hours ago', message: 'High latency detected on VM Detection', type: 'warning' },
  { time: '1 day ago', message: 'Scheduled maintenance completed', type: 'info' },
];

export default function Health() {
  const operationalCount = systemComponents.filter(c => c.status === 'operational').length;
  const allOperational = operationalCount === systemComponents.length;

  return (
    <Layout>
      <div className="space-y-6">
        {/* Header */}
        <div>
          <h1 className="flex items-center gap-2 text-2xl font-bold text-foreground">
            <Activity className="h-6 w-6 text-primary" />
            System Health
          </h1>
          <p className="text-sm text-muted-foreground">
            Monitor system status and performance metrics
          </p>
        </div>

        {/* Overall Status */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4 }}
          className={cn(
            'rounded-xl border p-6',
            allOperational 
              ? 'border-success/50 bg-success/5' 
              : 'border-warning/50 bg-warning/5'
          )}
        >
          <div className="flex items-center gap-4">
            {allOperational ? (
              <CheckCircle className="h-10 w-10 text-success" />
            ) : (
              <AlertCircle className="h-10 w-10 text-warning" />
            )}
            <div>
              <h2 className="text-xl font-bold text-foreground">
                {allOperational ? 'All Systems Operational' : 'Partial System Degradation'}
              </h2>
              <p className="text-sm text-muted-foreground">
                {operationalCount} of {systemComponents.length} services running normally
              </p>
            </div>
          </div>
        </motion.div>

        {/* Components Grid */}
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {systemComponents.map((component, index) => (
            <motion.div
              key={component.name}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3, delay: index * 0.05 }}
              className={cn(
                'rounded-xl border bg-card p-4',
                component.status === 'operational' ? 'border-border' : 'border-warning/50'
              )}
            >
              <div className="flex items-start justify-between">
                <div className="flex items-center gap-3">
                  <div className={cn(
                    'rounded-lg p-2',
                    component.status === 'operational' ? 'bg-success/10' : 'bg-warning/10'
                  )}>
                    <component.icon className={cn(
                      'h-5 w-5',
                      component.status === 'operational' ? 'text-success' : 'text-warning'
                    )} />
                  </div>
                  <div>
                    <p className="font-medium text-foreground">{component.name}</p>
                    <p className={cn(
                      'text-xs font-medium capitalize',
                      component.status === 'operational' ? 'text-success' : 'text-warning'
                    )}>
                      {component.status}
                    </p>
                  </div>
                </div>
              </div>
              <div className="mt-3 flex items-center justify-between text-xs text-muted-foreground">
                <span>Latency</span>
                <span className="font-mono font-medium text-foreground">{component.latency}</span>
              </div>
            </motion.div>
          ))}
        </div>

        {/* Recent Incidents */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, delay: 0.3 }}
          className="rounded-xl border border-border bg-card p-6"
        >
          <h3 className="mb-4 flex items-center gap-2 text-lg font-semibold text-foreground">
            <Clock className="h-5 w-5 text-primary" />
            Recent Incidents
          </h3>
          <div className="space-y-3">
            {recentIncidents.map((incident, index) => (
              <div 
                key={index}
                className="flex items-start gap-3 rounded-lg bg-muted/30 p-3"
              >
                <div className={cn(
                  'mt-0.5 h-2 w-2 rounded-full',
                  incident.type === 'resolved' && 'bg-success',
                  incident.type === 'warning' && 'bg-warning',
                  incident.type === 'info' && 'bg-info'
                )} />
                <div className="flex-1">
                  <p className="text-sm text-foreground">{incident.message}</p>
                  <p className="text-xs text-muted-foreground">{incident.time}</p>
                </div>
              </div>
            ))}
          </div>
        </motion.div>
      </div>
    </Layout>
  );
}
