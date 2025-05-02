# learning_manager.py

import json
import os

LEARNING_FILE = "coin_learning.json"
SCORE_MIN = -10
SCORE_MAX = 15

def load_learning_data():
    if not os.path.exists(LEARNING_FILE):
        return {}
    try:
        with open(LEARNING_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"[FEHLER] Laden der Lern-Daten: {e}")
        return {}

def save_learning_data(data):
    try:
        with open(LEARNING_FILE, "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"[FEHLER] Speichern Learning-Daten: {e}")

def update_coin_score(symbol, signal, success=True, strategy="main"):
    key = f"{symbol}_{strategy}_{signal}"
    data = load_learning_data()

    if key not in data:
        data[key] = 0

    delta = 1 if success else -1
    data[key] += delta
    data[key] = max(SCORE_MIN, min(SCORE_MAX, data[key]))

    save_learning_data(data)
    print(f"[LEARN] {symbol} ({strategy}/{signal}) → {data[key]}")

def get_coin_score(symbol, signal="neutral", strategy="main"):
    key = f"{symbol}_{strategy}_{signal}"
    data = load_learning_data()
    return data.get(key, 0)

def reward_coin(symbol, signal="Long", strategy="main", factor=1.0):
    key = f"{symbol}_{strategy}_{signal}"
    data = load_learning_data()
    data[key] = min(SCORE_MAX, data.get(key, 0) + int(1 * factor))
    save_learning_data(data)
    print(f"[REWARD] {symbol} +{factor} für {strategy}/{signal} → {data[key]}")

def punish_coin(symbol, signal="Long", strategy="main", factor=1.0):
    key = f"{symbol}_{strategy}_{signal}"
    data = load_learning_data()
    data[key] = max(SCORE_MIN, data.get(key, 0) - int(1 * factor))
    save_learning_data(data)
    print(f"[PUNISH] {symbol} -{factor} für {strategy}/{signal} → {data[key]}")

def decay_learning_scores(amount=1):
    """Reduziert alle Scores leicht, um alte Muster zu vergessen."""
    data = load_learning_data()
    changed = False

    for key in data:
        old = data[key]
        data[key] = max(SCORE_MIN, old - amount)
        if data[key] != old:
            changed = True

    if changed:
        save_learning_data(data)
        print(f"[DECAY] Lern-Scores um {amount} reduziert.")
