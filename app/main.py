from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import logging
from datetime import datetime
from pathlib import Path

from app.models import SimulationRequest, SimulationResponse, HealthResponse
from app.dwsim_runner import DWSIMRunner
from app.config import settings

# Configure logging
logging.basicConfig(level=getattr(logging, settings.log_level))
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Quinta DWSIM Service",
    description="DWSIM Chemical Process Simulation Service",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize DWSIM runner
dwsim_runner = DWSIMRunner()

@app.on_event("startup")
async def startup_event():
    """Initialize service on startup"""
    logger.info("Starting Quinta DWSIM Service")
    
    # Ensure directories exist
    for directory in [settings.temp_dir, settings.scripts_dir, settings.flow_dir, settings.reports_dir]:
        Path(directory).mkdir(parents=True, exist_ok=True)
        logger.info(f"Ensured directory exists: {directory}")
    
    # Initialize DWSIM
    try:
        await dwsim_runner.initialize()
        logger.info("DWSIM initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize DWSIM: {e}")
        raise

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    try:
        dwsim_status = await dwsim_runner.check_health()
        return HealthResponse(
            status="healthy",
            timestamp=datetime.utcnow().isoformat(),
            dwsim_status=dwsim_status,
            service="quinta-dwsim-service"
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return HealthResponse(
            status="unhealthy",
            timestamp=datetime.utcnow().isoformat(),
            error=str(e),
            service="quinta-dwsim-service"
        )

@app.post("/simulate", response_model=SimulationResponse)
async def simulate(request: SimulationRequest, background_tasks: BackgroundTasks):
    """Run DWSIM simulation"""
    try:
        logger.info(f"Starting simulation: {request.simulation_id}")
        
        # Run simulation
        result = await dwsim_runner.run_simulation(
            script_content=request.script_content,
            config=request.config,
            simulation_id=request.simulation_id
        )
        
        return SimulationResponse(
            simulation_id=request.simulation_id,
            status="completed",
            result=result,
            timestamp=datetime.utcnow().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Simulation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/simulation/{simulation_id}/status")
async def get_simulation_status(simulation_id: str):
    """Get simulation status"""
    try:
        status = await dwsim_runner.get_simulation_status(simulation_id)
        return {"simulation_id": simulation_id, "status": status}
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Simulation {simulation_id} not found")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Quinta DWSIM Service is running",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
