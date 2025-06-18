# Trading Robot Design

This document describes a simple microservice based trading robot. It is written to be used as a prompt for Codex or as guidance when extending the project.

## Overview
The platform is split into separate services which communicate over HTTP. Every service is a FastAPI application. All services are started with the provided `docker-compose.yml` file.

### Services
1. **api-gateway** – serves the web UI and proxies requests to the internal services.
2. **indicator-engine** – calculates indicators such as moving averages and RSI.
3. **strategy-engine** – stores strategies which are defined as a list of indicators and their weights.
4. **trade-executor** – places orders. The execution can be globally enabled or disabled via the `/toggle` endpoint.
5. **market-data** – connects to Bybit (mocked) and provides candle data.
6. **backtester** – runs simplified backtests using data from `market-data`.

## Features
- Web UI available at `/ui` to view service status, fetch market data and enable/disable trading.
- Toggle external activity (placing orders) via `POST /toggle` on the `trade-executor` service.
- Calculate indicators through `indicator-engine` (moving average and RSI are implemented).
- Create and fetch strategies with `strategy-engine`.
- Retrieve mocked candles from `market-data`.
- Run a minimal backtest using `backtester`.

This repository only contains minimal logic meant for demonstration and testing. The mocked Bybit connector located in `market_data/app/bybit_connector.py` can be replaced with a real implementation if API keys and network access are provided.
