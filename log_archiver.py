import os
import zipfile
from datetime import datetime
import requests
import config  # Stelle sicher, dass dein Telegram-Token & Chat-ID dort definiert sind

LOG_FOLDER = "logs"
ARCHIVE_FOLDER = "log_archive"
os.makedirs(ARCHIVE_FOLDER, exist_ok=True)

def zip_logs():
    date_str = datetime.now().strftime("%Y-%m-%d_%H-%M")
    zip_name = f"logs_{date_str}.zip"
    zip_path = os.path.join(ARCHIVE_FOLDER, zip_name)

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for filename in os.listdir(LOG_FOLDER):
            filepath = os.path.join(LOG_FOLDER, filename)
            if os.path.isfile(filepath):
                zipf.write(filepath, arcname=filename)

    print(f"[ARCHIV] Log-Dateien archiviert: {zip_name}")
    return zip_path

def send_to_telegram(file_path):
    try:
        token = config.TELEGRAM_BOT_TOKEN
        chat_id = config.TELEGRAM_CHAT_ID

        if not token or not chat_id:
            print("[TELEGRAM] Token oder Chat-ID fehlen.")
            return False

        with open(file_path, 'rb') as f:
            files = {'document': f}
            url = f"https://api.telegram.org/bot{token}/sendDocument"
            data = {'chat_id': chat_id}
            response = requests.post(url, data=data, files=files)

        if response.ok:
            print("[TELEGRAM] Log-Datei erfolgreich gesendet.")
            return True
        else:
            print(f"[TELEGRAM] Fehler beim Senden: {response.text}")
            return False
    except Exception as e:
        print(f"[TELEGRAM] Ausnahme beim Senden: {e}")
        return False

def archive_and_send_logs_if_due():
    now = datetime.now()
    if now.hour == 23 and now.minute >= 55:
        archive = zip_logs()
        if send_to_telegram(archive):
            try:
                os.remove(archive)
                print(f"[AUFRÄUMEN] ZIP-Datei gelöscht: {archive}")
            except Exception as e:
                print(f"[FEHLER] Beim Löschen der ZIP: {e}")

if __name__ == "__main__":
    archive = zip_logs()
    if send_to_telegram(archive):
        try:
            os.remove(archive)
            print(f"[AUFRÄUMEN] ZIP-Datei gelöscht: {archive}")
        except Exception as e:
            print(f"[FEHLER] Beim Löschen der ZIP: {e}")
