from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(slots=True)
class Settings:
    database_url: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./stock_scanner.db")
    scanner_refresh_seconds: int = int(os.getenv("SCANNER_REFRESH_SECONDS", "45"))
    universe_size: int = int(os.getenv("SCANNER_UNIVERSE_SIZE", "1200"))
    xtb_database_path: str = os.getenv("XTB_DATABASE_PATH", "")
    xtb_table_name: str = os.getenv("XTB_TABLE_NAME", "xtb_ohlcv")


settings = Settings()
