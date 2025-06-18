# Robot Platform

This repository contains a minimal skeleton for the trading platform described in the technical specification. Each service is implemented as a small FastAPI application.

## Services

- `api-gateway`
- `indicator-engine`
- `strategy-engine`
- `trade-executor`
- `market-data`
- `backtester`

## Running with Docker Compose

Build and run all services:

```bash
docker compose up --build
```
