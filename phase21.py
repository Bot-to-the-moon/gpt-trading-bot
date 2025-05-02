# 📁 Datei: phase21_debugger.py
# ✅ Phase 21: Strategie-Cluster, Trade-Bewertung & Signal-Konsistenz

import time
from market_analyzer import analyze_best_coins, multi_timeframe_confirmation
from indicators import calculate_indicators
from signal_scoring import score_signal
from momentum_detector import detect_momentum_break
from grid_engine import is_sideways
from scalping_engine import detect_scalping_opportunity

def run_phase_21_debug(symbol):
    print(f"\n📊 STRATEGIE-CLUSTER-TEST für {symbol}")

    indicators = calculate_indicators(symbol)
    if not indicators:
        print("⚠️ Keine Indikatoren.")
        return

    trend = multi_timeframe_confirmation(symbol)
    score = score_signal(indicators, trend=trend)
    momentum = detect_momentum_break(symbol)
    sideways = is_sideways(symbol)
    scalp = detect_scalping_opportunity(symbol)

    print(f"Trend     : {trend}")
    print(f"Score     : {score}/5")
    print(f"Momentum  : {momentum}")
    print(f"Seitwärts : {sideways}")
    print(f"Scalping  : {scalp}")

    decision = "SKIP"
    if score >= 3:
        decision = "ENTRY"

    print(f"\n🚦 Entscheidung: {decision}")

if __name__ == "__main__":
    print("🔍 Phase 21: Cluster-Test wird gestartet...")
    top = analyze_best_coins(limit=5)
    if not top:
        print("⚠️ Keine geeigneten Coins.")
        exit()

    for coin in top:
        run_phase_21_debug(coin)
        time.sleep(1)
