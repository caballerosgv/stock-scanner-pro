from __future__ import annotations

import asyncio
from dataclasses import dataclass

import numpy as np
import pandas as pd

from backend.scanner.universe import Ticker


@dataclass(slots=True)
class CachedFrame:
    frame: pd.DataFrame
    generated_at: float


class SyntheticMarketDataProvider:
    """Simula velas OHLCV para pruebas locales y desarrollo offline."""

    def __init__(self) -> None:
        self._cache: dict[str, CachedFrame] = {}
        self._ttl_seconds = 30

    async def fetch_ohlcv(self, ticker: Ticker, points: int = 260) -> pd.DataFrame:
        now = asyncio.get_event_loop().time()
        cached = self._cache.get(ticker.symbol)
        if cached and now - cached.generated_at < self._ttl_seconds:
            return cached.frame

        seed = sum(ord(ch) for ch in ticker.symbol)
        rng = np.random.default_rng(seed)
        drift = rng.uniform(0.02, 0.2)
        volatility = rng.uniform(0.5, 2.4)
        prices = np.maximum(5, 50 + np.cumsum(rng.normal(drift, volatility, points)))
        high = prices + rng.uniform(0.2, 1.2, points)
        low = prices - rng.uniform(0.2, 1.2, points)
        open_ = prices + rng.normal(0, 0.4, points)
        volume = rng.integers(50_000, 4_000_000, points)

        frame = pd.DataFrame(
            {
                "open": open_,
                "high": high,
                "low": low,
                "close": prices,
                "volume": volume,
            }
        )
        self._cache[ticker.symbol] = CachedFrame(frame=frame, generated_at=now)
        return frame
