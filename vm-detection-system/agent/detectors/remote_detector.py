import platform
import subprocess
import psutil
from typing import Dict, List, Tuple

# Safe import for winreg (Windows only)
try:
    import winreg
except ImportError:
    winreg = None

class RemoteAccessDetector:
    """Detects remote access software and sessions"""
    
    def __init__(self):
        self.remote_tools = {
            'rdp': ['mstsc.exe', 'rdpclip.exe', 'tstheme.exe'],
            'teamviewer': ['teamviewer.exe', 'tv_w32.exe', 'tv_x64.exe', 'teamviewerd'],
            'anydesk': ['anydesk.exe', 'anydesk'],
            'vnc': ['vncviewer.exe', 'winvnc.exe', 'tvnserver.exe', 'vncserver', 'xtightvncviewer'],
            'chrome_remote': ['remoting_host.exe', 'chrome-remote-desktop-host'],
            'parsec': ['parsecd.exe', 'parsec.exe', 'parsec'],
            'zoom': ['zoom.exe', 'zoom'],
            'skype': ['skype.exe', 'skypeforlinux']
        }
    
    def check_remote_processes(self) -> Tuple[bool, List[str]]:
        """Check for remote access tool processes"""
        detected = []
        try:
            for proc in psutil.process_iter(['name']):
                proc_name = proc.info['name'].lower()
                for tool_type, tool_names in self.remote_tools.items():
                    if any(t in proc_name for t in tool_names):
                        detected.append(f"{tool_type}: {proc.info['name']}")
        except:
            pass
        
        return len(detected) > 0, detected
    
    def check_rdp_session(self) -> Tuple[bool, str]:
        """Check for active RDP session (Windows only)"""
        if platform.system() != 'Windows':
            return False, "Not Windows"
        
        try:
            # Check for RDP session
            cmd = 'query session'
            output = subprocess.check_output(cmd, shell=True).decode()
            if 'rdp-tcp' in output.lower() or 'console' not in output.lower():
                return True, "RDP session detected"
        except:
            pass
        
        return False, "No RDP session"
    
    def check_network_connections(self) -> Tuple[bool, List[str]]:
        """Check for suspicious network connections"""
        suspicious_ports = [3389, 5900, 5800, 5938, 7070, 22]  # RDP, VNC, TeamViewer, AnyDesk, Parsec, SSH
        detected = []
        
        try:
            connections = psutil.net_connections(kind='inet')
            for conn in connections:
                if conn.status == 'ESTABLISHED':
                    # Check local or remote ports
                    if conn.laddr.port in suspicious_ports or (conn.raddr and conn.raddr.port in suspicious_ports):
                        port_num = conn.laddr.port if conn.laddr.port in suspicious_ports else conn.raddr.port
                        detected.append(f"Port {port_num}: {conn.status}")
        except:
            pass
        
        return len(detected) > 0, detected
    
    def check_registry_remote(self) -> Tuple[bool, List[str]]:
        """Check registry for remote access tools (Windows only)"""
        # FIX: Ensure we are on Windows AND winreg is available
        if platform.system() != 'Windows' or winreg is None:
            return False, []
        
        detected = []
        registry_paths = [
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\TeamViewer"),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\AnyDesk"),
            (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Google\Chrome Remote Desktop"),
        ]
        
        for hkey, path in registry_paths:
            try:
                key = winreg.OpenKey(hkey, path)
                detected.append(path.split('\\')[-1])
                winreg.CloseKey(key)
            except:
                pass
        
        return len(detected) > 0, detected
    
    def detect(self) -> Dict:
        """Run all remote access detection checks"""
        results = {
            'remote_detected': False,
            'risk_score': 0,
            'findings': []
        }
        
        # Run checks
        proc_detected, proc_list = self.check_remote_processes()
        rdp_detected, rdp_info = self.check_rdp_session()
        net_detected, net_list = self.check_network_connections()
        reg_detected, reg_list = self.check_registry_remote()
        
        # Aggregate results
        if proc_detected:
            results['findings'].append(f"Remote Tools Running: {', '.join(proc_list)}")
            results['risk_score'] += 40
        
        if rdp_detected:
            results['findings'].append(rdp_info)
            results['risk_score'] += 35
        
        if net_detected:
            results['findings'].append(f"Suspicious Connections: {', '.join(net_list[:3])}")
            results['risk_score'] += 20
        
        if reg_detected:
            results['findings'].append(f"Remote Tools Installed: {', '.join(reg_list)}")
            results['risk_score'] += 5
        
        results['remote_detected'] = results['risk_score'] > 30
        results['risk_score'] = min(results['risk_score'], 100)
        
        return results