export interface VMData {
  is_vm: boolean;
  confidence: number;
  vm_type?: string;
}

export interface RemoteData {
  remote_detected: boolean;
  risk_score: number;
  tools_detected?: string[];
}

export interface ScreenData {
  screen_sharing: boolean;
  multi_monitor: boolean;
  hdmi_detected: boolean;
}

export interface BehaviorData {
  anomaly_detected: boolean;
  confidence: number;
  anomaly_type?: string;
}

export interface TelemetryEvent {
  id: string;
  timestamp: string;
  user_id: string;
  risk_score: number;
  risk_level: RiskLevel;
  trigger_type: string;
  vm_data: VMData;
  remote_data: RemoteData;
  screen_data?: ScreenData;
  behavior_data?: BehaviorData;
  triggers: string[];
  status: 'open' | 'resolved' | 'investigating';
}

export type RiskLevel = 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW';

export interface DashboardStats {
  active_sessions: number;
  critical_threats: number;
  vms_detected: number;
  rdp_detected: number;
  total_alerts: number;
}

export interface ThreatDistribution {
  name: string;
  value: number;
  color: string;
}

export interface RiskTrend {
  timestamp: string;
  risk_score: number;
}

export interface UserDetailData {
  user_id: string;
  risk_score: number;
  risk_level: RiskLevel;
  vm_check: boolean;
  remote_access: boolean;
  screen_sharing: boolean;
  behavior_anomaly: boolean;
  vm_confidence: number;
  remote_confidence: number;
  telemetry_history: RiskTrend[];
  triggers: string[];
  session_start: string;
  last_activity: string;
}
