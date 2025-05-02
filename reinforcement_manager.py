# reinforcement_manager.py

import json
import os

FILE = "reinforcement_scores.json"
SCORE_MIN = -5
SCORE_MAX = 10

def load_scores():
    if not os.path.exists(FILE):
        return {}
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"[FEHLER] reinforcement load: {e}")
        return {}

def save_scores(data):
    try:
        with open(FILE, "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"[FEHLER] reinforcement save: {e}")

def update_strategy_score(symbol, strategy, success):
    """Verstärkungs-Score je Coin/Strategie aktualisieren"""
    scores = load_scores()

    if symbol not in scores:
        scores[symbol] = {}
    if strategy not in scores[symbol]:
        scores[symbol][strategy] = 0

    delta = 1 if success else -1
    scores[symbol][strategy] += delta

    # Begrenzen
    scores[symbol][strategy] = max(SCORE_MIN, min(SCORE_MAX, scores[symbol][strategy]))

    save_scores(scores)

def get_strategy_score(symbol, strategy):
    scores = load_scores()
    return scores.get(symbol, {}).get(strategy, 0)
