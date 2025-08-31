# DWSIM Service API Documentation

## Overview

The Quinta DWSIM Service provides a REST API for running DWSIM chemical process simulations.

## Base URL

```
https://your-dwsim-service.railway.app
```

## Authentication

The service supports optional token-based authentication. Include the token in the Authorization header:

```
Authorization: Bearer your-auth-token
```

## Endpoints

### Health Check

**GET** `/health`

Check the health status of the service and DWSIM availability.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00Z",
  "service": "quinta-dwsim-service",
  "dwsim_status": "available"
}
```

### Run Simulation

**POST** `/simulate`

Run a DWSIM simulation with the provided script and configuration.

**Request Body:**
```json
{
  "simulation_id": "sim_123",
  "script_content": "import dwsim\n# Your DWSIM script here",
  "config": {
    "timeout": 300,
    "parameters": {}
  }
}
```

**Response:**
```json
{
  "simulation_id": "sim_123",
  "status": "completed",
  "result": {
    "message": "Simulation completed successfully",
    "data": {}
  },
  "timestamp": "2024-01-01T00:00:00Z"
}
```

### Get Simulation Status

**GET** `/simulation/{simulation_id}/status`

Get the status of a running or completed simulation.

**Response:**
```json
{
  "simulation_id": "sim_123",
  "status": "running",
  "progress": 75.5,
  "message": "Processing simulation..."
}
```

## Error Responses

All endpoints return standard HTTP status codes:

- `200` - Success
- `400` - Bad Request
- `404` - Not Found
- `500` - Internal Server Error

Error responses include a detail message:

```json
{
  "detail": "Simulation failed: DWSIM execution error"
}
```

## Rate Limiting

The service implements rate limiting to prevent abuse. Limits are configurable via environment variables.

## Timeouts

Simulations have a configurable timeout (default: 300 seconds). Long-running simulations will be terminated if they exceed this limit.
