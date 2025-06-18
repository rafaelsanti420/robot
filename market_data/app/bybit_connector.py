from typing import List, Dict

class BybitConnector:
    """Mocked connector to the Bybit API."""

    def __init__(self):
        self.connected = True

    async def get_latest_candles(self, symbol: str, interval: str = "1m", limit: int = 10) -> List[Dict]:
        """Return mocked OHLCV candles."""
        return [
            {
                "symbol": symbol,
                "interval": interval,
                "open": 1 + i * 0.1,
                "high": 1.1 + i * 0.1,
                "low": 0.9 + i * 0.1,
                "close": 1 + i * 0.1,
                "volume": 100 + i,
            }
            for i in range(limit)
        ]
