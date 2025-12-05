from pydantic import BaseModel
from typing import List, Dict, Optional, Any

class TelemetryData(BaseModel):
    timestamp: str
    platform: str
    vm_data: Dict[str, Any]
    remote_data: Dict[str, Any]
    screen_data: Dict[str, Any]
    behavior_data: Dict[str, Any]
    network_data: Dict[str, Any]
    process_data: Dict[str, Any]
    
class AlertResponse(BaseModel):
    status: str
    risk_score: float
    risk_level: str
    actions_required: List[str]