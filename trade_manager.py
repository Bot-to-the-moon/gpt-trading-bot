# trade_manager.py

from exchange import exchange, get_balance

initial_balance_usdt = None
reserve_balance = 0.0

def place_order(symbol, amount, leverage=5):
    """Platziert eine Long-Order, nur auf Futures-Märkten."""
    try:
        market = exchange.market(symbol)
        if market.get('contractType') == 'PERPETUAL':
            exchange.set_leverage(leverage, symbol)
            price = exchange.fetch_ticker(symbol)['last']
            quantity = round(amount / price, 3)
            params = {'reduceOnly': False}
            exchange.create_order(symbol=symbol, type='market', side='buy', amount=quantity, params=params)
            print(f"[ORDER] LONG {symbol} {amount:.2f} USDT ({leverage}x Hebel)")
            return True
        else:
            print(f"[SKIP] {symbol} ist kein Futures-Markt.")
            return False
    except Exception as e:
        print(f"[FEHLER] Long-Order fehlgeschlagen: {e}")
        return False

def place_order_short(symbol, amount, leverage=5):
    """Platziert eine Short-Order, nur auf Futures-Märkten."""
    try:
        market = exchange.market(symbol)
        if market.get('contractType') == 'PERPETUAL':
            exchange.set_leverage(leverage, symbol)
            price = exchange.fetch_ticker(symbol)['last']
            quantity = round(amount / price, 3)
            params = {'reduceOnly': False}
            exchange.create_order(symbol=symbol, type='market', side='sell', amount=quantity, params=params)
            print(f"[ORDER] SHORT {symbol} {amount:.2f} USDT ({leverage}x Hebel)")
            return True
        else:
            print(f"[SKIP] {symbol} ist kein Futures-Markt.")
            return False
    except Exception as e:
        print(f"[FEHLER] Short-Order fehlgeschlagen: {e}")
        return False

def apply_trailing_stop(symbol, trailing_percent=0.5):
    """Setzt Trailing Stop, nur bei Futures."""
    try:
        market = exchange.market(symbol)
        if market.get('contractType') == 'PERPETUAL':
            price = exchange.fetch_ticker(symbol)['last']
            distance = price * (trailing_percent / 100)
            print(f"[TRAILING-STOP] {symbol}: {distance:.2f} Abstand gesetzt.")
        else:
            print(f"[SKIP] Trailing-Stop auf Spot {symbol} nicht möglich.")
    except Exception as e:
        print(f"[FEHLER] Trailing-Stop Fehler: {e}")

def calculate_trade_allocation_dynamic(balance, open_positions):
    """Berechnet dynamische Tradegröße."""
    try:
        if open_positions < 3:
            allocation = 0.15
        elif open_positions < 5:
            allocation = 0.10
        else:
            allocation = 0.05
        amount = balance * allocation
        return max(5, min(amount, 30))
    except Exception as e:
        print(f"[FEHLER] Trade Allocation Fehler: {e}")
        return 10

def reserve_profit():
    """20% Gewinn sichern."""
    global reserve_balance
    global initial_balance_usdt

    current_balance = get_balance()
    if isinstance(current_balance, dict):
        current_balance = current_balance.get('USDT', 0)

    if initial_balance_usdt is None:
        initial_balance_usdt = current_balance
        return

    if current_balance > initial_balance_usdt:
        profit = current_balance - initial_balance_usdt
        reserve = profit * 0.2
        reserve_balance += reserve
        initial_balance_usdt += profit - reserve
        print(f"[RESERVE] {reserve:.2f} USDT in Reserve gelegt.")

def emergency_stop_loss():
    """Stoppt Bot bei großem Verlust."""
    global initial_balance_usdt

    current_balance = get_balance()
    if isinstance(current_balance, dict):
        current_balance = current_balance.get('USDT', 0)

    if initial_balance_usdt is None:
        initial_balance_usdt = current_balance
        return

    loss = ((initial_balance_usdt - current_balance) / initial_balance_usdt) * 100
    print(f"[CHECK] Aktueller Verlust: {loss:.2f}%")

    if loss >= 25:
        print("[NOTFALL] Verlustgrenze überschritten. Alle Positionen schließen!")
        try:
            positions = exchange.fetch_positions()
            for pos in positions:
                if pos.get('contracts', 0) > 0:
                    symbol = pos['symbol']
                    side = 'sell' if pos['side'].lower() == 'long' else 'buy'
                    amount = pos['contracts']
                    exchange.create_order(symbol=symbol, type='market', side=side, amount=amount, params={'reduceOnly': True})
                    print(f"[VERKAUFT] {symbol}")
        except Exception as e:
            print(f"[FEHLER] Notverkauf Fehler: {e}")

def determine_dynamic_leverage(indicators):
    """Bestimmt dynamisch den Hebel basierend auf Signalstärke."""
    try:
        rsi = indicators.get('rsi', 50)
        ema_short = indicators.get('ema_short', 0)
        ema_long = indicators.get('ema_long', 0)

        if rsi < 25 or rsi > 75:
            return 10  # Sehr starker Trend → hoher Hebel
        elif (rsi < 30 or rsi > 70) and (abs(ema_short - ema_long) / ema_long > 0.01):
            return 5  # Guter Trend → mittlerer Hebel
        else:
            return 3  # Normales Signal → sicherer kleiner Hebel
    except Exception as e:
        print(f"[FEHLER] Hebelbestimmung fehlgeschlagen: {e}")
        return 3
def check_dynamic_partial_take_profit(symbol, entry_price):
    """Setzt smarte Teilverkäufe + aktiviert Trailing-Stop je nach Gewinn."""
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
            print(f"[TP 20%] {symbol}: +20% → Trailing-Stop übernimmt Rest.")
            apply_trailing_stop(symbol, trailing_percent=2.0)
        elif current_price >= tp10:
            print(f"[TP 10%] {symbol}: +10% → ein Drittel verkaufen.")
            exchange.create_order(symbol, 'market', 'sell', third, params={'reduceOnly': True})
            apply_trailing_stop(symbol, trailing_percent=1.5)
        elif current_price >= tp5:
            print(f"[TP 5%] {symbol}: +5% → Hälfte verkaufen.")
            exchange.create_order(symbol, 'market', 'sell', half, params={'reduceOnly': True})
            apply_trailing_stop(symbol, trailing_percent=1.0)

    except Exception as e:
        print(f"[FEHLER] TP-Stufen Fehler {symbol}: {e}")

def calculate_adaptive_position_size(balance, base_amount, signal_score, coin_score):
    """Ermittelt dynamische Positionsgröße nach Signalqualität & Historie"""
    multiplier = 1.0

    # Signal-Qualität bewerten
    if signal_score >= 4:
        multiplier += 0.25
    elif signal_score <= 2:
        multiplier -= 0.25

    # Coin-Historie bewerten
    if coin_score >= 3:
        multiplier += 0.25
    elif coin_score <= -2:
        multiplier -= 0.25

    # Begrenzen
    multiplier = max(0.5, min(multiplier, 1.5))
    final_amount = base_amount * multiplier
    print(f"[ADAPTIV] Einsatz angepasst: {final_amount:.2f} USDT (Multiplikator: {multiplier:.2f})")
    return round(final_amount, 2)



