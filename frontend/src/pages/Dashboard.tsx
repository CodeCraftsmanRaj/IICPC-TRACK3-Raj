import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Users, AlertTriangle, Monitor, Wifi } from 'lucide-react';
import { 
  fetchDashboardStats, 
  fetchTelemetryEvents, 
  fetchThreatDistribution,
  fetchTopThreats 
} from '@/api/client';
import type { TelemetryEvent } from '@/types';
import { Layout } from '@/components/layout/Layout';
import { StatCard } from '@/components/dashboard/StatCard';
import { EventFeed } from '@/components/dashboard/EventFeed';
import { RiskCharts } from '@/components/dashboard/RiskCharts';
import { UserDetailModal } from '@/components/user/UserDetailModal';

export default function Dashboard() {
  const [selectedEvent, setSelectedEvent] = useState<TelemetryEvent | null>(null);

  const { data: stats } = useQuery({
    queryKey: ['dashboardStats'],
    queryFn: fetchDashboardStats,
    refetchInterval: 5000,
  });

  const { data: events = [] } = useQuery({
    queryKey: ['telemetryEvents'],
    queryFn: fetchTelemetryEvents,
    refetchInterval: 3000,
  });

  const { data: distribution = [] } = useQuery({
    queryKey: ['threatDistribution'],
    queryFn: fetchThreatDistribution,
  });

  const { data: topThreats = [] } = useQuery({
    queryKey: ['topThreats'],
    queryFn: fetchTopThreats,
  });

  return (
    <Layout>
      <div className="space-y-6">
        {/* Header */}
        <div>
          <h1 className="text-2xl font-bold text-foreground">Security Dashboard</h1>
          <p className="text-sm text-muted-foreground">
            Real-time monitoring of examination sessions • VM & Remote Access Detection System
          </p>
        </div>

        {/* Stats Grid */}
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <StatCard
            title="Active Sessions"
            value={stats?.active_sessions ?? 0}
            icon={Users}
            trend={{ value: 12, isPositive: true }}
            index={0}
          />
          <StatCard
            title="Critical Threats"
            value={stats?.critical_threats ?? 0}
            icon={AlertTriangle}
            variant="critical"
            trend={{ value: 8, isPositive: false }}
            index={1}
          />
          <StatCard
            title="VMs Detected"
            value={stats?.vms_detected ?? 0}
            icon={Monitor}
            variant="warning"
            index={2}
          />
          <StatCard
            title="RDP Detected"
            value={stats?.rdp_detected ?? 0}
            icon={Wifi}
            variant="warning"
            index={3}
          />
        </div>

        {/* Main Content Grid */}
        <div className="grid gap-6 lg:grid-cols-3">
          {/* Event Feed - 2/3 width */}
          <div className="lg:col-span-2">
            <EventFeed 
              events={events} 
              onEventClick={(event) => setSelectedEvent(event)} 
            />
          </div>

          {/* Charts - 1/3 width */}
          <div className="lg:col-span-1">
            <RiskCharts distribution={distribution} topThreats={topThreats} />
          </div>
        </div>
      </div>

      {/* User Detail Modal */}
      <UserDetailModal 
        event={selectedEvent} 
        onClose={() => setSelectedEvent(null)} 
      />
    </Layout>
  );
}
