#!/usr/bin/env python3
"""
Behavioral Anomaly Detection Module
Detects non-human interaction patterns (mouse, keyboard)
Uses rule-based fallback when ML models aren't available
"""

import time
import statistics
from collections import deque
from typing import List, Dict, Tuple
import threading

try:
    from pynput import mouse, keyboard
    PYNPUT_AVAILABLE = True
except ImportError:
    PYNPUT_AVAILABLE = False

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False


class BehaviorMonitor:
    """Monitors user interaction patterns for anomalies"""
    
    def __init__(self, window_size=100):
        self.window_size = window_size
        self.mouse_events = deque(maxlen=window_size)
        self.keyboard_events = deque(maxlen=window_size)
        self.mouse_speeds = deque(maxlen=50)
        self.key_intervals = deque(maxlen=50)
        
        self.monitoring = False
        self.last_mouse_pos = None
        self.last_mouse_time = None
        self.last_key_time = None
        
        self.listener_mouse = None
        self.listener_keyboard = None
    
    def on_mouse_move(self, x, y):
        """Mouse movement callback"""
        current_time = time.time()
        
        if self.last_mouse_pos and self.last_mouse_time:
            # Calculate speed
            dx = x - self.last_mouse_pos[0]
            dy = y - self.last_mouse_pos[1]
            dt = current_time - self.last_mouse_time
            
            if dt > 0:
                distance = (dx**2 + dy**2) ** 0.5
                speed = distance / dt
                self.mouse_speeds.append(speed)
        
        self.mouse_events.append({
            'time': current_time,
            'x': x,
            'y': y,
            'type': 'move'
        })
        
        self.last_mouse_pos = (x, y)
        self.last_mouse_time = current_time
    
    def on_mouse_click(self, x, y, button, pressed):
        """Mouse click callback"""
        if pressed:
            self.mouse_events.append({
                'time': time.time(),
                'x': x,
                'y': y,
                'type': 'click',
                'button': str(button)
            })
    
    def on_key_press(self, key):
        """Keyboard press callback"""
        current_time = time.time()
        
        if self.last_key_time:
            interval = current_time - self.last_key_time
            self.key_intervals.append(interval)
        
        self.keyboard_events.append({
            'time': current_time,
            'key': str(key),
            'type': 'press'
        })
        
        self.last_key_time = current_time
    
    def start_monitoring(self, duration=10):
        """Start monitoring for specified duration"""
        if not PYNPUT_AVAILABLE:
            return False, "pynput library not available"
        
        self.monitoring = True
        
        # Start listeners
        self.listener_mouse = mouse.Listener(
            on_move=self.on_mouse_move,
            on_click=self.on_mouse_click
        )
        self.listener_keyboard = keyboard.Listener(
            on_press=self.on_key_press
        )
        
        self.listener_mouse.start()
        self.listener_keyboard.start()
        
        # Monitor for duration
        time.sleep(duration)
        
        self.stop_monitoring()
        return True, f"Monitored for {duration} seconds"
    
    def stop_monitoring(self):
        """Stop monitoring"""
        self.monitoring = False
        if self.listener_mouse:
            self.listener_mouse.stop()
        if self.listener_keyboard:
            self.listener_keyboard.stop()
    
    def analyze_mouse_behavior(self) -> Dict:
        """Analyze mouse behavior patterns (rule-based)"""
        if len(self.mouse_speeds) < 10:
            return {
                'sufficient_data': False,
                'anomaly_score': 0,
                'indicators': ['Insufficient mouse data']
            }
        
        indicators = []
        anomaly_score = 0
        
        # Convert to list for analysis
        speeds = list(self.mouse_speeds)
        
        # Rule 1: Check for suspiciously constant speeds
        if len(speeds) > 20:
            speed_variance = statistics.variance(speeds)
            if speed_variance < 10:  # Too consistent
                indicators.append("Mouse speed too consistent (possible automation)")
                anomaly_score += 25
        
        # Rule 2: Check for extremely high speeds (remote desktop compression)
        avg_speed = statistics.mean(speeds)
        if avg_speed > 3000:  # Pixels per second
            indicators.append(f"Unusually high mouse speed: {avg_speed:.0f} px/s")
            anomaly_score += 20
        
        # Rule 3: Check for perfect straight lines (remote control)
        if len(self.mouse_events) > 20:
            straight_line_count = 0
            events = list(self.mouse_events)
            for i in range(len(events) - 3):
                if events[i]['type'] == 'move':
                    dx1 = events[i+1]['x'] - events[i]['x']
                    dy1 = events[i+1]['y'] - events[i]['y']
                    dx2 = events[i+2]['x'] - events[i+1]['x']
                    dy2 = events[i+2]['y'] - events[i+1]['y']
                    
                    # Check if direction is perfectly maintained
                    if dx1 != 0 and dx2 != 0 and abs(dy1/dx1 - dy2/dx2) < 0.01:
                        straight_line_count += 1
            
            straight_ratio = straight_line_count / (len(events) - 3)
            if straight_ratio > 0.7:
                indicators.append(f"Too many straight mouse movements: {straight_ratio:.1%}")
                anomaly_score += 15
        
        # Rule 4: Check for jitter (common in remote desktop)
        if len(speeds) > 10:
            rapid_changes = sum(1 for i in range(len(speeds)-1) 
                              if abs(speeds[i] - speeds[i+1]) > 500)
            jitter_ratio = rapid_changes / (len(speeds) - 1)
            if jitter_ratio > 0.4:
                indicators.append(f"High mouse jitter detected: {jitter_ratio:.1%}")
                anomaly_score += 20
        
        return {
            'sufficient_data': True,
            'anomaly_score': min(anomaly_score, 100),
            'indicators': indicators if indicators else ['Normal mouse behavior'],
            'stats': {
                'avg_speed': statistics.mean(speeds),
                'speed_variance': statistics.variance(speeds) if len(speeds) > 1 else 0,
                'event_count': len(self.mouse_events)
            }
        }
    
    def analyze_keyboard_behavior(self) -> Dict:
        """Analyze keyboard behavior patterns (rule-based)"""
        if len(self.key_intervals) < 10:
            return {
                'sufficient_data': False,
                'anomaly_score': 0,
                'indicators': ['Insufficient keyboard data']
            }
        
        indicators = []
        anomaly_score = 0
        
        intervals = list(self.key_intervals)
        
        # Rule 1: Check for robotic typing (too consistent intervals)
        if len(intervals) > 15:
            interval_variance = statistics.variance(intervals)
            if interval_variance < 0.001:  # Suspiciously consistent
                indicators.append("Typing intervals too consistent (possible automation)")
                anomaly_score += 30
        
        # Rule 2: Check for unusually fast typing
        avg_interval = statistics.mean(intervals)
        if avg_interval < 0.05:  # Less than 50ms between keys
            indicators.append(f"Suspiciously fast typing: {1/avg_interval:.0f} keys/sec")
            anomaly_score += 25
        
        # Rule 3: Check for high latency (remote desktop lag)
        if len(intervals) > 20:
            high_latency_count = sum(1 for i in intervals if i > 0.5)
            if high_latency_count > len(intervals) * 0.3:
                indicators.append("High typing latency detected (possible remote control)")
                anomaly_score += 20
        
        # Rule 4: Check for burst patterns (copy-paste detection)
        if len(intervals) > 10:
            burst_count = 0
            for i in range(len(intervals) - 5):
                window = intervals[i:i+5]
                if all(val < 0.03 for val in window):  # Very fast burst
                    burst_count += 1
            
            if burst_count > 3:
                indicators.append(f"Multiple typing bursts detected: {burst_count}")
                anomaly_score += 15
        
        return {
            'sufficient_data': True,
            'anomaly_score': min(anomaly_score, 100),
            'indicators': indicators if indicators else ['Normal keyboard behavior'],
            'stats': {
                'avg_interval': statistics.mean(intervals),
                'interval_variance': statistics.variance(intervals) if len(intervals) > 1 else 0,
                'event_count': len(self.keyboard_events)
            }
        }
    
    def detect(self, monitor_duration=10) -> Dict:
        """Run behavioral detection"""
        results = {
            'behavior_anomaly': False,
            'anomaly_score': 0,
            'findings': [],
            'monitoring_available': PYNPUT_AVAILABLE
        }
        
        if not PYNPUT_AVAILABLE:
            results['findings'].append("⚠ pynput not available - install for behavior monitoring")
            return results
        
        # Start monitoring in background
        print(f"  Monitoring user behavior for {monitor_duration} seconds...")
        print("  (Move mouse and type to generate data)")
        
        success, msg = self.start_monitoring(duration=monitor_duration)
        
        if not success:
            results['findings'].append(f"Monitoring failed: {msg}")
            return results
        
        # Analyze collected data
        mouse_analysis = self.analyze_mouse_behavior()
        keyboard_analysis = self.analyze_keyboard_behavior()
        
        # Aggregate results
        if mouse_analysis['sufficient_data']:
            results['findings'].extend(mouse_analysis['indicators'])
            results['anomaly_score'] += mouse_analysis['anomaly_score'] * 0.5
        
        if keyboard_analysis['sufficient_data']:
            results['findings'].extend(keyboard_analysis['indicators'])
            results['anomaly_score'] += keyboard_analysis['anomaly_score'] * 0.5
        
        results['anomaly_score'] = min(int(results['anomaly_score']), 100)
        results['behavior_anomaly'] = results['anomaly_score'] > 40
        
        # Add stats
        results['mouse_stats'] = mouse_analysis.get('stats', {})
        results['keyboard_stats'] = keyboard_analysis.get('stats', {})
        
        if not results['findings']:
            results['findings'].append("No significant behavioral anomalies detected")
        
        return results


class SimpleMLBehaviorDetector:
    """ML-based behavior detector with rule-based fallback"""
    
    def __init__(self):
        self.model_loaded = False
        self.use_ml = NUMPY_AVAILABLE
    
    def train_simple_model(self, data):
        """Simple threshold-based model (fallback)"""
        # This is a placeholder for actual ML model
        # In production, you'd load a pre-trained model here
        pass
    
    def predict_anomaly(self, features) -> Tuple[bool, float]:
        """Predict if behavior is anomalous"""
        if not self.use_ml:
            # Rule-based fallback
            return self._rule_based_prediction(features)
        
        # ML prediction would go here
        return self._rule_based_prediction(features)
    
    def _rule_based_prediction(self, features) -> Tuple[bool, float]:
        """Fallback rule-based prediction"""
        score = 0
        
        if features.get('mouse_speed_variance', 100) < 10:
            score += 30
        if features.get('typing_speed', 0) > 20:
            score += 25
        if features.get('latency', 0) > 0.5:
            score += 20
        
        is_anomalous = score > 40
        return is_anomalous, score