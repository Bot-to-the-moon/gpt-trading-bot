# balance_manager.py

import os
import json

_snapshot_file = "start_snapshot.json"
_manual_adjustments_file = "manual_adjustments.json"

def load_start_snapshot():
    if os.path.exists(_snapshot_file):
        with open(_snapshot_file, "r") as f:
            return float(f.read())
    return 0.0

def save_start_snapshot(balance):
    with open(_snapshot_file, "w") as f:
        f.write(str(balance))

def get_current_snapshot():
    # Hier sollte der aktuelle Walletwert zurückgegeben werden
    # Platzhalter für Integration mit Exchange
    from exchange import get_total_assets
    return get_total_assets()

def record_deposit(current_balance):
    # In Zukunft für Einzahlungslogik erweiterbar
    pass

# 🆕 Manuelle Anpassungen für PnL-Korrektur
def record_manual_adjustment(amount):
    adjustments = load_manual_adjustments()
    adjustments.append(amount)
    with open(_manual_adjustments_file, "w") as f:
        json.dump(adjustments, f)

def get_manual_adjustments():
    if not os.path.exists(_manual_adjustments_file):
        return 0.0
    with open(_manual_adjustments_file, "r") as f:
        adjustments = json.load(f)
    return sum(adjustments)

def load_manual_adjustments():
    if not os.path.exists(_manual_adjustments_file):
        return []
    with open(_manual_adjustments_file, "r") as f:
        return json.load(f)
