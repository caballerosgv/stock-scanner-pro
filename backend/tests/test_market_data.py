from __future__ import annotations

import sqlite3

import asyncio

from backend.scanner.market_data import XtbSqliteMarketDataProvider
from backend.scanner.universe import Ticker


def test_xtb_sqlite_provider_reads_ohlcv(tmp_path) -> None:
    db_path = tmp_path / "xtb.db"
    conn = sqlite3.connect(db_path)
    conn.execute(
        """
        CREATE TABLE xtb_ohlcv (
            symbol TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            open REAL NOT NULL,
            high REAL NOT NULL,
            low REAL NOT NULL,
            close REAL NOT NULL,
            volume REAL NOT NULL
        )
        """
    )
    conn.executemany(
        "INSERT INTO xtb_ohlcv(symbol, timestamp, open, high, low, close, volume) VALUES (?, ?, ?, ?, ?, ?, ?)",
        [
            ("AAPL", "2024-01-01 09:00:00", 100, 101, 99, 100.5, 1000),
            ("AAPL", "2024-01-01 10:00:00", 101, 102, 100, 101.5, 1200),
            ("AAPL", "2024-01-01 11:00:00", 102, 103, 101, 102.5, 1400),
        ],
    )
    conn.commit()
    conn.close()

    provider = XtbSqliteMarketDataProvider(str(db_path))
    df = asyncio.run(provider.fetch_ohlcv(Ticker(symbol="AAPL", exchange="NASDAQ"), points=2))

    assert len(df) == 2
    assert list(df["close"]) == [101.5, 102.5]
