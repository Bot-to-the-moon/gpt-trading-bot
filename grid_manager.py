# grid_manager.py

grid_configs = {}

def setup_grid(symbol, entry_price, levels=5, distance_percent=0.5):
    """
    Erstellt eine Grid-Konfiguration für das Symbol mit Entry-Preis.
    """
    try:
        levels = max(1, levels)
        distance = entry_price * (distance_percent / 100)

        grid = []
        for i in range(1, levels + 1):
            grid.append({
                "buy": round(entry_price - i * distance, 4),
                "sell": round(entry_price + i * distance, 4)
            })

        grid_configs[symbol] = grid
        print(f"[GRID] {symbol}: Grid eingerichtet mit Abstand {distance:.2f} und {levels} Levels.")
        return grid

    except Exception as e:
        print(f"[FEHLER] setup_grid() für {symbol}: {e}")
        return []

def execute_grid(symbol, current_price):
    """
    Führt einfache Logik zur Ausführung von Grid-Leveln aus.
    """
    if symbol not in grid_configs:
        return

    grid = grid_configs[symbol]

    for level in grid:
        if current_price <= level["buy"]:
            print(f"[GRID-BUY] {symbol} @ {current_price} <= {level['buy']}")
        elif current_price >= level["sell"]:
            print(f"[GRID-SELL] {symbol} @ {current_price} >= {level['sell']}")
