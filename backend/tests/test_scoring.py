from backend.indicators.calculator import IndicatorSnapshot
from backend.scanner.scoring import calculate_score


def test_calculate_score_caps_at_ten() -> None:
    indicators = IndicatorSnapshot(
        rsi=72,
        sma20=110,
        sma50=100,
        sma200=90,
        rel_volume=4,
        atr=2,
        macd=1.5,
    )

    score, signals = calculate_score(last_price=120, max_52w=122, resistance=100, indicators=indicators)

    assert score == 10.0
    assert "breakout_resistance" in signals
