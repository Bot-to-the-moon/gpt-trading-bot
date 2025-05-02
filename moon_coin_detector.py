# moon_coin_detector.py

from exchange import exchange, fetch_ohlcv
import numpy as np

def detect_moon_candidates(limit=5):
    """Scannt nach Volumen- und Preisexplosionen in den letzten 30min."""
    try:
        markets = exchange.fetch_markets()
        symbols = [m['symbol'] for m in markets if m.get('contractType') == 'PERPETUAL' and m['quote'] == 'USDT']

        candidates = []

        for symbol in symbols:
            try:
                ohlcv = fetch_ohlcv(symbol, timeframe='5m', limit=12)
                if not ohlcv or len(ohlcv) < 12:
                    continue

                closes = [c[4] for c in ohlcv]
                volumes = [c[5] for c in ohlcv]

                price_gain = (closes[-1] - closes[0]) / closes[0] * 100
                volume_spike = volumes[-1] / np.mean(volumes[:-2])

                if price_gain > 10 and volume_spike > 3:
                    score = price_gain * volume_spike
                    candidates.append((symbol, score))

            except Exception:
                continue

        sorted_list = sorted(candidates, key=lambda x: x[1], reverse=True)
        return [sym for sym, _ in sorted_list[:limit]]
    except Exception as e:
        print(f"[FEHLER] MoonScan: {e}")
        return []
