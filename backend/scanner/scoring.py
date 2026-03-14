from __future__ import annotations

from backend.indicators.calculator import IndicatorSnapshot


def calculate_score(last_price: float, max_52w: float, resistance: float, indicators: IndicatorSnapshot) -> tuple[float, list[str]]:
    score = 0.0
    signals: list[str] = []

    breakout = last_price > resistance
    if breakout:
        score += 2.0
        signals.append("breakout_resistance")

    if indicators.rel_volume >= 3.0:
        score += 2.0
        signals.append("volume_3x")

    momentum = indicators.rsi >= 60 and indicators.macd > 0
    if momentum:
        score += 2.0
        signals.append("strong_momentum")

    uptrend = last_price > indicators.sma20 > indicators.sma50 > indicators.sma200
    if uptrend:
        score += 2.0
        signals.append("bullish_trend")

    near_52w_high = (last_price / max_52w) >= 0.95
    if near_52w_high:
        score += 2.0
        signals.append("near_52w_high")

    return round(min(score, 10.0), 2), signals
