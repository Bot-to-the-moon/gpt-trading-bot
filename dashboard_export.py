# dashboard_export.py

import json
import os
import time

DASHBOARD_FILE = "dashboard_state.json"

def export_bot_state(entries):
    state = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "entries": entries
    }

    with open(DASHBOARD_FILE, "w") as f:
        json.dump(state, f, indent=2)
