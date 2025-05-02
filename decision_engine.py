# decision_engine.py

from indicators import calculate_indicators

# Konfiguration
MIN_VOLUME_THRESHOLD = 1000000  # Mindestvolumen für einen Trade
MACD_THRESHOLD = 0.0005         # Mindestwert für MACD Signal
RSI_OVERSOLD = 35               # RSI Schwelle für Long
RSI_OVERBOUGHT = 65             # RSI Schwelle für Short

def decide_trade(symbol):
    """
    Entscheidet basierend auf Trend, Momentum, Volumen und RSI, ob LONG, SHORT oder NEUTRAL gehandelt wird.
    """
    indicators = calculate_indicators(symbol)
    if not indicators:
        return "Neutral"

    print(f"[INDIKATOREN] {symbol}: {indicators}")

    # Bedingungen prüfen
    ema_trend_up = indicators['ema_short'] > indicators['ema_long']
    ema_trend_down = indicators['ema_short'] < indicators['ema_long']
    macd_positive = indicators['macd'] > MACD_THRESHOLD
    macd_negative = indicators['macd'] < -MACD_THRESHOLD
    high_volume = indicators['volume'] > MIN_VOLUME_THRESHOLD
    rsi_oversold = indicators['rsi'] < RSI_OVERSOLD
    rsi_overbought = indicators['rsi'] > RSI_OVERBOUGHT

    # Entscheidung Long
    if ema_trend_up and macd_positive and high_volume and rsi_oversold:
        return "Long"

    # Entscheidung Short
    if ema_trend_down and macd_negative and high_volume and rsi_overbought:
        return "Short"

    # Wenn keine klare Bedingung erfüllt
    return "Neutral"
