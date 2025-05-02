from exchange import get_total_assets, get_balance

print("\n🔎 PnL-TEST: Funding-Analyse")

spot = get_balance()
total = get_total_assets()
funding = round(total - spot, 2)

print(f"\n💰 Kontostand-Analyse:")
print(f"→ Spot-Guthaben   : {spot:.2f} USDT")
print(f"→ Funding-Guthaben: {funding:.2f} USDT")
print(f"→ Gesamt (Total)  : {total:.2f} USDT")

print("\n✅ Test abgeschlossen.")
