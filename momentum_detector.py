# momentum_detector.py

from exchange import fetch_ohlcv
import numpy as np

def detect_momentum_break(symbol, tf="1m", lookback=10):
    data = fetch_ohlcv(symbol, timeframe=tf, limit=lookback + 2)
    if not data or len(data) < lookback + 1:
        return "neutral"

    closes = np.array([c[4] for c in data])
    highs = np.array([c[2] for c in data])
    lows  = np.array([c[3] for c in data])

    range_mean = np.mean(highs[:-1] - lows[:-1])
    current_range = highs[-1] - lows[-1]

    breakout = current_range > range_mean * 1.5
    close_jump = abs(closes[-1] - closes[-2]) > range_mean

    if breakout and closes[-1] > closes[-2]:
        return "bull"
    elif breakout and closes[-1] < closes[-2]:
        return "bear"
    else:
        return "neutral"
