from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass(slots=True)
class IndicatorSnapshot:
    rsi: float
    sma20: float
    sma50: float
    sma200: float
    rel_volume: float
    atr: float
    macd: float


def compute_indicators(df: pd.DataFrame) -> IndicatorSnapshot:
    close = df["close"].astype(float)
    high = df["high"].astype(float)
    low = df["low"].astype(float)
    volume = df["volume"].astype(float)

    sma20 = close.rolling(window=20).mean().iloc[-1]
    sma50 = close.rolling(window=50).mean().iloc[-1]
    sma200 = close.rolling(window=200).mean().iloc[-1]

    delta = close.diff()
    gain = np.where(delta > 0, delta, 0.0)
    loss = np.where(delta < 0, -delta, 0.0)
    avg_gain = pd.Series(gain).rolling(14).mean()
    avg_loss = pd.Series(loss).rolling(14).mean().replace(0, np.nan)
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs.iloc[-1]))

    rel_volume = (volume.iloc[-1] / volume.rolling(window=20).mean().iloc[-1]) if len(volume) >= 20 else 1.0

    tr = pd.concat(
        [
            high - low,
            (high - close.shift()).abs(),
            (low - close.shift()).abs(),
        ],
        axis=1,
    ).max(axis=1)
    atr = tr.rolling(window=14).mean().iloc[-1]

    ema12 = close.ewm(span=12, adjust=False).mean()
    ema26 = close.ewm(span=26, adjust=False).mean()
    macd = (ema12 - ema26).iloc[-1]

    return IndicatorSnapshot(
        rsi=float(np.nan_to_num(rsi, nan=50.0)),
        sma20=float(np.nan_to_num(sma20, nan=close.iloc[-1])),
        sma50=float(np.nan_to_num(sma50, nan=close.iloc[-1])),
        sma200=float(np.nan_to_num(sma200, nan=close.iloc[-1])),
        rel_volume=float(np.nan_to_num(rel_volume, nan=1.0)),
        atr=float(np.nan_to_num(atr, nan=0.0)),
        macd=float(np.nan_to_num(macd, nan=0.0)),
    )
