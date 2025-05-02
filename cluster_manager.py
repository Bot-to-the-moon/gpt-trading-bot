import time
from indicators import calculate_indicators
from market_analyzer import multi_timeframe_confirmation
from signal_scoring import score_signal
from momentum_detector import detect_momentum_break
from grid_engine import is_sideways
from scalping_engine import detect_scalping_opportunity

def run_cluster_diagnose(symbols):
    print("\n🔍 Phase 21: Cluster-Test wird gestartet...")

    for symbol in symbols:
        print("\n📊 STRATEGIE-CLUSTER-TEST für", symbol)

        indicators = calculate_indicators(symbol)
        if not indicators:
            print("⚠️ Keine Indikatoren.")
            continue

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

        decision = "ENTRY" if score >= 3 else "SKIP"
        print(f"\n🚦 Entscheidung: {decision}")

        time.sleep(0.5)
