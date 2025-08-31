import asyncio
import subprocess
import os
import logging
import tempfile
from pathlib import Path
from typing import Dict, Any, Optional
import json

from app.config import settings

logger = logging.getLogger(__name__)

class DWSIMRunner:
    """DWSIM simulation runner"""
    
    def __init__(self):
        self.dwsim_path = settings.dwsim_bin_path
        self.timeout = settings.dwsim_timeout
        self.simulations = {}  # Track running simulations
        
    async def initialize(self):
        """Initialize DWSIM environment"""
        try:
            # Check if DWSIM is available
            if not os.path.exists(self.dwsim_path):
                logger.warning(f"DWSIM not found at {self.dwsim_path}")
                # In production, this would download/install DWSIM
                return False
            
            logger.info("DWSIM initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize DWSIM: {e}")
            return False
    
    async def check_health(self) -> str:
        """Check DWSIM health"""
        try:
            if os.path.exists(self.dwsim_path):
                return "available"
            else:
                return "not_found"
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return "error"
    
    async def run_simulation(
        self, 
        script_content: str, 
        config: Dict[str, Any], 
        simulation_id: str
    ) -> Dict[str, Any]:
        """Run DWSIM simulation"""
        
        # Create temporary files
        script_file = Path(settings.scripts_dir) / f"{simulation_id}.py"
        output_file = Path(settings.reports_dir) / f"{simulation_id}_output.json"
        
        try:
            # Write script to file
            script_file.write_text(script_content)
            
            # Update simulation status
            self.simulations[simulation_id] = {
                "status": "running",
                "progress": 0.0,
                "start_time": asyncio.get_event_loop().time()
            }
            
            # Run simulation using Wine
            result = await self._execute_dwsim_script(script_file, output_file)
            
            # Update status
            self.simulations[simulation_id]["status"] = "completed"
            self.simulations[simulation_id]["progress"] = 100.0
            
            return result
            
        except Exception as e:
            # Update status
            self.simulations[simulation_id]["status"] = "failed"
            self.simulations[simulation_id]["error"] = str(e)
            
            logger.error(f"Simulation {simulation_id} failed: {e}")
            raise
            
        finally:
            # Cleanup temporary files
            if script_file.exists():
                script_file.unlink()
    
    async def _execute_dwsim_script(self, script_file: Path, output_file: Path) -> Dict[str, Any]:
        """Execute DWSIM script using Wine"""
        
        # Create the command to run DWSIM with the script
        cmd = [
            "wine", 
            self.dwsim_path,
            "/script", str(script_file),
            "/output", str(output_file)
        ]
        
        try:
            # Run the command
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await asyncio.wait_for(
                process.communicate(), 
                timeout=self.timeout
            )
            
            if process.returncode != 0:
                raise Exception(f"DWSIM execution failed: {stderr.decode()}")
            
            # Read output file
            if output_file.exists():
                with open(output_file, 'r') as f:
                    result = json.load(f)
            else:
                result = {"message": "Simulation completed", "stdout": stdout.decode()}
            
            return result
            
        except asyncio.TimeoutError:
            raise Exception(f"Simulation timed out after {self.timeout} seconds")
        except Exception as e:
            raise Exception(f"DWSIM execution error: {e}")
    
    async def get_simulation_status(self, simulation_id: str) -> Dict[str, Any]:
        """Get simulation status"""
        if simulation_id not in self.simulations:
            raise Exception(f"Simulation {simulation_id} not found")
        
        return self.simulations[simulation_id]
