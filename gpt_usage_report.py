from datetime import datetime
from collections import defaultdict
from telegram_manager import send_telegram_message

USAGE_FILE = "gpt_usage_count.txt"

def load_usage():
    usage = defaultdict(list)
    try:
        with open(USAGE_FILE, "r") as f:
            for line in f:
                parts = line.strip().split("|")
                if len(parts) == 2:
                    timestamp = float(parts[0].strip())
                    symbol = parts[1].strip()
                    date = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")
                    usage[date].append(symbol)
    except FileNotFoundError:
        return usage
    return usage

def generate_report():
    usage = load_usage()
    total = 0
    lines = []

    lines.append("📊 GPT Monatsreport:")
    for date in sorted(usage.keys()):
        day_total = len(usage[date])
        total += day_total
        coins = ", ".join(set(usage[date]))
        lines.append(f"🗓 {date}: {day_total} Anfragen – Coins: {coins}")

    lines.append(f"\n📈 Gesamt: {total} GPT-Anfragen")

    return "\n".join(lines)

if __name__ == "__main__":
    report = generate_report()
    print(report)
    send_telegram_message(report)
