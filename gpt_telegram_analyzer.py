import requests
import time
import openai
import config

BOT_TOKEN = config.TELEGRAM_BOT_TOKEN
GPT_KEY = config.OPENAI_API_KEY
URL = f"https://api.telegram.org/bot{BOT_TOKEN}"
openai.api_key = GPT_KEY

def get_updates(offset=None):
    url = f"{URL}/getUpdates?timeout=100"
    if offset:
        url += f"&offset={offset}"
    return requests.get(url).json()

def send_message(chat_id, text):
    requests.post(f"{URL}/sendMessage", data={"chat_id": chat_id, "text": text})

def analyze_symbol(symbol):
    prompt = f"""
Du bist ein Krypto-Trading-Analyst. Analysiere das Symbol '{symbol}/USDT' technisch.
Berücksichtige Trend, RSI, MACD, Momentum, Breakout-Muster.

Gib bitte Folgendes zurück:
- Empfohlene Aktion (LONG, SHORT oder WAIT)
- Begründung (1–2 Sätze)
- Risiko (niedrig / mittel / hoch)
"""

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6
    )

    return response.choices[0].message.content

def handle_message(text, chat_id):
    if text.startswith("/analyse"):
        parts = text.split()
        if len(parts) == 2:
            symbol = parts[1].upper()
            send_message(chat_id, f"🔍 GPT analysiert {symbol}...")
            result = analyze_symbol(symbol)
            send_message(chat_id, f"📊 GPT-Analyse für {symbol}:\n{result}")
        else:
            send_message(chat_id, "❗ Verwendung: /analyse KDA")

    elif text.startswith("/help"):
        send_message(chat_id,
            "🤖 Verfügbare Befehle:\n"
            "/analyse <SYMBOL> – z. B. /analyse TRIAS\n"
            "/info – Statusinfo zum Bot")

    elif text.startswith("/info"):
        send_message(chat_id, "🧠 KI-Bot läuft. GPT-Analyse bereit. Reinforcement & Matrix aktiv.")

    else:
        send_message(chat_id, "❓ Unbekannter Befehl. Nutze /help")

def main():
    last_update_id = None
    print("📡 GPT-Analyse-Bot läuft...")

    while True:
        updates = get_updates(last_update_id)
        for update in updates.get("result", []):
            last_update_id = update["update_id"] + 1
            msg = update.get("message", {})
            chat_id = msg.get("chat", {}).get("id")
            text = msg.get("text", "")

            if text:
                print("📨 Neue Nachricht erkannt:", text)
                handle_message(text.strip(), chat_id)
        time.sleep(1)

if __name__ == "__main__":
    main()
