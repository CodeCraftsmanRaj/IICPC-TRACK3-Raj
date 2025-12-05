from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from database import Base
from datetime import datetime

class TelemetryRecord(Base):
    __tablename__ = "telemetry"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Risk Assessment
    risk_score = Column(Float)
    risk_level = Column(String)
    
    # Store nested JSON data as Strings (serialized JSON)
    # This prevents complex relationships for a simple dashboard
    vm_data = Column(Text)       
    remote_data = Column(Text)
    screen_data = Column(Text)
    behavior_data = Column(Text)
    network_data = Column(Text)
    process_data = Column(Text)
    
    # Store lists as comma-separated strings or JSON
    triggers = Column(Text) 
    actions = Column(Text)