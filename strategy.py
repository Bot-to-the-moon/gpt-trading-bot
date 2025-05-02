# strategy.py

from exchange import fetch_ohlcv
import numpy as np

def calculate_indicators(symbol):
    """Berechnet RSI, EMA, MACD, Bollinger Bänder und Volumen."""
    ohlcv = fetch_ohlcv(symbol)
    if not ohlcv or len(ohlcv) < 26:
        return {}

    closes = np.array([c[4] for c in ohlcv])
    delta = np.diff(closes)
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)

    avg_gain = np.mean(gain[-14:])
    avg_loss = np.mean(loss[-14:])
    rs = avg_gain / avg_loss if avg_loss else 0
    rsi = 100 - (100 / (1 + rs))

    ema_short = np.mean(closes[-12:])
    ema_long = np.mean(closes[-26:])
    macd = ema_short - ema_long

    sma = np.mean(closes[-20:])
    stddev = np.std(closes[-20:])
    upper_band = sma + (2 * stddev)
    lower_band = sma - (2 * stddev)

    volume = sum(c[5] for c in ohlcv[-20:])

    return {
        'rsi': float(rsi),
        'macd': float(macd),
        'ema_short': float(ema_short),
        'ema_long': float(ema_long),
        'upper_band': float(upper_band),
        'lower_band': float(lower_band),
        'volume': float(volume)
    }

def decide_action(symbol):
    """Entscheidet Long oder Short basierend auf Indikatoren."""
    indicators = calculate_indicators(symbol)
    if not indicators:
        return "Neutral"

    print(f"[INDIKATOREN] {symbol}: {indicators}")

    if indicators['rsi'] < 35 and indicators['ema_short'] > indicators['ema_long']:
        return "Long"
    elif indicators['rsi'] > 65 and indicators['ema_short'] < indicators['ema_long']:
        return "Short"
    else:
        return "Neutral"
