# exchange.py

import ccxt
import config

# ✅ Nur BYBIT – Binance wird ignoriert
exchange = ccxt.bybit({
    'apiKey': config.BYBIT_API_KEY,
    'secret': config.BYBIT_SECRET,
    'enableRateLimit': True,
    'options': {
        'defaultType': 'unified'
    }
})

# 🧪 Testverbindung
def test_api_key():
    try:
        exchange.fetch_balance()
        print("[API-Check] Verbindung zur Bybit erfolgreich ✅")
        return True
    except Exception as e:
        print(f"[API-Fehler] Verbindung gescheitert: {e}")
        return False

def get_balance():
    try:
        balance = exchange.fetch_balance()
        return float(balance['USDT']['free'])
    except Exception as e:
        print(f"[FEHLER] get_balance(): {e}")
        return 0.0

def get_total_assets():
    try:
        balance = exchange.fetch_balance()
        spot = float(balance['USDT']['free']) if 'USDT' in balance else 0.0

        # Funding aus coin-Liste extrahieren
        funding = 0.0
        try:
            coin_list = balance['info']['result']['list'][0]['coin']
            for item in coin_list:
                if item.get('coin') == 'USDT':
                    full = float(item.get('walletBalance', 0))
                    funding = max(0.0, full - spot)
        except Exception as e:
            print(f"[INFO] Funding nicht extrahierbar: {e}")

        total = spot + funding
        return round(total, 2)

    except Exception as e:
        print(f"[FEHLER] TotalAssets: {e}")
        return 0.0

def get_trade_snapshot():
    try:
        balance = exchange.fetch_balance()
        return float(balance['USDT']['free'])
    except Exception as e:
        print(f"[FEHLER] TradeBalance: {e}")
        return 0.0

def fetch_ohlcv(symbol, timeframe='5m', limit=100):
    try:
        return exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
    except Exception as e:
        print(f"[FEHLER] OHLCV konnte nicht geladen werden: {e}")
        return []

def place_order(symbol, amount, side="buy", leverage=5):
    try:
        market = exchange.market(symbol)
        price = exchange.fetch_ticker(symbol)['last']
        quantity = round(amount / price, 3)

        exchange.set_leverage(leverage, symbol)
        params = {'reduceOnly': False}
        return exchange.create_order(symbol, 'market', side, quantity, params=params)
    except Exception as e:
        print(f"[FEHLER] Order: {e}")
        return None

def place_order_short(symbol, amount, leverage=5):
    return place_order(symbol, amount, side="sell", leverage=leverage)

def apply_trailing_stop(symbol, distance_percent=0.5):
    try:
        price = exchange.fetch_ticker(symbol)['last']
        distance = price * (distance_percent / 100)
        print(f"[TRAILING] {symbol}: {distance:.2f}")
    except Exception as e:
        print(f"[FEHLER] Trailing: {e}")
