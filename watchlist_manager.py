# watchlist_manager.py

import json
import os
from collections import defaultdict

WATCHLIST_FILE = "watchlist_scores.json"

def update_watchlist(symbol, success):
    watch = defaultdict(lambda: {"score": 0, "count": 0})

    if os.path.exists(WATCHLIST_FILE):
        with open(WATCHLIST_FILE, "r") as f:
            try:
                watch = json.load(f)
            except:
                pass

    if symbol not in watch:
        watch[symbol] = {"score": 0, "count": 0}

    watch[symbol]["count"] += 1
    watch[symbol]["score"] += 1 if success else -1

    with open(WATCHLIST_FILE, "w") as f:
        json.dump(watch, f, indent=2)

def get_watchlist():
    if not os.path.exists(WATCHLIST_FILE):
        return {}

    try:
        with open(WATCHLIST_FILE, "r") as f:
            return json.load(f)
    except:
        return {}
