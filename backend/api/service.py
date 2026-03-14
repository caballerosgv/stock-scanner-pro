from __future__ import annotations

import asyncio
import logging
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from backend.alerts.channels import AlertDispatcher
from backend.database.repository import ScanRepository
from backend.scanner.engine import ScanEngine
from backend.scanner.types import ScanOutcome
from backend.scanner.universe import build_universe
from backend.settings import settings

logger = logging.getLogger(__name__)


class ScanService:
    def __init__(self) -> None:
        self._engine = ScanEngine()
        self._dispatcher = AlertDispatcher()
        self._cache: list[ScanOutcome] = []
        self._cache_updated_at: datetime | None = None
        self._lock = asyncio.Lock()

    async def run_scan(self, session: AsyncSession) -> list[ScanOutcome]:
        async with self._lock:
            tickers = build_universe(settings.universe_size)
            outcomes = await self._engine.scan_universe(tickers)
            repo = ScanRepository(session)
            await repo.store_scan(outcomes[:300])
            for outcome in outcomes[:25]:
                await self._dispatcher.dispatch_for(outcome)
            self._cache = outcomes
            self._cache_updated_at = datetime.utcnow()
            logger.info("scan_completed", extra={"symbols": len(outcomes)})
            return outcomes

    async def get_cached_or_scan(self, session: AsyncSession) -> list[ScanOutcome]:
        if self._cache and self._cache_updated_at:
            age = (datetime.utcnow() - self._cache_updated_at).total_seconds()
            if age < settings.scanner_refresh_seconds:
                return self._cache
        return await self.run_scan(session)
