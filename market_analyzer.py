import numpy as np
import config
from exchange import exchange, fetch_ohlcv

def analyze_best_coins(limit=30):
    """Scannt alle Futures-Coins mit Volumen & Bewegung."""
    try:
        markets = exchange.fetch_markets()
        valid_quotes = ['USDT', 'USDC', 'USD']  # Alle bekannten Varianten

        filtered = []
        with open("filtered_markets_log.txt", "w", encoding="utf-8") as log:
            log.write("Gefilterte Märkte mit Grund:\n\n")

            for m in markets:
                symbol = m['symbol']
                quote = m.get("quote", "")
                reason = None

                if m.get("contract") is not True:
                    reason = "Kein Perpetual"
                elif m.get('linear') is not True:
                    reason = "Nicht linear"
                elif m.get('settle') != 'USDT':
                    reason = f"Nicht USDT-Settled: {m.get('settle')}"
                elif ':' in symbol and not symbol.endswith(":USDT"):
                    reason = "Symbol enthält ':' (kein USDT)"

                if reason:
                    log.write(f"{symbol}: {reason}\n")
                    continue

                try:
                    ticker = exchange.fetch_ticker(symbol)
                    vol = float(ticker.get("quoteVolume", 0) or 0)
                    change = abs(float(ticker.get("percentage", 0) or 0))
                    score = vol * change

                    if vol < 10000:
                        log.write(f"{symbol}: Volumen zu niedrig ({vol})\n")
                        continue
                    if score < 20000:
                        log.write(f"{symbol}: Score zu niedrig ({score})\n")
                        continue

                    log.write(f"{symbol}: ✅ OK (Vol: {vol}, Score: {score})\n")
                    filtered.append((symbol, score))
                except Exception as e:
                    log.write(f"{symbol}: Fehler beim Ticker: {e}\n")

        sorted_coins = sorted(filtered, key=lambda x: x[1], reverse=True)
        return [s[0] for s in sorted_coins[:limit]]

    except Exception as e:
        print(f"[FEHLER] Coin-Analyse: {e}")
        return []

def multi_timeframe_confirmation(symbol):
    """Bestätigt Trend durch 5m + 15m-Analyse."""
    try:
        ohlcv_5m = fetch_ohlcv(symbol, timeframe='5m', limit=50)
        ohlcv_15m = fetch_ohlcv(symbol, timeframe='15m', limit=50)

        if len(ohlcv_5m) < 10 or len(ohlcv_15m) < 10:
            return "neutral"

        closes_5m = [c[4] for c in ohlcv_5m]
        closes_15m = [c[4] for c in ohlcv_15m]

        if closes_5m[-1] > closes_5m[-5] and closes_15m[-1] > closes_15m[-5]:
            return "up"
        elif closes_5m[-1] < closes_5m[-5] and closes_15m[-1] < closes_15m[-5]:
            return "down"
        else:
            return "neutral"
    except Exception as e:
        print(f"[FEHLER] Multi-Timeframe Analyse fehlgeschlagen: {e}")
        return "neutral"

def decide_action(indicators):
    """Entscheidet Long, Short oder Neutral basierend auf RSI und EMAs."""
    try:
        if not indicators:
            return "Neutral"

        rsi = indicators.get('rsi', 50)
        ema_s = indicators.get('ema_short', 0)
        ema_l = indicators.get('ema_long', 0)

        if rsi < 35 and ema_s > ema_l:
            return "Long"
        elif rsi > 65 and ema_s < ema_l:
            return "Short"
        else:
            return "Neutral"
    except Exception:
        return "Neutral"
