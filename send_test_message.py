import requests

# Ersetze diese zwei Werte mit deinen echten Daten:
TELEGRAM_BOT_TOKEN = "7842965218:AAGokWrOcq7kuPeCV4aMUeF8IjrjdaiJ1aQ"
TELEGRAM_CHAT_ID = "1788470377"  # z. B. "123456789"

def send_test_message():
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": "📨 Testnachricht: Telegram-Verbindung erfolgreich! ✅"
    }
    response = requests.post(url, data=data)
    if response.ok:
        print("[OK] Nachricht gesendet ✅")
    else:
        print(f"[FEHLER] Antwort: {response.text}")

if __name__ == "__main__":
    send_test_message()
