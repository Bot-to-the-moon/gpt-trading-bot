from exchange import exchange

print("\n🔍 Funding-Diagnose RAW (Bybit UNIFIED)")

try:
    balance = exchange.fetch_balance()
    print("✅ Balance geladen.")

    accounts = balance.get("info", {}).get("result", {}).get("list", [])
    for account in accounts:
        if account.get("accountType") == "UNIFIED":
            print(f"\n📘 Account-Typ: {account['accountType']}")
            for coin in account.get("coin", []):
                print(f"  → Coin: {coin.get('coin')}")
                for k, v in coin.items():
                    print(f"     {k:20}: {v}")

except Exception as e:
    print(f"[FEHLER] Dump fehlgeschlagen: {e}")
