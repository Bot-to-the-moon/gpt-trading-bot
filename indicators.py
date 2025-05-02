# indicators.py

import numpy as np
import pandas as pd
from exchange import fetch_ohlcv

def calculate_rsi(prices, period=14):
    delta = np.diff(prices)
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)

    avg_gain = pd.Series(gain).rolling(window=period).mean()
    avg_loss = pd.Series(loss).rolling(window=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.iloc[-1]

def calculate_ema(prices, span):
    return pd.Series(prices).ewm(span=span, adjust=False).mean().iloc[-1]

def calculate_macd(prices, short_span=12, long_span=26, signal_span=9):
    ema_short = pd.Series(prices).ewm(span=short_span, adjust=False).mean()
    ema_long = pd.Series(prices).ewm(span=long_span, adjust=False).mean()
    macd_line = ema_short - ema_long
    signal_line = macd_line.ewm(span=signal_span, adjust=False).mean()
    macd_value = macd_line.iloc[-1] - signal_line.iloc[-1]
    return macd_value

def calculate_bollinger_bands(prices, window=20, num_std=2):
    rolling_mean = pd.Series(prices).rolling(window).mean().iloc[-1]
    rolling_std = pd.Series(prices).rolling(window).std().iloc[-1]
    upper_band = rolling_mean + (rolling_std * num_std)
    lower_band = rolling_mean - (rolling_std * num_std)
    return upper_band, lower_band

def is_trend(prices, short_window=20, long_window=50):
    short_ema = pd.Series(prices).ewm(span=short_window, adjust=False).mean().iloc[-1]
    long_ema = pd.Series(prices).ewm(span=long_window, adjust=False).mean().iloc[-1]
    return short_ema > long_ema

def calculate_indicators(symbol):
    ohlcv = fetch_ohlcv(symbol)
    if not ohlcv:
        return None

    closes = np.array([candle[4] for candle in ohlcv])

    indicators = {
        "rsi": calculate_rsi(closes),
        "ema_short": calculate_ema(closes, span=12),
        "ema_long": calculate_ema(closes, span=26),
        "macd": calculate_macd(closes),
        "upper_band": calculate_bollinger_bands(closes)[0],
        "lower_band": calculate_bollinger_bands(closes)[1],
        "volume": sum(candle[5] for candle in ohlcv[-20:])  # Volumen der letzten 20 Kerzen
    }
    return indicators
