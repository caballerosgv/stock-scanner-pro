from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class ScanResultDTO(BaseModel):
    symbol: str
    exchange: str
    last_price: float
    score: float
    rsi: float
    sma20: float
    sma50: float
    sma200: float
    rel_volume: float
    atr: float
    macd: float
    signal: str
    timestamp: datetime


class ScanResponse(BaseModel):
    total: int
    results: list[ScanResultDTO]
