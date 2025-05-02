# position_manager.py

from exchange import exchange, fetch_ohlcv
from spot_manager import safe_spot_exit
import time

def close_stale_positions(max_hours_open=12):
    """Schließt alte Futures-Positionen."""
    try:
        positions = exchange.fetch_positions()
        now = int(time.time() * 1000)

        for pos in positions:
            if pos['contracts'] > 0:
                open_time = pos.get('timestamp')
                if open_time:
                    duration = (now - open_time) / (1000 * 60 * 60)
                    if duration > max_hours_open:
                        symbol = pos['symbol']
                        side = 'sell' if pos['side'].lower() == 'long' else 'buy'
                        amount = pos['contracts']
                        print(f"[AUTO-CLOSE] {symbol} seit {duration:.2f}h offen → wird geschlossen.")
                        exchange.create_order(symbol, 'market', side, amount, params={'reduceOnly': True})
    except Exception as e:
        print(f"[FEHLER] Fehler bei Schließen alter Positionen: {e}")

def auto_exit_stagnant_positions(movement_threshold=0.3, max_minutes=30):
    """Schließt Positionen ohne nennenswerte Bewegung."""
    try:
        positions = exchange.fetch_positions()
        for pos in positions:
            if pos['contracts'] > 0:
                symbol = pos['symbol']
                ohlcv = fetch_ohlcv(symbol, timeframe='1m', limit=max_minutes)
                if not ohlcv:
                    continue
                closes = [c[4] for c in ohlcv]
                high, low = max(closes), min(closes)
                move_percent = ((high - low) / high) * 100 if high > 0 else 0

                if move_percent < movement_threshold:
                    side = 'sell' if pos['side'].lower() == 'long' else 'buy'
                    amount = pos['contracts']
                    print(f"[AUTO-EXIT] {symbol}: Bewegung {move_percent:.2f}% → Verkauf.")
                    exchange.create_order(symbol, 'market', side, amount, params={'reduceOnly': True})
    except Exception as e:
        print(f"[FEHLER] Bewegungserkennung fehlgeschlagen: {e}")

def manage_spot_wallet(min_value_usdt=5, stagnant_threshold=0.7, large_stagnant_threshold=15):
    """Verkauft kleine oder lahme Spot-Bestände, die nicht sinnvoll gehalten werden."""
    try:
        balances = exchange.fetch_balance()
        for asset, amount in balances['total'].items():
            if asset in ['USDT', 'USDC'] or amount == 0:
                continue

            symbol = f"{asset}/USDT"
            try:
                ticker = exchange.fetch_ticker(symbol)
                price = ticker['last']
                value_usdt = amount * price

                # 💰 Verkauf bei Miniwert
                if value_usdt < min_value_usdt:
                    print(f"[SPOT-EXIT] {asset} unter {min_value_usdt} USDT → Verkauf!")
                    safe_spot_exit(symbol, amount)
                    continue

                # 🧊 Verkauf bei Stagnation + hoher Coinwert
                ohlcv = fetch_ohlcv(symbol, timeframe='30m', limit=48)
                if ohlcv:
                    closes = [c[4] for c in ohlcv]
                    movement = ((max(closes) - min(closes)) / max(closes)) * 100 if max(closes) > 0 else 0
                    if movement < stagnant_threshold and value_usdt > large_stagnant_threshold:
                        print(f"[SPOT-EXIT] {asset}: kaum Bewegung ({movement:.2f}%) + Wert {value_usdt:.2f} → Verkauf!")
                        safe_spot_exit(symbol, amount)

            except Exception as e:
                print(f"[WARNUNG] Fehler bei {asset}: {e}")
    except Exception as e:
        print(f"[FEHLER] Walletprüfung fehlgeschlagen: {e}")
