import asyncio

from backend.scanner.engine import ScanEngine
from backend.scanner.universe import build_universe


def test_scan_engine_returns_outcomes() -> None:
    engine = ScanEngine(max_concurrency=10)
    tickers = build_universe(30)

    outcomes = asyncio.run(engine.scan_universe(tickers))

    assert len(outcomes) == 30
    assert outcomes[0].score >= outcomes[-1].score
