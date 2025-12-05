#!/usr/bin/env python3
"""
VM & Remote Access Detection CLI Tool - COMPLETE VERSION
Usage: python cli_detector.py [options]
"""

import argparse
import json
import time
import sys
from datetime import datetime

# Import all detection modules
from .vm_detector import VMDetector, RemoteAccessDetector, ScreenSharingDetector

# Try importing optional modules with fallbacks
try:
    from behavior_detector import BehaviorMonitor
    BEHAVIOR_AVAILABLE = True
except ImportError:
    BEHAVIOR_AVAILABLE = False
    print("⚠ Behavior detection not available - install pynput")

try:
    from network_detector import NetworkAnalyzer, SimpleIDSEngine
    NETWORK_AVAILABLE = True
except ImportError:
    NETWORK_AVAILABLE = False
    print("⚠ Advanced network detection not available")

try:
    from system_forensics import ProcessAnalyzer, SystemIntegrityChecker, WebGLFingerprinting, TimingAttackDetector
    FORENSICS_AVAILABLE = True
except ImportError:
    FORENSICS_AVAILABLE = False
    print("⚠ System forensics not available")


class ComprehensiveDetectionCLI:
    """Complete detection system with all modules"""
    
    def __init__(self):
        # Core detectors (always available)
        self.vm_detector = VMDetector()
        self.remote_detector = RemoteAccessDetector()
        self.screen_detector = ScreenSharingDetector()
        
        # Optional detectors with fallbacks
        self.behavior_monitor = BehaviorMonitor() if BEHAVIOR_AVAILABLE else None
        self.network_analyzer = NetworkAnalyzer() if NETWORK_AVAILABLE else None
        self.ids_engine = SimpleIDSEngine() if NETWORK_AVAILABLE else None
        
        if FORENSICS_AVAILABLE:
            self.process_analyzer = ProcessAnalyzer()
            self.integrity_checker = SystemIntegrityChecker()
            self.webgl_detector = WebGLFingerprinting()
            self.timing_detector = TimingAttackDetector()
        else:
            self.process_analyzer = None
            self.integrity_checker = None
            self.webgl_detector = None
            self.timing_detector = None
    
    def print_header(self):
        """Print CLI header"""
        print("=" * 80)
        print(" VM & REMOTE ACCESS DETECTION SYSTEM - COMPREHENSIVE SCAN")
        print("=" * 80)
        print(f" Scan Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f" Platform: {sys.platform}")
        print("=" * 80)
        print()
    
    def print_module_status(self):
        """Print available modules"""
        print("📦 AVAILABLE MODULES:")
        print(f"  ✓ Core VM Detection")
        print(f"  ✓ Remote Access Detection")
        print(f"  ✓ Screen Sharing Detection")
        print(f"  {'✓' if BEHAVIOR_AVAILABLE else '✗'} Behavior Analysis {'' if BEHAVIOR_AVAILABLE else '(install pynput)'}")
        print(f"  {'✓' if NETWORK_AVAILABLE else '✗'} Network Analysis {'' if NETWORK_AVAILABLE else '(limited)'}")
        print(f"  {'✓' if FORENSICS_AVAILABLE else '✗'} System Forensics {'' if FORENSICS_AVAILABLE else '(limited)'}")
        print()
    
    def print_section(self, title, data, risk_key, findings_key):
        """Print a detection section"""
        print(f"\n{'─' * 80}")
        print(f"[{title}]")
        print(f"{'─' * 80}")
        
        risk_detected = data.get(risk_key, False)
        
        if 'confidence' in data:
            score = data['confidence']
            status = f"⚠ DETECTED ({score}%)" if risk_detected else f"✓ CLEAR ({score}%)"
        elif 'risk_score' in data:
            score = data['risk_score']
            status = f"⚠ DETECTED (Risk: {score}%)" if risk_detected else f"✓ CLEAR (Risk: {score}%)"
        elif 'alert_score' in data:
            score = data['alert_score']
            status = f"⚠ ALERT (Score: {score}%)" if risk_detected else f"✓ NO ALERT (Score: {score}%)"
        elif 'anomaly_score' in data:
            score = data['anomaly_score']
            status = f"⚠ ANOMALY ({score}%)" if risk_detected else f"✓ NORMAL ({score}%)"
        else:
            status = "⚠ DETECTED" if risk_detected else "✓ CLEAR"
        
        print(f"Status: {status}")
        
        findings = data.get(findings_key, [])
        if findings:
            print(f"\n📋 Findings ({len(findings)}):")
            for i, finding in enumerate(findings, 1):
                print(f"  {i}. {finding}")
        else:
            print("\n✓ No suspicious indicators found")
    
    def run_full_scan(self, verbose=False, skip_slow=False):
        """Run complete detection scan"""
        self.print_header()
        self.print_module_status()
        
        print("🔍 RUNNING DETECTION MODULES...")
        print("=" * 80)
        
        all_results = {}
        
        # === CORE DETECTIONS (FAST) ===
        print("\n[1/10] VM Detection...")
        vm_results = self.vm_detector.detect()
        all_results['vm_detection'] = vm_results
        
        print("[2/10] Remote Access Detection...")
        remote_results = self.remote_detector.detect()
        all_results['remote_access'] = remote_results
        
        print("[3/10] Screen Sharing Detection...")
        screen_results = self.screen_detector.detect()
        all_results['screen_sharing'] = screen_results
        
        # === NETWORK ANALYSIS ===
        print("[4/10] Network Analysis...")
        if self.network_analyzer:
            network_results = self.network_analyzer.detect(measure_bandwidth=not skip_slow)
            all_results['network_analysis'] = network_results
        else:
            all_results['network_analysis'] = {
                'network_suspicious': False,
                'risk_score': 0,
                'findings': ['⚠ Network analysis module not available']
            }
        
        # === IDS ===
        print("[5/10] Intrusion Detection System...")
        if self.ids_engine:
            ids_results = self.ids_engine.detect(all_results.get('network_analysis', {}))
            all_results['ids'] = ids_results
        else:
            all_results['ids'] = {
                'ids_alert': False,
                'alert_score': 0,
                'alerts': ['⚠ IDS module not available']
            }
        
        # === PROCESS ANALYSIS ===
        print("[6/10] Process Analysis...")
        if self.process_analyzer:
            process_results = self.process_analyzer.analyze()
            all_results['process_analysis'] = process_results
        else:
            all_results['process_analysis'] = {
                'process_suspicious': False,
                'risk_score': 0,
                'findings': ['⚠ Process analysis not available']
            }
        
        # === SYSTEM INTEGRITY ===
        print("[7/10] System Integrity Check...")
        if self.integrity_checker:
            integrity_results = self.integrity_checker.analyze()
            all_results['system_integrity'] = integrity_results
        else:
            all_results['system_integrity'] = {
                'integrity_compromised': False,
                'risk_score': 0,
                'findings': ['⚠ System integrity checks not available']
            }
        
        # === WEBGL FINGERPRINTING ===
        print("[8/10] WebGL GPU Fingerprinting...")
        if self.webgl_detector:
            webgl_results = self.webgl_detector.analyze()
            all_results['webgl_fingerprint'] = webgl_results
        else:
            all_results['webgl_fingerprint'] = {
                'webgl_vm_detected': False,
                'confidence': 0,
                'findings': ['⚠ WebGL detection not available']
            }
        
        # === TIMING ATTACK ===
        print("[9/10] Timing-Based VM Detection...")
        if self.timing_detector:
            timing_results = self.timing_detector.analyze()
            all_results['timing_attack'] = timing_results
        else:
            all_results['timing_attack'] = {
                'timing_vm_detected': False,
                'confidence': 0,
                'findings': ['⚠ Timing detection not available']
            }
        
        # === BEHAVIOR ANALYSIS (SLOWEST) ===
        print("[10/10] Behavioral Analysis...")
        if self.behavior_monitor and not skip_slow:
            behavior_results = self.behavior_monitor.detect(monitor_duration=8)
            all_results['behavior_analysis'] = behavior_results
        else:
            reason = "skipped (use --full for behavior analysis)" if skip_slow else "module not available (install pynput)"
            all_results['behavior_analysis'] = {
                'behavior_anomaly': False,
                'anomaly_score': 0,
                'findings': [f'⚠ Behavior analysis {reason}']
            }
        
        # === DISPLAY RESULTS ===
        print("\n")
        print("=" * 80)
        print(" DETECTION RESULTS")
        print("=" * 80)
        
        self.print_section("1. VIRTUAL MACHINE DETECTION", vm_results, 'is_vm', 'indicators')
        self.print_section("2. REMOTE ACCESS DETECTION", remote_results, 'remote_detected', 'findings')
        self.print_section("3. SCREEN SHARING DETECTION", screen_results, 'screen_sharing_risk', 'details')
        self.print_section("4. NETWORK ANALYSIS", all_results['network_analysis'], 'network_suspicious', 'findings')
        self.print_section("5. INTRUSION DETECTION", all_results['ids'], 'ids_alert', 'alerts')
        self.print_section("6. PROCESS ANALYSIS", all_results['process_analysis'], 'process_suspicious', 'findings')
        self.print_section("7. SYSTEM INTEGRITY", all_results['system_integrity'], 'integrity_compromised', 'findings')
        self.print_section("8. WEBGL FINGERPRINT", all_results['webgl_fingerprint'], 'webgl_vm_detected', 'findings')
        self.print_section("9. TIMING ANALYSIS", all_results['timing_attack'], 'timing_vm_detected', 'findings')
        self.print_section("10. BEHAVIOR ANALYSIS", all_results['behavior_analysis'], 'behavior_anomaly', 'findings')
        
        # === OVERALL RISK ASSESSMENT ===
        print("\n" + "=" * 80)
        print(" OVERALL RISK ASSESSMENT")
        print("=" * 80)
        
        risk_factors = []
        total_risk = 0
        
        # VM detection (35 points)
        if vm_results.get('is_vm'):
            total_risk += 35
            risk_factors.append(f"Virtual Machine ({vm_results['confidence']}%)")
        
        # Remote access (40 points)
        if remote_results.get('remote_detected'):
            total_risk += 40
            risk_factors.append(f"Remote Access ({remote_results['risk_score']}%)")
        
        # Screen sharing (25 points)
        if screen_results.get('screen_sharing_risk'):
            total_risk += 25
            risk_factors.append("Screen Sharing Risk")
        
        # Network (20 points)
        if all_results['network_analysis'].get('network_suspicious'):
            total_risk += 20
            risk_factors.append("Network Anomaly")
        
        # IDS (30 points)
        if all_results['ids'].get('ids_alert'):
            total_risk += 30
            risk_factors.append("IDS Alert")
        
        # Process (25 points)
        if all_results['process_analysis'].get('process_suspicious'):
            total_risk += 25
            risk_factors.append("Suspicious Processes")
        
        # System integrity (15 points)
        if all_results['system_integrity'].get('integrity_compromised'):
            total_risk += 15
            risk_factors.append("System Integrity")
        
        # Behavior (20 points)
        if all_results['behavior_analysis'].get('behavior_anomaly'):
            total_risk += 20
            risk_factors.append("Behavior Anomaly")
        
        # Cap at 100
        total_risk = min(total_risk, 100)
        
        # Determine risk level
        if total_risk >= 70:
            risk_level = "🔴 CRITICAL"
        elif total_risk >= 50:
            risk_level = "🟠 HIGH"
        elif total_risk >= 30:
            risk_level = "🟡 MEDIUM"
        else:
            risk_level = "🟢 LOW"
        
        print(f"\n📊 Overall Risk Score: {total_risk}/100")
        print(f"🎯 Risk Level: {risk_level}")
        
        if risk_factors:
            print(f"\n⚠️  Risk Factors Detected:")
            for i, factor in enumerate(risk_factors, 1):
                print(f"  {i}. {factor}")
        else:
            print("\n✅ No significant risks detected")
        
        print("\n" + "=" * 80)
        
        # Add overall assessment to results
        all_results['overall_assessment'] = {
            'timestamp': datetime.now().isoformat(),
            'risk_score': total_risk,
            'risk_level': risk_level,
            'risk_factors': risk_factors
        }
        
        return all_results
    
    def run_monitoring_mode(self, interval=30):
        """Run continuous monitoring"""
        print("=" * 80)
        print(" CONTINUOUS MONITORING MODE")
        print(f" Scanning every {interval} seconds (Press Ctrl+C to stop)")
        print("=" * 80)
        
        try:
            scan_count = 0
            while True:
                scan_count += 1
                print(f"\n[Scan #{scan_count}] {datetime.now().strftime('%H:%M:%S')}")
                
                # Quick checks only
                vm_results = self.vm_detector.detect()
                remote_results = self.remote_detector.detect()
                screen_results = self.screen_detector.detect()
                
                alerts = []
                if vm_results.get('is_vm'):
                    alerts.append(f"VM ({vm_results['confidence']}%)")
                if remote_results.get('remote_detected'):
                    alerts.append(f"Remote ({remote_results['risk_score']}%)")
                if screen_results.get('screen_sharing_risk'):
                    alerts.append(f"Screen Sharing")
                
                if alerts:
                    print(f"  ⚠️  ALERTS: {', '.join(alerts)}")
                else:
                    print("  ✅ All clear")
                
                time.sleep(interval)
        
        except KeyboardInterrupt:
            print("\n\n🛑 Monitoring stopped by user")


def main():
    parser = argparse.ArgumentParser(
        description='VM & Remote Access Detection Tool - Complete Version',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli_detector.py                       # Quick scan
  python cli_detector.py --full                # Full scan (includes behavior)
  python cli_detector.py --json results.json   # Save to JSON
  python cli_detector.py --monitor             # Continuous monitoring
  python cli_detector.py --monitor -i 60       # Monitor every 60s
        """
    )
    
    parser.add_argument('-m', '--monitor', action='store_true',
                        help='Run in continuous monitoring mode')
    parser.add_argument('-i', '--interval', type=int, default=30,
                        help='Monitoring interval in seconds (default: 30)')
    parser.add_argument('-j', '--json', type=str, metavar='FILE',
                        help='Save results to JSON file')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Verbose output')
    parser.add_argument('--full', action='store_true',
                        help='Run full scan including slow modules (behavior analysis)')
    
    args = parser.parse_args()
    
    cli = ComprehensiveDetectionCLI()
    
    if args.monitor:
        cli.run_monitoring_mode(interval=args.interval)
    else:
        results = cli.run_full_scan(verbose=args.verbose, skip_slow=not args.full)
        
        if args.json:
            with open(args.json, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"\n💾 Results saved to: {args.json}")


if __name__ == '__main__':
    main()