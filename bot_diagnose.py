# bot_diagnose.py

import time
import config
from exchange import exchange, get_total_assets
from indicators import calculate_indicators
from market_analyzer import analyze_best_coins, multi_timeframe_confirmation
from signal_scoring import score_signal
from momentum_detector import detect_momentum_break
from grid_engine import is_sideways
from scalping_engine import detect_scalping_opportunity

print("\n🔍 DIAGNOSE-ANALYSE MODUS AKTIVIERT")

print(f"[INFO] Verbundene Börse: {'Bybit' if config.USE_BYBIT else 'Binance'}")
print(f"[INFO] Gesamtvermögen (inkl. Funding): {get_total_assets():.2f} USDT\n")

print("[CHECK] Top Coins werden analysiert...")
top_coins = analyze_best_coins(limit=10)

if not top_coins:
    print("[FEHLER] Keine geeigneten Coins gefunden.")
    exit()

print(f"[INFO] {len(top_coins)} Coins gefunden: {top_coins}\n")

for symbol in top_coins:
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"🔎 Analyse: {symbol}")

    indicators = calculate_indicators(symbol)
    if not indicators:
        print("[SKIP] Keine Indikatordaten verfügbar.")
        continue

    rsi = indicators.get("rsi", "?")
    macd = indicators.get("macd", "?")
    trend = multi_timeframe_confirmation(symbol)
    score = score_signal(indicators, trend=trend, is_moon=False)
    momentum = detect_momentum_break(symbol)
    sideways = is_sideways(symbol)
    scalp = detect_scalping_opportunity(symbol)

    print(f"RSI: {rsi:.2f} | MACD: {macd:.4f}")
    print(f"Trend-Richtung: {trend}")
    print(f"Momentum: {momentum}")
    print(f"Seitwärtsmarkt: {sideways}")
    print(f"Scalping-Signal: {scalp}")
    print(f"Gesamtscore: {score}/5")

    if score >= 3:
        print("✅ TRADE MÖGLICH (Score OK)")
    else:
        print("❌ Kein Einstieg (Score zu niedrig)")

    time.sleep(1)

print("\n🧠 Diagnose abgeschlossen.")
