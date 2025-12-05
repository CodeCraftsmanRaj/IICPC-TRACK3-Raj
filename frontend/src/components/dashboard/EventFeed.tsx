import { motion } from 'framer-motion';
import { AlertCircle, Clock, User } from 'lucide-react';
import type { TelemetryEvent, RiskLevel } from '@/types';
import { cn } from '@/lib/utils';
import { Badge } from '@/components/ui/badge';

interface EventFeedProps {
  events: TelemetryEvent[];
  onEventClick: (event: TelemetryEvent) => void;
}

const riskBadgeVariants: Record<RiskLevel, string> = {
  CRITICAL: 'bg-destructive/20 text-destructive border-destructive/50 animate-pulse',
  HIGH: 'bg-warning/20 text-warning border-warning/50',
  MEDIUM: 'bg-yellow-500/20 text-yellow-500 border-yellow-500/50',
  LOW: 'bg-info/20 text-info border-info/50',
};

const statusVariants = {
  open: 'bg-destructive/20 text-destructive',
  investigating: 'bg-warning/20 text-warning',
  resolved: 'bg-success/20 text-success',
};

function formatTimestamp(timestamp: string): string {
  const date = new Date(timestamp);
  return date.toLocaleTimeString('en-US', { 
    hour: '2-digit', 
    minute: '2-digit', 
    second: '2-digit',
    hour12: false 
  });
}

export function EventFeed({ events, onEventClick }: EventFeedProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay: 0.4 }}
      className="rounded-xl border border-border bg-card"
    >
      <div className="flex items-center justify-between border-b border-border p-4">
        <div className="flex items-center gap-2">
          <AlertCircle className="h-5 w-5 text-primary" />
          <h2 className="font-semibold text-foreground">Live Event Feed</h2>
        </div>
        <Badge variant="outline" className="border-primary/50 text-primary">
          {events.length} events
        </Badge>
      </div>
      
      <div className="max-h-[400px] overflow-y-auto scrollbar-thin">
        <table className="w-full">
          <thead className="sticky top-0 bg-card">
            <tr className="border-b border-border text-left text-xs font-medium uppercase text-muted-foreground">
              <th className="px-4 py-3">
                <div className="flex items-center gap-1">
                  <Clock className="h-3 w-3" />
                  Time
                </div>
              </th>
              <th className="px-4 py-3">
                <div className="flex items-center gap-1">
                  <User className="h-3 w-3" />
                  Student ID
                </div>
              </th>
              <th className="px-4 py-3">Trigger</th>
              <th className="px-4 py-3">Risk</th>
              <th className="px-4 py-3">Status</th>
            </tr>
          </thead>
          <tbody>
            {events.map((event, index) => (
              <motion.tr
                key={event.id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.3, delay: index * 0.05 }}
                onClick={() => onEventClick(event)}
                className={cn(
                  'cursor-pointer border-b border-border/50 transition-colors hover:bg-muted/30',
                  event.risk_level === 'CRITICAL' && 'bg-destructive/5'
                )}
              >
                <td className="px-4 py-3 font-mono text-sm text-muted-foreground">
                  {formatTimestamp(event.timestamp)}
                </td>
                <td className="px-4 py-3">
                  <span className="font-mono text-sm font-medium text-foreground">
                    {event.user_id}
                  </span>
                </td>
                <td className="px-4 py-3">
                  <span className="text-sm text-foreground">{event.trigger_type}</span>
                </td>
                <td className="px-4 py-3">
                  <Badge 
                    variant="outline" 
                    className={cn('text-xs', riskBadgeVariants[event.risk_level])}
                  >
                    {event.risk_level}
                  </Badge>
                </td>
                <td className="px-4 py-3">
                  <Badge 
                    variant="outline" 
                    className={cn('text-xs capitalize', statusVariants[event.status])}
                  >
                    {event.status}
                  </Badge>
                </td>
              </motion.tr>
            ))}
          </tbody>
        </table>
      </div>
    </motion.div>
  );
}
