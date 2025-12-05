import { motion } from 'framer-motion';
import { LucideIcon } from 'lucide-react';
import { cn } from '@/lib/utils';

interface StatCardProps {
  title: string;
  value: number | string;
  icon: LucideIcon;
  trend?: {
    value: number;
    isPositive: boolean;
  };
  variant?: 'default' | 'critical' | 'warning' | 'success';
  index?: number;
}

export function StatCard({ 
  title, 
  value, 
  icon: Icon, 
  trend, 
  variant = 'default',
  index = 0 
}: StatCardProps) {
  const variants = {
    default: 'border-border bg-card',
    critical: 'border-destructive/50 bg-destructive/5 glow-critical',
    warning: 'border-warning/50 bg-warning/5',
    success: 'border-success/50 bg-success/5',
  };

  const iconVariants = {
    default: 'bg-primary/10 text-primary',
    critical: 'bg-destructive/20 text-destructive',
    warning: 'bg-warning/20 text-warning',
    success: 'bg-success/20 text-success',
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay: index * 0.1 }}
      className={cn(
        'rounded-xl border p-6 transition-all duration-300 hover:scale-[1.02]',
        variants[variant],
        variant === 'critical' && 'animate-pulse'
      )}
    >
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm font-medium text-muted-foreground">{title}</p>
          <p className="mt-2 font-mono text-3xl font-bold text-foreground">{value}</p>
          {trend && (
            <p className={cn(
              'mt-1 text-xs font-medium',
              trend.isPositive ? 'text-success' : 'text-destructive'
            )}>
              {trend.isPositive ? '↑' : '↓'} {Math.abs(trend.value)}% from last hour
            </p>
          )}
        </div>
        <div className={cn('rounded-lg p-3', iconVariants[variant])}>
          <Icon className="h-6 w-6" />
        </div>
      </div>
    </motion.div>
  );
}
