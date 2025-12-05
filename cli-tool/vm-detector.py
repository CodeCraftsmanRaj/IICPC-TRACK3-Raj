#!/usr/bin/env python3
"""
VM & Remote Access Detection Engine
Core detection module for identifying virtualization and remote access
"""

import platform
import subprocess
import psutil
import re
import os
import winreg
from typing import Dict, List, Tuple

class VMDetector:
    """Detects virtual machine environments"""
    
    def __init__(self):
        self.vm_indicators = {
            'vmware': ['vmware', 'vmx', 'vmtoolsd'],
            'virtualbox': ['vbox', 'virtualbox'],
            'hyperv': ['hyper-v', 'hvix64', 'vmsrvc'],
            'qemu': ['qemu', 'virtio'],
            'parallels': ['parallels', 'prl_']
        }
    
    def check_processes(self) -> Tuple[bool, List[str]]:
        """Check for VM-related processes"""
        detected = []
        try:
            for proc in psutil.process_iter(['name']):
                proc_name = proc.info['name'].lower()
                for vm_type, indicators in self.vm_indicators.items():
                    if any(ind in proc_name for ind in indicators):
                        detected.append(f"{vm_type}: {proc.info['name']}")
        except:
            pass
        return len(detected) > 0, detected
    
    def check_system_vendor(self) -> Tuple[bool, str]:
        """Check system manufacturer/vendor"""
        if platform.system() != 'Windows':
            return False, "Non-Windows system"
        
        try:
            # Check BIOS vendor
            cmd = 'wmic bios get manufacturer'
            output = subprocess.check_output(cmd, shell=True).decode().lower()
            
            vm_vendors = ['vmware', 'virtualbox', 'qemu', 'microsoft corporation', 'xen', 'innotek']
            for vendor in vm_vendors:
                if vendor in output:
                    return True, f"VM Vendor: {vendor}"
        except:
            pass
        
        return False, "Physical hardware detected"
    
    def check_mac_address(self) -> Tuple[bool, List[str]]:
        """Check for VM MAC address prefixes"""
        vm_mac_prefixes = [
            '00:05:69', '00:0c:29', '00:1c:14', '00:50:56',  # VMware
            '08:00:27',  # VirtualBox
            '00:15:5d',  # Hyper-V
            '00:16:3e',  # Xen
        ]
        
        detected = []
        try:
            addrs = psutil.net_if_addrs()
            for iface, addr_list in addrs.items():
                for addr in addr_list:
                    if addr.family == psutil.AF_LINK:
                        mac = addr.address.upper()
                        mac_prefix = ':'.join(mac.split(':')[:3])
                        if mac_prefix in [p.upper() for p in vm_mac_prefixes]:
                            detected.append(f"{iface}: {mac}")
        except:
            pass
        
        return len(detected) > 0, detected
    
    def check_registry(self) -> Tuple[bool, List[str]]:
        """Check Windows registry for VM indicators (Windows only)"""
        if platform.system() != 'Windows':
            return False, []
        
        detected = []
        registry_paths = [
            (winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Services\VBoxGuest"),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\VMware, Inc.\VMware Tools"),
            (winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Services\vmicheartbeat"),
        ]
        
        for hkey, path in registry_paths:
            try:
                key = winreg.OpenKey(hkey, path)
                detected.append(path)
                winreg.CloseKey(key)
            except:
                pass
        
        return len(detected) > 0, detected
    
    def check_cpu_flags(self) -> Tuple[bool, str]:
        """Check for hypervisor CPU flag"""
        if platform.system() != 'Windows':
            return False, "CPU check unavailable"
        
        try:
            cmd = 'wmic cpu get description'
            output = subprocess.check_output(cmd, shell=True).decode().lower()
            if 'virtual' in output or 'hypervisor' in output:
                return True, "Virtual CPU detected"
        except:
            pass
        
        return False, "Physical CPU"
    
    def detect(self) -> Dict:
        """Run all VM detection checks"""
        results = {
            'is_vm': False,
            'confidence': 0,
            'indicators': []
        }
        
        # Run checks
        proc_detected, proc_list = self.check_processes()
        vendor_detected, vendor_info = self.check_system_vendor()
        mac_detected, mac_list = self.check_mac_address()
        reg_detected, reg_list = self.check_registry()
        cpu_detected, cpu_info = self.check_cpu_flags()
        
        # Aggregate results
        if proc_detected:
            results['indicators'].append(f"VM Processes: {', '.join(proc_list)}")
            results['confidence'] += 30
        
        if vendor_detected:
            results['indicators'].append(vendor_info)
            results['confidence'] += 35
        
        if mac_detected:
            results['indicators'].append(f"VM MAC Addresses: {', '.join(mac_list)}")
            results['confidence'] += 20
        
        if reg_detected:
            results['indicators'].append(f"VM Registry Keys Found: {len(reg_list)}")
            results['confidence'] += 10
        
        if cpu_detected:
            results['indicators'].append(cpu_info)
            results['confidence'] += 5
        
        results['is_vm'] = results['confidence'] > 30
        results['confidence'] = min(results['confidence'], 100)
        
        return results


class RemoteAccessDetector:
    """Detects remote access software and sessions"""
    
    def __init__(self):
        self.remote_tools = {
            'rdp': ['mstsc.exe', 'rdpclip.exe', 'tstheme.exe'],
            'teamviewer': ['teamviewer.exe', 'tv_w32.exe', 'tv_x64.exe'],
            'anydesk': ['anydesk.exe'],
            'vnc': ['vncviewer.exe', 'winvnc.exe', 'tvnserver.exe'],
            'chrome_remote': ['remoting_host.exe'],
            'parsec': ['parsecd.exe', 'parsec.exe'],
            'zoom': ['zoom.exe'],
            'skype': ['skype.exe']
        }
    
    def check_remote_processes(self) -> Tuple[bool, List[str]]:
        """Check for remote access tool processes"""
        detected = []
        try:
            for proc in psutil.process_iter(['name']):
                proc_name = proc.info['name'].lower()
                for tool_type, tool_names in self.remote_tools.items():
                    if proc_name in [t.lower() for t in tool_names]:
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
                if conn.laddr.port in suspicious_ports or (conn.raddr and conn.raddr.port in suspicious_ports):
                    detected.append(f"Port {conn.laddr.port if conn.laddr.port in suspicious_ports else conn.raddr.port}: {conn.status}")
        except:
            pass
        
        return len(detected) > 0, detected
    
    def check_registry_remote(self) -> Tuple[bool, List[str]]:
        """Check registry for remote access tools (Windows only)"""
        if platform.system() != 'Windows':
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


class ScreenSharingDetector:
    """Detects screen sharing and multi-monitor setups"""
    
    def check_display_count(self) -> Tuple[int, str]:
        """Check number of connected displays"""
        if platform.system() == 'Windows':
            try:
                import ctypes
                user32 = ctypes.windll.user32
                count = user32.GetSystemMetrics(80)  # SM_CMONITORS
                return count, f"{count} display(s) detected"
            except:
                pass
        
        return 1, "Display check unavailable"
    
    def check_sharing_processes(self) -> Tuple[bool, List[str]]:
        """Check for screen sharing software"""
        sharing_tools = ['obs', 'streamlabs', 'discord', 'skype', 'zoom', 'meet', 'teams']
        detected = []
        
        try:
            for proc in psutil.process_iter(['name']):
                proc_name = proc.info['name'].lower()
                for tool in sharing_tools:
                    if tool in proc_name:
                        detected.append(proc.info['name'])
        except:
            pass
        
        return len(detected) > 0, detected
    
    def detect(self) -> Dict:
        """Run screen sharing detection"""
        results = {
            'screen_sharing_risk': False,
            'risk_level': 0,
            'details': []
        }
        
        display_count, display_info = self.check_display_count()
        sharing_detected, sharing_list = self.check_sharing_processes()
        
        if display_count > 1:
            results['details'].append(display_info)
            results['risk_level'] += 25
        
        if sharing_detected:
            results['details'].append(f"Sharing Tools: {', '.join(sharing_list)}")
            results['risk_level'] += 40
        
        results['screen_sharing_risk'] = results['risk_level'] > 30
        
        return results