import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { motion } from 'framer-motion';
import { AlertTriangle, Filter, Search } from 'lucide-react';
import { fetchTelemetryEvents } from '@/api/client';
import type { TelemetryEvent, RiskLevel } from '@/types';
import { Layout } from '@/components/layout/Layout';
import { EventFeed } from '@/components/dashboard/EventFeed';
import { UserDetailModal } from '@/components/user/UserDetailModal';
import { Badge } from '@/components/ui/badge';
import { cn } from '@/lib/utils';

const riskFilters: { label: string; value: RiskLevel | 'ALL' }[] = [
  { label: 'All', value: 'ALL' },
  { label: 'Critical', value: 'CRITICAL' },
  { label: 'High', value: 'HIGH' },
  { label: 'Medium', value: 'MEDIUM' },
  { label: 'Low', value: 'LOW' },
];

const filterColors: Record<string, string> = {
  ALL: 'bg-primary/20 text-primary border-primary/50',
  CRITICAL: 'bg-destructive/20 text-destructive border-destructive/50',
  HIGH: 'bg-warning/20 text-warning border-warning/50',
  MEDIUM: 'bg-yellow-500/20 text-yellow-500 border-yellow-500/50',
  LOW: 'bg-info/20 text-info border-info/50',
};

export default function Alerts() {
  const [selectedEvent, setSelectedEvent] = useState<TelemetryEvent | null>(null);
  const [activeFilter, setActiveFilter] = useState<RiskLevel | 'ALL'>('ALL');
  const [searchQuery, setSearchQuery] = useState('');

  const { data: events = [] } = useQuery({
    queryKey: ['telemetryEvents'],
    queryFn: fetchTelemetryEvents,
    refetchInterval: 3000,
  });

  const filteredEvents = events.filter(event => {
    const matchesRisk = activeFilter === 'ALL' || event.risk_level === activeFilter;
    const matchesSearch = searchQuery === '' || 
      event.user_id.toLowerCase().includes(searchQuery.toLowerCase()) ||
      event.trigger_type.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesRisk && matchesSearch;
  });

  const alertCounts = {
    ALL: events.length,
    CRITICAL: events.filter(e => e.risk_level === 'CRITICAL').length,
    HIGH: events.filter(e => e.risk_level === 'HIGH').length,
    MEDIUM: events.filter(e => e.risk_level === 'MEDIUM').length,
    LOW: events.filter(e => e.risk_level === 'LOW').length,
  };

  return (
    <Layout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="flex items-center gap-2 text-2xl font-bold text-foreground">
              <AlertTriangle className="h-6 w-6 text-warning" />
              Security Alerts
            </h1>
            <p className="text-sm text-muted-foreground">
              Filter and manage security events
            </p>
          </div>
          <Badge variant="outline" className="border-destructive/50 text-destructive">
            {alertCounts.CRITICAL} Critical
          </Badge>
        </div>

        {/* Filters */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4 }}
          className="rounded-xl border border-border bg-card p-4"
        >
          <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
            {/* Risk Filters */}
            <div className="flex items-center gap-2">
              <Filter className="h-4 w-4 text-muted-foreground" />
              <div className="flex flex-wrap gap-2">
                {riskFilters.map((filter) => (
                  <button
                    key={filter.value}
                    onClick={() => setActiveFilter(filter.value)}
                    className={cn(
                      'rounded-lg border px-3 py-1.5 text-xs font-medium transition-all',
                      activeFilter === filter.value
                        ? filterColors[filter.value]
                        : 'border-border bg-muted/30 text-muted-foreground hover:bg-muted'
                    )}
                  >
                    {filter.label}
                    <span className="ml-1.5 font-mono">({alertCounts[filter.value]})</span>
                  </button>
                ))}
              </div>
            </div>

            {/* Search */}
            <div className="relative">
              <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
              <input
                type="text"
                placeholder="Search by ID or trigger..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="h-9 w-full rounded-lg border border-border bg-background pl-9 pr-4 text-sm text-foreground placeholder:text-muted-foreground focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary sm:w-64"
              />
            </div>
          </div>
        </motion.div>

        {/* Events Feed */}
        <EventFeed 
          events={filteredEvents} 
          onEventClick={(event) => setSelectedEvent(event)} 
        />
      </div>

      {/* User Detail Modal */}
      <UserDetailModal 
        event={selectedEvent} 
        onClose={() => setSelectedEvent(null)} 
      />
    </Layout>
  );
}
