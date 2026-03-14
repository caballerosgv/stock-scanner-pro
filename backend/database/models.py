from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class ScanResult(Base):
    __tablename__ = "scan_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    symbol: Mapped[str] = mapped_column(String(12), index=True)
    exchange: Mapped[str] = mapped_column(String(16), index=True)
    last_price: Mapped[float] = mapped_column(Float)
    score: Mapped[float] = mapped_column(Float, index=True)
    rsi: Mapped[float] = mapped_column(Float)
    sma20: Mapped[float] = mapped_column(Float)
    sma50: Mapped[float] = mapped_column(Float)
    sma200: Mapped[float] = mapped_column(Float)
    rel_volume: Mapped[float] = mapped_column(Float)
    atr: Mapped[float] = mapped_column(Float)
    macd: Mapped[float] = mapped_column(Float)
    signal: Mapped[str] = mapped_column(String(64), default="none")
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
