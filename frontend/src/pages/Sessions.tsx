import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { motion } from 'framer-motion';
import { Users, Search, RefreshCw } from 'lucide-react';
import { fetchTelemetryEvents } from '@/api/client';
import type { TelemetryEvent } from '@/types';
import { Layout } from '@/components/layout/Layout';
import { UserDetailModal } from '@/components/user/UserDetailModal';
import { Badge } from '@/components/ui/badge';
import { cn } from '@/lib/utils';

const riskBadgeVariants = {
  CRITICAL: 'bg-destructive/20 text-destructive border-destructive/50 animate-pulse',
  HIGH: 'bg-warning/20 text-warning border-warning/50',
  MEDIUM: 'bg-yellow-500/20 text-yellow-500 border-yellow-500/50',
  LOW: 'bg-info/20 text-info border-info/50',
};

export default function Sessions() {
  const [selectedEvent, setSelectedEvent] = useState<TelemetryEvent | null>(null);
  const [searchQuery, setSearchQuery] = useState('');

  const { data: events = [], refetch, isFetching } = useQuery({
    queryKey: ['telemetryEvents'],
    queryFn: fetchTelemetryEvents,
    refetchInterval: 5000,
  });

  // Get unique sessions (latest event per user)
  const sessions = events.reduce((acc, event) => {
    if (!acc.has(event.user_id) || new Date(event.timestamp) > new Date(acc.get(event.user_id)!.timestamp)) {
      acc.set(event.user_id, event);
    }
    return acc;
  }, new Map<string, TelemetryEvent>());

  const sessionList = Array.from(sessions.values()).filter(session =>
    searchQuery === '' || session.user_id.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <Layout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="flex items-center gap-2 text-2xl font-bold text-foreground">
              <Users className="h-6 w-6 text-primary" />
              Live Sessions
            </h1>
            <p className="text-sm text-muted-foreground">
              Monitor active examination sessions in real-time
            </p>
          </div>
          <div className="flex items-center gap-3">
            <Badge variant="outline" className="border-success/50 text-success">
              {sessionList.length} Active
            </Badge>
            <button
              onClick={() => refetch()}
              disabled={isFetching}
              className="flex h-9 items-center gap-2 rounded-lg border border-border bg-card px-3 text-sm font-medium text-foreground transition-colors hover:bg-muted disabled:opacity-50"
            >
              <RefreshCw className={cn('h-4 w-4', isFetching && 'animate-spin')} />
              Refresh
            </button>
          </div>
        </div>

        {/* Search */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4 }}
          className="relative"
        >
          <Search className="absolute left-4 top-1/2 h-5 w-5 -translate-y-1/2 text-muted-foreground" />
          <input
            type="text"
            placeholder="Search by Student ID..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="h-12 w-full rounded-xl border border-border bg-card pl-12 pr-4 text-foreground placeholder:text-muted-foreground focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary"
          />
        </motion.div>

        {/* Sessions Grid */}
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {sessionList.map((session, index) => (
            <motion.div
              key={session.user_id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3, delay: index * 0.05 }}
              onClick={() => setSelectedEvent(session)}
              className={cn(
                'cursor-pointer rounded-xl border bg-card p-4 transition-all hover:scale-[1.02]',
                session.risk_level === 'CRITICAL' 
                  ? 'border-destructive/50 glow-critical' 
                  : 'border-border hover:border-primary/50'
              )}
            >
              <div className="flex items-start justify-between">
                <div>
                  <p className="font-mono text-lg font-bold text-foreground">{session.user_id}</p>
                  <p className="mt-1 text-xs text-muted-foreground">
                    Last activity: {new Date(session.timestamp).toLocaleTimeString()}
                  </p>
                </div>
                <Badge 
                  variant="outline" 
                  className={cn('text-xs', riskBadgeVariants[session.risk_level])}
                >
                  {session.risk_level}
                </Badge>
              </div>
              
              <div className="mt-4 flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <div className="text-2xl font-mono font-bold text-foreground">
                    {session.risk_score}
                  </div>
                  <span className="text-xs text-muted-foreground">Risk Score</span>
                </div>
                <div className="flex gap-1">
                  {session.vm_data.is_vm && (
                    <Badge variant="outline" className="text-xs border-warning/50 text-warning">VM</Badge>
                  )}
                  {session.remote_data.remote_detected && (
                    <Badge variant="outline" className="text-xs border-destructive/50 text-destructive">RDP</Badge>
                  )}
                </div>
              </div>

              {/* Risk bar */}
              <div className="mt-3">
                <div className="h-1.5 w-full rounded-full bg-muted">
                  <div
                    className={cn(
                      'h-full rounded-full transition-all',
                      session.risk_level === 'CRITICAL' && 'bg-destructive',
                      session.risk_level === 'HIGH' && 'bg-warning',
                      session.risk_level === 'MEDIUM' && 'bg-yellow-500',
                      session.risk_level === 'LOW' && 'bg-info'
                    )}
                    style={{ width: `${session.risk_score}%` }}
                  />
                </div>
              </div>
            </motion.div>
          ))}
        </div>

        {sessionList.length === 0 && (
          <div className="flex flex-col items-center justify-center py-12 text-center">
            <Users className="h-12 w-12 text-muted-foreground" />
            <p className="mt-4 text-lg font-medium text-foreground">No sessions found</p>
            <p className="text-sm text-muted-foreground">
              {searchQuery ? 'Try a different search term' : 'Waiting for active sessions...'}
            </p>
          </div>
        )}
      </div>

      {/* User Detail Modal */}
      <UserDetailModal 
        event={selectedEvent} 
        onClose={() => setSelectedEvent(null)} 
      />
    </Layout>
  );
}
