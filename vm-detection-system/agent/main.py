import time
import argparse
import sys
from datetime import datetime
import json

# Import detectors (assuming files are moved to agent/detectors/)
from detectors.vm_detector import VMDetector
from detectors.remote_detector import RemoteAccessDetector
from detectors.screen_detector import ScreenSharingDetector
from detectors.network_detector import NetworkAnalyzer
from detectors.behaviour_detector import BehaviorMonitor
from detectors.system_forensics import ProcessAnalyzer

from communicator import ServerCommunicator

def collect_snapshot(detectors, behavior_monitor=None):
    """Runs one cycle of data collection"""
    
    # Core checks (Fast)
    vm_data = detectors['vm'].detect()
    remote_data = detectors['remote'].detect()
    screen_data = detectors['screen'].detect()
    
    # Process & Network (Medium)
    if detectors.get('network'):
        network_data = detectors['network'].detect(measure_bandwidth=False)
    else:
        network_data = {}
        
    if detectors.get('process'):
        process_data = detectors['process'].analyze()
    else:
        process_data = {}

    # Behavior (Slow/Async) - In a real loop, this data is buffered
    behavior_data = {}
    if behavior_monitor:
        # In a real agent, this would be non-blocking. 
        # For POC, we take a 5-second sample if requested
        res = behavior_monitor.detect(monitor_duration=5)
        behavior_data = res

    payload = {
        "timestamp": datetime.now().isoformat(),
        "platform": sys.platform,
        "vm_data": vm_data,
        "remote_data": remote_data,
        "screen_data": screen_data,
        "behavior_data": behavior_data,
        "network_data": network_data,
        "process_data": process_data
    }
    
    return payload

def main():
    parser = argparse.ArgumentParser(description="IICPC Track 3 Agent")
    # parser.add_argument("--server", default="http://localhost:8000", help="Backend API URL")
    # use my hosted URL
    parser.add_argument("--server", default="https://iicpc-track3-raj.onrender.com", help="Backend API URL")
    parser.add_argument("--interval", type=int, default=10, help="Scan interval in seconds")
    args = parser.parse_args()

    print(f"[*] Starting Agent. Connecting to {args.server}")
    
    # Initialize Detectors
    detectors = {
        'vm': VMDetector(),
        'remote': RemoteAccessDetector(),
        'screen': ScreenSharingDetector(),
        'network': NetworkAnalyzer(),
        'process': ProcessAnalyzer()
    }
    
    # Behavior monitor (requires user interaction)
    behavior = BehaviorMonitor()
    
    comm = ServerCommunicator(server_url=args.server)

    try:
        while True:
            print(f"[*] Scanning system... {datetime.now().strftime('%H:%M:%S')}")
            
            # Collect data
            snapshot = collect_snapshot(detectors, behavior)
            
            # Send to Server
            response = comm.send_telemetry(snapshot)
            
            if response:
                risk = response.get('risk_level', 'UNKNOWN')
                score = response.get('risk_score', 0)
                print(f"    -> Server Response: [{risk}] Score: {score}")
                
                if risk in ['HIGH', 'CRITICAL']:
                    print("    !!! WARNING: FLAGGED BY SERVER !!!")
                    print(f"    Actions: {response.get('actions_required')}")
            
            time.sleep(args.interval)
            
    except KeyboardInterrupt:
        print("\nStopping Agent...")

if __name__ == "__main__":
    main()