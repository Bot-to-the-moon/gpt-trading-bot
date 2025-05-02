# allocation_manager.py

import config

def calculate_trade_allocation_dynamic(balance, signal_score):
    """Dynamische Einsatzberechnung basierend auf Signalstärke (0–5)."""
    try:
        usage_factor = min(0.1 + 0.1 * signal_score, config.MAX_EQUITY_USAGE)
        amount = balance * usage_factor
        return round(amount, 2)
    except Exception as e:
        print(f"[FEHLER] Allocation: {e}")
        return 10

def determine_dynamic_leverage(indicators):
    """Bestimmt Hebel anhand RSI und EMA-Trend"""
    try:
        rsi = indicators.get('rsi', 50)
        ema_short = indicators.get('ema_short', 0)
        ema_long = indicators.get('ema_long', 1)

        if rsi < 25 or rsi > 75:
            return 10
        elif (rsi < 30 or rsi > 70) and abs(ema_short - ema_long) / ema_long > 0.01:
            return 5
        else:
            return 3
    except Exception as e:
        print(f"[FEHLER] Leverage: {e}")
        return 3

def calculate_adaptive_position_size(balance, base_amount, signal_score, coin_score):
    """Dynamisches Positionssizing anhand von Score + Historie"""
    try:
        multiplier = 1.0
        if signal_score >= 4:
            multiplier += 0.25
        elif signal_score <= 2:
            multiplier -= 0.25
        if coin_score >= 3:
            multiplier += 0.25
        elif coin_score <= -2:
            multiplier -= 0.25

        multiplier = max(0.5, min(multiplier, 1.5))
        final_amount = base_amount * multiplier
        print(f"[ADAPTIV] Einsatz: {final_amount:.2f} USDT (x{multiplier:.2f})")
        return round(final_amount, 2)
    except Exception as e:
        print(f"[FEHLER] PositionSize: {e}")
        return base_amount
