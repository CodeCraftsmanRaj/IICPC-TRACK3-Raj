import uvicorn
import json
from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func
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
    allow_origins=["*"], # In production, set to frontend URL
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

# --- AGENT ENDPOINTS (Ingestion) ---

@app.post("/api/v1/telemetry/{session_id}", response_model=AlertResponse)
async def ingest_telemetry(
    session_id: str, 
    data: TelemetryData, 
    db: Session = Depends(get_db)
):
    # 1. Analyze Data
    analysis = fusion_engine.analyze(data.dict())
    
    # 2. Store in Database (Real persistence)
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

# --- FRONTEND ENDPOINTS (Visualization) ---

@app.get("/api/v1/dashboard/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    """Returns real aggregate statistics from the database"""
    # Active sessions (unique session_ids in last 5 minutes)
    five_min_ago = datetime.now() - timedelta(minutes=5)
    active_count = db.query(TelemetryRecord.session_id).filter(
        TelemetryRecord.timestamp >= five_min_ago
    ).distinct().count()
    
    # Count Critical Threats (Total)
    critical_count = db.query(TelemetryRecord).filter(
        TelemetryRecord.risk_level == 'CRITICAL'
    ).count()
    
    # Simple keyword search in stored JSON for specific threats
    vm_count = db.query(TelemetryRecord).filter(
        TelemetryRecord.vm_data.like('%"is_vm": true%')
    ).count()
    
    rdp_count = db.query(TelemetryRecord).filter(
        TelemetryRecord.remote_data.like('%"remote_detected": true%')
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
    """Returns list of recent events for the feed"""
    records = db.query(TelemetryRecord).order_by(
        TelemetryRecord.timestamp.desc()
    ).limit(limit).all()
    
    events = []
    for r in records:
        # Convert DB model back to Frontend format
        triggers = json.loads(r.triggers)
        events.append({
            "id": str(r.id),
            "timestamp": r.timestamp.isoformat(),
            "user_id": r.session_id,
            "risk_score": r.risk_score,
            "risk_level": r.risk_level,
            "trigger_type": triggers[0] if triggers else "Routine Scan",
            "triggers": triggers,
            "status": "open" if r.risk_score > 50 else "resolved",
            # Deserialize JSON strings back to objects
            "vm_data": json.loads(r.vm_data),
            "remote_data": json.loads(r.remote_data),
            "screen_data": json.loads(r.screen_data),
            "behavior_data": json.loads(r.behavior_data)
        })
    return events

@app.get("/api/v1/threats/distribution")
def get_threat_distribution(db: Session = Depends(get_db)):
    """Returns counts grouped by risk level"""
    results = db.query(
        TelemetryRecord.risk_level, func.count(TelemetryRecord.risk_level)
    ).group_by(TelemetryRecord.risk_level).all()
    
    dist_map = {r[0]: r[1] for r in results}
    
    return [
        {"name": "Critical", "value": dist_map.get("CRITICAL", 0), "color": "hsl(0, 72%, 51%)"},
        {"name": "High", "value": dist_map.get("HIGH", 0), "color": "hsl(38, 92%, 50%)"},
        {"name": "Medium", "value": dist_map.get("MEDIUM", 0), "color": "hsl(48, 96%, 53%)"},
        {"name": "Low", "value": dist_map.get("LOW", 0), "color": "hsl(199, 89%, 48%)"},
    ]

@app.get("/api/v1/users/{user_id}/detail")
def get_user_detail(user_id: str, db: Session = Depends(get_db)):
    """Get detailed history for a specific user"""
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