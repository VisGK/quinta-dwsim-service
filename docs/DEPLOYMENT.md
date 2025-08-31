# DWSIM Service Deployment Guide

## Overview

This guide covers deploying the Quinta DWSIM Service to various platforms.

## Railway Deployment (Recommended)

### Prerequisites

- Railway account
- GitHub repository access
- Docker knowledge (basic)

### Step 1: Connect to Railway

1. Go to [railway.app](https://railway.app)
2. Sign in with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose your `quinta-dwsim-service` repository

### Step 2: Configure Environment Variables

In Railway dashboard, add these variables:

```env
# Service Configuration
PORT=8001
LOG_LEVEL=INFO

# DWSIM Configuration
DWSIM_TIMEOUT=300
DWSIM_PATH=/app/dwsim
DWSIM_BIN_PATH=/app/dwsim/DWSIM.exe

# Security (Optional)
AUTH_TOKEN=your-secure-auth-token

# File Paths
TEMP_DIR=/app/temp
SCRIPTS_DIR=/app/scripts
FLOW_DIR=/app/flow
REPORTS_DIR=/app/reports
```

### Step 3: Deploy

Railway will automatically:
- Build the Docker container
- Install DWSIM and dependencies
- Start the service
- Make it available at `https://your-service-name.railway.app`

## Docker Deployment

### Local Development

```bash
# Build the image
docker build -t quinta-dwsim .

# Run the container
docker run -p 8001:8001 quinta-dwsim
```

### Production Deployment

```bash
# Build with production settings
docker build -t quinta-dwsim:latest .

# Run with environment variables
docker run -d \
  -p 8001:8001 \
  -e AUTH_TOKEN=your-token \
  -e LOG_LEVEL=INFO \
  --name quinta-dwsim \
  quinta-dwsim:latest
```

## Render Deployment

### Step 1: Create Service

1. Go to [render.com](https://render.com)
2. Create new Web Service
3. Connect your GitHub repository

### Step 2: Configure

```yaml
# render.yaml
services:
  - type: web
    name: quinta-dwsim-service
    env: docker
    dockerfilePath: ./Dockerfile
    plan: starter
    healthCheckPath: /health
    envVars:
      - key: PORT
        value: 8001
      - key: DWSIM_TIMEOUT
        value: 300
```

## Google Cloud Run

### Deploy Command

```bash
gcloud run deploy quinta-dwsim \
  --source . \
  --platform managed \
  --region us-central1 \
  --memory 2Gi \
  --timeout 900 \
  --max-instances 10 \
  --set-env-vars PORT=8001,DWSIM_TIMEOUT=300
```

## Health Monitoring

### Health Check Endpoint

```
GET /health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00Z",
  "service": "quinta-dwsim-service",
  "dwsim_status": "available"
}
```

### Monitoring Setup

1. **Railway**: Built-in monitoring
2. **Custom**: Set up alerts for `/health` endpoint
3. **Logs**: Monitor application logs for errors

## Troubleshooting

### Common Issues

1. **DWSIM not found**
   - Check DWSIM installation in Dockerfile
   - Verify DWSIM_BIN_PATH environment variable

2. **Wine issues**
   - Ensure Xvfb is running
   - Check Wine installation

3. **Timeout errors**
   - Increase DWSIM_TIMEOUT
   - Check simulation complexity

### Debug Commands

```bash
# Check container logs
docker logs quinta-dwsim

# Access container shell
docker exec -it quinta-dwsim /bin/bash

# Test DWSIM directly
wine /app/dwsim/DWSIM.exe --help
```

## Security Considerations

1. **Authentication**: Use AUTH_TOKEN for API access
2. **Network**: Restrict access to trusted sources
3. **Updates**: Keep dependencies updated
4. **Monitoring**: Monitor for unusual activity

## Performance Optimization

1. **Resource Limits**: Set appropriate memory/CPU limits
2. **Caching**: Implement result caching for repeated simulations
3. **Queue Management**: Handle multiple concurrent simulations
4. **Cleanup**: Regular cleanup of temporary files
