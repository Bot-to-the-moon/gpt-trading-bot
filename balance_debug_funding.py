from exchange import exchange
import json

print("🔎 Lade RAW-Balance-Info...\n")

balance = exchange.fetch_balance()
info = balance.get("info", {})
result = info.get("result", {})
accounts = result.get("list", [])

if not accounts:
    print("[FEHLER] Kein Eintrag in result['list']")
    exit()

print("📦 Gefundene Konten:")

for acc in accounts:
    acc_type = acc.get("accountType", "?")
    print(f"\n📄 Account: {acc_type}")

    for coin in acc.get("coin", []):
        if coin.get("coin") == "USDT":
            print(json.dumps(coin, indent=2))
