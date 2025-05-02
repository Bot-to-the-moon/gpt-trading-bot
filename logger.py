# logger.py

import os
from datetime import datetime

LOG_FOLDER = "logs"
os.makedirs(LOG_FOLDER, exist_ok=True)

def write_log(filename, content):
    """Schreibt Textzeile mit Zeitstempel in Logdatei."""
    path = os.path.join(LOG_FOLDER, filename)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(path, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {content}\n")

def log_event(message):
    """Globaler Bot-Logeintrag."""
    write_log("events.log", message)

def log_trade_event(symbol, message):
    """Trade-spezifischer Log für jeden Coin pro Tag."""
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"{symbol.replace('/', '_')}_{date_str}.log"
    write_log(filename, message)
