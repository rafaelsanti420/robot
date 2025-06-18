# Robot Platform

This repository implements a small example of the trading robot described in the technical specification. Each component is a FastAPI microservice and all services can be started with Docker Compose.

## Services
- **api-gateway** – exposes the UI and provides a central entry point to other services
- **indicator-engine** – calculates trading indicators (e.g. moving average and RSI)
- **strategy-engine** – stores simple strategies composed of weighted indicators
- **trade-executor** – mock order execution with an on/off toggle
- **market-data** – provides mocked market data using a Bybit connector
- **backtester** – runs a very basic backtest using market data

### Indicator Engine Endpoints

- `POST /ma` – calculate a simple moving average.
- `POST /rsi` – calculate the relative strength index.
- `POST /ema` – calculate the exponential moving average.

### Strategy Engine Endpoints

- `POST /strategy` – create a new strategy.
- `GET /strategy/{name}` – fetch a strategy by name.
- `GET /strategies` – list all stored strategies.

## Running with Docker Compose

```bash
docker compose up --build
```

After startup open [http://localhost:8000/ui](http://localhost:8000/ui) to access the web UI.
