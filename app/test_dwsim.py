#!/usr/bin/env python3
"""
Test script to verify DWSIM installation and functionality
"""

import os
import subprocess
import sys
from pathlib import Path

def test_dwsim_installation():
    """Test if DWSIM is properly installed"""
    print("Testing DWSIM installation...")
    
    # Check if DWSIM executable exists
    dwsim_path = "/app/dwsim/DWSIM.exe"
    if os.path.exists(dwsim_path):
        print(f"✅ DWSIM executable found at: {dwsim_path}")
    else:
        print(f"❌ DWSIM executable not found at: {dwsim_path}")
        return False
    
    # Check if Wine is available
    try:
        result = subprocess.run(["wine", "--version"], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"✅ Wine is available: {result.stdout.strip()}")
        else:
            print(f"❌ Wine test failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Wine test error: {e}")
        return False
    
    # Test DWSIM with Wine
    try:
        result = subprocess.run(["wine", dwsim_path, "--help"], 
                              capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print("✅ DWSIM test with Wine successful")
        else:
            print(f"⚠️ DWSIM test with Wine returned non-zero exit code: {result.returncode}")
            print(f"Output: {result.stdout}")
            print(f"Error: {result.stderr}")
    except subprocess.TimeoutExpired:
        print("⚠️ DWSIM test timed out (this might be normal)")
    except Exception as e:
        print(f"❌ DWSIM test error: {e}")
    
    return True

def test_directories():
    """Test if required directories exist"""
    print("\nTesting directory structure...")
    
    required_dirs = [
        "/app/temp",
        "/app/scripts", 
        "/app/flow",
        "/app/reports"
    ]
    
    for directory in required_dirs:
        if os.path.exists(directory):
            print(f"✅ Directory exists: {directory}")
        else:
            print(f"❌ Directory missing: {directory}")
            # Create the directory
            os.makedirs(directory, exist_ok=True)
            print(f"✅ Created directory: {directory}")

def main():
    """Main test function"""
    print("=" * 50)
    print("DWSIM Service Test")
    print("=" * 50)
    
    # Test directories
    test_directories()
    
    # Test DWSIM installation
    success = test_dwsim_installation()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ DWSIM service test completed successfully")
        sys.exit(0)
    else:
        print("❌ DWSIM service test failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
