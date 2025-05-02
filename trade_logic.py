# trade_logic.py

from exchange import exchange
from execution_manager import apply_trailing_stop

def check_dynamic_partial_take_profit(symbol, entry_price):
    """Setzt Teilverkäufe und Trailing-Stop bei 5%, 10%, 20% Gewinn."""
    try:
        ticker = exchange.fetch_ticker(symbol)
        current_price = ticker['last']

        tp5 = entry_price * 1.05
        tp10 = entry_price * 1.10
        tp20 = entry_price * 1.20

        position = next((pos for pos in exchange.fetch_positions() if pos['symbol'] == symbol), None)
        if not position or position['contracts'] <= 0:
            return

        contracts = position['contracts']
        half = contracts / 2
        third = contracts / 3

        if current_price >= tp20:
            print(f"[TP 20%] {symbol}: +20% → Trailing-Stop aktiviert.")
            apply_trailing_stop(symbol, distance_percent=2.0)

        elif current_price >= tp10:
            print(f"[TP 10%] {symbol}: +10% → 1/3 verkaufen.")
            exchange.create_order(symbol, 'market', 'sell', third, params={'reduceOnly': True})
            apply_trailing_stop(symbol, distance_percent=1.5)

        elif current_price >= tp5:
            print(f"[TP 5%] {symbol}: +5% → 1/2 verkaufen.")
            exchange.create_order(symbol, 'market', 'sell', half, params={'reduceOnly': True})
            apply_trailing_stop(symbol, distance_percent=1.0)

    except Exception as e:
        print(f"[FEHLER] TP-Logik {symbol}: {e}")
