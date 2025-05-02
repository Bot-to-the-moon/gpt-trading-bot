import time
from datetime import datetime
from telegram_manager import send_telegram_message

LIMIT = 500     # Max. GPT-Nutzungen (bei ~0.01 $/Stück = 5 $)
WARN_AT = 0.8   # Warnung bei 80 %

USAGE_FILE = "gpt_usage_count.txt"
LOCK_FILE = "gpt_locked.txt"

def count_usage():
    try:
        with open(USAGE_FILE, "r") as f:
            lines = [l.strip() for l in f if l.strip()]
        return len(lines)
    except FileNotFoundError:
        return 0

def log_usage(symbol):
    with open(USAGE_FILE, "a") as f:
        f.write(f"{time.time()} | {symbol}\n")

def gpt_is_locked():
    return os.path.exists(LOCK_FILE)

def lock_gpt():
    with open(LOCK_FILE, "w") as f:
        f.write("LOCKED")

def gpt_guard(symbol=""):
    if gpt_is_locked():
        return False

    used = count_usage()

    if used >= LIMIT:
        send_telegram_message("⛔ GPT-Nutzungslimit erreicht – Analyse wird deaktiviert.")
        lock_gpt()
        return False

    if used >= LIMIT * WARN_AT:
        send_telegram_message(f"⚠️ Achtung: GPT-Nutzung bei {used}/{LIMIT} ({(used/LIMIT)*100:.1f} %)")

    log_usage(symbol)
    return True
