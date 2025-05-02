# scalping_engine.py

from exchange import fetch_ohlcv
import numpy as np

def detect_scalping_opportunity(symbol):
    """Schnelles RSI/Candle-Breakout-System auf 1m Chart."""
    try:
        ohlcv = fetch_ohlcv(symbol, timeframe='1m', limit=20)
        if not ohlcv or len(ohlcv) < 15:
            return False

        closes = [c[4] for c in ohlcv]
        recent = closes[-1]
        rsi = calculate_rsi(closes)

        if rsi > 72 and recent > max(closes[-5:-1]):
            return "Short"
        elif rsi < 28 and recent < min(closes[-5:-1]):
            return "Long"
        return "Neutral"
    except Exception as e:
        print(f"[SCALPING-FEHLER] {symbol}: {e}")
        return "Neutral"

def calculate_rsi(closes, period=14):
    closes = np.array(closes)
    delta = np.diff(closes)
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)
    avg_gain = np.mean(gain[-period:])
    avg_loss = np.mean(loss[-period:])
    rs = avg_gain / avg_loss if avg_loss else 0
    return 100 - (100 / (1 + rs))
