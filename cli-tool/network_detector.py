#!/usr/bin/env python3
"""
Network Analysis & Intrusion Detection Module
Analyzes network traffic for suspicious patterns
Uses rule-based detection with ML fallback
"""

import psutil
import socket
import time
from collections import defaultdict, deque
from typing import Dict, List, Tuple
import platform

try:
    import scapy.all as scapy
    SCAPY_AVAILABLE = True
except ImportError:
    SCAPY_AVAILABLE = False


class NetworkAnalyzer:
    """Network connection and traffic analyzer"""
    
    def __init__(self):
        self.suspicious_ports = {
            3389: 'RDP',
            5900: 'VNC',
            5800: 'VNC-HTTP',
            5938: 'TeamViewer',
            7070: 'TeamViewer',
            22: 'SSH',
            23: 'Telnet',
            4899: 'Radmin',
            6129: 'DameWare',
            5631: 'pcAnywhere',
            5632: 'pcAnywhere',
            8080: 'HTTP-Proxy',
            1080: 'SOCKS',
            9050: 'Tor'
        }
        
        self.connection_history = deque(maxlen=1000)
        self.bandwidth_samples = deque(maxlen=50)
    
    def get_active_connections(self) -> List[Dict]:
        """Get all active network connections"""
        connections = []
        try:
            for conn in psutil.net_connections(kind='inet'):
                if conn.status == 'ESTABLISHED':
                    connections.append({
                        'local_addr': f"{conn.laddr.ip}:{conn.laddr.port}",
                        'remote_addr': f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A",
                        'status': conn.status,
                        'pid': conn.pid,
                        'local_port': conn.laddr.port,
                        'remote_port': conn.raddr.port if conn.raddr else None
                    })
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            pass
        
        return connections
    
    def check_suspicious_connections(self) -> Tuple[bool, List[str]]:
        """Check for connections on suspicious ports"""
        suspicious = []
        connections = self.get_active_connections()
        
        for conn in connections:
            local_port = conn['local_port']
            remote_port = conn['remote_port']
            
            if local_port in self.suspicious_ports:
                suspicious.append(
                    f"Listening on {self.suspicious_ports[local_port]} port {local_port}"
                )
            
            if remote_port and remote_port in self.suspicious_ports:
                suspicious.append(
                    f"Connected to {self.suspicious_ports[remote_port]} port {remote_port} at {conn['remote_addr']}"
                )
        
        return len(suspicious) > 0, suspicious
    
    def analyze_connection_patterns(self) -> Dict:
        """Analyze connection patterns for anomalies"""
        connections = self.get_active_connections()
        
        # Count connections by remote IP
        remote_ips = defaultdict(int)
        for conn in connections:
            if conn['remote_addr'] != "N/A":
                ip = conn['remote_addr'].split(':')[0]
                remote_ips[ip] += 1
        
        indicators = []
        anomaly_score = 0
        
        # Rule 1: Too many connections to single IP (remote desktop)
        for ip, count in remote_ips.items():
            if count > 5:
                indicators.append(f"Multiple connections to {ip}: {count}")
                anomaly_score += 15
        
        # Rule 2: Check for non-standard ports with high activity
        high_port_connections = sum(1 for c in connections 
                                   if c['remote_port'] and c['remote_port'] > 10000)
        if high_port_connections > 10:
            indicators.append(f"High activity on non-standard ports: {high_port_connections}")
            anomaly_score += 10
        
        # Rule 3: Check for private IP connections (local network remote access)
        private_ip_pattern = ['192.168.', '10.', '172.16.', '172.17.', '172.18.']
        private_connections = []
        for conn in connections:
            remote_addr = conn['remote_addr']
            if remote_addr != "N/A":
                ip = remote_addr.split(':')[0]
                if any(ip.startswith(prefix) for prefix in private_ip_pattern):
                    private_connections.append(remote_addr)
        
        if len(private_connections) > 3:
            indicators.append(f"Multiple local network connections: {len(private_connections)}")
            anomaly_score += 20
        
        return {
            'total_connections': len(connections),
            'unique_ips': len(remote_ips),
            'private_connections': len(private_connections),
            'anomaly_score': min(anomaly_score, 100),
            'indicators': indicators
        }
    
    def measure_bandwidth(self, duration=5) -> Dict:
        """Measure network bandwidth usage"""
        print(f"  Measuring network activity for {duration} seconds...")
        
        # Get initial counters
        net_io_start = psutil.net_io_counters()
        time.sleep(duration)
        net_io_end = psutil.net_io_counters()
        
        # Calculate rates
        bytes_sent = net_io_end.bytes_sent - net_io_start.bytes_sent
        bytes_recv = net_io_end.bytes_recv - net_io_start.bytes_recv
        
        send_rate = bytes_sent / duration / 1024  # KB/s
        recv_rate = bytes_recv / duration / 1024  # KB/s
        
        indicators = []
        anomaly_score = 0
        
        # Rule: High bandwidth usage (screen sharing/remote desktop)
        if send_rate > 500:  # More than 500 KB/s upload
            indicators.append(f"High upload rate: {send_rate:.0f} KB/s (possible screen sharing)")
            anomaly_score += 25
        
        if recv_rate > 1000:  # More than 1 MB/s download
            indicators.append(f"High download rate: {recv_rate:.0f} KB/s")
            anomaly_score += 15
        
        total_rate = send_rate + recv_rate
        if total_rate > 1500:
            indicators.append(f"High total bandwidth: {total_rate:.0f} KB/s")
            anomaly_score += 20
        
        return {
            'send_rate_kbps': send_rate,
            'recv_rate_kbps': recv_rate,
            'total_rate_kbps': total_rate,
            'anomaly_score': min(anomaly_score, 100),
            'indicators': indicators
        }
    
    def detect(self, measure_bandwidth=True) -> Dict:
        """Run network analysis"""
        results = {
            'network_suspicious': False,
            'risk_score': 0,
            'findings': []
        }
        
        # Check suspicious connections
        susp_detected, susp_list = self.check_suspicious_connections()
        if susp_detected:
            results['findings'].extend(susp_list)
            results['risk_score'] += 35
        
        # Analyze connection patterns
        pattern_analysis = self.analyze_connection_patterns()
        if pattern_analysis['indicators']:
            results['findings'].extend(pattern_analysis['indicators'])
            results['risk_score'] += pattern_analysis['anomaly_score']
        
        # Add connection stats
        results['connection_stats'] = {
            'total': pattern_analysis['total_connections'],
            'unique_ips': pattern_analysis['unique_ips'],
            'private_network': pattern_analysis['private_connections']
        }
        
        # Measure bandwidth if requested
        if measure_bandwidth:
            bandwidth_data = self.measure_bandwidth(duration=5)
            if bandwidth_data['indicators']:
                results['findings'].extend(bandwidth_data['indicators'])
                results['risk_score'] += bandwidth_data['anomaly_score']
            
            results['bandwidth'] = {
                'upload_kbps': bandwidth_data['send_rate_kbps'],
                'download_kbps': bandwidth_data['recv_rate_kbps']
            }
        
        results['risk_score'] = min(results['risk_score'], 100)
        results['network_suspicious'] = results['risk_score'] > 30
        
        if not results['findings']:
            results['findings'].append("No suspicious network activity detected")
        
        return results


class SimpleIDSEngine:
    """Simple Intrusion Detection System with rule-based detection"""
    
    def __init__(self):
        self.alert_rules = []
        self.packet_buffer = deque(maxlen=100)
        self.use_scapy = SCAPY_AVAILABLE
    
    def add_rule(self, rule_name, condition_func):
        """Add detection rule"""
        self.alert_rules.append({
            'name': rule_name,
            'condition': condition_func
        })
    
    def check_port_scan(self, connections: List[Dict]) -> Tuple[bool, str]:
        """Detect port scanning behavior"""
        if len(connections) < 10:
            return False, ""
        
        # Check for many connections to different ports on same IP
        ip_ports = defaultdict(set)
        for conn in connections:
            if conn['remote_addr'] != "N/A":
                ip = conn['remote_addr'].split(':')[0]
                port = conn['remote_port']
                if port:
                    ip_ports[ip].add(port)
        
        for ip, ports in ip_ports.items():
            if len(ports) > 10:
                return True, f"Possible port scan to {ip}: {len(ports)} ports"
        
        return False, ""
    
    def check_data_exfiltration(self, bandwidth_data: Dict) -> Tuple[bool, str]:
        """Check for potential data exfiltration"""
        upload_rate = bandwidth_data.get('send_rate_kbps', 0)
        download_rate = bandwidth_data.get('recv_rate_kbps', 0)
        
        # High upload with low download = suspicious
        if upload_rate > 1000 and download_rate < 100:
            return True, f"Asymmetric traffic pattern (upload: {upload_rate:.0f} KB/s, download: {download_rate:.0f} KB/s)"
        
        return False, ""
    
    def detect(self, network_data: Dict) -> Dict:
        """Run IDS detection"""
        results = {
            'ids_alert': False,
            'alert_score': 0,
            'alerts': [],
            'scapy_available': self.use_scapy
        }
        
        if not self.use_scapy:
            results['alerts'].append("⚠ Scapy not available - limited IDS functionality")
        
        # Get active connections
        analyzer = NetworkAnalyzer()
        connections = analyzer.get_active_connections()
        
        # Run detection rules
        port_scan_detected, port_scan_msg = self.check_port_scan(connections)
        if port_scan_detected:
            results['alerts'].append(port_scan_msg)
            results['alert_score'] += 40
        
        if 'bandwidth' in network_data:
            exfil_detected, exfil_msg = self.check_data_exfiltration(network_data['bandwidth'])
            if exfil_detected:
                results['alerts'].append(exfil_msg)
                results['alert_score'] += 35
        
        # Check for suspicious process network activity
        suspicious_processes = self._check_process_network_activity()
        if suspicious_processes:
            results['alerts'].extend(suspicious_processes)
            results['alert_score'] += 20
        
        results['alert_score'] = min(results['alert_score'], 100)
        results['ids_alert'] = results['alert_score'] > 40
        
        if not results['alerts']:
            results['alerts'].append("No IDS alerts triggered")
        
        return results
    
    def _check_process_network_activity(self) -> List[str]:
        """Check which processes have active network connections"""
        suspicious = []
        try:
            process_connections = defaultdict(int)
            for conn in psutil.net_connections(kind='inet'):
                if conn.pid and conn.status == 'ESTABLISHED':
                    try:
                        proc = psutil.Process(conn.pid)
                        process_connections[proc.name()] += 1
                    except:
                        pass
            
            # Flag processes with many connections
            for proc_name, count in process_connections.items():
                if count > 10:
                    suspicious.append(f"Process '{proc_name}' has {count} active connections")
        
        except:
            pass
        
        return suspicious