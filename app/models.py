from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from datetime import datetime

class SimulationRequest(BaseModel):
    """Request model for simulation"""
    simulation_id: str = Field(..., description="Unique simulation identifier")
    script_content: str = Field(..., description="Python script content for DWSIM")
    config: Dict[str, Any] = Field(default_factory=dict, description="Simulation configuration")

class SimulationResponse(BaseModel):
    """Response model for simulation"""
    simulation_id: str
    status: str
    result: Dict[str, Any]
    timestamp: str
    error: Optional[str] = None

class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    timestamp: str
    service: str
    dwsim_status: Optional[str] = None
    error: Optional[str] = None

class SimulationStatus(BaseModel):
    """Simulation status response"""
    simulation_id: str
    status: str
    progress: Optional[float] = None
    message: Optional[str] = None
