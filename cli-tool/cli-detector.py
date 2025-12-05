#!/usr/bin/env python3
"""
VM & Remote Access Detection CLI Tool
Usage: python cli_detector.py [options]
"""

import argparse
import json
import time
from datetime import datetime
from vm_detector import VMDetector, RemoteAccessDetector, ScreenSharingDetector

class DetectionCLI:
    def __init__(self):
        self.vm_detector = VMDetector()
        self.remote_detector = RemoteAccessDetector()
        self.screen_detector = ScreenSharingDetector()
    
    def print_header(self):
        """Print CLI header"""
        print("=" * 70)
        print("VM & REMOTE ACCESS DETECTION SYSTEM")
        print("=" * 70)
        print(f"Scan Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        print()
    
    def print_section(self, title, data, risk_key, findings_key):
        """Print a detection section"""
        print(f"\n[{title}]")
        print("-" * 70)
        
        risk_detected = data.get(risk_key, False)
        status = "⚠ DETECTED" if risk_detected else "✓ CLEAR"
        
        if 'confidence' in data:
            print(f"Status: {status} (Confidence: {data['confidence']}%)")
        elif 'risk_score' in data:
            print(f"Status: {status} (Risk Score: {data['risk_score']}%)")
        elif 'risk_level' in data:
            print(f"Status: {status} (Risk Level: {data['risk_level']}%)")
        else:
            print(f"Status: {status}")
        
        findings = data.get(findings_key, [])
        if findings:
            print(f"\nFindings ({len(findings)}):")
            for i, finding in enumerate(findings, 1):
                print(f"  {i}. {finding}")
        else:
            print("\nNo suspicious indicators found.")
    
    def run_full_scan(self, verbose=False):
        """Run complete detection scan"""
        self.print_header()
        
        print("Running detection modules...")
        print()
        
        # VM Detection
        print("[1/3] Scanning for Virtual Machines...")
        vm_results = self.vm_detector.detect()
        
        # Remote Access Detection
        print("[2/3] Scanning for Remote Access...")
        remote_results = self.remote_detector.detect()
        
        # Screen Sharing Detection
        print("[3/3] Scanning for Screen Sharing...")
        screen_results = self.screen_detector.detect()
        
        print("\n" + "=" * 70)
        print("DETECTION RESULTS")
        print("=" * 70)
        
        # Print results
        self.print_section("VIRTUAL MACHINE DETECTION", vm_results, 'is_vm', 'indicators')
        self.print_section("REMOTE ACCESS DETECTION", remote_results, 'remote_detected', 'findings')
        self.print_section("SCREEN SHARING DETECTION", screen_results, 'screen_sharing_risk', 'details')
        
        # Calculate overall risk
        print("\n" + "=" * 70)
        print("OVERALL ASSESSMENT")
        print("=" * 70)
        
        total_risk = 0
        risk_factors = []
        
        if vm_results.get('is_vm'):
            total_risk += 35
            risk_factors.append("Virtual Machine Detected")
        
        if remote_results.get('remote_detected'):
            total_risk += 40
            risk_factors.append("Remote Access Detected")
        
        if screen_results.get('screen_sharing_risk'):
            total_risk += 25
            risk_factors.append("Screen Sharing Risk")
        
        risk_level = "HIGH" if total_risk >= 60 else "MEDIUM" if total_risk >= 30 else "LOW"
        
        print(f"\nOverall Risk Score: {total_risk}/100")
        print(f"Risk Level: {risk_level}")
        
        if risk_factors:
            print(f"\nRisk Factors:")
            for factor in risk_factors:
                print(f"  - {factor}")
        else:
            print("\n✓ No significant risks detected.")
        
        print("\n" + "=" * 70)
        
        # Return results for JSON output
        return {
            'timestamp': datetime.now().isoformat(),
            'vm_detection': vm_results,
            'remote_access': remote_results,
            'screen_sharing': screen_results,
            'overall_risk': {
                'score': total_risk,
                'level': risk_level,
                'factors': risk_factors
            }
        }
    
    def run_monitoring_mode(self, interval=30):
        """Run continuous monitoring"""
        print("=" * 70)
        print("CONTINUOUS MONITORING MODE")
        print(f"Scanning every {interval} seconds (Press Ctrl+C to stop)")
        print("=" * 70)
        
        try:
            scan_count = 0
            while True:
                scan_count += 1
                print(f"\n[Scan #{scan_count}] {datetime.now().strftime('%H:%M:%S')}")
                
                vm_results = self.vm_detector.detect()
                remote_results = self.remote_detector.detect()
                screen_results = self.screen_detector.detect()
                
                # Quick summary
                alerts = []
                if vm_results.get('is_vm'):
                    alerts.append(f"VM ({vm_results['confidence']}%)")
                if remote_results.get('remote_detected'):
                    alerts.append(f"Remote ({remote_results['risk_score']}%)")
                if screen_results.get('screen_sharing_risk'):
                    alerts.append(f"Screen ({screen_results['risk_level']}%)")
                
                if alerts:
                    print(f"  ⚠ ALERTS: {', '.join(alerts)}")
                else:
                    print("  ✓ All clear")
                
                time.sleep(interval)
        
        except KeyboardInterrupt:
            print("\n\nMonitoring stopped by user.")


def main():
    parser = argparse.ArgumentParser(
        description='VM & Remote Access Detection Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli_detector.py                    # Run single scan
  python cli_detector.py --json output.json # Save results to JSON
  python cli_detector.py --monitor          # Continuous monitoring
  python cli_detector.py --monitor -i 60    # Monitor every 60 seconds
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
    
    args = parser.parse_args()
    
    cli = DetectionCLI()
    
    if args.monitor:
        cli.run_monitoring_mode(interval=args.interval)
    else:
        results = cli.run_full_scan(verbose=args.verbose)
        
        if args.json:
            with open(args.json, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"\nResults saved to: {args.json}")


if __name__ == '__main__':
    main()