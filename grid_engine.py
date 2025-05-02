# grid_engine.py

from exchange import fetch_ohlcv
import numpy as np

active_grids = {}

def setup_grid(symbol, levels=5, spacing_pct=1.0):
    """Erzeuge dynamisches Gitter um aktuellen Preis"""
    ohlcv = fetch_ohlcv(symbol, timeframe="15m", limit=20)
    if not ohlcv:
        return []

    price = ohlcv[-1][4]
    spacing = price * spacing_pct / 100

    grid = []
    for i in range(-levels, levels + 1):
        level_price = round(price + i * spacing, 4)
        grid.append(level_price)

    active_grids[symbol] = {
        "center": price,
        "grid": grid,
        "last_price": price
    }

    print(f"[GRID] {symbol}: {len(grid)} Levels erzeugt um {price:.4f}")
    return active_grids[symbol]

def execute_grid(symbol, current_price):
    """Reagiere auf Preisbewegungen im Grid"""
    grid_data = active_grids.get(symbol)
    if not grid_data:
        return

    grid = grid_data["grid"]
    if current_price > grid_data["last_price"]:
        print(f"[GRID-MOVE] {symbol}: Preis gestiegen – prüfe Verkauf")
    elif current_price < grid_data["last_price"]:
        print(f"[GRID-MOVE] {symbol}: Preis gefallen – prüfe Kauf")

    grid_data["last_price"] = current_price

def is_sideways(symbol, tf="15m", threshold=1.5):
    """Erkenne Seitwärtsmarkt (low Vola, kein richtiger Trend)"""
    data = fetch_ohlcv(symbol, timeframe=tf, limit=20)
    if not data or len(data) < 20:
        return False

    closes = np.array([c[4] for c in data])
    change = abs(closes[-1] - closes[0]) / closes[0] * 100
    std = np.std(closes)

    if change < threshold and std < closes[-1] * 0.01:
        return True
    return False

