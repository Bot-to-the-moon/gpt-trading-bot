# execution_manager.py

from exchange import exchange
from config import DRY_MODE

def open_long(symbol, amount, leverage=3):
    """Eröffne Long-Position auf Futures-Markt oder simuliere sie im Dry-Run."""
    if DRY_MODE:
        print(f"[DRY-RUN] LONG {symbol} {amount:.2f} USDT @ {leverage}x")
        return True
    try:
        market = exchange.market(symbol)
        if market.get('contractType') != 'PERPETUAL':
            print(f"[SKIP] {symbol} ist kein Futures-Markt.")
            return False
        exchange.set_leverage(leverage, symbol)
        price = exchange.fetch_ticker(symbol)['last']
        quantity = round(amount / price, 3)
        params = {'reduceOnly': False}
        exchange.create_order(symbol, 'market', 'buy', quantity, params=params)
        print(f"[ORDER] LONG {symbol} {amount:.2f} USDT @ {leverage}x")
        return True
    except Exception as e:
        print(f"[FEHLER] open_long(): {e}")
        return False

def open_short(symbol, amount, leverage=3):
    """Eröffne Short-Position oder simuliere sie im Dry-Run."""
    if DRY_MODE:
        print(f"[DRY-RUN] SHORT {symbol} {amount:.2f} USDT @ {leverage}x")
        return True
    try:
        market = exchange.market(symbol)
        if market.get('contractType') != 'PERPETUAL':
            print(f"[SKIP] {symbol} ist kein Futures-Markt.")
            return False
        exchange.set_leverage(leverage, symbol)
        price = exchange.fetch_ticker(symbol)['last']
        quantity = round(amount / price, 3)
        params = {'reduceOnly': False}
        exchange.create_order(symbol, 'market', 'sell', quantity, params=params)
        print(f"[ORDER] SHORT {symbol} {amount:.2f} USDT @ {leverage}x")
        return True
    except Exception as e:
        print(f"[FEHLER] open_short(): {e}")
        return False

def close_position(symbol, side, contracts):
    """Schließt eine Position vollständig."""
    try:
        opposite = 'sell' if side == 'long' else 'buy'
        exchange.create_order(symbol, 'market', opposite, contracts, params={'reduceOnly': True})
        print(f"[CLOSE] {symbol} → {contracts} geschlossen")
    except Exception as e:
        print(f"[FEHLER] close_position(): {e}")

def apply_trailing_stop(symbol, distance_percent=0.5):
    try:
        price = exchange.fetch_ticker(symbol)['last']
        distance = price * (distance_percent / 100)
        print(f"[TRAILING] {symbol}: {distance:.2f} Abstand gesetzt.")
    except Exception as e:
        print(f"[FEHLER] apply_trailing_stop(): {e}")
