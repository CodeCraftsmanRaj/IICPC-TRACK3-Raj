#!/usr/bin/env python3
"""
System-Level Forensics Module
Deep system analysis for suspicious activity
Uses OS-level APIs and forensic techniques
"""

import psutil
import os
import platform
import subprocess
from typing import Dict, List, Tuple
from collections import defaultdict

try:
    import win32api
    import win32con
    import win32process
    WIN32_AVAILABLE = True
except ImportError:
    WIN32_AVAILABLE = False


class ProcessAnalyzer:
    """Analyzes running processes for suspicious patterns"""
    
    def __init__(self):
        self.suspicious_names = [
            'inject', 'keylog', 'rat', 'backdoor', 'trojan',
            'payload', 'exploit', 'hack', 'crack'
        ]
    
    def get_process_tree(self) -> Dict[int, List[int]]:
        """Build process parent-child tree"""
        tree = defaultdict(list)
        try:
            for proc in psutil.process_iter(['pid', 'ppid']):
                tree[proc.info['ppid']].append(proc.info['pid'])
        except:
            pass
        return tree
    
    def check_suspicious_processes(self) -> Tuple[bool, List[str]]:
        """Check for processes with suspicious names"""
        suspicious = []
        try:
            for proc in psutil.process_iter(['pid', 'name', 'exe']):
                proc_name = proc.info['name'].lower()
                
                # Check against suspicious keywords
                for keyword in self.suspicious_names:
                    if keyword in proc_name:
                        suspicious.append(f"Suspicious process: {proc.info['name']} (PID: {proc.info['pid']})")
                
                # Check for processes running from temp directories
                try:
                    if proc.info['exe']:
                        exe_path = proc.info['exe'].lower()
                        if any(temp in exe_path for temp in ['\\temp\\', '\\tmp\\', 'appdata\\local\\temp']):
                            suspicious.append(f"Process from temp: {proc.info['name']}")
                except:
                    pass
        
        except:
            pass
        
        return len(suspicious) > 0, suspicious
    
    def check_hidden_processes(self) -> Tuple[bool, List[str]]:
        """Check for processes with no window (potentially hidden)"""
        hidden = []
        try:
            if WIN32_AVAILABLE and platform.system() == 'Windows':
                # This is a simplified check
                for proc in psutil.process_iter(['pid', 'name']):
                    try:
                        # Some processes naturally have no window
                        name = proc.info['name'].lower()
                        if not any(svc in name for svc in ['service', 'svchost', 'system']):
                            # Additional checks could go here
                            pass
                    except:
                        pass
        except:
            pass
        
        return len(hidden) > 0, hidden
    
    def check_process_injection(self) -> Tuple[bool, List[str]]:
        """Check for signs of process injection"""
        indicators = []
        
        try:
            # Check for unusual memory usage patterns
            for proc in psutil.process_iter(['pid', 'name', 'memory_info', 'num_threads']):
                try:
                    # Rule: Process with unusually high thread count
                    if proc.info['num_threads'] > 100:
                        indicators.append(
                            f"{proc.info['name']} has {proc.info['num_threads']} threads"
                        )
                except:
                    pass
        except:
            pass
        
        return len(indicators) > 0, indicators
    
    def analyze(self) -> Dict:
        """Run process analysis"""
        results = {
            'process_suspicious': False,
            'risk_score': 0,
            'findings': []
        }
        
        # Check suspicious processes
        susp_detected, susp_list = self.check_suspicious_processes()
        if susp_detected:
            results['findings'].extend(susp_list)
            results['risk_score'] += 40
        
        # Check hidden processes
        hidden_detected, hidden_list = self.check_hidden_processes()
        if hidden_detected:
            results['findings'].extend(hidden_list)
            results['risk_score'] += 20
        
        # Check process injection
        inject_detected, inject_list = self.check_process_injection()
        if inject_detected:
            results['findings'].extend(inject_list)
            results['risk_score'] += 30
        
        results['risk_score'] = min(results['risk_score'], 100)
        results['process_suspicious'] = results['risk_score'] > 30
        
        if not results['findings']:
            results['findings'].append("No suspicious processes detected")
        
        return results


class SystemIntegrityChecker:
    """Checks system integrity and modifications"""
    
    def __init__(self):
        self.critical_files = []
    
    def check_startup_items(self) -> Tuple[bool, List[str]]:
        """Check startup programs"""
        suspicious = []
        
        if platform.system() == 'Windows':
            try:
                # Check common startup locations
                startup_paths = [
                    os.path.expanduser('~\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup'),
                    'C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Startup'
                ]
                
                for path in startup_paths:
                    if os.path.exists(path):
                        items = os.listdir(path)
                        if len(items) > 10:  # Many startup items
                            suspicious.append(f"Many startup items in {path}: {len(items)}")
            except:
                pass
        
        return len(suspicious) > 0, suspicious
    
    def check_drivers(self) -> Tuple[bool, List[str]]:
        """Check for suspicious drivers (Windows)"""
        suspicious = []
        
        if platform.system() == 'Windows':
            try:
                cmd = 'driverquery'
                output = subprocess.check_output(cmd, shell=True).decode()
                
                # Look for virtualization or remote access drivers
                suspicious_keywords = ['vm', 'virtual', 'remote', 'vnc', 'teamviewer']
                for line in output.split('\n'):
                    line_lower = line.lower()
                    for keyword in suspicious_keywords:
                        if keyword in line_lower:
                            suspicious.append(f"Driver: {line.strip()}")
                            break
            except:
                pass
        
        return len(suspicious) > 0, suspicious
    
    def check_services(self) -> Tuple[bool, List[str]]:
        """Check for suspicious services"""
        suspicious = []
        
        try:
            # Check Windows services
            if platform.system() == 'Windows':
                cmd = 'sc query type= service state= all'
                output = subprocess.check_output(cmd, shell=True).decode()
                
                # Count running services
                running_count = output.lower().count('running')
                if running_count > 200:  # Unusually high number
                    suspicious.append(f"High number of running services: {running_count}")
        except:
            pass
        
        return len(suspicious) > 0, suspicious
    
    def analyze(self) -> Dict:
        """Run system integrity checks"""
        results = {
            'integrity_compromised': False,
            'risk_score': 0,
            'findings': []
        }
        
        # Check startup items
        startup_detected, startup_list = self.check_startup_items()
        if startup_detected:
            results['findings'].extend(startup_list)
            results['risk_score'] += 15
        
        # Check drivers
        driver_detected, driver_list = self.check_drivers()
        if driver_detected:
            results['findings'].extend(driver_list)
            results['risk_score'] += 25
        
        # Check services
        service_detected, service_list = self.check_services()
        if service_detected:
            results['findings'].extend(service_list)
            results['risk_score'] += 10
        
        results['risk_score'] = min(results['risk_score'], 100)
        results['integrity_compromised'] = results['risk_score'] > 30
        
        if not results['findings']:
            results['findings'].append("System integrity appears normal")
        
        return results


class WebGLFingerprinting:
    """WebGL-based VM detection (simulated)"""
    
    def __init__(self):
        self.vm_gpu_signatures = [
            'virtualbox', 'vmware', 'parallels', 'microsoft basic',
            'hyper-v', 'qemu', 'virtio'
        ]
    
    def get_gpu_info(self) -> Dict:
        """Get GPU information"""
        gpu_info = {
            'detected': False,
            'vendor': 'Unknown',
            'renderer': 'Unknown',
            'is_vm': False
        }
        
        if platform.system() == 'Windows':
            try:
                # Try to get GPU info from WMI
                cmd = 'wmic path win32_VideoController get name'
                output = subprocess.check_output(cmd, shell=True).decode()
                
                gpu_info['detected'] = True
                gpu_info['renderer'] = output.split('\n')[1].strip() if len(output.split('\n')) > 1 else 'Unknown'
                
                # Check if it's a VM GPU
                renderer_lower = gpu_info['renderer'].lower()
                for signature in self.vm_gpu_signatures:
                    if signature in renderer_lower:
                        gpu_info['is_vm'] = True
                        break
            except:
                pass
        
        return gpu_info
    
    def analyze(self) -> Dict:
        """Analyze GPU for VM signatures"""
        results = {
            'webgl_vm_detected': False,
            'confidence': 0,
            'findings': []
        }
        
        gpu_info = self.get_gpu_info()
        
        if gpu_info['detected']:
            results['findings'].append(f"GPU Renderer: {gpu_info['renderer']}")
            
            if gpu_info['is_vm']:
                results['webgl_vm_detected'] = True
                results['confidence'] = 40
                results['findings'].append("Virtual GPU detected")
        else:
            results['findings'].append("Could not detect GPU information")
        
        return results


class TimingAttackDetector:
    """Detects VM through timing attacks"""
    
    def __init__(self):
        self.samples = 100
    
    def rdtsc_test(self) -> Tuple[bool, float]:
        """Simplified timing test for VM detection"""
        import time
        
        timings = []
        for _ in range(self.samples):
            start = time.perf_counter()
            # Minimal operation
            _ = 1 + 1
            end = time.perf_counter()
            timings.append(end - start)
        
        # Calculate variance
        avg = sum(timings) / len(timings)
        variance = sum((t - avg) ** 2 for t in timings) / len(timings)
        
        # High variance can indicate VM (due to hypervisor scheduling)
        is_vm = variance > 0.00001
        
        return is_vm, variance
    
    def analyze(self) -> Dict:
        """Run timing-based detection"""
        results = {
            'timing_vm_detected': False,
            'confidence': 0,
            'findings': []
        }
        
        is_vm, variance = self.rdtsc_test()
        
        results['findings'].append(f"Timing variance: {variance:.8f}")
        
        if is_vm:
            results['timing_vm_detected'] = True
            results['confidence'] = 30
            results['findings'].append("High timing variance (possible VM)")
        
        return results