# system_check.py

from exchange import exchange, fetch_ohlcv, get_total_assets
import time

def run_tests():
    print("🔍 SYSTEM-TEST START")

    # 1. API Test
    try:
        balance = exchange.fetch_balance()
        print(f"[✓] API Verbindung OK – Balance: {balance['USDT']['free']} USDT")
    except Exception as e:
        print(f"[✗] API-Verbindung fehlgeschlagen: {e}")

    # 2. OHLCV Test
    try:
        data = fetch_ohlcv("BTC/USDT", timeframe="5m", limit=10)
        if data:
            print("[✓] OHLCV Datenabruf erfolgreich")
        else:
            print("[✗] OHLCV leer")
    except Exception as e:
        print(f"[✗] OHLCV Fehler: {e}")

    # 3. Kontostand Test
    try:
        assets = get_total_assets()
        print(f"[✓] Total Assets abrufbar: {assets:.2f} USDT")
    except Exception as e:
        print(f"[✗] Total Assets Fehler: {e}")

    print("✅ SYSTEM-TEST BEENDET")

if __name__ == "__main__":
    run_tests()
