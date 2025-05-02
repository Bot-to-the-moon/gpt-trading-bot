# trade_cooldown.py

import time

COOLDOWN_MINUTES = 2  # Testlauf: nur 2 Minuten Cooldown
trade_memory = {}

def is_coin_on_cooldown(symbol):
    now = time.time()
    last_trade = trade_memory.get(symbol, 0)
    remaining = COOLDOWN_MINUTES * 60 - (now - last_trade)
    if remaining > 0:
        print(f"[COOLDOWN] {symbol}: {remaining:.1f}s verbleibend.")
        return True
    return False

def mark_coin_traded(symbol):
    trade_memory[symbol] = time.time()
    print(f"[COOLDOWN] {symbol} → Cooldown gestartet.")
