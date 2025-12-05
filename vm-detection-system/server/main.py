import uvicorn
import json
from collections import Counter
from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime, timedelta
from typing import List

from database import SessionLocal, engine, Base
from models import TelemetryRecord
from schemas import TelemetryData, AlertResponse
from engine.fusion_engine import DecisionFusionEngine

# Create Tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="VM & Remote Access Detection System API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

fusion_engine = DecisionFusionEngine()

# --- AGENT ENDPOINTS ---

@app.post("/api/v1/telemetry/{session_id}", response_model=AlertResponse)
async def ingest_telemetry(
    session_id: str, 
    data: TelemetryData, 
    db: Session = Depends(get_db)
):
    # Real-time Analysis
    analysis = fusion_engine.analyze(data.dict())
    
    # Save to DB
    db_record = TelemetryRecord(
        session_id=session_id,
        timestamp=datetime.now(),
        risk_score=analysis['risk_score'],
        risk_level=analysis['risk_level'],
        vm_data=json.dumps(data.vm_data),
        remote_data=json.dumps(data.remote_data),
        screen_data=json.dumps(data.screen_data),
        behavior_data=json.dumps(data.behavior_data),
        network_data=json.dumps(data.network_data),
        process_data=json.dumps(data.process_data),
        triggers=json.dumps(analysis['triggers']),
        actions=json.dumps(analysis['actions'])
    )
    
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    
    return {
        "status": "processed",
        "risk_score": analysis['risk_score'],
        "risk_level": analysis['risk_level'],
        "actions_required": analysis['actions']
    }

# --- DASHBOARD ENDPOINTS ---

@app.get("/api/v1/dashboard/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    five_min_ago = datetime.now() - timedelta(minutes=5)
    
    # Active sessions in last 5 mins
    active_count = db.query(TelemetryRecord.session_id).filter(
        TelemetryRecord.timestamp >= five_min_ago
    ).distinct().count()
    
    # Total critical alerts
    critical_count = db.query(TelemetryRecord).filter(
        TelemetryRecord.risk_level == 'CRITICAL'
    ).count()
    
    # Count specific threat types via string matching in JSON
    # (In production, use specific boolean columns for performance)
    vm_count = db.query(TelemetryRecord).filter(
        TelemetryRecord.triggers.like('%Virtual Machine%')
    ).count()
    
    rdp_count = db.query(TelemetryRecord).filter(
        TelemetryRecord.triggers.like('%Remote Access%')
    ).count()
    
    return {
        "active_sessions": active_count,
        "critical_threats": critical_count,
        "vms_detected": vm_count,
        "rdp_detected": rdp_count,
        "total_alerts": db.query(TelemetryRecord).count()
    }

@app.get("/api/v1/telemetry/events")
def get_telemetry_events(limit: int = 50, db: Session = Depends(get_db)):
    records = db.query(TelemetryRecord).order_by(
        TelemetryRecord.timestamp.desc()
    ).limit(limit).all()
    
    events = []
    for r in records:
        triggers = json.loads(r.triggers)
        # Determine main trigger type for UI display
        main_trigger = triggers[0] if triggers else "Routine Check"
        
        events.append({
            "id": str(r.id),
            "timestamp": r.timestamp.isoformat(),
            "user_id": r.session_id,
            "risk_score": r.risk_score,
            "risk_level": r.risk_level,
            "trigger_type": main_trigger,
            "triggers": triggers,
            "status": "open" if r.risk_score > 50 else "resolved",
            "vm_data": json.loads(r.vm_data),
            "remote_data": json.loads(r.remote_data),
            "screen_data": json.loads(r.screen_data),
            "behavior_data": json.loads(r.behavior_data)
        })
    return events

@app.get("/api/v1/threats/distribution")
def get_threat_distribution(db: Session = Depends(get_db)):
    # Group by risk level
    results = db.query(
        TelemetryRecord.risk_level, func.count(TelemetryRecord.risk_level)
    ).group_by(TelemetryRecord.risk_level).all()
    
    dist = {r[0]: r[1] for r in results}
    
    return [
        {"name": "Critical", "value": dist.get("CRITICAL", 0), "color": "hsl(0, 72%, 51%)"},
        {"name": "High", "value": dist.get("HIGH", 0), "color": "hsl(38, 92%, 50%)"},
        {"name": "Medium", "value": dist.get("MEDIUM", 0), "color": "hsl(48, 96%, 53%)"},
        {"name": "Low", "value": dist.get("LOW", 0), "color": "hsl(199, 89%, 48%)"},
    ]

@app.get("/api/v1/threats/top")
def get_top_threats(db: Session = Depends(get_db)):
    """
    Parses triggers from the last 100 records to find top threats.
    This replaces the dummy data with real aggregated data.
    """
    records = db.query(TelemetryRecord.triggers).order_by(
        TelemetryRecord.timestamp.desc()
    ).limit(100).all()
    
    all_triggers = []
    for r in records:
        triggers = json.loads(r[0])
        all_triggers.extend(triggers)
        
    # Count occurrences
    counts = Counter(all_triggers)
    
    # Format for Frontend
    # If DB is empty, return empty list to show "No Data" instead of fake data
    return [{"name": name, "count": count} for name, count in counts.most_common(6)]

@app.get("/api/v1/users/{user_id}/detail")
def get_user_detail(user_id: str, db: Session = Depends(get_db)):
    records = db.query(TelemetryRecord).filter(
        TelemetryRecord.session_id == user_id
    ).order_by(TelemetryRecord.timestamp.desc()).limit(20).all()
    
    if not records:
        raise HTTPException(status_code=404, detail="User not found")
        
    latest = records[0]
    vm_data = json.loads(latest.vm_data)
    remote_data = json.loads(latest.remote_data)
    screen_data = json.loads(latest.screen_data)
    behavior_data = json.loads(latest.behavior_data)
    
    history = [
        {"timestamp": r.timestamp.isoformat(), "risk_score": r.risk_score} 
        for r in records
    ]
    
    return {
        "user_id": user_id,
        "risk_score": latest.risk_score,
        "risk_level": latest.risk_level,
        "vm_check": vm_data.get('is_vm', False),
        "remote_access": remote_data.get('remote_detected', False),
        "screen_sharing": screen_data.get('screen_sharing_risk', False),
        "behavior_anomaly": behavior_data.get('behavior_anomaly', False),
        "vm_confidence": vm_data.get('confidence', 0),
        "remote_confidence": remote_data.get('risk_score', 0),
        "telemetry_history": history,
        "triggers": json.loads(latest.triggers),
        "session_start": records[-1].timestamp.isoformat(),
        "last_activity": latest.timestamp.isoformat()
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)