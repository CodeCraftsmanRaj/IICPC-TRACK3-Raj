"""
Decision Fusion Engine
Aggregates risk signals from multiple detection modules to form a unified risk score.
Uses weighted probability fusion.
"""

class DecisionFusionEngine:
    def __init__(self):
        # Weighted factors based on threat severity (Total = 1.0 + Bonuses)
        self.weights = {
            'vm': 0.35,        # High impact (Fundamental evasion)
            'remote': 0.40,    # Critical impact (Cheating assistance)
            'screen': 0.20,    # Medium impact (Content leakage)
            'anomaly': 0.15,   # Low impact (False positive prone)
            'ids': 0.25        # Variable impact
        }
        
    def analyze(self, data: dict) -> dict:
        score = 0.0
        triggers = []
        
        # 1. VM Analysis
        vm_res = data.get('vm_data', {})
        if vm_res.get('is_vm'):
            # Calculate severity based on confidence
            confidence = vm_res.get('confidence', 50) / 100.0
            score += self.weights['vm'] * confidence * 100
            
            # Extract specific indicators for better reporting
            indicators = vm_res.get('indicators', [])
            detail = indicators[0] if indicators else "Generic VM Signatures"
            triggers.append(f"Virtual Machine Detected: {detail}")

        # 2. Remote Access
        remote_res = data.get('remote_data', {})
        if remote_res.get('remote_detected'):
            risk = remote_res.get('risk_score', 0)
            score += self.weights['remote'] * risk
            
            # Check for specific tools
            findings = remote_res.get('findings', [])
            tools = [f for f in findings if "Remote Tools" in f]
            if tools:
                triggers.append(f"Remote Control Software: {tools[0]}")
            else:
                triggers.append(f"Remote Access Detected (Risk: {risk})")

        # 3. Screen Sharing / HDMI
        screen_res = data.get('screen_data', {})
        if screen_res.get('screen_sharing_risk'):
            score += self.weights['screen'] * 100
            details = screen_res.get('details', [])
            if any("display" in d.lower() for d in details):
                triggers.append("Multi-Monitor Setup Detected")
            else:
                triggers.append("Screen Sharing / Casting Detected")

        # 4. Behavioral Anomaly
        beh_res = data.get('behavior_data', {})
        if beh_res.get('behavior_anomaly'):
            anom_score = beh_res.get('anomaly_score', 0)
            score += self.weights['anomaly'] * anom_score
            triggers.append(f"Behavioral Anomaly (Score: {anom_score})")

        # 5. Network/IDS
        net_res = data.get('network_data', {})
        if net_res.get('network_suspicious'):
            # Network risks are additive
            net_risk = net_res.get('risk_score', 0)
            score += self.weights['ids'] * net_risk
            
            findings = net_res.get('findings', [])
            if findings:
                triggers.append(f"Network Anomaly: {findings[0]}")
            else:
                triggers.append("Suspicious Network Activity")

        # 6. Process Forensics (Bonus risk)
        proc_res = data.get('process_data', {})
        if proc_res.get('process_suspicious'):
             score += 15 # Flat penalty
             triggers.append("Malicious Process Signatures Found")

        # Cap score at 100
        total_risk = min(score, 100)
        
        # Determine Risk Level
        if total_risk >= 75:
            level = "CRITICAL"
            actions = ["TERMINATE_SESSION", "FLAG_ADMIN", "CAPTURE_EVIDENCE"]
        elif total_risk >= 50:
            level = "HIGH"
            actions = ["WARN_USER", "ENABLE_STRICT_LOGGING", "DISABLE_CLIPBOARD"]
        elif total_risk >= 25:
            level = "MEDIUM"
            actions = ["LOG_EVENT", "INCREASE_SAMPLING_RATE"]
        else:
            level = "LOW"
            actions = ["CONTINUE_MONITORING"]

        return {
            "risk_score": round(total_risk, 2),
            "risk_level": level,
            "triggers": triggers,
            "actions": actions
        }