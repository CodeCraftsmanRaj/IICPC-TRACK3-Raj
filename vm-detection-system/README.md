# VM & Remote Access Detection System - Complete Implementation

**Comprehensive real-time detection system for virtual machines, remote access tools, screen sharing, behavioral anomalies, network suspicious activity, and system-level threats.**

---

## 🚀 Quick Start

```bash
# Windows
install.bat
python cli_detector.py

# Linux/Mac
chmod +x install.sh
./install.sh
python3 cli_detector.py
```

---

## 📦 Complete Module List

### ✅ **Core Modules** (Always Available)
1. **VM Detection** - VMware, VirtualBox, Hyper-V, QEMU, Parallels
2. **Remote Access Detection** - RDP, TeamViewer, AnyDesk, VNC, Chrome Remote
3. **Screen Sharing Detection** - Multi-monitor, OBS, Discord, Zoom, Teams

### 🔧 **Advanced Modules** (Install Optional Dependencies)
4. **Behavioral Analysis** - Mouse/keyboard pattern anomalies (requires `pynput`)
5. **Network Analysis** - Connection patterns, bandwidth monitoring
6. **IDS Engine** - Intrusion detection, port scans, data exfiltration
7. **Process Forensics** - Suspicious processes, injection detection
8. **System Integrity** - Startup items, drivers, services
9. **WebGL Fingerprinting** - GPU-based VM detection
10. **Timing Attacks** - Hypervisor detection via timing variance

---

## 📋 Installation

### Option 1: Quick Install (Recommended)
```bash
# Windows
install.bat

# Linux/Mac
chmod +x install.sh && ./install.sh
```

### Option 2: Manual Install
```bash
# Minimum (core features only)
pip install psutil

# Recommended (most features)
pip install psutil pynput

# Full (Windows - all features)
pip install psutil pynput pywin32

# Advanced (optional - packet analysis)
pip install scapy  # Requires admin/root
```

---

## 🎯 Usage Examples

### Basic Scan (2-3 seconds)
```bash
python cli_detector.py
```

### Full Scan (includes 8-sec behavior monitoring)
```bash
python cli_detector.py --full
```

### Save Results to JSON
```bash
python cli_detector.py --json results.json
python cli_detector.py --full --json detailed_results.json
```

### Continuous Monitoring
```bash
python cli_detector.py --monitor           # Every 30 seconds
python cli_detector.py --monitor -i 60     # Every 60 seconds
```

---

## 🔍 Detection Capabilities

### 1. **Virtual Machine Detection**
- ✅ Process signatures (VMware Tools, VBox Guest Additions)
- ✅ BIOS/System vendor checks
- ✅ MAC address fingerprinting
- ✅ Registry keys (Windows)
- ✅ CPU hypervisor flags
- ✅ GPU renderer detection
- ✅ Timing-based detection

### 2. **Remote Access Detection**
- ✅ Active processes (TeamViewer, AnyDesk, etc.)
- ✅ RDP session detection
- ✅ Network ports (3389, 5900, 5938, etc.)
- ✅ Registry analysis
- ✅ Shadow sessions

### 3. **Screen Sharing Detection**
- ✅ Multi-monitor enumeration
- ✅ Display mirroring detection
- ✅ Screen capture tools (OBS, XSplit)
- ✅ Communication apps (Zoom, Discord, Teams)

### 4. **Behavioral Analysis** (requires pynput)
- ✅ Mouse movement patterns
- ✅ Keyboard typing patterns
- ✅ Speed consistency analysis
- ✅ Remote control indicators
- ✅ Latency detection

### 5. **Network Analysis**
- ✅ Active connection enumeration
- ✅ Suspicious port detection
- ✅ Connection pattern analysis
- ✅ Bandwidth monitoring
- ✅ Private network connections

### 6. **Intrusion Detection**
- ✅ Port scan detection
- ✅ Data exfiltration patterns
- ✅ Process network activity
- ✅ Asymmetric traffic analysis

### 7. **Process Forensics**
- ✅ Suspicious process names
- ✅ Temp directory execution
- ✅ Process injection indicators
- ✅ High thread count detection

### 8. **System Integrity**
- ✅ Startup item analysis
- ✅ Driver enumeration
- ✅ Service inspection
- ✅ System modification detection

---

## 📊 Output Example

```
================================================================================
 VM & REMOTE ACCESS DETECTION SYSTEM - COMPREHENSIVE SCAN
================================================================================
 Scan Time: 2024-12-05 15:30:45
 Platform: win32
================================================================================

📦 AVAILABLE MODULES:
  ✓ Core VM Detection
  ✓ Remote Access Detection
  ✓ Screen Sharing Detection
  ✓ Behavior Analysis
  ✓ Network Analysis
  ✓ System Forensics

🔍 RUNNING DETECTION MODULES...
[1/10] VM Detection...
[2/10] Remote Access Detection...
...

================================================================================
 OVERALL RISK ASSESSMENT
================================================================================

📊 Overall Risk Score: 45/100
🎯 Risk Level: 🟡 MEDIUM

⚠️  Risk Factors Detected:
  1. Virtual Machine (65%)
  2. Network Anomaly
```

---

## 🏗️ Architecture

### Detection Layers
```
┌─────────────────────────────────────────┐
│  CLI Interface (cli_detector.py)        │
├─────────────────────────────────────────┤
│  Detection Orchestrator                 │
├─────────────────────────────────────────┤
│  ┌─────────────┐  ┌──────────────────┐  │
│  │ VM Detector │  │ Remote Detector  │  │
│  └─────────────┘  └──────────────────┘  │
│  ┌─────────────┐  ┌──────────────────┐  │
│  │  Behavior   │  │    Network       │  │
│  └─────────────┘  └──────────────────┘  │
│  ┌─────────────┐  ┌──────────────────┐  │
│  │  Forensics  │  │      IDS         │  │
│  └─────────────┘  └──────────────────┘  │
├─────────────────────────────────────────┤
│  Rule-Based Engine (Fallback)           │
│  ML-Ready Architecture (Optional)       │
└─────────────────────────────────────────┘
```

### Module Independence
Each module works independently with graceful fallbacks:
- **Core modules** require only `psutil`
- **Advanced modules** are optional
- **Missing dependencies** trigger fallback to rule-based detection
- **No module failure** breaks the entire system

---

## 🧪 Testing

### Test on VM
```bash
# Should detect VM with high confidence
python cli_detector.py
```

### Test with Remote Desktop
```bash
# Connect via RDP first, then run
python cli_detector.py --full
```

### Test Multi-Monitor
```bash
# Connect second display, then run
python cli_detector.py
```

---

## 🔧 File Structure

```
vm-detection-system/
├── cli_detector.py           # Main CLI tool (orchestrator)
├── vm_detector.py            # VM detection engine
├── behavior_detector.py      # Behavioral analysis
├── network_detector.py       # Network & IDS
├── system_forensics.py       # Process & integrity checks
├── requirements.txt          # Dependencies
├── install.bat              # Windows installer
├── install.sh               # Linux/Mac installer
└── README.md                # This file
```

---

## 🛠️ Technical Details

### Detection Methods

**Rule-Based (Primary)**
- Process enumeration
- Registry inspection
- System fingerprinting
- Network analysis
- Hardware checks

**Heuristic Analysis**
- Pattern matching
- Threshold detection
- Behavioral rules
- Timing analysis

**ML-Ready Architecture**
- Feature extraction layers
- Fallback to rule-based
- Easy model integration
- Extensible design

---

## 🚨 Limitations

1. **Advanced Evasion**: Sophisticated VM hiding techniques may bypass detection
2. **Encrypted Tools**: Some remote access tools with strong encryption harder to detect
3. **Permissions**: Some checks require administrator/root privileges
4. **Platform**: Full features work best on Windows; limited on Linux/Mac
5. **Behavior Analysis**: Requires user interaction during scan

---

## 🎓 Research Context

### Detection Techniques Implemented
1. **CPUID & Hypervisor Flags** - CPU-level VM detection
2. **MAC Address Fingerprinting** - Network hardware signatures
3. **Registry Forensics** - Windows system artifacts
4. **Process Memory Analysis** - Runtime process inspection
5. **Network Traffic Patterns** - Connection behavior analysis
6. **GPU Fingerprinting** - WebGL renderer detection
7. **Timing Attacks** - Hypervisor scheduling variance
8. **Behavioral Heuristics** - Human interaction patterns

### Use Case
Designed for educational integrity monitoring in online examination environments. Detects attempts to:
- Run exams in virtual machines (multiple OS instances)
- Use remote assistance during exams
- Share screens with others
- Exhibit non-human interaction patterns

---

## 📈 Performance

- **Quick Scan**: 2-3 seconds
- **Full Scan**: 10-12 seconds (with behavior monitoring)
- **CPU Usage**: < 5% average
- **Memory**: < 50MB
- **Monitoring Overhead**: < 2% continuous

---

## 🤝 Contributing

This is a proof-of-concept for the IICPC Technical Challenge. To extend:

1. Add new detectors in separate modules
2. Implement ML models (replace rule-based fallbacks)
3. Enhance evasion resistance
4. Add cross-platform support
5. Improve performance

---

## 📝 License

Educational/Research Project - IICPC Technical Challenge Track 3

---

## 👤 Author

**Raj Kalpesh Mathuria**  
IITM / SPIT (B. Tech 3rd year)

**Background**: NTRO (Intelligence), ISRO (ML Engineering), Barclays (Confirmed Internship), SIH National Winner, Multiple Research Publications

---

## 🎯 Challenge Submission

This implementation addresses all requirements:
- ✅ Research on cheating methods
- ✅ Technical indicators identification
- ✅ Detection system implementation
- ✅ Real-time monitoring
- ✅ Evasion resistance
- ✅ Documentation

**Key Features**:
- 10 detection modules
- Rule-based with ML-ready architecture
- Graceful fallbacks for missing dependencies
- Production-grade code structure
- Comprehensive documentation