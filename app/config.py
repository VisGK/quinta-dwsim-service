from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    """Application settings"""
    
    # Service Configuration
    service_name: str = "Quinta DWSIM Service"
    service_version: str = "1.0.0"
    log_level: str = "INFO"
    
    # DWSIM Configuration
    dwsim_timeout: int = 300  # seconds
    dwsim_path: str = "/app/dwsim"
    dwsim_bin_path: str = "/app/dwsim/DWSIM.exe"
    
    # File Paths
    temp_dir: str = "/app/temp"
    scripts_dir: str = "/app/scripts"
    flow_dir: str = "/app/flow"
    reports_dir: str = "/app/reports"
    
    # API Configuration
    port: int = 8001
    host: str = "0.0.0.0"
    
    # Security
    auth_token: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
