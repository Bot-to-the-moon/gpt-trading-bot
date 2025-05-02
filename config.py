# config.py

TIMEFRAME = '15m'
VOL_FILTER = 100000  # Mindestvolumenfilter für Coins

# BYBIT
BYBIT_API_KEY = "79CEdBPmgnqaYaVGTz"
BYBIT_SECRET = "bU5xYUYhsJnL3JrHwJyOrkfCzSPmj85ksuBr"

# BINANCE
BINANCE_API_KEY = "nkMKckBVaPdzyhYK5ZaoN706rsHGQCfskBdGOH377rEpVe7CucJmmnfWM6Kaf3cd"
BINANCE_SECRET = "JKzVAHUFxU76jSq0gCAFp3Nvtib4lfA9BOG6cujpTdZq0Zy8qeVDIijqdvSEH9ll"

# Steuerung
USE_BYBIT = True  # oder False, um Binance zu nutzen

SNAPSHOT_FILE = "bot_snapshot_bybit.json"
ACCEPTED_QUOTES = ['USDT', 'USDC']

MAX_EQUITY_USAGE = 0.05
MIN_EQUITY_LEFT = 20

# 🆕 Dry-Run Modus (für Testlauf ohne echte Orders)

DRY_MODE = False

TEST_SYMBOLS = ["TRIAS/USDT:USDT"]

# Für Telegram-Versand von Logs
TELEGRAM_BOT_TOKEN = "7842965218:AAGokWrOcq7kuPeCV4aMUeF8IjrjdaiJ1aQ"
TELEGRAM_CHAT_ID = "1788470377"

OPENAI_API_KEY = "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"  # Dein echter OpenAI Key
TELEGRAM_BOT_TOKEN = "7842965218:AAGokWrOcq7kuPeCV4aMUeF8IjrjdaiJ1aQ"
TELEGRAM_CHAT_ID = "1788470377"  # Nur für Fallback, nicht zwingend nötig hier

