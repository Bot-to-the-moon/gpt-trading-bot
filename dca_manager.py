# dca_manager.py

from exchange import exchange

MAX_DCA_ENTRIES = 1
dca_tracker = {}  # {symbol: [5, 10]} → ausgelöste Level

def check_dca_opportunity(symbol, entry_price, levels=[5, 10, 15]):
    try:
        ticker = exchange.fetch_ticker(symbol)
        current_price = ticker['last']

        drawdown = ((entry_price - current_price) / entry_price) * 100

        position = next((pos for pos in exchange.fetch_positions() if pos['symbol'] == symbol), None)
        if not position or position['contracts'] <= 0:
            return

        # DCA-Tracking initialisieren
        if symbol not in dca_tracker:
            dca_tracker[symbol] = []

        if len(dca_tracker[symbol]) >= MAX_DCA_ENTRIES:
            print(f"[DCA] {symbol}: Max. DCA-Level erreicht.")
            return

        for level in levels:
            if drawdown >= level and level not in dca_tracker[symbol]:
                quantity = position['contracts'] / 3
                print(f"[DCA] {symbol}: Drawdown {drawdown:.2f}% → Nachkauf {quantity:.4f} bei Level {level}%!")
                exchange.create_order(symbol, 'market', 'buy', quantity, params={'reduceOnly': False})
                dca_tracker[symbol].append(level)
                break

    except Exception as e:
        print(f"[FEHLER] DCA Fehler {symbol}: {e}")
