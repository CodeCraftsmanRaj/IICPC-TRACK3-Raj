import axios from 'axios';
import type { DashboardStats, TelemetryEvent, ThreatDistribution, UserDetailData, RiskLevel } from '@/types';

// Points to the FastAPI backend
const API_BASE_URL = 'http://localhost:8000';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 5000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// ============================================================================
// MOCK DATA GENERATORS (Fallback / Simulation Mode)
// ============================================================================
// These are used ONLY if the Python backend is offline or unreachable.
// They generate realistic-looking data for UI testing.

const generateUserId = () => `STU-${Math.random().toString(36).substring(2, 8).toUpperCase()}`;

const getRiskLevel = (score: number): RiskLevel => {
  if (score >= 75) return 'CRITICAL';
  if (score >= 50) return 'HIGH';
  if (score >= 25) return 'MEDIUM';
  return 'LOW';
};

const triggerTypes = [
  'Virtual Machine Detected',
  'RDP Session Active',
  'AnyDesk Running',
  'TeamViewer Detected',
  'VMware Detected',
  'VirtualBox Detected',
  'HDMI Splitter Detected',
  'Multi-Monitor Setup',
  'Screen Sharing Active',
  'Behavior Anomaly',
  'Network Anomaly',
  'USB Device Connected',
];

const generateMockEvent = (index: number): TelemetryEvent => {
  const riskScore = Math.floor(Math.random() * 100);
  const isVM = Math.random() > 0.6;
  const isRemote = Math.random() > 0.5;
  const timestamp = new Date(Date.now() - index * 30000).toISOString();
  
  return {
    id: `evt-${Date.now()}-${index}`,
    timestamp,
    user_id: generateUserId(),
    risk_score: riskScore,
    risk_level: getRiskLevel(riskScore),
    trigger_type: triggerTypes[Math.floor(Math.random() * triggerTypes.length)],
    vm_data: {
      is_vm: isVM,
      confidence: isVM ? 70 + Math.floor(Math.random() * 30) : Math.floor(Math.random() * 30),
      vm_type: isVM ? ['VMware', 'VirtualBox', 'Hyper-V', 'QEMU'][Math.floor(Math.random() * 4)] : undefined,
    },
    remote_data: {
      remote_detected: isRemote,
      risk_score: isRemote ? 60 + Math.floor(Math.random() * 40) : Math.floor(Math.random() * 30),
      tools_detected: isRemote ? ['RDP', 'AnyDesk', 'TeamViewer'].slice(0, Math.floor(Math.random() * 3) + 1) : [],
    },
    screen_data: {
      screen_sharing: Math.random() > 0.7,
      multi_monitor: Math.random() > 0.5,
      hdmi_detected: Math.random() > 0.8,
    },
    behavior_data: {
      anomaly_detected: Math.random() > 0.7,
      confidence: Math.floor(Math.random() * 100),
      anomaly_type: Math.random() > 0.5 ? 'Rapid Tab Switching' : 'Unusual Mouse Pattern',
    },
    triggers: triggerTypes.slice(0, Math.floor(Math.random() * 3) + 1),
    status: riskScore > 50 ? 'open' : 'resolved',
  };
};

// Default Mock Data Containers
export const mockStats: DashboardStats = {
  active_sessions: 247,
  critical_threats: 12,
  vms_detected: 8,
  rdp_detected: 15,
  total_alerts: 45,
};

export const mockEvents: TelemetryEvent[] = Array.from({ length: 20 }, (_, i) => generateMockEvent(i));

export const mockThreatDistribution: ThreatDistribution[] = [
  { name: 'Critical', value: 12, color: 'hsl(0, 72%, 51%)' },
  { name: 'High', value: 23, color: 'hsl(38, 92%, 50%)' },
  { name: 'Medium', value: 45, color: 'hsl(48, 96%, 53%)' },
  { name: 'Low', value: 167, color: 'hsl(199, 89%, 48%)' },
];

export const mockTopThreats: { name: string; count: number }[] = [
  { name: 'VMware', count: 45 },
  { name: 'AnyDesk', count: 38 },
  { name: 'RDP', count: 32 },
  { name: 'TeamViewer', count: 28 },
  { name: 'HDMI Splitter', count: 15 },
  { name: 'VirtualBox', count: 12 },
];

export const generateUserDetail = (userId: string): UserDetailData => {
  const riskScore = Math.floor(Math.random() * 100);
  const vmCheck = Math.random() > 0.5;
  const remoteAccess = Math.random() > 0.5;
  
  return {
    user_id: userId,
    risk_score: riskScore,
    risk_level: getRiskLevel(riskScore),
    vm_check: vmCheck,
    remote_access: remoteAccess,
    screen_sharing: Math.random() > 0.7,
    behavior_anomaly: Math.random() > 0.6,
    vm_confidence: vmCheck ? 70 + Math.floor(Math.random() * 30) : Math.floor(Math.random() * 30),
    remote_confidence: remoteAccess ? 60 + Math.floor(Math.random() * 40) : Math.floor(Math.random() * 30),
    telemetry_history: Array.from({ length: 30 }, (_, i) => ({
      timestamp: new Date(Date.now() - (30 - i) * 60000).toISOString(),
      risk_score: Math.max(0, Math.min(100, riskScore + (Math.random() - 0.5) * 30)),
    })),
    triggers: triggerTypes.slice(0, Math.floor(Math.random() * 4) + 1),
    session_start: new Date(Date.now() - Math.random() * 3600000).toISOString(),
    last_activity: new Date().toISOString(),
  };
};

// ============================================================================
// REAL API IMPLEMENTATION
// ============================================================================

export const fetchDashboardStats = async (): Promise<DashboardStats> => {
  try {
    const response = await apiClient.get('/api/v1/dashboard/stats');
    return response.data;
  } catch (error) {
    console.warn('Backend unavailable, using simulation data for Stats.', error);
    return mockStats;
  }
};

export const fetchTelemetryEvents = async (): Promise<TelemetryEvent[]> => {
  try {
    const response = await apiClient.get('/api/v1/telemetry/events');
    // Ensure dates are strings for consistency
    return response.data;
  } catch (error) {
    console.warn('Backend unavailable, using simulation data for Events.', error);
    return mockEvents;
  }
};

export const fetchThreatDistribution = async (): Promise<ThreatDistribution[]> => {
  try {
    const response = await apiClient.get('/api/v1/threats/distribution');
    return response.data;
  } catch (error) {
    console.warn('Backend unavailable, using simulation data for Distribution.', error);
    return mockThreatDistribution;
  }
};

// Note: Top Threats endpoint might not be implemented in MVP backend yet, 
// so we might default to mock often.
export const fetchTopThreats = async (): Promise<{ name: string; count: number }[]> => {
  try {
    // REAL: Fetch aggregated triggers from the backend
    const response = await apiClient.get('/api/v1/threats/top');
    return response.data;
  } catch (error) {
    console.warn('Backend unavailable, using simulation data for Top Threats.', error);
    return mockTopThreats;
  }
};
export const fetchUserDetail = async (userId: string): Promise<UserDetailData> => {
  try {
    const response = await apiClient.get(`/api/v1/users/${userId}/detail`);
    return response.data;
  } catch (error) {
    console.warn(`Backend unavailable, simulating details for user ${userId}.`, error);
    return generateUserDetail(userId);
  }
};