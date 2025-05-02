import requests
import config

def send_telegram_message(message):
    try:
        token = config.TELEGRAM_BOT_TOKEN
        chat_id = config.TELEGRAM_CHAT_ID

        if not token or not chat_id:
            print("[TELEGRAM] Token oder Chat-ID fehlen.")
            return

        url = f"https://api.telegram.org/bot{token}/sendMessage"
        data = {"chat_id": chat_id, "text": message}
        response = requests.post(url, data=data)

        if response.ok:
            print("[TELEGRAM] Nachricht gesendet.")
        else:
            print(f"[TELEGRAM] Fehler: {response.text}")
    except Exception as e:
        print(f"[TELEGRAM] Ausnahme: {e}")

def send_telegram_file(file_path):
    try:
        token = config.TELEGRAM_BOT_TOKEN
        chat_id = config.TELEGRAM_CHAT_ID

        with open(file_path, 'rb') as f:
            files = {'document': f}
            url = f"https://api.telegram.org/bot{token}/sendDocument"
            data = {'chat_id': chat_id}
            response = requests.post(url, data=data, files=files)

        if response.ok:
            print("[TELEGRAM] Log-Datei gesendet.")
        else:
            print(f"[TELEGRAM] Fehler beim Senden: {response.text}")
    except Exception as e:
        print(f"[TELEGRAM] Datei-Sendeausnahme: {e}")
