import uvicorn
from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Dict, Any

from database import SessionLocal, engine, Base
from schemas import TelemetryData, AlertResponse
from engine.fusion_engine import DecisionFusionEngine

# Initialize Database
Base.metadata.create_all(bind=engine)

app = FastAPI(title="VM & Remote Access Detection System API")

# CORS for Frontend (Lovable/React)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize Engines
fusion_engine = DecisionFusionEngine()

@app.get("/")
def read_root():
    return {"status": "active", "system": "IICPC Track 3 Detection Engine"}

@app.post("/api/v1/telemetry/{session_id}", response_model=AlertResponse)
async def ingest_telemetry(
    session_id: str, 
    data: TelemetryData, 
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Receives JSON telemetry from the Client Agent.
    Runs the Fusion Engine to determine risk.
    """
    # 1. Log raw data (in production, send to TimescaleDB/Mongo)
    print(f"[{datetime.now()}] Received telemetry from {session_id}")
    
    # 2. Real-time Analysis via Fusion Engine
    risk_assessment = fusion_engine.analyze(data.dict())
    
    # 3. Store significant alerts in SQL (Simplified)
    # In a real impl, you'd save to the DB model here
    
    return {
        "status": "processed",
        "risk_score": risk_assessment['risk_score'],
        "risk_level": risk_assessment['risk_level'],
        "actions_required": risk_assessment['actions']
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)