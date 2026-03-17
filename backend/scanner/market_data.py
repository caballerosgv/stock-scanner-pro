from __future__ import annotations

import asyncio
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from backend.scanner.universe import Ticker
from backend.settings import settings


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


class XtbSqliteMarketDataProvider:
    """Lee velas OHLCV desde una base SQLite exportada desde XTB."""

    def __init__(self, database_path: str, table_name: str = "xtb_ohlcv") -> None:
        self._database_path = Path(database_path).expanduser()
        self._table_name = table_name
        self._engine = create_async_engine(f"sqlite+aiosqlite:///{self._database_path}")

    @property
    def is_available(self) -> bool:
        return bool(self._database_path) and self._database_path.exists()

    async def fetch_ohlcv(self, ticker: Ticker, points: int = 260) -> pd.DataFrame:
        stmt = text(
            f"""
            SELECT open, high, low, close, volume
            FROM {self._table_name}
            WHERE symbol = :symbol
            ORDER BY timestamp DESC
            LIMIT :limit
            """
        )

        async with self._engine.connect() as conn:
            rows = (await conn.execute(stmt, {"symbol": ticker.symbol, "limit": points})).mappings().all()

        if not rows:
            raise LookupError(f"No hay datos de XTB para {ticker.symbol}")

        frame = pd.DataFrame(rows)
        frame = frame.iloc[::-1].reset_index(drop=True)
        return frame[["open", "high", "low", "close", "volume"]].astype(float)


class MarketDataProvider:
    """Proveedor compuesto: usa XTB si está configurado y hace fallback a datos sintéticos."""

    def __init__(self) -> None:
        self._synthetic = SyntheticMarketDataProvider()
        self._xtb = (
            XtbSqliteMarketDataProvider(settings.xtb_database_path, settings.xtb_table_name)
            if settings.xtb_database_path
            else None
        )

    async def fetch_ohlcv(self, ticker: Ticker, points: int = 260) -> pd.DataFrame:
        if self._xtb and self._xtb.is_available:
            try:
                return await self._xtb.fetch_ohlcv(ticker=ticker, points=points)
            except Exception:
                return await self._synthetic.fetch_ohlcv(ticker=ticker, points=points)
        return await self._synthetic.fetch_ohlcv(ticker=ticker, points=points)
