# reinforcement_tracker.py

import json
import os
from datetime import datetime, timedelta

FILE = "reinforcement_data.json"
SCORE_MIN = -10
SCORE_MAX = 20
DECAY_HOURS = 12
DECAY_RATE = 0.98

def load_data():
    if not os.path.exists(FILE):
        return {}
    with open(FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=2)

def update_strategy_score(symbol, strategy, success):
    key = f"{symbol}_{strategy}"
    now = datetime.now().isoformat()
    data = load_data()

    if key not in data:
        data[key] = {"score": 0, "wins": 0, "trades": 0, "last_updated": now}

    record = data[key]
    record["trades"] += 1
    if success:
        record["wins"] += 1
        record["score"] += 1
    else:
        record["score"] -= 1

    record["score"] = max(SCORE_MIN, min(SCORE_MAX, record["score"]))
    record["last_updated"] = now
    save_data(data)

def get_strategy_score(symbol, strategy):
    key = f"{symbol}_{strategy}"
    data = load_data()
    return data.get(key, {}).get("score", 0)

def get_success_rate(symbol, strategy):
    key = f"{symbol}_{strategy}"
    data = load_data()
    entry = data.get(key)
    if not entry or entry["trades"] == 0:
        return 0
    return round(entry["wins"] / entry["trades"], 2)

def decay_scores():
    data = load_data()
    now = datetime.now()
    changed = False

    for key, val in data.items():
        last = datetime.fromisoformat(val["last_updated"])
        if now - last > timedelta(hours=DECAY_HOURS):
            val["score"] *= DECAY_RATE
            val["score"] = round(val["score"], 2)
            val["last_updated"] = now.isoformat()
            changed = True

    if changed:
        save_data(data)
