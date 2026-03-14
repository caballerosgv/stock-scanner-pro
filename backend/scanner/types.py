from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class ScanOutcome:
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
    signals: list[str] = field(default_factory=list)
