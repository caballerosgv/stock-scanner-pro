from __future__ import annotations

from backend.database.models import Base
from backend.database.session import engine


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
