"""
Decision Fusion Engine
Implements the formula: P(Suspicious) = w1*VM + w2*RDP + w3*Screen + w4*Anomaly + w5*IDS
"""

class DecisionFusionEngine:
    def __init__(self):
        # Weights defined in Research Report
        self.weights = {
            'vm': 0.35,
            'remote': 0.40,
            'screen': 0.25,
            'anomaly': 0.20,
            'ids': 0.30
        }
        
    def analyze(self, data: dict) -> dict:
        score = 0.0
        triggers = []
        
        # 1. VM Analysis
        vm_res = data.get('vm_data', {})
        if vm_res.get('is_vm'):
            confidence = vm_res.get('confidence', 50) / 100.0
            score += self.weights['vm'] * confidence * 100
            triggers.append(f"Virtual Machine Detected ({int(confidence*100)}%)")

        # 2. Remote Access
        remote_res = data.get('remote_data', {})
        if remote_res.get('remote_detected'):
            risk = remote_res.get('risk_score', 0)
            score += self.weights['remote'] * risk
            triggers.append(f"Remote Access Tools Active (Risk: {risk})")

        # 3. Screen Sharing
        screen_res = data.get('screen_data', {})
        if screen_res.get('screen_sharing_risk'):
            score += self.weights['screen'] * 100
            triggers.append("Secondary Display / Screen Sharing Detected")

        # 4. Behavioral Anomaly
        beh_res = data.get('behavior_data', {})
        if beh_res.get('behavior_anomaly'):
            anom_score = beh_res.get('anomaly_score', 0)
            score += self.weights['anomaly'] * anom_score
            triggers.append("Non-Human Interaction Pattern")

        # 5. Network/IDS
        net_res = data.get('network_data', {})
        if net_res.get('network_suspicious'):
            score += self.weights['ids'] * net_res.get('risk_score', 0)
            triggers.append("Network Traffic Anomaly")

        # Cap score
        total_risk = min(score, 100)
        
        # Determine Level
        if total_risk >= 75:
            level = "CRITICAL"
            actions = ["TERMINATE_SESSION", "FLAG_ADMIN"]
        elif total_risk >= 50:
            level = "HIGH"
            actions = ["WARN_USER", "ENABLE_STRICT_LOGGING"]
        elif total_risk >= 25:
            level = "MEDIUM"
            actions = ["LOG_EVENT"]
        else:
            level = "LOW"
            actions = []

        return {
            "risk_score": round(total_risk, 2),
            "risk_level": level,
            "triggers": triggers,
            "actions": actions
        }