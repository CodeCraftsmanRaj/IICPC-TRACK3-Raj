import { motion, AnimatePresence } from 'framer-motion';
import { X, Monitor, Wifi, Share2, Brain, Clock, Activity, AlertTriangle } from 'lucide-react';
import { useQuery } from '@tanstack/react-query';
import { fetchUserDetail } from '@/api/client';
import type { TelemetryEvent } from '@/types';
import { cn } from '@/lib/utils';
import { Badge } from '@/components/ui/badge';
import { TelemetryGraph } from './TelemetryGraph';

interface UserDetailModalProps {
  event: TelemetryEvent | null;
  onClose: () => void;
}

const riskColors = {
  CRITICAL: 'text-destructive',
  HIGH: 'text-warning',
  MEDIUM: 'text-yellow-500',
  LOW: 'text-info',
};

const riskBgColors = {
  CRITICAL: 'stroke-destructive',
  HIGH: 'stroke-warning',
  MEDIUM: 'stroke-yellow-500',
  LOW: 'stroke-info',
};

function CircularProgress({ value, riskLevel }: { value: number; riskLevel: string }) {
  const radius = 60;
  const circumference = 2 * Math.PI * radius;
  const progress = (value / 100) * circumference;

  return (
    <div className="relative inline-flex items-center justify-center">
      <svg className="h-36 w-36 -rotate-90 transform">
        <circle
          cx="72"
          cy="72"
          r={radius}
          fill="none"
          stroke="hsl(217, 33%, 17%)"
          strokeWidth="8"
        />
        <circle
          cx="72"
          cy="72"
          r={radius}
          fill="none"
          className={cn('transition-all duration-1000', riskBgColors[riskLevel as keyof typeof riskBgColors])}
          strokeWidth="8"
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={circumference - progress}
        />
      </svg>
      <div className="absolute flex flex-col items-center">
        <span className={cn('font-mono text-3xl font-bold', riskColors[riskLevel as keyof typeof riskColors])}>
          {Math.round(value)}
        </span>
        <span className="text-xs text-muted-foreground">Risk Score</span>
      </div>
    </div>
  );
}

function CheckItem({ 
  icon: Icon, 
  label, 
  passed, 
  confidence 
}: { 
  icon: typeof Monitor; 
  label: string; 
  passed: boolean; 
  confidence?: number;
}) {
  return (
    <div className={cn(
      'rounded-lg border p-3 transition-all',
      passed 
        ? 'border-destructive/50 bg-destructive/10' 
        : 'border-success/50 bg-success/10'
    )}>
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Icon className={cn('h-4 w-4', passed ? 'text-destructive' : 'text-success')} />
          <span className="text-sm font-medium text-foreground">{label}</span>
        </div>
        <Badge 
          variant="outline" 
          className={cn(
            'text-xs',
            passed 
              ? 'border-destructive/50 text-destructive' 
              : 'border-success/50 text-success'
          )}
        >
          {passed ? 'DETECTED' : 'CLEAR'}
        </Badge>
      </div>
      {confidence !== undefined && (
        <div className="mt-2">
          <div className="flex justify-between text-xs text-muted-foreground">
            <span>Confidence</span>
            <span className="font-mono">{confidence}%</span>
          </div>
          <div className="mt-1 h-1.5 rounded-full bg-muted">
            <div 
              className={cn(
                'h-full rounded-full transition-all',
                passed ? 'bg-destructive' : 'bg-success'
              )}
              style={{ width: `${confidence}%` }}
            />
          </div>
        </div>
      )}
    </div>
  );
}

export function UserDetailModal({ event, onClose }: UserDetailModalProps) {
  const { data: userDetail, isLoading } = useQuery({
    queryKey: ['userDetail', event?.user_id],
    queryFn: () => fetchUserDetail(event?.user_id || ''),
    enabled: !!event,
  });

  if (!event) return null;

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="fixed inset-0 z-50 flex items-center justify-center bg-background/80 backdrop-blur-sm"
        onClick={onClose}
      >
        <motion.div
          initial={{ opacity: 0, scale: 0.95, y: 20 }}
          animate={{ opacity: 1, scale: 1, y: 0 }}
          exit={{ opacity: 0, scale: 0.95, y: 20 }}
          transition={{ duration: 0.3 }}
          className="relative max-h-[90vh] w-full max-w-3xl overflow-y-auto rounded-2xl border border-border bg-card p-6 shadow-2xl scrollbar-thin"
          onClick={(e) => e.stopPropagation()}
        >
          {/* Close Button */}
          <button
            onClick={onClose}
            className="absolute right-4 top-4 rounded-lg p-2 text-muted-foreground transition-colors hover:bg-muted hover:text-foreground"
          >
            <X className="h-5 w-5" />
          </button>

          {isLoading ? (
            <div className="flex h-64 items-center justify-center">
              <div className="h-8 w-8 animate-spin rounded-full border-2 border-primary border-t-transparent" />
            </div>
          ) : userDetail ? (
            <div className="space-y-6">
              {/* Header */}
              <div className="flex items-start gap-6">
                <CircularProgress value={userDetail.risk_score} riskLevel={userDetail.risk_level} />
                <div className="flex-1">
                  <div className="flex items-center gap-3">
                    <h2 className="font-mono text-xl font-bold text-foreground">{userDetail.user_id}</h2>
                    <Badge 
                      variant="outline" 
                      className={cn(
                        'text-xs',
                        userDetail.risk_level === 'CRITICAL' && 'animate-pulse border-destructive/50 text-destructive',
                        userDetail.risk_level === 'HIGH' && 'border-warning/50 text-warning',
                        userDetail.risk_level === 'MEDIUM' && 'border-yellow-500/50 text-yellow-500',
                        userDetail.risk_level === 'LOW' && 'border-info/50 text-info'
                      )}
                    >
                      {userDetail.risk_level}
                    </Badge>
                  </div>
                  <div className="mt-2 flex flex-wrap gap-4 text-sm text-muted-foreground">
                    <div className="flex items-center gap-1">
                      <Clock className="h-4 w-4" />
                      Session: {new Date(userDetail.session_start).toLocaleTimeString()}
                    </div>
                    <div className="flex items-center gap-1">
                      <Activity className="h-4 w-4" />
                      Last: {new Date(userDetail.last_activity).toLocaleTimeString()}
                    </div>
                  </div>
                  {userDetail.triggers.length > 0 && (
                    <div className="mt-3 flex flex-wrap gap-2">
                      {userDetail.triggers.map((trigger, i) => (
                        <Badge key={i} variant="outline" className="text-xs">
                          <AlertTriangle className="mr-1 h-3 w-3" />
                          {trigger}
                        </Badge>
                      ))}
                    </div>
                  )}
                </div>
              </div>

              {/* Detection Checks */}
              <div>
                <h3 className="mb-3 flex items-center gap-2 text-sm font-semibold text-foreground">
                  <Activity className="h-4 w-4 text-primary" />
                  Detection Status
                </h3>
                <div className="grid grid-cols-2 gap-3">
                  <CheckItem 
                    icon={Monitor} 
                    label="VM Detection" 
                    passed={userDetail.vm_check}
                    confidence={userDetail.vm_confidence}
                  />
                  <CheckItem 
                    icon={Wifi} 
                    label="Remote Access" 
                    passed={userDetail.remote_access}
                    confidence={userDetail.remote_confidence}
                  />
                  <CheckItem 
                    icon={Share2} 
                    label="Screen Sharing" 
                    passed={userDetail.screen_sharing}
                  />
                  <CheckItem 
                    icon={Brain} 
                    label="Behavior Anomaly" 
                    passed={userDetail.behavior_anomaly}
                  />
                </div>
              </div>

              {/* Telemetry Graph */}
              <div>
                <h3 className="mb-3 flex items-center gap-2 text-sm font-semibold text-foreground">
                  <Activity className="h-4 w-4 text-primary" />
                  Risk Score Timeline (Last 30 min)
                </h3>
                <div className="rounded-lg border border-border bg-background/50 p-4">
                  <TelemetryGraph data={userDetail.telemetry_history} />
                </div>
              </div>
            </div>
          ) : null}
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
}
