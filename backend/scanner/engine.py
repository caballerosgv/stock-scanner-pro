from __future__ import annotations

import asyncio
import logging
from collections.abc import Sequence

from backend.indicators.calculator import compute_indicators
from backend.scanner.market_data import MarketDataProvider
from backend.scanner.scoring import calculate_score
from backend.scanner.types import ScanOutcome
from backend.scanner.universe import Ticker

logger = logging.getLogger(__name__)


class ScanEngine:
    def __init__(self, max_concurrency: int = 50) -> None:
        self._provider = MarketDataProvider()
        self._sem = asyncio.Semaphore(max_concurrency)

    async def scan_universe(self, tickers: Sequence[Ticker]) -> list[ScanOutcome]:
        tasks = [self._scan_ticker(ticker) for ticker in tickers]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        outcomes: list[ScanOutcome] = []
        for result in results:
            if isinstance(result, Exception):
                logger.exception("scan_failed", exc_info=result)
                continue
            outcomes.append(result)

        outcomes.sort(key=lambda item: item.score, reverse=True)
        return outcomes

    async def _scan_ticker(self, ticker: Ticker) -> ScanOutcome:
        async with self._sem:
            df = await self._provider.fetch_ohlcv(ticker)
            indicators = compute_indicators(df)
            last_price = float(df["close"].iloc[-1])
            resistance = float(df["high"].tail(40).max())
            max_52w = float(df["high"].max())
            score, signals = calculate_score(last_price, max_52w, resistance, indicators)

            return ScanOutcome(
                symbol=ticker.symbol,
                exchange=ticker.exchange,
                last_price=round(last_price, 2),
                score=score,
                rsi=round(indicators.rsi, 2),
                sma20=round(indicators.sma20, 2),
                sma50=round(indicators.sma50, 2),
                sma200=round(indicators.sma200, 2),
                rel_volume=round(indicators.rel_volume, 2),
                atr=round(indicators.atr, 2),
                macd=round(indicators.macd, 2),
                signals=signals,
            )
