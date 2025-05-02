# strategy_matrix_manager.py

import json
import os

FILE = "strategy_matrix.json"

def load_matrix():
    if not os.path.exists(FILE):
        return {}
    with open(FILE, "r") as f:
        return json.load(f)

def save_matrix(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=2)

def update_strategy_score(symbol, strategy, success, trend="neutral", signal_score=3):
    data = load_matrix()

    if symbol not in data:
        data[symbol] = {}

    if strategy not in data[symbol]:
        data[symbol][strategy] = {
            "score": 0,
            "trend": {},
            "total": 0,
            "success": 0
        }

    entry = data[symbol][strategy]

    # Gewichteter Score (z. B. Score 5 zählt mehr als 3)
    delta = 1 if success else -1
    weighted = delta * (1 + (signal_score - 3) * 0.5)
    entry["score"] += round(weighted, 2)
    entry["total"] += 1
    if success:
        entry["success"] += 1

    # Trend speichern
    if trend not in entry["trend"]:
        entry["trend"][trend] = 0
    entry["trend"][trend] += 1

    save_matrix(data)

def get_best_strategy(symbol):
    data = load_matrix()
    options = data.get(symbol, {})
    if not options:
        return "core"
    return max(options, key=lambda k: options[k].get("score", 0))

def print_matrix_summary():
    data = load_matrix()
    print("🔍 Strategie-Matrix Übersicht:")
    for coin, strategies in data.items():
        best = max(strategies, key=lambda k: strategies[k].get("score", 0))
        print(f"{coin}: Beste Strategie = {best} | Details: {strategies[best]}")
