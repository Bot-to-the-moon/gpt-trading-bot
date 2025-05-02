# spot_manager.py

from exchange import exchange

MIN_FALLBACK_AMOUNT = 5.0  # Fallback-USDT, wenn keine Mindestmenge bekannt

def get_min_order_amount(symbol):
    try:
        market = exchange.market(symbol)
        min_amount = market.get("limits", {}).get("amount", {}).get("min", None)
        if min_amount is not None:
            return float(min_amount)
    except Exception as e:
        print(f"[WARNUNG] Mindestmenge für {symbol} nicht abrufbar: {e}")
    return MIN_FALLBACK_AMOUNT

def safe_spot_exit(symbol, quantity):
    try:
        min_qty = get_min_order_amount(symbol)
        if quantity < min_qty:
            print(f"[SPOT-EXIT] {symbol}: Menge {quantity} < Mindestmenge {min_qty:.6f} → SKIP")
            return False

        quantity = round(quantity, 6)
        exchange.create_order(symbol=symbol, type='market', side='sell', amount=quantity)
        print(f"[SPOT-EXIT] {symbol}: {quantity} verkauft")
        return True

    except Exception as e:
        print(f"[FEHLER] Spot-Verkauf {symbol}: {e}")
        return False
