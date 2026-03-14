from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Ticker:
    symbol: str
    exchange: str


def build_universe(size: int = 1200) -> list[Ticker]:
    exchanges = ["NASDAQ", "NYSE", "SP500"]
    tickers: list[Ticker] = []
    for idx in range(size):
        exchange = exchanges[idx % len(exchanges)]
        symbol = f"{exchange[:2]}{idx:04d}"
        tickers.append(Ticker(symbol=symbol, exchange=exchange))
    return tickers
