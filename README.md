# 🚨 VM & Remote Access Detection System (IICPC Track 3)

A real-time proctoring security system that detects Virtual Machines, Remote Access tools, and behavioral anomalies using a **Client–Server architecture** with a live monitoring dashboard.

---

## 🏗 System Architecture Overview

### **1. Agent** (`vm-detection-system/agent`)
Runs on the student's machine.  
Collects telemetry and performs local detection (VM checks, remote-access scans, behavior monitoring).

### **2. Server** (`vm-detection-system/server`)
FastAPI backend that:
- Receives telemetry streams
- Runs the Fusion Risk Engine
- Maintains sessions & threat logs

### **3. Dashboard** (`frontend`)
React + Vite interface for proctors:
- Live threat alerts  
- Session feed  
- Real-time risk score visualization  

---

## 🚀 Quick Start Guide

You must open **3 separate terminal windows** to run the complete stack.

### **Prerequisites**
- Python **3.10+** with `uv` installed  
- **Bun** (for frontend)

---

## 1️⃣ Start the Backend Server (Terminal 1)

Processes telemetry and risk scoring.

```bash
cd vm-detection-system/server
uv run main.py --server http://localhost:8000
```

---

## 📂 Project Structure

```
.
├── frontend/                      # React Dashboard (Bun + Vite)
│
├── vm-detection-system/
│   ├── agent/                     # Client-side detection agent
│   │   ├── detectors/             # VM / Network / Behavior detectors
│   │   └── main.py                # Agent entry point
│   │
│   └── server/                    # FastAPI backend server
│       ├── engine/                # Risk fusion engine logic
│       └── main.py                # Server entry point
│
└── ml_models/                     # LSTM & ML models used for prediction/scoring
```

---

## 🛠 Key Features

### ✔ **VM Detection**

* CPUID signature checks
* MAC address & vendor analysis
* Registry & driver inspection
* Virtualization flag detection

### ✔ **Remote Access Tool Detection**

Detects tools such as:

* AnyDesk
* TeamViewer
* RDP
* VNC
* Chrome Remote Desktop
* Screen-sharing services

### ✔ **Behavioral Analysis**

* Mouse movement entropy
* Keystroke timing irregularities
* Automation / bot-pattern detection

### ✔ **Real-Time Risk Scoring**

A weighted **Fusion Engine** produces a unified **Risk Score (0–100)** updated every 3–5 seconds.

### ✔ **Live Monitoring Dashboard**

* Active session list
* Real-time alerts
* Timeline of detected anomalies
* Session-level risk score trends

---

## 📜 License

This project is developed for **IICPC Track 3** and intended strictly for academic and proctoring-related research.

---

If you need a **LICENSE file**, **project badges**, or a **logo section**, tell me and I’ll add them.
