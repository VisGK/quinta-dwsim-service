# Quinta DWSIM Service

A containerized DWSIM simulation service for the Quinta chemical process platform.

## ⚖️ Legal Notice

This service uses DWSIM, which is licensed under GPL v3. DWSIM is developed by Daniel Medeiros and contributors. This wrapper service is licensed separately under MIT.

- **DWSIM**: GPL v3 License - https://github.com/DanWBR/dwsim6
- **This Service**: MIT License

## 🚀 Quick Start

### Using Docker
```bash
docker build -t quinta-dwsim .
docker run -p 8001:8001 quinta-dwsim
```

### Deploy to Railway
```bash
railway login
railway link
railway up
```

## 📖 API Documentation

See [API.md](docs/API.md) for complete endpoint documentation.

## 🔧 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PORT` | Service port | `8001` |
| `DWSIM_TIMEOUT` | Simulation timeout (seconds) | `300` |
| `LOG_LEVEL` | Logging level | `INFO` |
| `AUTH_TOKEN` | API authentication token | None |

## 📋 Legal Compliance

This service includes DWSIM under its GPL v3 license. See [LEGAL.md](docs/LEGAL.md) for full compliance details.

## 🏗️ Architecture

This service provides a REST API wrapper around DWSIM for chemical process simulation. It handles:

- Script execution in DWSIM
- File management (flowsheets, reports)
- Simulation monitoring
- Result processing and formatting

## 🔗 Integration

Connect this service to your main Quinta backend by setting the `DWSIM_SERVICE_URL` environment variable.

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.