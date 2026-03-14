from __future__ import annotations

from collections.abc import Sequence
from datetime import datetime

from sqlalchemy import Select, desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database.models import ScanResult
from backend.scanner.types import ScanOutcome


class ScanRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def store_scan(self, outcomes: Sequence[ScanOutcome]) -> None:
        now = datetime.utcnow()
        rows = [
            ScanResult(
                symbol=o.symbol,
                exchange=o.exchange,
                last_price=o.last_price,
                score=o.score,
                rsi=o.rsi,
                sma20=o.sma20,
                sma50=o.sma50,
                sma200=o.sma200,
                rel_volume=o.rel_volume,
                atr=o.atr,
                macd=o.macd,
                signal=",".join(o.signals),
                timestamp=now,
            )
            for o in outcomes
        ]
        self._session.add_all(rows)
        await self._session.commit()

    async def latest_results(self, limit: int = 200) -> list[ScanResult]:
        stmt: Select[tuple[ScanResult]] = (
            select(ScanResult).order_by(desc(ScanResult.timestamp), desc(ScanResult.score)).limit(limit)
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())
