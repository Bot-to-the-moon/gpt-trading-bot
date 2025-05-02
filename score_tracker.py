# score_tracker.py

import json
import os
import time

SCORE_FILE = "coin_score_log.json"

def append_score(symbol, score, signal):
    log = []
    if os.path.exists(SCORE_FILE):
        with open(SCORE_FILE, "r") as f:
            try:
                log = json.load(f)
            except:
                log = []

    log.append({
        "symbol": symbol,
        "score": score,
        "signal": signal,
        "timestamp": time.time()
    })

    with open(SCORE_FILE, "w") as f:
        json.dump(log[-500:], f, indent=2)  # Nur die letzten 500 Einträge
