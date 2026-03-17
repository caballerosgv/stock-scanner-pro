from __future__ import annotations

from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.schemas import (
    ProviderConfigDTO,
    ProviderConfigResponse,
    ProviderConfigUpdate,
    ScanResponse,
    ScanResultDTO,
)
from backend.api.service import ScanService
from backend.database.bootstrap import init_db
from backend.database.repository import ScanRepository
from backend.database.session import get_session
from backend.logging_config import configure_logging

configure_logging()
app = FastAPI(title="Stock Scanner Pro", version="0.1.0")
service = ScanService()
SUPPORTED_PROVIDERS = ["polygon", "iex", "alpaca", "finnhub", "twelvedata", "xtb"]

frontend_dir = Path(__file__).resolve().parents[2] / "frontend"
app.mount("/assets", StaticFiles(directory=str(frontend_dir / "components")), name="assets")


@app.on_event("startup")
async def startup() -> None:
    await init_db()


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/scan", response_model=ScanResponse)
async def trigger_scan(session: AsyncSession = Depends(get_session)) -> ScanResponse:
    outcomes = await service.run_scan(session)
    results = [
        ScanResultDTO(
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
            timestamp=service._cache_updated_at,
        )
        for o in outcomes[:200]
    ]
    return ScanResponse(total=len(outcomes), results=results)


@app.get("/api/results", response_model=ScanResponse)
async def get_results(session: AsyncSession = Depends(get_session)) -> ScanResponse:
    repo = ScanRepository(session)
    rows = await repo.latest_results(limit=200)
    results = [
        ScanResultDTO(
            symbol=row.symbol,
            exchange=row.exchange,
            last_price=row.last_price,
            score=row.score,
            rsi=row.rsi,
            sma20=row.sma20,
            sma50=row.sma50,
            sma200=row.sma200,
            rel_volume=row.rel_volume,
            atr=row.atr,
            macd=row.macd,
            signal=row.signal,
            timestamp=row.timestamp,
        )
        for row in rows
    ]
    return ScanResponse(total=len(results), results=results)


@app.get("/api/provider-configs", response_model=ProviderConfigResponse)
async def get_provider_configs(session: AsyncSession = Depends(get_session)) -> ProviderConfigResponse:
    repo = ScanRepository(session)
    rows = await repo.get_provider_configs()
    row_map = {row.provider: row for row in rows}
    providers = [
        ProviderConfigDTO(
            provider=provider,
            configured=bool(row_map.get(provider) and row_map[provider].api_key),
            updated_at=row_map[provider].updated_at if provider in row_map else None,
        )
        for provider in SUPPORTED_PROVIDERS
    ]
    return ProviderConfigResponse(providers=providers)


@app.put("/api/provider-configs/{provider}", response_model=ProviderConfigDTO)
async def upsert_provider_config(
    provider: str,
    payload: ProviderConfigUpdate,
    session: AsyncSession = Depends(get_session),
) -> ProviderConfigDTO:
    provider = provider.lower()
    if provider not in SUPPORTED_PROVIDERS:
        raise HTTPException(status_code=404, detail="Proveedor no soportado")

    repo = ScanRepository(session)
    row = await repo.upsert_provider_config(provider=provider, api_key=payload.api_key.strip())
    return ProviderConfigDTO(provider=row.provider, configured=bool(row.api_key), updated_at=row.updated_at)


@app.get("/")
async def dashboard() -> FileResponse:
    return FileResponse(frontend_dir / "dashboard" / "index.html")
