# order_manager.py

from exchange import exchange, fetch_ohlcv
import numpy as np

def decide_trade_amount(balance_usdt, open_positions_count):
    """Bestimmt die Trade-Größe."""
    reserve = balance_usdt * 0.2
    available = balance_usdt - reserve
    if available <= 0:
        return 0
    return max(available / (open_positions_count + 1), 5)

def place_order(symbol, amount, leverage=5):
    """Platziert eine Long-Order."""
    if amount < 5:
        print(f"[ABGELEHNT] Betrag zu klein ({amount:.2f} USDT) für {symbol}.")
        return False

    try:
        print(f"[ORDER] Versuche LONG: {symbol} für {amount:.2f} USDT mit Hebel {leverage}x.")
        market = exchange.market(symbol)
        if market.get('contractType') == 'PERPETUAL':
            exchange.set_leverage(leverage, symbol)

        params = {'reduceOnly': False}
        exchange.create_order(symbol=symbol, type='market', side='buy', amount=amount, params=params)
        print(f"[ERFOLG] Long-Order platziert für {symbol}.")
        return True
    except Exception as e:
        print(f"[FEHLER] Long-Order fehlgeschlagen: {e}")
        return False

def place_order_short(symbol, amount, leverage=5):
    """Platziert eine Short-Order."""
    if amount < 5:
        print(f"[ABGELEHNT] Betrag zu klein ({amount:.2f} USDT) für {symbol}.")
        return False

    try:
        print(f"[ORDER] Versuche SHORT: {symbol} für {amount:.2f} USDT mit Hebel {leverage}x.")
        market = exchange.market(symbol)
        if market.get('contractType') == 'PERPETUAL':
            exchange.set_leverage(leverage, symbol)

        params = {'reduceOnly': False}
        exchange.create_order(symbol=symbol, type='market', side='sell', amount=amount, params=params)
        print(f"[ERFOLG] Short-Order platziert für {symbol}.")
        return True
    except Exception as e:
        print(f"[FEHLER] Short-Order fehlgeschlagen: {e}")
        return False

def apply_trailing_stop(symbol, entry_price, trailing_percent=2.5):
    """Setzt einen Trailing Stop, um Gewinne zu sichern."""
    try:
        ticker = exchange.fetch_ticker(symbol)
        current_price = ticker['last']
        if current_price > entry_price * (1 + trailing_percent / 100):
            stop_price = current_price * (1 - trailing_percent / 100)
            params = {'stopPrice': stop_price}
            exchange.create_order(symbol=symbol, type='stop_market', side='sell', amount=1, params=params)
            print(f"[TRAILING STOP] gesetzt bei {stop_price:.2f} für {symbol}")
    except Exception as e:
        print(f"[FEHLER] Trailing Stop konnte nicht gesetzt werden: {e}")
